"""Shared file boundaries for the offline evidence CLIs; no source execution."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import tempfile
from decimal import Decimal
from pathlib import Path, PurePosixPath
from typing import Any


class InputError(ValueError):
    """An input cannot be interpreted safely or completely."""


def root_path(value: str) -> Path:
    path = Path(value).absolute()
    reject_links(path)
    if not path.is_dir():
        raise InputError(f"root is not a directory: {path}")
    return path.resolve()


def reject_links(path: Path) -> None:
    """Refuse symlinks and Windows reparse points in every existing component."""
    for part in [*reversed(path.parents), path]:
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise InputError(f"links/reparse points are not supported: {part}")


def relative_name(value: Any, *, allow_dot: bool = False) -> str:
    if (
        not isinstance(value, str)
        or not value
        or any(char in value for char in '\\:<>"|?*')
        or any(ord(char) < 32 or ord(char) == 127 for char in value)
    ):
        raise InputError("paths must be nonempty relative POSIX paths")
    parts = value.split("/")
    if value == "." and allow_dot:
        return value
    if any(part in ("", ".", "..") for part in parts) or PurePosixPath(value).is_absolute():
        raise InputError(f"unsafe or noncanonical relative path: {value}")
    reserved = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        *(f"COM{i}" for i in range(10)),
        *(f"LPT{i}" for i in range(10)),
    }
    if any(part.endswith((".", " ")) or part.split(".")[0].upper() in reserved for part in parts):
        raise InputError(f"path has a nonportable Windows component: {value}")
    return value


def inside(root: Path, value: str, *, allow_dot: bool = False) -> Path:
    name = relative_name(value, allow_dot=allow_dot)
    path = root if name == "." else root.joinpath(*name.split("/"))
    reject_links(path)
    if not path.resolve().is_relative_to(root):
        raise InputError(f"path leaves root: {name}")
    return path


def read_bytes(root: Path, name: str) -> bytes:
    path = inside(root, name)
    if not path.is_file():
        raise InputError(f"not a regular readable file: {name}")
    return path.read_bytes()


def evidence(name: str, data: bytes) -> dict[str, Any]:
    return {"path": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def file_evidence(root: Path, name: str) -> dict[str, Any]:
    path = inside(root, name)
    if not path.is_file():
        raise InputError(f"not a regular readable file: {name}")
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
            size += len(block)
    return {"path": name, "bytes": size, "sha256": digest.hexdigest()}


def _pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise InputError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _constant(value: str) -> Any:
    raise InputError(f"nonfinite JSON number: {value}")


def parse_json(data: bytes, *, quantities: bool = False) -> Any:
    try:
        return json.loads(
            data.decode("utf-8-sig"),
            object_pairs_hook=_pairs,
            parse_constant=_constant,
            parse_float=Decimal,
            parse_int=Decimal if quantities else int,
        )
    except (UnicodeError, ValueError, ArithmeticError, RecursionError) as exc:
        raise InputError(f"invalid JSON: {exc}") from exc


def require_keys(obj: Any, required: set[str], optional: set[str] | None = None) -> None:
    if not isinstance(obj, dict) or not required <= obj.keys():
        raise InputError(f"expected object with required keys: {sorted(required)}")
    extra = obj.keys() - required - (optional or set())
    if extra:
        raise InputError(f"unknown fields: {sorted(extra)}")


def text_field(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{label} must be a nonempty string")
    return value


def write_report(root: Path, name: str, report: dict[str, Any], protected: set[str]) -> None:
    path = inside(root, name)
    sources = [inside(root, source) for source in protected]
    if any(
        path == source or (path.exists() and source.exists() and path.samefile(source))
        for source in sources
    ):
        raise InputError("output must not overwrite an input")
    if not path.parent.is_dir():
        raise InputError("output parent directory must already exist")
    raw = json.dumps(report, indent=2, ensure_ascii=True, allow_nan=False, default=str) + "\n"
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=path.parent, delete=False
        ) as stream:
            temp_name = stream.name
            stream.write(raw)
        os.replace(temp_name, path)
    finally:
        if temp_name and Path(temp_name).exists():
            Path(temp_name).unlink()


def invalid_report(exc: Exception) -> int:
    print(json.dumps({"status": "invalid", "error": str(exc)}, ensure_ascii=True))
    return 2
