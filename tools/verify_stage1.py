#!/usr/bin/env python3
"""Valida los dos entregables documentales de SAMURAI, etapa 1. Sin dependencias externas."""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "VISION_Y_ALCANCE.md"
LOGO = ROOT / "assets" / "samurai-logo.svg"


def main() -> int:
    if not DOC.is_file() or not LOGO.is_file():
        print("FAIL: faltan archivos de la etapa 1")
        return 1

    content = DOC.read_text(encoding="utf-8")
    required = ["## 1.", "## 2.", "## 3.", "## 4.", "## 5.", "## 6.", "## 7.", "1000 niveles", "16 clanes", "etapa 14"]
    missing = [part for part in required if part not in content]
    if missing:
        print(f"FAIL: contenido documental incompleto: {missing}")
        return 1

    try:
        svg = ET.parse(LOGO).getroot()
    except ET.ParseError as exc:
        print(f"FAIL: SVG invalido: {exc}")
        return 1

    namespace = "{http://www.w3.org/2000/svg}"
    if svg.tag != namespace + "svg" or svg.get("viewBox") != "0 0 512 512":
        print("FAIL: el logo no es un SVG cuadrado de 512x512")
        return 1
    if svg.findall(".//" + namespace + "script"):
        print("FAIL: el logo no debe ejecutar scripts")
        return 1
    if "http://" in LOGO.read_text(encoding="utf-8").replace('xmlns="http://www.w3.org/2000/svg"', ""):
        print("FAIL: el logo contiene referencias externas inesperadas")
        return 1
    print("PASS: etapa 1 valida (documento, secciones y logo SVG)")
    print("NOTA: la aprobacion de alcance por el usuario sigue pendiente.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
