#!/usr/bin/env python3
"""Preflight de la correccion visual de v2. No sustituye build/test/auditoria NuGet."""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "Samurai.Web"


def main() -> int:
    problems: list[str] = []
    required = [
        ".gitattributes",
        "assets/samurai-logo.svg",
        "Samurai.Web/wwwroot/images/samurai-logo.svg",
        "Samurai.Web/wwwroot/css/app.css",
        "Samurai.Web/wwwroot/index.html",
        "Samurai.Web/Layout/MainLayout.razor",
        "Samurai.Web/Pages/Home.razor",
        "Samurai.Web/Pages/Status.razor",
        "Samurai.Web/Pages/NotFound.razor",
        "docs/ETAPA_02_AJUSTES.md",
    ]
    for item in required:
        if not (ROOT / item).is_file():
            problems.append(f"Falta: {item}")

    if problems:
        for issue in problems:
            print(f"ERROR: {issue}")
        return 1

    src_logo = (ROOT / "assets/samurai-logo.svg").read_bytes()
    web_logo = (WEB / "wwwroot/images/samurai-logo.svg").read_bytes()
    if src_logo != web_logo:
        problems.append("El logo web difiere del logo original de Etapa 1")
    try:
        logo = ET.fromstring(web_logo)
        if not logo.tag.endswith("svg"):
            problems.append("El logo web no es SVG")
    except ET.ParseError:
        problems.append("El logo web no es SVG valido")

    index = (WEB / "wwwroot/index.html").read_text(encoding="utf-8")
    css = (WEB / "wwwroot/css/app.css").read_text(encoding="utf-8")
    layout = (WEB / "Layout/MainLayout.razor").read_text(encoding="utf-8")
    home = (WEB / "Pages/Home.razor").read_text(encoding="utf-8")
    status = (WEB / "Pages/Status.razor").read_text(encoding="utf-8")

    checks = [
        ('<base href="/" />' in index, "base href alterado: debe ser /"),
        ('href="images/samurai-logo.svg"' in index, "Falta favicon original"),
        ('src="_framework/blazor.webassembly.js"' in index, "Falta el runtime Blazor"),
        ('src="images/samurai-logo.svg"' in layout and 'src="images/samurai-logo.svg"' in home, "El layout y el inicio deben reutilizar el unico emblema"),
        ('<main id="main-content"' in layout and 'class="skip-link"' in layout, "Falta navegacion accesible"),
        ('@page "/"' in home and '@page "/estado"' in status, "Faltan rutas"),
        ('@ProjectDefinition.AcademicLevels' in home and '@ProjectDefinition.ProfessionalClans' in home, "Los contadores deben venir de Samurai.Core"),
        ('Vista visual preliminar de la Etapa 2' in home, "Falta indicar que es una vista preliminar"),
        ('prefers-reduced-motion' in css, "Falta soporte de movimiento reducido"),
        ('@media (max-width: 580px)' in css, "Falta diseno responsive"),
        (not re.search(r'<script[^>]+src=["\']https?://', index, re.IGNORECASE), "No usar JavaScript remoto en el host"),
        ('**/bin/' in (ROOT / '.gitignore').read_text(encoding='utf-8'), 'Falta ignorar bin/ de .NET'),
        ('**/obj/' in (ROOT / '.gitignore').read_text(encoding='utf-8'), 'Falta ignorar obj/ de .NET'),
    ]
    for ok, message in checks:
        if not ok:
            problems.append(message)

    if problems:
        for issue in problems:
            print(f"ERROR: {issue}")
        return 1

    print("PASS: v2 refactor valida estructura, identidad grafica, navegacion y responsive")
    print("NOTA: aun se requiere dotnet restore/build/test y revision visual local")
    return 0


if __name__ == "__main__":
    sys.exit(main())
