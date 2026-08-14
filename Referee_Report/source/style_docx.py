#!/usr/bin/env python3
"""Apply the referee-report DOCX style system with deterministic OOXML edits.

The builder uses Pandoc for semantic document construction and this script for
the exact ``standard_business_brief`` typography, page geometry, list indents,
and quiet running furniture required by the Documents skill. It intentionally
uses only Python's standard library so it can run in the project's recorded
environment without adding a document-generation dependency.
"""

from __future__ import annotations

import argparse
import copy
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
XML_NS = "http://www.w3.org/XML/1998/namespace"

ET.register_namespace("w", W_NS)
ET.register_namespace("r", R_NS)
ET.register_namespace("", PKG_REL_NS)
ET.register_namespace("ct", CT_NS)


def qn(namespace: str, local: str) -> str:
    """Return a Clark-notation XML name."""

    return f"{{{namespace}}}{local}"


def ensure_child(parent: ET.Element, tag: str) -> ET.Element:
    """Return the first child named ``tag``, creating it if absent."""

    child = parent.find(tag)
    if child is None:
        child = ET.SubElement(parent, tag)
    return child


def set_attr(element: ET.Element, namespace: str, name: str, value: str) -> None:
    """Set a namespaced XML attribute."""

    element.set(qn(namespace, name), value)


def remove_children(parent: ET.Element, tags: set[str]) -> None:
    """Remove direct children whose tags occur in ``tags``."""

    for child in list(parent):
        if child.tag in tags:
            parent.remove(child)


def set_spacing(
    p_pr: ET.Element,
    *,
    before: int,
    after: int,
    line: int,
    line_rule: str = "auto",
) -> None:
    """Set paragraph spacing values in twentieths of a point."""

    spacing = ensure_child(p_pr, qn(W_NS, "spacing"))
    set_attr(spacing, W_NS, "before", str(before))
    set_attr(spacing, W_NS, "after", str(after))
    set_attr(spacing, W_NS, "line", str(line))
    set_attr(spacing, W_NS, "lineRule", line_rule)


def set_font(
    r_pr: ET.Element,
    *,
    family: str,
    half_points: int,
    color: str,
    bold: bool = False,
    italic: bool = False,
) -> None:
    """Set explicit run typography on a Word style."""

    fonts = ensure_child(r_pr, qn(W_NS, "rFonts"))
    for key in ("ascii", "hAnsi", "eastAsia", "cs"):
        set_attr(fonts, W_NS, key, family)

    size = ensure_child(r_pr, qn(W_NS, "sz"))
    set_attr(size, W_NS, "val", str(half_points))
    size_cs = ensure_child(r_pr, qn(W_NS, "szCs"))
    set_attr(size_cs, W_NS, "val", str(half_points))

    color_el = ensure_child(r_pr, qn(W_NS, "color"))
    set_attr(color_el, W_NS, "val", color)

    for tag, enabled in (("b", bold), ("bCs", bold), ("i", italic), ("iCs", italic)):
        element = r_pr.find(qn(W_NS, tag))
        if enabled:
            if element is None:
                ET.SubElement(r_pr, qn(W_NS, tag))
        elif element is not None:
            r_pr.remove(element)


def style_by_id(root: ET.Element, style_id: str) -> ET.Element | None:
    """Find a Word style by its style identifier."""

    for style in root.findall(qn(W_NS, "style")):
        if style.get(qn(W_NS, "styleId")) == style_id:
            return style
    return None


def apply_style(
    root: ET.Element,
    style_id: str,
    *,
    size: int,
    color: str,
    before: int,
    after: int,
    line: int,
    bold: bool = False,
    italic: bool = False,
    alignment: str | None = None,
    keep_next: bool = False,
) -> None:
    """Apply explicit standard-business-brief tokens to one Word style."""

    style = style_by_id(root, style_id)
    if style is None:
        return

    p_pr = ensure_child(style, qn(W_NS, "pPr"))
    set_spacing(p_pr, before=before, after=after, line=line)
    if alignment is not None:
        jc = ensure_child(p_pr, qn(W_NS, "jc"))
        set_attr(jc, W_NS, "val", alignment)
    if keep_next and p_pr.find(qn(W_NS, "keepNext")) is None:
        ET.SubElement(p_pr, qn(W_NS, "keepNext"))
    if p_pr.find(qn(W_NS, "widowControl")) is None:
        ET.SubElement(p_pr, qn(W_NS, "widowControl"))
    remove_children(p_pr, {qn(W_NS, "pBdr")})

    r_pr = ensure_child(style, qn(W_NS, "rPr"))
    set_font(
        r_pr,
        family="Calibri",
        half_points=size,
        color=color,
        bold=bold,
        italic=italic,
    )


def patch_styles(xml: bytes) -> bytes:
    """Patch document styles to the selected exact token map."""

    root = ET.fromstring(xml)

    doc_defaults = ensure_child(root, qn(W_NS, "docDefaults"))
    r_pr_default = ensure_child(doc_defaults, qn(W_NS, "rPrDefault"))
    r_pr = ensure_child(r_pr_default, qn(W_NS, "rPr"))
    set_font(r_pr, family="Calibri", half_points=22, color="000000")
    p_pr_default = ensure_child(doc_defaults, qn(W_NS, "pPrDefault"))
    p_pr = ensure_child(p_pr_default, qn(W_NS, "pPr"))
    set_spacing(p_pr, before=0, after=120, line=264)

    apply_style(
        root,
        "Normal",
        size=22,
        color="000000",
        before=0,
        after=120,
        line=264,
    )
    apply_style(
        root,
        "Title",
        size=46,
        color="000000",
        before=0,
        after=80,
        line=276,
        bold=True,
        alignment="center",
        keep_next=True,
    )
    apply_style(
        root,
        "Subtitle",
        size=28,
        color="555555",
        before=0,
        after=80,
        line=280,
        alignment="center",
        keep_next=True,
    )
    apply_style(
        root,
        "Heading1",
        size=32,
        color="2E74B5",
        before=320,
        after=160,
        line=264,
        bold=True,
        keep_next=True,
    )
    apply_style(
        root,
        "Heading2",
        size=26,
        color="2E74B5",
        before=240,
        after=120,
        line=264,
        bold=True,
        keep_next=True,
    )
    apply_style(
        root,
        "Heading3",
        size=24,
        color="1F4D78",
        before=160,
        after=80,
        line=264,
        bold=True,
        keep_next=True,
    )
    apply_style(
        root,
        "Caption",
        size=18,
        color="555555",
        before=80,
        after=120,
        line=240,
        italic=True,
        alignment="center",
        keep_next=False,
    )
    apply_style(
        root,
        "ImageCaption",
        size=18,
        color="555555",
        before=80,
        after=120,
        line=240,
        italic=True,
        alignment="center",
        keep_next=False,
    )
    apply_style(
        root,
        "BlockText",
        size=22,
        color="333333",
        before=80,
        after=120,
        line=280,
        italic=False,
    )

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def patch_numbering(xml: bytes) -> bytes:
    """Set level-zero list geometry to the preset's real-numbering tokens."""

    root = ET.fromstring(xml)
    for level in root.iter(qn(W_NS, "lvl")):
        if level.get(qn(W_NS, "ilvl")) != "0":
            continue
        p_pr = ensure_child(level, qn(W_NS, "pPr"))
        tabs = ensure_child(p_pr, qn(W_NS, "tabs"))
        tab = tabs.find(qn(W_NS, "tab"))
        if tab is None:
            tab = ET.SubElement(tabs, qn(W_NS, "tab"))
        set_attr(tab, W_NS, "val", "num")
        set_attr(tab, W_NS, "pos", "720")
        ind = ensure_child(p_pr, qn(W_NS, "ind"))
        set_attr(ind, W_NS, "left", "720")
        set_attr(ind, W_NS, "hanging", "360")
        set_spacing(p_pr, before=0, after=160, line=280)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def patch_document(xml: bytes) -> bytes:
    """Set Letter page geometry and attach quiet header/footer references."""

    root = ET.fromstring(xml)
    for sect_pr in root.iter(qn(W_NS, "sectPr")):
        for child in list(sect_pr):
            if child.tag in {qn(W_NS, "headerReference"), qn(W_NS, "footerReference")}:
                sect_pr.remove(child)

        header_ref = ET.Element(qn(W_NS, "headerReference"))
        set_attr(header_ref, W_NS, "type", "default")
        header_ref.set(qn(R_NS, "id"), "rIdRefereeHeader")
        footer_ref = ET.Element(qn(W_NS, "footerReference"))
        set_attr(footer_ref, W_NS, "type", "default")
        footer_ref.set(qn(R_NS, "id"), "rIdRefereeFooter")
        sect_pr.insert(0, footer_ref)
        sect_pr.insert(0, header_ref)

        pg_sz = ensure_child(sect_pr, qn(W_NS, "pgSz"))
        set_attr(pg_sz, W_NS, "w", "12240")
        set_attr(pg_sz, W_NS, "h", "15840")
        pg_sz.attrib.pop(qn(W_NS, "orient"), None)

        pg_mar = ensure_child(sect_pr, qn(W_NS, "pgMar"))
        for key in ("top", "right", "bottom", "left"):
            set_attr(pg_mar, W_NS, key, "1440")
        set_attr(pg_mar, W_NS, "header", "708")
        set_attr(pg_mar, W_NS, "footer", "708")
        set_attr(pg_mar, W_NS, "gutter", "0")

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def patch_relationships(xml: bytes) -> bytes:
    """Add deterministic document relationships for header and footer parts."""

    root = ET.fromstring(xml)
    for relationship in list(root):
        if relationship.get("Id") in {"rIdRefereeHeader", "rIdRefereeFooter"}:
            root.remove(relationship)

    ET.SubElement(
        root,
        qn(PKG_REL_NS, "Relationship"),
        {
            "Id": "rIdRefereeHeader",
            "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/header",
            "Target": "header1.xml",
        },
    )
    ET.SubElement(
        root,
        qn(PKG_REL_NS, "Relationship"),
        {
            "Id": "rIdRefereeFooter",
            "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer",
            "Target": "footer1.xml",
        },
    )
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def patch_content_types(xml: bytes) -> bytes:
    """Register the header and footer content types."""

    root = ET.fromstring(xml)
    desired = {
        "/word/header1.xml": "application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml",
        "/word/footer1.xml": "application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml",
    }
    for part_name, content_type in desired.items():
        existing = next(
            (item for item in root if item.get("PartName") == part_name),
            None,
        )
        if existing is None:
            ET.SubElement(
                root,
                qn(CT_NS, "Override"),
                {"PartName": part_name, "ContentType": content_type},
            )
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def patch_settings(xml: bytes) -> bytes:
    """Ask Word to update displayed fields, including page numbers."""

    root = ET.fromstring(xml)
    update_fields = root.find(qn(W_NS, "updateFields"))
    if update_fields is None:
        update_fields = ET.SubElement(root, qn(W_NS, "updateFields"))
    set_attr(update_fields, W_NS, "val", "true")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def header_xml() -> bytes:
    """Return a restrained two-sided running header."""

    root = ET.Element(qn(W_NS, "hdr"))
    paragraph = ET.SubElement(root, qn(W_NS, "p"))
    p_pr = ET.SubElement(paragraph, qn(W_NS, "pPr"))
    tabs = ET.SubElement(p_pr, qn(W_NS, "tabs"))
    tab = ET.SubElement(tabs, qn(W_NS, "tab"))
    set_attr(tab, W_NS, "val", "right")
    set_attr(tab, W_NS, "pos", "9360")
    spacing = ET.SubElement(p_pr, qn(W_NS, "spacing"))
    set_attr(spacing, W_NS, "after", "0")

    for text, insert_tab in (
        ("Referee Report", False),
        ("July 25, 2025 draft", True),
    ):
        if insert_tab:
            tab_run = ET.SubElement(paragraph, qn(W_NS, "r"))
            ET.SubElement(tab_run, qn(W_NS, "tab"))
        run = ET.SubElement(paragraph, qn(W_NS, "r"))
        r_pr = ET.SubElement(run, qn(W_NS, "rPr"))
        set_font(r_pr, family="Calibri", half_points=18, color="6B7280")
        text_el = ET.SubElement(run, qn(W_NS, "t"))
        text_el.text = text
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def footer_xml() -> bytes:
    """Return a centered PAGE field with muted styling."""

    root = ET.Element(qn(W_NS, "ftr"))
    paragraph = ET.SubElement(root, qn(W_NS, "p"))
    p_pr = ET.SubElement(paragraph, qn(W_NS, "pPr"))
    jc = ET.SubElement(p_pr, qn(W_NS, "jc"))
    set_attr(jc, W_NS, "val", "center")
    spacing = ET.SubElement(p_pr, qn(W_NS, "spacing"))
    set_attr(spacing, W_NS, "after", "0")

    field = ET.SubElement(paragraph, qn(W_NS, "fldSimple"))
    set_attr(field, W_NS, "instr", " PAGE ")
    run = ET.SubElement(field, qn(W_NS, "r"))
    r_pr = ET.SubElement(run, qn(W_NS, "rPr"))
    set_font(r_pr, family="Calibri", half_points=18, color="6B7280")
    text_el = ET.SubElement(run, qn(W_NS, "t"))
    text_el.text = "1"
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def transform_parts(parts: dict[str, bytes]) -> dict[str, bytes]:
    """Return a transformed copy of all DOCX package parts."""

    updated = copy.copy(parts)
    updated["word/styles.xml"] = patch_styles(parts["word/styles.xml"])
    updated["word/document.xml"] = patch_document(parts["word/document.xml"])
    if "word/numbering.xml" in parts:
        updated["word/numbering.xml"] = patch_numbering(parts["word/numbering.xml"])
    updated["word/_rels/document.xml.rels"] = patch_relationships(
        parts["word/_rels/document.xml.rels"]
    )
    updated["[Content_Types].xml"] = patch_content_types(parts["[Content_Types].xml"])
    if "word/settings.xml" in parts:
        updated["word/settings.xml"] = patch_settings(parts["word/settings.xml"])
    updated["word/header1.xml"] = header_xml()
    updated["word/footer1.xml"] = footer_xml()
    return updated


def write_docx(input_path: Path, output_path: Path) -> None:
    """Read, patch, and atomically write one DOCX package."""

    with zipfile.ZipFile(input_path) as archive:
        parts = {name: archive.read(name) for name in archive.namelist()}
    updated = transform_parts(parts)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        prefix="referee_report_", suffix=".docx", dir=output_path.parent, delete=False
    ) as temporary:
        temporary_path = Path(temporary.name)

    try:
        with zipfile.ZipFile(
            temporary_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as archive:
            for name, payload in updated.items():
                archive.writestr(name, payload)
        temporary_path.replace(output_path)
    finally:
        temporary_path.unlink(missing_ok=True)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("input_docx", type=Path)
    parser.add_argument("output_docx", type=Path)
    return parser.parse_args()


def main() -> None:
    """Apply the style and save the result."""

    args = parse_args()
    write_docx(args.input_docx, args.output_docx)


if __name__ == "__main__":
    main()
