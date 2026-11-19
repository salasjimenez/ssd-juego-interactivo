#!/usr/bin/env python3
"""Preflight sin paquetes externos: verifica estructura, referencias y seguridad.
No sustituye `dotnet restore`, `dotnet build`, `dotnet test` ni la auditoria NuGet.
"""
from pathlib import Path
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "Samurai.sln",
    "global.json",
    "NuGet.Config",
    "Directory.Build.props",
    "Directory.Packages.props",
    "Samurai.Core/Samurai.Core.csproj",
    "Samurai.Core/ProjectDefinition.cs",
    "Samurai.Web/Samurai.Web.csproj",
    "Samurai.Web/Program.cs",
    "Samurai.Web/App.razor",
    "Samurai.Web/Pages/Home.razor",
    "Samurai.Web/Pages/NotFound.razor",
    "Samurai.Web/Pages/Status.razor",
    "Samurai.Web/Layout/MainLayout.razor",
    "Samurai.Web/wwwroot/index.html",
    "Samurai.Web/wwwroot/content/.gitkeep",
    "Samurai.Tests/Samurai.Tests.csproj",
    "Samurai.Tests/ProjectDefinitionTests.cs",
    "assets/samurai-logo.svg",
    "docs/VISION_Y_ALCANCE.md",
]


def check(condition: bool, issue: str, problems: list[str]) -> None:
    if not condition:
        problems.append(issue)


def main() -> int:
    problems: list[str] = []
    for file in REQUIRED:
        check((ROOT / file).is_file(), f"Falta el archivo: {file}", problems)

    if problems:
        for error in problems:
            print("ERROR:", error)
        return 1

    sdk = json.loads((ROOT / "global.json").read_text(encoding="utf-8"))["sdk"]
    check(sdk["version"] == "10.0.404", "SDK no fijado a 10.0.404", problems)
    check(sdk.get("allowPrerelease") is False, "Prereleases del SDK no bloqueadas", problems)
    check(sdk.get("rollForward") == "latestPatch", "RollForward debe ser latestPatch", problems)

    for name in ("Samurai.Core", "Samurai.Web", "Samurai.Tests"):
        sln = (ROOT / "Samurai.sln").read_text(encoding="utf-8")
        check(f'{name}\\{name}.csproj' in sln, f"La solucion no incluye {name}", problems)

    props = ET.parse(ROOT / "Directory.Build.props").getroot()
    def prop(name: str) -> str:
        match = props.find(f".//{name}")
        return (match.text or "").strip() if match is not None else ""

    check(prop("TargetFramework") == "net10.0", "TargetFramework incorrecto", problems)
    check(prop("NuGetAudit") == "true", "Auditoria NuGet desactivada", problems)
    check(prop("NuGetAuditMode") == "all", "No se auditan paquetes transitivos", problems)
    check(prop("NuGetAuditLevel") == "high", "Umbral de severidad no es high", problems)
    check("NU1903" in prop("WarningsAsErrors") and "NU1904" in prop("WarningsAsErrors"), "Advertencias altas/criticas no detienen build", problems)

    packages = ET.parse(ROOT / "Directory.Packages.props").getroot()
    versions = {p.attrib["Include"]: p.attrib.get("Version", "") for p in packages.findall(".//PackageVersion")}
    expected = {
        "Microsoft.AspNetCore.Components.WebAssembly": "10.0.15",
        "Microsoft.AspNetCore.Components.WebAssembly.DevServer": "10.0.15",
        "xunit.v3.mtp-off": "4.0.3",
        "xunit.runner.visualstudio": "4.0.1",
        "Microsoft.NET.Test.Sdk": "18.11.1",
    }
    check(versions == expected, "Las versiones de paquetes no coinciden con la lista aprobada", problems)
    for name in ("Samurai.Core", "Samurai.Web", "Samurai.Tests"):
        project = ET.parse(ROOT / name / f"{name}.csproj").getroot()
        for ref in project.findall(".//PackageReference"):
            check("Version" not in ref.attrib, f"{name}: version fuera del archivo central", problems)
            check(ref.attrib["Include"] in versions, f"{name}: paquete sin version central", problems)
        for ref in project.findall(".//ProjectReference"):
            other = (ROOT / name / ref.attrib["Include"].replace("\\", "/")).resolve()
            check(other.is_file(), f"{name}: ProjectReference roto: {other.name}", problems)

    host = (ROOT / "Samurai.Web/wwwroot/index.html").read_text(encoding="utf-8")
    check('<base href="/" />' in host, 'Base href debe ser "/"', problems)
    check('src="_framework/blazor.webassembly.js"' in host, "Falta el script del runtime Blazor", problems)
    check(not re.search(r'<script[^>]+src=["\']https?://', host, re.IGNORECASE), "Se detecto un script externo", problems)

    page = (ROOT / "Samurai.Web/Pages/Home.razor").read_text(encoding="utf-8")
    check('@page "/"' in page, "Falta ruta raiz de Blazor", problems)
    status = (ROOT / "Samurai.Web/Pages/Status.razor").read_text(encoding="utf-8")
    check('@page "/estado"' in status, "Falta ruta de estado de Blazor", problems)
    app = (ROOT / "Samurai.Web/App.razor").read_text(encoding="utf-8")
    check('NotFoundPage=' in app, "Blazor .NET 10 requiere NotFoundPage", problems)
    check('<NotFound>' not in app, "El fragmento NotFound es incompatible con .NET 10", problems)

    for problem in problems:
        print("ERROR:", problem)
    if problems:
        return 1
    print("PASS: etapa 2 valida (estructura, proyectos, rutas, SDK y auditoria).")
    print("NOTA: ejecutar dotnet restore, dotnet build y dotnet test en Windows para validar el build real.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
