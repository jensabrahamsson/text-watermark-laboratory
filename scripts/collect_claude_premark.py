"""Collect Claude long-form text via a headed browser (pre-mark control corpus).

Uses a persistent Chromium profile so a claude.ai login survives across runs.
Does not read watermark keys. Saves raw assistant text + manifest metadata.
Skips prompts already present in manifest.jsonl with a long enough reply.
Default: AppleScript against a Chrome tab already open on claude.ai.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experiments" / "claude-premark-2026-08"
PROFILE = ROOT / ".browser-profile"
MANIFEST = OUT / "manifest.jsonl"
MIN_CHARS = 800
CHAT_ONLY = (
    " Write the full text in the chat only. "
    "Do not create a file, artifact, or document."
)
JS_DIR = OUT / ".js"

# Append only. Never edit a string that is already in manifest.jsonl.
PROMPTS = [
    "Write a 600-word travel essay about arriving in a small harbour town at dusk. Everyday words, no lists, no title.",
    "Explain how a municipal library actually works day to day, 500-700 words, concrete and a bit messy, not a brochure.",
    "A short story about two neighbours arguing over a shared apple tree. About 500 words. No moral at the end.",
    "Describe a rainy Tuesday commute in a northern European city in 600 words. Sensory, no metaphors stacked on metaphors.",
    "Write 600 words on why people keep houseplants they cannot keep alive. Conversational, not a listicle.",
    "A letter from a retired ferry captain to his granddaughter about fog. 500-600 words.",
    "Explain sourdough as if you have failed at it twice. 500 words. No recipe card formatting.",
    "A 600-word scene in a second-hand bookshop just before closing. Dialogue allowed.",
    "Write about 500 words as a night-shift nurse walking home at dawn. Everyday words, no lists, no title.",
    "Describe a weekday morning in a small independent hardware store. About 500 words. Concrete, a bit messy, not a brochure.",
    "A short story about a chess club that meets in a church basement. About 500 words. No moral at the end.",
    "A letter from someone who just moved apartments, written to a friend who helped carry boxes. 500 words.",
    "Write about 500 words on a community radio station that still uses a dusty CD rack. Conversational, no listicle.",
    "Describe the last hour of a bakery before it closes. About 500 words. Sensory, no stacked metaphors.",
    "A 500-word scene in a hospital waiting room at 2 a.m. Dialogue allowed. No diagnosis lecture.",
    "Explain ice fishing as if you only went once and were mostly cold. About 500 words. No how-to card.",
    "Write about 500 words as a city bus driver at the end of a long route. Everyday words, no lists.",
    "A short story about two people locking up a volunteer fire station after a false alarm. About 500 words.",
    "Describe an allotment garden in late September. About 500 words. Concrete, not a nature essay.",
    "A letter from a lighthouse keeper to his sister about a week of bad weather. About 500 words.",
    "Write about 500 words on a small-town museum that nobody visits on Tuesdays. Conversational, no brochure.",
    "A 500-word scene in a laundromat during a rainstorm. Dialogue allowed.",
    "Describe a night receptionist in a cheap hotel. About 500 words. Everyday words, no crime plot.",
    "Explain bicycle repair as if you learned it from a neighbour who was impatient. About 500 words. No manual.",
    "A short story about a community choir rehearsal that keeps falling apart. About 500 words. No moral.",
    "Write about 500 words as a school janitor after the children have gone. Concrete, not sentimental.",
    "A letter from a market stall holder to her daughter about a slow Saturday. About 500 words.",
    "Describe a hiking hut on a foggy afternoon. About 500 words. Sensory, no stacked metaphors.",
    "A 500-word scene in a university corridor between lectures. Dialogue allowed.",
    "Write about 500 words on an unused municipal swimming pool in winter. Conversational, no campaign speech.",
    "Explain printing a local newspaper as if the machines keep jamming. About 500 words. No industry overview.",
    "A short story about walking other people's dogs in a city park. About 500 words. No cute twist.",
    "Describe a fishing village in January. About 500 words. Everyday words, no postcard.",
    "A letter from a night-train passenger who missed their stop. About 500 words.",
    "Write about 500 words as someone closing a second-hand clothes shop. Concrete, a bit tired.",
    "A 500-word scene in a rehearsal room with a broken piano. Dialogue allowed.",
    "Describe a rooftop greenhouse that is mostly failing. About 500 words. Not a gardening guide.",
    "A short story about neighbours sharing a washing line in a courtyard. About 500 words. No moral.",
    "Write about 500 words on a small ferry delayed by wind. Everyday words, no timetable lecture.",
    "A letter from a retired teacher to a former pupil who wrote first. About 500 words.",
]


def _next_id() -> str:
    existing = sorted(OUT.glob("*.txt"))
    n = 1
    for p in existing:
        m = re.match(r"^(\d+)", p.name)
        if m:
            n = max(n, int(m.group(1)) + 1)
    return f"{n:04d}"


def _append_manifest(row: dict) -> None:
    with MANIFEST.open("a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


class UsageLimit(RuntimeError):
    """Claude free/paid usage cap. Stop instead of saving garbage."""


LIMIT_MARKERS = (
    "you've hit your limit",
    "you have hit your limit",
    "you've reached your limit",
    "you have reached your limit",
    "usage limit",
    "usage cap",
    "rate limit",
    "try again later",
    "try again in",
    "upgrade to pro",
    "upgrade to max",
    "upgrade your plan",
    "subscribe to pro",
    "limit resets",
    "come back in",
    "too many messages",
    "out of extra usage",
    # Claude.ai Swedish UI (match only; do not translate these needles)
    "du har nått din gräns",
    "du har nått gränsen",
    "försök igen senare",
    "uppgradera till",
)


def _looks_like_limit(text: str) -> bool:
    low = text.lower()
    return any(m in low for m in LIMIT_MARKERS)


def _page_looks_like_limit(page) -> bool:
    try:
        body = page.inner_text("body", timeout=2000)
    except Exception:
        return False
    return _looks_like_limit(body)


def _open_inspect_page() -> None:
    try:
        subprocess.run(
            [
                "osascript",
                "-e",
                'tell application "Google Chrome" to open location "chrome://inspect/#remote-debugging"',
            ],
            check=False,
            timeout=8,
        )
    except Exception:
        pass


def _sent(prompt: str) -> str:
    if "Do not create a file" in prompt:
        return prompt
    return prompt + CHAT_ONLY


def _already_collected_prompts() -> set[str]:
    """Only long replies count. Short artifact-chrome files are retried."""
    if not MANIFEST.exists():
        return set()
    seen: set[str] = set()
    for line in MANIFEST.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if int(row.get("n_chars") or 0) < MIN_CHARS:
            continue
        prompt = row.get("prompt")
        if not prompt:
            continue
        seen.add(prompt)
        if prompt.endswith(CHAT_ONLY):
            seen.add(prompt[: -len(CHAT_ONLY)].rstrip())
    return seen


def _composer(page):
    for sel in (
        "div[contenteditable='true']",
        "fieldset div[contenteditable='true']",
        "[data-testid='chat-input']",
        "textarea",
    ):
        loc = page.locator(sel).last
        if loc.count() and loc.is_visible():
            return loc
    return None


def _wait_logged_in(page, timeout_ms: int) -> bool:
    deadline = time.time() + timeout_ms / 1000
    print("log in at claude.ai in the window if needed...", flush=True)
    while time.time() < deadline:
        try:
            if page.is_closed():
                return False
            if _composer(page) is not None:
                return True
        except Exception:
            return False
        time.sleep(1)
    try:
        return _composer(page) is not None
    except Exception:
        return False


def _new_chat(page) -> None:
    for sel in (
        "a[href='/new']",
        "a[href*='/chat/new']",
        "button:has-text('New chat')",
        "button:has-text('Ny chatt')",  # Claude.ai Swedish UI
    ):
        loc = page.locator(sel).first
        if loc.count():
            try:
                loc.click(timeout=3000)
                page.wait_for_timeout(800)
                return
            except PlaywrightTimeout:
                continue
    page.goto("https://claude.ai/new", wait_until="domcontentloaded")
    page.wait_for_timeout(1500)


def _send_and_read(page, prompt: str, wait_s: int) -> str:
    box = _composer(page)
    if box is None:
        raise RuntimeError("no chat composer")
    box.click()
    box.fill(prompt)
    page.keyboard.press("Enter")

    # Wait until the composer is enabled again (generation finished).
    page.wait_for_timeout(3000)
    deadline = time.time() + wait_s
    last = ""
    stable = 0
    while time.time() < deadline:
        parts = page.locator("[data-is-streaming], .font-claude-message, [data-testid='assistant-message']")
        texts = []
        try:
            n = parts.count()
            if n:
                texts.append(parts.nth(n - 1).inner_text(timeout=2000))
        except Exception:
            pass
        if not texts:
            try:
                texts.append(page.inner_text("main", timeout=2000))
            except Exception:
                texts.append("")
        cur = (texts[-1] if texts else "").strip()
        if cur and cur == last and len(cur) > 200:
            stable += 1
            if stable >= 3:
                break
        else:
            stable = 0
        last = cur
        time.sleep(2)
    return last


def _connect_or_launch(p, headed: bool, cdp: str | None, wait_cdp_s: int):
    # claude.ai rejects Chrome for Testing / stock Chromium.
    if cdp:
        print("CDP", cdp, flush=True)
        deadline = time.time() + max(wait_cdp_s, 0)
        last = None
        while True:
            try:
                browser = p.chromium.connect_over_cdp(cdp, timeout=4000)
                ctx = browser.contexts[0] if browser.contexts else browser.new_context()
                page = ctx.new_page()
                return browser, ctx, page, False
            except Exception as exc:
                last = exc
                if time.time() >= deadline:
                    raise SystemExit(
                        "no Chrome CDP. In Chrome already logged in at claude.ai: "
                        "chrome://inspect/#remote-debugging → "
                        "Allow remote debugging for this browser instance. "
                        f"last: {last}"
                    )
                print("waiting for Allow remote debugging...", flush=True)
                time.sleep(3)
    chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    PROFILE.mkdir(parents=True, exist_ok=True)
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=str(PROFILE),
        headless=not headed,
        viewport={"width": 1280, "height": 900},
        channel="chrome",
        executable_path=str(chrome) if chrome.exists() else None,
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    return None, ctx, page, True


def collect(
    n: int,
    headed: bool,
    cdp: str | None,
    *,
    pause_s: int = 20,
    wait_cdp_s: int = 180,
) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    already = _already_collected_prompts()
    remaining = [p for p in PROMPTS if p not in already]
    if n <= 0:
        n = len(remaining)
    print(
        f"{len(remaining)} prompts left, taking at most {n}. "
        f"pause {pause_s}s. free plan: stop at the cap.",
        flush=True,
    )
    if cdp:
        _open_inspect_page()
    with sync_playwright() as p:
        browser, ctx, page, owns_ctx = _connect_or_launch(
            p, headed, cdp, wait_cdp_s
        )
        page.goto("https://claude.ai/new", wait_until="domcontentloaded")
        print("opened", page.url, flush=True)
        if not _wait_logged_in(page, 180_000):
            shot = OUT / "need_login.png"
            page.screenshot(path=str(shot))
            if owns_ctx:
                ctx.close()
            raise SystemExit(
                f"not logged in at claude.ai — log in in the opened window "
                f"or in {PROFILE} and rerun. screenshot={shot}"
            )

        taken = 0
        short_streak = 0
        for prompt in remaining:
            if taken >= n:
                break
            if taken and pause_s:
                print(f"pause {pause_s}s (free plan)", flush=True)
                time.sleep(pause_s)
            _new_chat(page)
            if _composer(page) is None:
                page.goto("https://claude.ai/new", wait_until="domcontentloaded")
                page.wait_for_timeout(2000)
            if _page_looks_like_limit(page):
                page.screenshot(path=str(OUT / f"limit-{_next_id()}.png"))
                print("usage limit in UI — stopping.", flush=True)
                break
            print("prompt:", prompt[:60], "...", flush=True)
            try:
                text = _send_and_read(page, prompt, wait_s=180)
            except Exception as exc:
                print("fail:", exc, flush=True)
                page.screenshot(path=str(OUT / f"fail-{_next_id()}.png"))
                if _page_looks_like_limit(page):
                    print("usage limit after fail — stopping.", flush=True)
                    break
                continue
            if _looks_like_limit(text) or _page_looks_like_limit(page):
                page.screenshot(path=str(OUT / f"limit-{_next_id()}.png"))
                print("usage limit — not saving. stopping.", flush=True)
                break
            if len(text) < MIN_CHARS:
                short_streak += 1
                print("too short:", len(text), flush=True)
                page.screenshot(path=str(OUT / f"short-{_next_id()}.png"))
                if short_streak >= 2:
                    print("two short replies — probably the cap. stopping.", flush=True)
                    break
                continue
            short_streak = 0
            _save_premark(prompt, text)
            taken += 1
        if owns_ctx:
            ctx.close()
    print("done", taken, "in", OUT)


def _save_premark(prompt: str, text: str) -> Path:
    sid = _next_id()
    path = OUT / f"{sid}-sonnet5-premark.txt"
    path.write_text(text.strip() + "\n")
    _append_manifest(
        {
            "id": sid,
            "file": path.name,
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "assumed_watermark": False,
            "reason": (
                "Sonnet 5 launched 2026-06-30; day-one marking is "
                "models from 2026-08-02; retrofit unpublished"
            ),
            "surface": "claude.ai",
            "model_claimed": "sonnet-5-or-ui-default",
            "via": "applescript-or-cdp",
            "prompt": prompt,
            "n_chars": len(text),
        }
    )
    print("wrote", path.name, "chars", len(text), flush=True)
    return path


def _osascript(script: str) -> str:
    JS_DIR.mkdir(parents=True, exist_ok=True)
    applescript = JS_DIR / "run.applescript"
    applescript.write_text(script)
    r = subprocess.run(
        ["osascript", str(applescript)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout or "osascript fail").strip())
    return (r.stdout or "").rstrip("\n")


def _chrome_js(js: str) -> str:
    JS_DIR.mkdir(parents=True, exist_ok=True)
    js_path = JS_DIR / "page.js"
    js_path.write_text(js, encoding="utf-8")
    script = f'''
tell application "Google Chrome"
  activate
  set js to read POSIX file "{js_path}" as «class utf8»
  repeat with w in windows
    repeat with t in tabs of w
      if (URL of t) starts with "https://claude.ai" then
        tell t to return execute javascript js
      end if
    end repeat
  end repeat
  return "NO_TAB"
end tell
'''
    return _osascript(script)


def _chrome_open_new_chat() -> None:
    script = '''
tell application "Google Chrome"
  activate
  set found to false
  repeat with w in windows
    repeat with t in tabs of w
      if (URL of t) starts with "https://claude.ai" then
        set URL of t to "https://claude.ai/new"
        set found to true
        exit repeat
      end if
    end repeat
    if found then exit repeat
  end repeat
  if not found then
    open location "https://claude.ai/new"
  end if
end tell
'''
    _osascript(script)
    time.sleep(2.5)


def _chrome_keystroke_return() -> None:
    script = '''
tell application "Google Chrome" to activate
delay 0.2
tell application "System Events" to keystroke return
'''
    _osascript(script)


def _extract_js() -> str:
    return r"""
(() => {
  const junk = /created a file|architected |document · md|\bdownload\b|read a file|creating a /i;
  const nodes = [...document.querySelectorAll(
    "[data-testid='assistant-message'], .font-claude-message, [data-is-streaming], article, pre, [class*='markdown']"
  )];
  let best = "";
  for (const n of nodes) {
    const t = (n.innerText || "").trim();
    if (t.length > best.length && !junk.test(t.slice(0, 240))) best = t;
  }
  if (best.length < 400) {
    const main = document.querySelector("main");
    if (main) {
      const t = (main.innerText || "").trim();
      if (t.length > best.length) best = t;
    }
  }
  return best;
})()
"""


def _fill_js(prompt: str) -> str:
    payload = json.dumps(prompt)
    return f"""
(() => {{
  const prompt = {payload};
  const box = [...document.querySelectorAll("div[contenteditable='true'], textarea")]
    .filter(e => e.offsetParent !== null)
    .at(-1);
  if (!box) return "NO_COMPOSER";
  box.focus();
  document.execCommand("selectAll");
  const ok = document.execCommand("insertText", false, prompt);
  return (ok ? "OK " : "FALLBACK ") + (box.innerText || box.value || "").length;
}})()
"""


def collect_applescript(n: int, *, pause_s: int = 25) -> None:
    """Drive a Chrome tab already open on claude.ai. No CDP attach."""
    OUT.mkdir(parents=True, exist_ok=True)
    already = _already_collected_prompts()
    remaining = [p for p in PROMPTS if p not in already]
    if n <= 0:
        n = len(remaining)
    print(
        f"AppleScript. {len(remaining)} prompts left, taking at most {n}. "
        f"pause {pause_s}s. no CDP.",
        flush=True,
    )
    _chrome_open_new_chat()
    probe = _chrome_js(
        "document.querySelector(\"div[contenteditable='true']\") ? 'composer' : document.body.innerText.slice(0,180)"
    )
    print("chrome:", probe[:160], flush=True)
    if "composer" not in probe.lower() and "NO_TAB" in probe:
        raise SystemExit("no claude.ai tab — open https://claude.ai and log in")
    if "log in" in probe.lower() or "sign in" in probe.lower():
        print("log in in Chrome if needed...", flush=True)
        deadline = time.time() + 180
        while time.time() < deadline:
            time.sleep(3)
            probe = _chrome_js(
                "document.querySelector(\"div[contenteditable='true']\") ? 'composer' : 'wait'"
            )
            if "composer" in probe:
                break
        else:
            raise SystemExit("not logged in at claude.ai in Chrome")

    taken = 0
    short_streak = 0
    for prompt in remaining:
        if taken >= n:
            break
        if taken and pause_s:
            print(f"pause {pause_s}s (free plan)", flush=True)
            time.sleep(pause_s)
        sent = _sent(prompt)
        print("prompt:", prompt[:60], "...", flush=True)
        _chrome_open_new_chat()
        fill = _chrome_js(_fill_js(sent))
        print("fill", fill, flush=True)
        if "NO_COMPOSER" in fill or fill == "NO_TAB":
            body = _chrome_js("document.body.innerText.slice(0,800)")
            if _looks_like_limit(body):
                print("usage limit — stopping.", flush=True)
                break
            print("no composer", body[:120], flush=True)
            short_streak += 1
            if short_streak >= 2:
                break
            continue
        clicked = _chrome_js(
            """
(() => {
  const btns = [...document.querySelectorAll("button")];
  const send = btns.find(b => /send|skicka|submit/i.test((b.getAttribute("aria-label")||"") + " " + (b.innerText||"")));
  if (send) { send.click(); return "clicked"; }
  return "no-button";
})()
"""
        )
        print("send", clicked, flush=True)
        if "clicked" not in clicked:
            try:
                _chrome_keystroke_return()
            except Exception as exc:
                print("keystroke fail", exc, flush=True)
        last = ""
        stable = 0
        text = ""
        deadline = time.time() + 180
        while time.time() < deadline:
            time.sleep(2)
            text = _chrome_js(_extract_js())
            if _looks_like_limit(text):
                print("usage limit — not saving. stopping.", flush=True)
                return
            if text and text == last and len(text) >= MIN_CHARS:
                stable += 1
                if stable >= 3:
                    break
            else:
                stable = 0
            last = text
        if _looks_like_limit(text):
            print("usage limit — stopping.", flush=True)
            break
        if len(text) < MIN_CHARS:
            short_streak += 1
            print("too short:", len(text), flush=True)
            (OUT / f"short-{_next_id()}.txt").write_text((text or "") + "\n")
            if short_streak >= 2:
                print("two short replies — probably the cap. stopping.", flush=True)
                break
            continue
        short_streak = 0
        _save_premark(sent, text)
        taken += 1
    print("done", taken, "in", OUT)


def seed_existing() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if any(OUT.glob("*-existing-*.txt")):
        return
    src = ROOT / "experiments" / "2026-08-15-gpt2-sonnet5"
    pairs = [
        (src / "t_prime_sonnet5.txt", "full rewrite of watermarked GPT-2 text"),
        (src / "t_prime_sonnet5_proofread.txt", "grammar-only pass on error-injected GPT-2 text"),
    ]
    for src_path, note in pairs:
        if not src_path.exists():
            continue
        sid = _next_id()
        dest = OUT / f"{sid}-sonnet5-existing-{src_path.stem}.txt"
        text = src_path.read_text()
        dest.write_text(text)
        _append_manifest(
            {
                "id": sid,
                "file": dest.name,
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "assumed_watermark": False,
                "reason": "existing 2026-08-15 Sonnet 5 session; pre-retrofit window",
                "surface": "manual-paste",
                "model_claimed": "sonnet-5",
                "note": note,
                "n_chars": len(text),
            }
        )
        print("seeded", dest.name)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--n",
        type=int,
        default=0,
        help="Max new texts. 0 = all remaining prompts (stops on usage limit)",
    )
    ap.add_argument("--seed-only", action="store_true")
    ap.add_argument("--headed", action="store_true", default=True)
    ap.add_argument("--headless", action="store_true")
    ap.add_argument(
        "--pause",
        type=int,
        default=20,
        help="Seconds between prompts (free-tier courtesy)",
    )
    ap.add_argument(
        "--wait-cdp",
        type=int,
        default=180,
        help="Seconds to wait for chrome://inspect remote debugging",
    )
    ap.add_argument(
        "--via",
        choices=("applescript", "cdp"),
        default="applescript",
        help="applescript = Chrome tab on claude.ai. cdp = inspect attach",
    )
    ap.add_argument(
        "--cdp",
        default="chrome",
        help="Only with --via cdp: 'chrome' or http://127.0.0.1:9222",
    )
    ap.add_argument(
        "--no-cdp",
        action="store_true",
        help="With --via cdp: launch a separate real-Chrome profile",
    )
    args = ap.parse_args()
    seed_existing()
    if args.seed_only:
        return
    if args.via == "applescript":
        collect_applescript(args.n, pause_s=args.pause)
        return
    cdp = None if args.no_cdp else args.cdp
    collect(
        args.n,
        headed=not args.headless,
        cdp=cdp,
        pause_s=args.pause,
        wait_cdp_s=args.wait_cdp,
    )


if __name__ == "__main__":
    main()
