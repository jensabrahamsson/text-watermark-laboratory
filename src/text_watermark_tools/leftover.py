"""Occupancy leftover bounds from published JSON.

Official prefix scores use detector keys (positive control). Interpolate
atoms on leftover files do not. Leftover-18 remaining readers re-slice
published holdouts. Cross-generator occupancy-free leftover coverage
uses Distil tables on the original 12. None of that is a new probe
method. None replaces 25/48.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence

from text_watermark_tools.atoms import DEFAULT_ATOM_WINDOWS, window_atom_summary
from text_watermark_tools.openings import (
    _holdout_file_lrs,
    _leftover_sign,
    _zero_keys,
)


def leftover_keys_from_coverage(
    coverage: Path, *, method: str = "postokhits"
) -> set[tuple[str, int]]:
    pay = json.loads(Path(coverage).read_text())
    if pay.get("used_keys"):
        raise RuntimeError("leftover coverage consulted keys")
    return _zero_keys(pay, method)


def leftover_keys_from_union(union: Path) -> set[tuple[str, int]]:
    """Leftover keys from a published occupancy-free coverage union dump."""
    pay = json.loads(Path(union).read_text())
    if pay.get("used_keys"):
        raise RuntimeError("coverage union consulted keys")
    return {(str(r["stem"]), int(r["sample"])) for r in pay.get("leftover") or []}


def summarize_official_on_keys(
    keys: set[tuple[str, int]],
    official: Path,
    *,
    prefixes: Sequence[str] = ("5", "16", "128"),
) -> dict:
    """Re-slice published official prefix scores on an explicit leftover set.

    This path uses detector keys. It is a positive control, not key-free
    indication. Does not replace 25/48.
    """
    raw = json.loads(Path(official).read_text())
    if not raw.get("used_keys"):
        raise RuntimeError("official leftover slice needs a keyed dump")
    leftover = set(keys)
    rows = list(raw.get("rows") or [])
    marked = [r for r in rows if str(r.get("side") or "") == "marked"]
    unmarked = [r for r in rows if str(r.get("side") or "") == "unmarked"]
    marked_keys = {(str(r["stem"]), int(r["sample"])) for r in marked}
    if leftover - marked_keys:
        raise RuntimeError("leftover keys missing from official dump")
    prefixes_out = {}
    for prefix in prefixes:
        key = str(prefix)
        left_vals = [
            float(r["prefixes"][key]["mean"])
            for r in marked
            if (str(r["stem"]), int(r["sample"])) in leftover
        ]
        prefixes_out[key] = {"leftover_marked": _mean_stats(left_vals)}
    return {
        "note": (
            "Official public-deepmind-30 mean re-sliced on leftover keys. "
            "Uses detector keys and g-values. Not a key-free reader. "
            "Does not replace 25/48."
        ),
        "used_keys": True,
        "used_hash_iv": True,
        "used_g_values": True,
        "n_leftover": len(leftover),
        "n_marked": len(marked_keys),
        "n_unmarked": len(unmarked),
        "leftover": sorted(
            [{"stem": s, "sample": n} for s, n in leftover],
            key=lambda r: (r["stem"], r["sample"]),
        ),
        "prefixes": prefixes_out,
    }


def _mean_stats(values: Sequence[float]) -> dict:
    nums = [float(v) for v in values]
    n = len(nums)
    return {
        "n": n,
        "mean": (sum(nums) / n) if n else 0.0,
        "min": min(nums) if nums else None,
        "max": max(nums) if nums else None,
        "n_above_055": sum(1 for v in nums if v > 0.55),
        "n_above_060": sum(1 for v in nums if v > 0.60),
    }


def summarize_occupancy_leftover_official(
    coverage: Path,
    official: Path,
    *,
    method: str = "postokhits",
    prefixes: Sequence[str] = ("5", "16", "128"),
) -> dict:
    """Re-slice published official prefix scores on occupancy leftover keys.

    This path uses detector keys. It is a positive control, not key-free
    indication. Leftover membership stays mixed postokhits zeros.
    """
    leftover = leftover_keys_from_coverage(coverage, method=method)
    raw = json.loads(Path(official).read_text())
    if not raw.get("used_keys"):
        raise RuntimeError("official leftover bound needs a keyed dump")
    rows = list(raw.get("rows") or [])
    marked = [
        r
        for r in rows
        if str(r.get("side") or "") == "marked"
    ]
    unmarked = [
        r
        for r in rows
        if str(r.get("side") or "") == "unmarked"
    ]
    marked_keys = {(str(r["stem"]), int(r["sample"])) for r in marked}
    if leftover - marked_keys:
        raise RuntimeError("leftover keys missing from official dump")
    prefixes_out = {}
    for prefix in prefixes:
        key = str(prefix)
        left_vals = [
            float(r["prefixes"][key]["mean"])
            for r in marked
            if (str(r["stem"]), int(r["sample"])) in leftover
        ]
        cov_vals = [
            float(r["prefixes"][key]["mean"])
            for r in marked
            if (str(r["stem"]), int(r["sample"])) not in leftover
        ]
        unmarked_vals = [float(r["prefixes"][key]["mean"]) for r in unmarked]
        prefixes_out[key] = {
            "leftover_marked": _mean_stats(left_vals),
            "covered_marked": _mean_stats(cov_vals),
            "unmarked": _mean_stats(unmarked_vals),
        }
    return {
        "note": (
            "Official public-deepmind-30 mean re-sliced on occupancy leftover "
            "20. Uses detector keys and g-values. Not a key-free reader. "
            "Does not replace 25/48."
        ),
        "used_keys": True,
        "used_hash_iv": True,
        "used_g_values": True,
        "method": method,
        "n_leftover": len(leftover),
        "n_covered": len(marked_keys) - len(leftover),
        "leftover": sorted(
            [{"stem": s, "sample": n} for s, n in leftover],
            key=lambda r: (r["stem"], r["sample"]),
        ),
        "prefixes": prefixes_out,
    }


def summarize_leftover_interpolate_atoms(
    atoms: dict,
    leftover: set[tuple[str, int]],
    *,
    windows: Sequence[tuple[int, int]] = DEFAULT_ATOM_WINDOWS,
    top_k: int = 20,
) -> dict:
    """Window atom summary restricted to occupancy leftover files.

    Requires per-file atom rows. Not keys. Not a new probe method.
    """
    if atoms.get("used_keys") or atoms.get("used_hash_iv") or atoms.get("used_g_values"):
        raise RuntimeError("leftover atoms consulted keys")
    rows = [
        r
        for r in (atoms.get("rows") or [])
        if (str(r.get("stem") or ""), int(r.get("sample") or 0)) in leftover
    ]
    if not rows:
        raise RuntimeError("leftover atom summary needs store_rows=True")
    marked = [r for r in rows if str(r.get("side") or "") == "marked"]
    return {
        "note": (
            "Interpolate last-4 atoms on occupancy leftover files only. "
            "unseen_next is Witten–Bell backoff. Not keys, not a new probe "
            "method, not a leftover-file detector. Does not replace 25/48."
        ),
        "used_keys": False,
        "used_hash_iv": False,
        "used_g_values": False,
        "n_rows": len(rows),
        "n_leftover": len(leftover),
        "n_marked_lr_positive": sum(
            1 for r in marked if float(r.get("lr") or 0.0) > 0.0
        ),
        "windows": window_atom_summary(rows, windows, top_k=top_k),
    }


def print_leftover_bound(*, official: dict, atoms: dict) -> str:
    lines = [
        "# Occupancy leftover-20 bound",
        "",
        "Official prefix scores use detector keys (positive control). "
        "Leftover interpolate atoms do not. Neither replaces 25/48.",
        "",
        (
            f"official_used_keys={official.get('used_keys')} "
            f"leftover={official.get('n_leftover')} "
            f"covered={official.get('n_covered')}"
        ),
        "",
        "| prefix | leftover marked mean | >0.55 | covered marked mean | >0.55 | unmarked mean | >0.55 |",
        "|---|---|---|---|---|---|---|",
    ]
    for prefix, row in (official.get("prefixes") or {}).items():
        left = row.get("leftover_marked") or {}
        cov = row.get("covered_marked") or {}
        um = row.get("unmarked") or {}
        lines.append(
            f"| {prefix} | {left.get('mean'):.4f} | "
            f"{left.get('n_above_055')}/{left.get('n')} | "
            f"{cov.get('mean'):.4f} | "
            f"{cov.get('n_above_055')}/{cov.get('n')} | "
            f"{um.get('mean'):.4f} | "
            f"{um.get('n_above_055')}/{um.get('n')} |"
        )
    lines.extend(
        [
            "",
            (
                f"atoms_used_keys={atoms.get('used_keys')} "
                f"n_rows={atoms.get('n_rows')} "
                f"leftover marked lr>0={atoms.get('n_marked_lr_positive')}"
            ),
            "",
            "| window | mean marked Δ | mean unmarked Δ | seen | unseen |",
            "|---|---|---|---|---|",
        ]
    )
    for win in atoms.get("windows") or []:
        lines.append(
            f"| {win.get('start')}:{win.get('end')} | "
            f"{float(win.get('mean_marked_delta') or 0):.4f} | "
            f"{float(win.get('mean_unmarked_delta') or 0):.4f} | "
            f"{win.get('n_seen')} | {win.get('n_unseen')} |"
        )
    lines.extend(
        [
            "",
            "Official leftover detection uses keys. Leftover atoms are not "
            "a leftover-file detector. Does not replace 25/48.",
        ]
    )
    return "\n".join(lines) + "\n"


def persist_leftover_bound(
    *,
    official: dict,
    atoms: dict,
    out_dir: Path,
) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "official.json").write_text(json.dumps(official, indent=2) + "\n")
    (out_dir / "atoms.json").write_text(json.dumps(atoms, indent=2) + "\n")
    (out_dir / "results.md").write_text(
        print_leftover_bound(official=official, atoms=atoms)
    )


def summarize_leftover_holdouts(
    keys: set[tuple[str, int]],
    holdouts: dict[str, Path],
) -> dict:
    """Leftover-file signs from published holdouts. Not a new probe method."""
    leftover = set(keys)
    leftover_rows = []
    used_keys = False
    used_hash_iv = False
    used_g_values = False
    for name, path in holdouts.items():
        raw = json.loads(Path(path).read_text())
        if raw.get("used_keys"):
            used_keys = True
        if raw.get("used_hash_iv"):
            used_hash_iv = True
        if raw.get("used_g_values"):
            used_g_values = True
        marked_keys, marked, unmarked = _holdout_file_lrs(path)
        missing = leftover - marked_keys
        if missing:
            raise RuntimeError("leftover keys missing from holdout")
        leftover_rows.append(
            {"label": name, **_leftover_sign(leftover, marked, unmarked)}
        )
    return {
        "note": (
            "Leftover-18 remaining readers on published holdouts. "
            "Not mixed tables, not a new probe method. "
            "Does not replace 25/48."
        ),
        "used_keys": used_keys,
        "used_hash_iv": used_hash_iv,
        "used_g_values": used_g_values,
        "n_leftover": len(leftover),
        "leftover": sorted(
            [{"stem": s, "sample": n} for s, n in leftover],
            key=lambda r: (r["stem"], r["sample"]),
        ),
        "leftover_signs": leftover_rows,
    }


def print_leftover_readers(payload: dict) -> str:
    lines = [
        "# Leftover-18 remaining readers",
        "",
        str(payload.get("note") or ""),
        "",
        (
            f"used_keys={payload.get('used_keys')} "
            f"leftover={payload.get('n_leftover')}"
        ),
        "",
        "Leftover signs:",
        "",
    ]
    for row in payload.get("leftover_signs") or []:
        lines.append(
            f"- {row['label']}: marked>0 {row['marked_above_zero']}/{row['n']}, "
            f"unmarked≤0 {row['unmarked_at_most_zero']}/{row['n']}"
        )
    atoms = payload.get("atoms") or {}
    if atoms:
        lines.extend(
            [
                "",
                (
                    f"atoms_used_keys={atoms.get('used_keys')} "
                    f"n_rows={atoms.get('n_rows')} "
                    f"leftover marked lr>0={atoms.get('n_marked_lr_positive')}"
                ),
                "",
                "| window | mean marked Δ | mean unmarked Δ | seen | unseen |",
                "|---|---|---|---|---|",
            ]
        )
        for win in atoms.get("windows") or []:
            lines.append(
                f"| {win.get('start')}:{win.get('end')} | "
                f"{float(win.get('mean_marked_delta') or 0):.4f} | "
                f"{float(win.get('mean_unmarked_delta') or 0):.4f} | "
                f"{win.get('n_seen')} | {win.get('n_unseen')} |"
            )
    lines.extend(
        [
            "",
            "Leftover-18 remaining readers are not occupancy-free coverage. "
            "Does not replace 25/48.",
        ]
    )
    return "\n".join(lines) + "\n"


def persist_leftover_readers(payload: dict, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "readers.json").write_text(json.dumps(payload, indent=2) + "\n")
    (out_dir / "results.md").write_text(print_leftover_readers(payload))


def leftover_openings_coverage(
    keys: set[tuple[str, int]],
    openings: Path,
    *,
    method: str = "postokhits",
) -> dict:
    """How many leftover keys a published openings dump covers.

    Not a new probe method. Distil occupancy-free leftover-18 uses this
    after PROTOCOL-isolated-xgen decode. Does not replace 25/48.
    """
    pay = json.loads(Path(openings).read_text())
    if pay.get("used_keys"):
        raise RuntimeError("leftover openings coverage consulted keys")
    leftover = set(keys)
    zeros = _zero_keys(pay, method)
    covered = leftover - zeros
    uncovered = leftover & zeros
    final = (pay.get("final") or {}).get(method) or {}
    return {
        "used_keys": False,
        "used_hash_iv": False,
        "used_g_values": False,
        "method": method,
        "n_leftover": len(leftover),
        "n_covered": len(covered),
        "n_uncovered": len(uncovered),
        "n_train_openings": int(final.get("n_train_openings") or 0),
        "n_marked_covered": int(final.get("n_covered") or 0),
        "covered": sorted(
            [{"stem": s, "sample": n} for s, n in covered],
            key=lambda r: (r["stem"], r["sample"]),
        ),
        "uncovered": sorted(
            [{"stem": s, "sample": n} for s, n in uncovered],
            key=lambda r: (r["stem"], r["sample"]),
        ),
    }


def summarize_xgen_leftover(
    keys: set[tuple[str, int]],
    *,
    holdouts: dict[str, Path],
    openings: Path,
    method: str = "postokhits",
) -> dict:
    """Distil occupancy-free leftover-18 on the original 12.

    Same BPE as GPT-2. The 100 Distil prompts were frozen before leftover
    peeking. Not a new probe method. Does not replace 25/48.
    """
    payload = summarize_leftover_holdouts(keys, holdouts)
    payload["note"] = (
        "Distil occupancy-free leftover-18 on the original 12. "
        "Same BPE, 100 prompts frozen before leftover peeking. "
        "Not mixed tables, not a new probe method. "
        "Does not replace 25/48."
    )
    payload["openings"] = leftover_openings_coverage(
        keys, openings, method=method
    )
    return payload


def print_xgen_leftover(payload: dict) -> str:
    lines = [
        "# Distil occupancy-free leftover-18",
        "",
        str(payload.get("note") or ""),
        "",
        (
            f"used_keys={payload.get('used_keys')} "
            f"leftover={payload.get('n_leftover')}"
        ),
        "",
        "Leftover signs:",
        "",
    ]
    for row in payload.get("leftover_signs") or []:
        lines.append(
            f"- {row['label']}: marked>0 {row['marked_above_zero']}/{row['n']}, "
            f"unmarked≤0 {row['unmarked_at_most_zero']}/{row['n']}"
        )
    cov = payload.get("openings") or {}
    lines.extend(
        [
            "",
            (
                f"openings leftover covered={cov.get('n_covered')}/"
                f"{cov.get('n_leftover')} uncovered={cov.get('n_uncovered')} "
                f"full marked covered={cov.get('n_marked_covered')}/48"
            ),
            "",
            "Distil occupancy-free leftover-18 is not leftover-file detection. "
            "Does not replace 25/48.",
        ]
    )
    return "\n".join(lines) + "\n"


def persist_xgen_leftover(payload: dict, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "xgen.json").write_text(json.dumps(payload, indent=2) + "\n")
    (out_dir / "results.md").write_text(print_xgen_leftover(payload))
