# SAMURAI — El dojo del código

**Etapa actual:** 2 de 50 — solución .NET 10 y presentación visual provisional. **Todavía no es un juego funcional**.

SAMURAI es una plataforma educativa gratuita e individual para aprender programación e Ingeniería de Sistemas. Plantea un camino universitario de 1000 niveles en 10 ciclos y 16 clanes profesionales. No se utilizarán cuentas, rankings ni funciones sociales.

## Stack y decisiones

- C#, .NET 10 LTS, Blazor WebAssembly **standalone**, páginas y layout con componentes Razor.
- CSS y SVG propios para presentación, sin JS interop adicional ni servicios externos en esta etapa.
- Se utilizará MudBlazor en la Etapa 3, conservando la identidad de SAMURAI.
- Los archivos HTML se limitan al documento host mínimo `Samurai.Web/wwwroot/index.html`, obligatorio para Blazor WASM; las pantallas están en Razor.
- NuGet centralizado en `Directory.Packages.props`, auditoría directa/transitiva en `Directory.Build.props` y dependencias bloqueadas con `packages.lock.json` tras la restauración.

## Estructura

```text
Samurai.sln
Samurai.Core/                         Biblioteca de reglas del dominio
Samurai.Web/                          Blazor WebAssembly standalone
  Layout/MainLayout.razor             Cabecera, navegación y pie
  Pages/                               Inicio, estado y ruta desconocida
  wwwroot/css/app.css                  Presentación responsive provisional
  wwwroot/images/samurai-logo.svg      Copia idéntica del logo original
  wwwroot/content/                    JSON/Markdown en etapas posteriores
Samurai.Tests/                        Pruebas xUnit v3
assets/samurai-logo.svg               Fuente original y única del emblema
docs/                                 Documentación y decisiones
tools/                                Validadores locales
Directory.Build.props                 Seguridad y propiedades comunes
Directory.Packages.props              Paquetes NuGet centralizados
NuGet.Config                           Fuentes oficiales de restauración
```

La copia del logo en `wwwroot` es necesaria para servirlo en el navegador. `tools/verify_stage2_polish.py` comprueba que sea **exactamente el mismo SVG**, sin nuevas versiones visuales.

## Requisitos

- SDK .NET 10.0.404 o parche superior **en la misma banda**.
- Git y conexión inicial a NuGet.
- Python 3 (para validadores estructurales).

## Validar y ejecutar (Git Bash)

```bash
cd /c/dev/Samurai
python tools/verify_stage1.py
python tools/verify_stage2.py
python tools/verify_stage2_polish.py
dotnet --version
dotnet restore Samurai.sln
dotnet build Samurai.sln -c Debug --no-restore
dotnet test Samurai.sln -c Debug --no-restore
dotnet package list Samurai.sln --vulnerable --include-transitive
dotnet run --project Samurai.Web --launch-profile http
```

Sitio: http://localhost:5127/  
Estado: http://localhost:5127/estado

Los archivos `packages.lock.json` generados al restaurar **deben versionarse**. Los directorios `bin/` y `obj/` se ignoran en `.gitignore`.

## Seguridad

`NuGetAuditMode=all` audita paquetes directos y transitivos, y `NU1903`/`NU1904` detienen restauraciones con vulnerabilidades altas o críticas. Revisar el reporte completo de vulnerabilidades y cualquier error `NU1900` de conexión con la fuente de auditoría; no confundir un fallo al consultar con la ausencia de hallazgos.

## Estado funcional

**Disponible en etapa 2:** estructura de tres proyectos .NET, pruebas unitarias iniciales, navegación `Inicio`/`Estado`, diseño previo responsive y logo único.

**No implementado:** cursos, niveles reales, gamificación, mapa, clanes jugables, almacenamiento, ejecución de código, offline/PWA, MudBlazor ni despliegue a Render. Estas capacidades se incorporan únicamente en las etapas previstas de la hoja de ruta.

Documentación: `docs/VISION_Y_ALCANCE.md`, `docs/ETAPA_02.md` y `docs/ETAPA_02_AJUSTES.md`.
