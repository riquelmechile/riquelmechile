#!/usr/bin/env python3
"""Repository-local GitHub profile integrity checks. No network access required."""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RAW_PREFIX = "https://raw.githubusercontent.com/riquelmechile/riquelmechile/main/"

EXPECTED_ASSETS = {
    "assets/profile/typing-name.svg",
    "assets/profile/contributions-year-dark.svg",
    "assets/profile/contributions-year-light.svg",
    "assets/profile/hero-dark.svg",
    "assets/profile/hero-light.svg",
    "assets/profile/pattern-lattice-dark.svg",
    "assets/profile/pattern-lattice-light.svg",
    "assets/profile/execution-pulse-dark.svg",
    "assets/profile/execution-pulse-light.svg",
    "assets/projects/panter-ai.svg",
    "assets/projects/doctor-chile.svg",
    "assets/projects/intelagent-private.svg",
    "assets/projects/xanxittoo-private.svg",
    "assets/projects/elcontador-private.svg",
}
BANNED_SVG = (
    "<image", "data:image", "base64,", "<script", "javascript:",
    "<foreignobject", "onload=", "onclick=", "onerror="
)
BANNED_EXTERNAL_SERVICES = (
    "capsule-render", "readme-typing-svg",
    "github-profile-summary-cards", "komarev.com"
)
PRIVATE_REPO_LINK = re.compile(
    r"https://github\.com/riquelmechile/(?:intelagent|xanxittoo|elcontador|"
    r"harness-medico-chile|msl)(?:[/#?]|$)", re.IGNORECASE
)


def validate_svg(path: Path) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8")
    lowered = text.lower()
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        return [f"{path}: invalid XML: {exc}"]

    if not root.tag.endswith("svg"):
        errors.append(f"{path}: root element is not SVG")
    for attr in ("viewBox", "role", "aria-labelledby"):
        if not root.attrib.get(attr):
            errors.append(f"{path}: missing {attr}")
    if root.attrib.get("role") != "img":
        errors.append(f"{path}: role must equal img")
    for tag in ("title", "desc"):
        node = next((item for item in root.iter() if item.tag.endswith(tag)), None)
        if node is None or not "".join(node.itertext()).strip():
            errors.append(f"{path}: missing nonempty {tag}")

    ids = [node.attrib["id"] for node in root.iter() if "id" in node.attrib]
    if len(ids) != len(set(ids)):
        errors.append(f"{path}: duplicate element IDs")

    for token in BANNED_SVG:
        if token in lowered:
            errors.append(f"{path}: prohibited SVG content {token}")
    if re.search(r"\son[a-z]+\s*=", lowered):
        errors.append(f"{path}: inline event handler")
    for node in root.iter():
        for attr, value in node.attrib.items():
            if attr.endswith("href") and value.startswith(("http://", "https://", "//")):
                errors.append(f"{path}: external SVG dependency {value}")
    return errors


def validate_readme_and_docs(root: Path) -> list[str]:
    errors = []
    filenames = ("README.md", "PROJECTS.md", "RESEARCH_COLLABORATION.md")
    documents = {}
    for name in filenames:
        target = root / name
        if not target.is_file():
            errors.append(f"Missing public document: {name}")
        else:
            documents[name] = target.read_text(encoding="utf-8")
    if "README.md" not in documents:
        return errors

    readme = documents["README.md"]
    required_readme = (
        "La variedad no es dispersión. Es búsqueda de estructura.",
        "neurodivergente",
        "https://github.com/riquelmechile/Panter-ai",
        "https://github.com/riquelmechile/Skills-Chile",
        "MCP Doctor Chile",
        "Harness Médico Chile",
        "Buscamos colaboración",
        "casos sintéticos",
        "06-NOV-2026",
        "Archivo histórico",
        "7.310 contribuciones",
        "76% commits",
        "19% pull requests",
        "4% issues",
        "1% revisiones de código",
        "https://github.com/riquelmechile/ZanaLLaima",
        "assets/profile/activity-2026-11-dark.svg",
        "assets/profile/activity-2026-11-light.svg",
        "RESEARCH_COLLABORATION.md",
        "PROJECTS.md#intelagent",
        "PROJECTS.md#xanxittoo",
        "PROJECTS.md#elcontador",
        "https://x.com/riquelme44127",
        "https://www.linkedin.com/in/sebastian-riquelme-vera-482778198",
    )
    for needle in required_readme:
        if needle.casefold() not in readme.casefold():
            errors.append(f"README missing expected content: {needle}")

    if "RESEARCH_COLLABORATION.md" in documents:
        clinical = documents["RESEARCH_COLLABORATION.md"].casefold()
        for needle in ("experimental", "casos sintéticos", "no envíes",
                       "no es un dispositivo médico", "médicos", "privacidad"):
            if needle.casefold() not in clinical:
                errors.append(f"Research collaboration safety text missing: {needle}")

    combined = "\n".join(documents.values())
    if PRIVATE_REPO_LINK.search(combined):
        errors.append("Public docs must not link directly to inaccessible private repositories")
    for token in BANNED_EXTERNAL_SERVICES:
        if token in readme:
            errors.append(f"External profile-rendering service prohibited: {token}")

    refs = re.findall(r'(?:src|srcset)="([^"]+\.svg)"', readme)
    if len(refs) < 14:
        errors.append(f"Expected at least 14 SVG image references, found {len(refs)}")
    for ref in refs:
        if not ref.startswith(RAW_PREFIX):
            errors.append(f"Noncanonical GitHub raw SVG URL: {ref}")
            continue
        relative = ref[len(RAW_PREFIX):]
        if not relative.startswith("assets/") or not (root / relative).is_file():
            errors.append(f"README SVG target missing or outside assets/: {relative}")

    for path in EXPECTED_ASSETS:
        if not (root / path).is_file():
            errors.append(f"Missing core SVG: {path}")

    signature = root / "assets/profile/typing-name.svg"
    if signature.is_file() and "<animate " not in signature.read_text(encoding="utf-8"):
        errors.append("Original animated name signature must be retained")
    return errors


def validate(root: Path = ROOT) -> tuple[list[str], int]:
    paths = sorted(root.glob("assets/**/*.svg"))
    errors = []
    if len(paths) < 21:
        errors.append(f"Expected at least 21 locally owned SVGs, found {len(paths)}")
    for path in paths:
        errors.extend(validate_svg(path))
    errors.extend(validate_readme_and_docs(root))
    return errors, len(paths)


if __name__ == "__main__":
    violations, count = validate()
    if violations:
        print("PROFILE VALIDATION FAILED")
        for violation in violations:
            print(f"- {violation}")
        sys.exit(1)
    print(f"PROFILE VALIDATION OK · {count} SVG assets · locally validated")
