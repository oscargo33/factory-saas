from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


CORPUS_VERSION = "2026.03.16"
ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = ROOT / "Docs"
README_PATH = DOCS_DIR / "README.md"
REGISTRY_PATH = DOCS_DIR / "REGISTRO-ULTIMA-VERSION.md"

VERSION_PATTERNS = (
    re.compile(r"^\*\*Versi[oó]n del documento:\*\*\s*(.+)$", re.IGNORECASE),
    re.compile(r"^\*\*(?:Versi[oó]n|Version):\*\*\s*(.+)$", re.IGNORECASE),
    re.compile(r"^Versi[oó]n:\s*(.+)$", re.IGNORECASE),
)
DATE_PATTERNS = (
    re.compile(r"^\*\*[^*]*[UuÚú]ltima actualizaci[oó]n:?\*\*\s*(.+)$"),
    re.compile(r"^[UuÚú]ltima actualizaci[oó]n:\s*(.+)$"),
)
STATE_WITH_VERSION_PATTERNS = (
    re.compile(r"^\*\*Estado:\*\*\s*v?(\d+(?:\.\d+){1,2})\s*[\-\u2014]\s*(.+)$", re.IGNORECASE),
    re.compile(r"^Estado:\s*v?(\d+(?:\.\d+){1,2})\s*[\-\u2014]\s*(.+)$", re.IGNORECASE),
)


def detect_existing_update_date(path: Path) -> str | None:
    if not path.exists():
        return None

    for line in path.read_text(encoding="utf-8").splitlines()[:12]:
        stripped = line.strip()
        for pattern in DATE_PATTERNS:
            match = pattern.match(stripped)
            if match:
                date_match = re.search(r"\d{4}-\d{2}-\d{2}", match.group(1))
                if date_match:
                    return date_match.group(0)
    return None


RUN_DATE = (
    os.environ.get("DOCS_SYNC_DATE")
    or detect_existing_update_date(README_PATH)
    or detect_existing_update_date(REGISTRY_PATH)
    or "2026-03-16"
)


def extract_version_parts(payload: str) -> tuple[str | None, str | None, str | None]:
    version_match = re.search(r"v?(\d+(?:\.\d+){1,2})", payload)
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", payload)
    version = version_match.group(1) if version_match else None
    date = date_match.group(1) if date_match else None
    remainder = payload
    if version_match:
        remainder = remainder.replace(version_match.group(0), "", 1)
    if date_match:
        remainder = remainder.replace(date_match.group(1), "", 1)
    remainder = remainder.strip(" -\u2014\u2013")
    return version, date, remainder or None


def normalize_markdown_text(original_text: str) -> tuple[str, str, str, str, bool]:
    lines = original_text.splitlines()
    heading_index = next((idx for idx, line in enumerate(lines) if line.startswith("# ")), None)

    detected_version = None
    detected_status = None
    removable_indexes: set[int] = set()

    scan_limit = min(len(lines), 30)
    for idx in range(scan_limit):
        if idx == heading_index:
            continue
        stripped = lines[idx].strip()
        if not stripped:
            continue

        for pattern in VERSION_PATTERNS:
            match = pattern.match(stripped)
            if match:
                version, _date, remainder = extract_version_parts(match.group(1))
                if version:
                    detected_version = version
                if remainder and not detected_status:
                    detected_status = remainder
                removable_indexes.add(idx)
                break
        else:
            matched_date = False
            for pattern in DATE_PATTERNS:
                if pattern.match(stripped):
                    removable_indexes.add(idx)
                    matched_date = True
                    break
            if matched_date:
                continue

            for pattern in STATE_WITH_VERSION_PATTERNS:
                match = pattern.match(stripped)
                if match:
                    if not detected_version:
                        detected_version = match.group(1)
                    if not detected_status:
                        detected_status = match.group(2).strip()
                    removable_indexes.add(idx)
                    break

    cleaned_lines = [line for idx, line in enumerate(lines) if idx not in removable_indexes]
    version = detected_version or "1.0.0"

    metadata_lines = [
        f"**Versión del documento:** {version}",
        f"**Última actualización:** {RUN_DATE}",
    ]
    if detected_status:
        metadata_lines.append(f"**Estado documental:** {detected_status}")

    if heading_index is None:
        body = cleaned_lines[:]
        while body and not body[0].strip():
            body.pop(0)
        final_lines = metadata_lines + [""] + body
    else:
        new_heading_index = heading_index - sum(1 for idx in removable_indexes if idx < heading_index)
        prefix = cleaned_lines[: new_heading_index + 1]
        suffix = cleaned_lines[new_heading_index + 1 :]
        while suffix and not suffix[0].strip():
            suffix.pop(0)
        final_lines = prefix + [""] + metadata_lines + [""] + suffix

    normalized_text = "\n".join(final_lines).rstrip() + "\n"
    first_line = normalized_text.splitlines()[0] if normalized_text else ""
    return version, RUN_DATE, first_line, normalized_text, normalized_text != original_text


def build_readme_content(total_files: int, markdown_files: int) -> str:
    return "\n".join(
        [
            "# Docs — Factory SaaS",
            "",
            f"**Versión del documento:** {CORPUS_VERSION}",
            f"**Última actualización:** {RUN_DATE}",
            "",
            "## Propósito",
            "",
            "Centralizar la documentación viva del proyecto y asegurar que cada artefacto tenga una versión explícita y un registro maestro consultable desde la raíz de `Docs/`.",
            "",
            "## Convención de versionado",
            "",
            "- Todo documento Markdown dentro de `Docs/` debe incluir `Versión del documento` y `Última actualización` en la cabecera.",
            "- Los artefactos no Markdown de `Docs/` se registran en el maestro de versiones aunque no soporten cabecera embebida.",
            "- La referencia de última versión consolidada del corpus vive en `Docs/REGISTRO-ULTIMA-VERSION.md`.",
            "- Cuando un documento cambie de fondo, debe actualizarse su versión documental antes de cerrar el item asociado.",
            "",
            "## Cobertura actual",
            "",
            f"- Archivos documentales registrados: {total_files}",
            f"- Documentos Markdown normalizados: {markdown_files}",
            f"- Versión actual del corpus Docs: {CORPUS_VERSION}",
            "",
            "## Registro maestro",
            "",
            "Ver `Docs/REGISTRO-ULTIMA-VERSION.md` para la versión más reciente de cada documento y artefacto documental.",
            "",
            "## Automatización",
            "",
            "- `make docs-sync`: regenera cabeceras versionadas y el registro maestro usando la fecha actual.",
            "- `make docs-check`: valida en modo no destructivo si el sincronizador dejaría cambios pendientes en `Docs/`.",
            "- El workflow `.github/workflows/docs-governance.yml` corre automáticamente en PRs y pushes a `main` cuando cambian artefactos documentales o el sincronizador.",
            "",
            "## Paquetes principales",
            "",
            "- `00-knowledge-base/`: criterios y estándares base.",
            "- `1-Core_Concept/`: visión conceptual y documentos ancla del producto.",
            "- `2-Design-Concept/`: diseño global y por app.",
            "- `Agile/`: backlog y artefactos Scrum activos.",
            "",
        ]
    )


def registry_row(path: Path, version: str, updated_at: str, title: str) -> str:
    relative_path = path.relative_to(ROOT).as_posix()
    safe_title = title.replace("|", "\\|")
    doc_type = path.suffix.lstrip(".") or "file"
    return f"| `{relative_path}` | {doc_type} | {version} | {updated_at} | {safe_title} |"


def extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("**Versión del documento:**"):
            continue
        if stripped.startswith("**Última actualización:**"):
            continue
        if stripped.startswith("**Estado documental:**"):
            continue
        if stripped.startswith("# "):
            return stripped[2:].strip()
        return stripped
    return fallback


def build_registry_content(entries: list[dict[str, str]]) -> str:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for entry in entries:
        relative = entry["path"].split("/", 2)
        section = relative[1] if len(relative) > 1 else "root"
        grouped[section].append(entry)

    lines = [
        "# Registro Maestro de Ultima Version de Docs",
        "",
        f"**Versión del documento:** {CORPUS_VERSION}",
        f"**Última actualización:** {RUN_DATE}",
        f"**Total de artefactos registrados:** {len(entries)}",
        "",
        "Este registro es la referencia canónica para consultar la última versión conocida de cada artefacto dentro de `Docs/`.",
        "",
    ]

    for section in sorted(grouped):
        lines.extend(
            [
                f"## {section}",
                "",
                "| Ruta | Tipo | Versión | Ultima actualización | Título / identificador |",
                "|---|---|---|---|---|",
            ]
        )
        for entry in sorted(grouped[section], key=lambda item: item["path"]):
            lines.append(entry["row"])
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize Docs metadata headers and rebuild the master version registry.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate whether synchronization would modify files without writing changes.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    write = not args.check

    docs_files = sorted(path for path in DOCS_DIR.rglob("*") if path.is_file())
    markdown_files = [path for path in docs_files if path.suffix.lower() == ".md"]

    entries: list[dict[str, str]] = []
    has_changes = False

    for path in markdown_files:
        if path in {README_PATH, REGISTRY_PATH}:
            continue

        original_text = path.read_text(encoding="utf-8")
        version, updated_at, first_line, normalized_text, changed = normalize_markdown_text(original_text)
        if changed and write:
            path.write_text(normalized_text, encoding="utf-8")
        has_changes = has_changes or changed
        title = extract_title(normalized_text, first_line or path.name)
        entries.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "row": registry_row(path, version, updated_at, title),
            }
        )

    extra_root_files = 0
    if not README_PATH.exists():
        extra_root_files += 1
    if not REGISTRY_PATH.exists():
        extra_root_files += 1

    final_total_files = len(docs_files) + extra_root_files
    final_markdown_files = len(markdown_files) + extra_root_files

    readme_content = build_readme_content(
        total_files=final_total_files,
        markdown_files=final_markdown_files,
    )
    readme_version, readme_updated, readme_first_line, normalized_readme_content, _ = normalize_markdown_text(
        readme_content,
    )
    current_readme = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else ""
    readme_changed = current_readme != normalized_readme_content
    if readme_changed and write:
        README_PATH.write_text(normalized_readme_content, encoding="utf-8")
    has_changes = has_changes or readme_changed
    entries.append(
        {
            "path": README_PATH.relative_to(ROOT).as_posix(),
            "row": registry_row(
                README_PATH,
                readme_version,
                readme_updated,
                extract_title(normalized_readme_content, readme_first_line or README_PATH.name),
            ),
        }
    )

    for path in docs_files:
        if path.suffix.lower() == ".md":
            continue
        entries.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "row": registry_row(path, "1.0.0", RUN_DATE, path.name),
            }
        )

    initial_registry_content = build_registry_content(entries)
    final_entries = entries + [
        {
            "path": REGISTRY_PATH.relative_to(ROOT).as_posix(),
            "row": registry_row(
                REGISTRY_PATH,
                CORPUS_VERSION,
                RUN_DATE,
                extract_title(initial_registry_content, REGISTRY_PATH.name),
            ),
        }
    ]
    final_registry_content = build_registry_content(final_entries)
    current_registry = REGISTRY_PATH.read_text(encoding="utf-8") if REGISTRY_PATH.exists() else ""
    registry_changed = current_registry != final_registry_content
    if registry_changed and write:
        REGISTRY_PATH.write_text(final_registry_content, encoding="utf-8")
    has_changes = has_changes or registry_changed

    if args.check and has_changes:
        print("Docs synchronization required.", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()