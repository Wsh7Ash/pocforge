"""Tamper-evident evidence manifests.

A PoC is only as good as the artifacts behind it. This module hashes the files a
researcher cites, writes a manifest, and later re-hashes them to prove nothing
was edited after the fact. Verification is deliberately strict: a missing file,
a changed byte count and a changed digest are all reported separately, because
they mean different things during triage.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

SCHEMA = "pocforge.evidence/v1"
CHUNK = 64 * 1024


class EvidenceError(RuntimeError):
    """Raised when a manifest cannot be built or read."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(CHUNK), b""):
            digest.update(block)
    return digest.hexdigest()


def collect(root: Path, paths: Iterable[str] | None = None) -> list[Path]:
    """Resolve evidence files, relative to ``root``, in stable sorted order."""
    if paths:
        resolved: list[Path] = []
        for raw in paths:
            candidate = Path(raw)
            if not candidate.is_absolute():
                candidate = root / candidate
            if candidate.is_dir():
                resolved.extend(sorted(path for path in candidate.rglob("*") if path.is_file()))
            else:
                resolved.append(candidate)
        return sorted(resolved)
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and not path.name.endswith(".manifest.json")
    )


def infer_root(files: Iterable[Path]) -> Path:
    """Common parent of the given files, used when no root was supplied."""
    parents = [path.resolve().parent for path in files]
    if not parents:
        return Path(".")
    shared = parents[0]
    for parent in parents[1:]:
        while shared != parent and parent not in shared.parents:
            if shared.parent == shared:  # filesystem root reached, no common parent
                return Path(".")
            shared = shared.parent
    return shared


def build_manifest(
    root: Path | None = None, paths: Iterable[str] | None = None
) -> dict[str, Any]:
    """Hash every evidence file into a manifest dict.

    Paths are always recorded relative to the manifest root, so a manifest can be
    verified from its own directory on any machine. When no root is given the
    common parent of the collected files is used, which keeps a single-directory
    hash producing short names.
    """
    files = collect(root or Path("."), paths)
    if not files:
        raise EvidenceError(f"no evidence files found under {root or Path('.')}")
    if root is None:
        root = infer_root(files)

    entries: list[dict[str, Any]] = []
    for path in files:
        if not path.is_file():
            raise EvidenceError(f"evidence file is missing: {path}")
        try:
            relative = path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            relative = path.as_posix()
        entries.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )

    entries.sort(key=lambda item: item["path"])
    return {
        "schema": SCHEMA,
        "root": ".",
        "count": len(entries),
        "total_bytes": sum(item["bytes"] for item in entries),
        "files": entries,
        "manifest_sha256": hashlib.sha256(
            json.dumps(entries, sort_keys=True).encode("utf-8")
        ).hexdigest(),
    }


def write_manifest(manifest: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise EvidenceError(f"manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise EvidenceError(f"manifest is not valid JSON: {exc}") from exc
    if data.get("schema") != SCHEMA:
        raise EvidenceError(f"unexpected manifest schema: {data.get('schema')!r}")
    return data


def verify_manifest(
    manifest: dict[str, Any], root: Path, manifest_path: Path | None = None
) -> list[str]:
    """Re-hash each recorded file. Returns human-readable problems.

    ``manifest_path`` is skipped when scanning for unrecorded files: a manifest
    stored inside the evidence directory cannot contain its own digest.
    """
    problems: list[str] = []
    entries = manifest.get("files")
    if not isinstance(entries, list) or not entries:
        return ["manifest records no files"]

    for entry in entries:
        raw = entry.get("path") if isinstance(entry, dict) else None
        if not isinstance(raw, str) or not raw:
            problems.append("manifest entry without a path")
            continue
        path = Path(raw)
        if not path.is_absolute():
            path = root / path
        if not path.is_file():
            problems.append(f"missing: {raw}")
            continue
        size = path.stat().st_size
        if size != entry.get("bytes"):
            problems.append(f"size changed: {raw} ({entry.get('bytes')} -> {size} bytes)")
        if sha256_file(path) != entry.get("sha256"):
            problems.append(f"digest changed: {raw}")

    recorded = {str(entry.get("path")) for entry in entries if isinstance(entry, dict)}
    skip = manifest_path.resolve() if manifest_path is not None else None
    for path in collect(root):
        if skip is not None and path.resolve() == skip:
            continue
        try:
            relative = path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            relative = path.as_posix()
        if relative not in recorded:
            problems.append(f"unrecorded file: {relative}")

    return problems
