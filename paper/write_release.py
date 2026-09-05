"""Record git SHA and dated-PDF SHA-256. No DOI is minted."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPORT = ROOT / "report" / (
    "Abrahamsson-2026-09-04-paired-reference-key-free-indication.pdf"
)


def main() -> None:
    git_sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    digest = hashlib.sha256(REPORT.read_bytes()).hexdigest()
    payload = {
        "document_version": "2026-09-05",
        "git_sha": git_sha,
        "pdf": "report/Abrahamsson-2026-09-04-paired-reference-key-free-indication.pdf",
        "pdf_sha256": digest,
        "github_release": (
            "gh release create report-2026-09-05 "
            "--title 'Paired-reference key-free indication (2026-09-05)' "
            "--notes-file paper/release.json "
            "--attach report/Abrahamsson-2026-09-04-paired-reference-key-free-indication.pdf"
        ),
    }
    (HERE / "release.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote paper/release.json sha256={digest[:16]}...")


if __name__ == "__main__":
    main()
