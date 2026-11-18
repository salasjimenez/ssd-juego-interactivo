# SAMURAI — Visión y alcance

**Etapa:** 1 de 50 | **Fecha:** 18/11/2026 | **Versión:** 1.0 | **Estado:** Pendiente de aprobación

## 1. Visión y público objetivo

SAMURAI será una aplicación web educativa, gratuita e individual con una experiencia de videojuego inspirada en un dojo samurái. Permitirá aprender programación e Ingeniería de Sistemas mediante retos cortos, práctica gradual y evaluaciones de dominio. Está dirigida a principiantes, estudiantes universitarios y profesionales que quieren especializarse. No sustituye una carrera acreditada ni emite títulos oficiales. Funcionará en navegadores actuales de computadora y móvil; el modo PWA offline llegará en la etapa 46.

## 2. Recorridos de aprendizaje

**Camino del Aprendiz:** 1000 niveles organizados en 10 ciclos de unos 100 niveles. Cada ciclo tendrá una región, un jefe final y un proyecto integrador. El contenido evolucionará de fundamentos de programación hacia sistemas, datos, infraestructura, seguridad, calidad y arquitectura.

**Rutas Profesionales:** 16 clanes: Frontend, Backend, Full Stack, Móvil, Videojuegos, Cloud, DevOps/SRE, Datos/IA, DBA, Redes y Sistemas, Ciberseguridad, QA, Arquitecto, Analista, PO/Scrum y Tech Lead. Cada clan progresará por Junior → Semi-Senior → Senior con proyectos y pruebas técnicas. Los dos recorridos podrán explorarse sin autenticación.

**Privacidad:** sin cuentas, contraseñas, rankings, chats, perfiles públicos ni funciones sociales. El usuario elegirá un nombre local. Su progreso permanecerá en el navegador y podrá exportarse/importarse en JSON versionado; no existirá sincronización automática entre dispositivos.

## 3. Alcance del MVP (etapa 14)

El primer **MVP jugable**, al finalizar la etapa 14, permitirá: ingresar un nombre; abrir una lección desde JSON; responder entre 5 y 10 ejercicios; recibir feedback y explicaciones; consultar un resumen; conservar avance tras cerrar el navegador; y exportar/importar progreso validado, con confirmación antes de reemplazarlo. Será usable con teclado y en pantallas móviles.

**No incluido inicialmente:** los 1000 niveles completos, clanes jugables, jefes, mapa, monedas, vidas, rangos, rachas, ejecución de código, certificados y soporte offline. Se implementarán en sus etapas planificadas (15–50). No se considerarán terminados sin sus correspondientes pruebas.

**Pruebas del MVP:** completar una lección de principio a fin; mostrar corrección y explicación en cada respuesta; recargar y conservar progreso; exportar/importar un archivo correcto; rechazar un archivo inválido; funcionar sin registro de usuario.

## 4. Principios pedagógicos y de experiencia

Cada lección tendrá un objetivo verificable, ejercicios con dificultad progresiva, feedback comprensible y oportunidades de repaso. Los jefes finales evaluarán competencias y los proyectos integradores aplicarán lo aprendido. La narrativa del sensei y las recompensas reforzarán la motivación sin sustituir la evaluación. Las animaciones respetarán la preferencia de movimiento reducido.

## 5. Arquitectura, operación y riesgos

**Stack:** C# con **.NET 10 LTS** y Blazor WebAssembly standalone; MudBlazor para interfaz, Razor para componentes y SVG/CSS para mapa y animaciones. Solución: `Samurai.Web`, `Samurai.Core`, `Samurai.Tests`, `tools/` y `Samurai.Web/wwwroot/content/`. No habrá páginas HTML artesanales; se conservará únicamente el host mínimo requerido por Blazor. JS interop se limitará a runtimes, audio y editor.

**Datos y calidad:** contenido JSON + Markdown validable y generable en Python/C#; progreso en IndexedDB, preferencias pequeñas en localStorage. Pruebas con xUnit, bUnit y Playwright. GitHub Actions generará una rama con archivos publicados y Render Static Site los servirá sin compilar, con reescritura SPA a `/index.html` y base `/`.

**Dependencias:** se adoptará .NET 10 LTS con parches vigentes (último parche 10.0.15 al 18/11/2026). MudBlazor y demás bibliotecas se fijarán en versiones estables compatibles, previa auditoría de vulnerabilidades directas y transitivas. No se aceptarán vulnerabilidades conocidas **altas o críticas** sin remediación documentada. La auditoría y revisión de parches continuarán en CI; no existe garantía de ausencia de vulnerabilidades futuras.

**Riesgos:** borrar datos del navegador puede destruir el progreso, de ahí la exportación JSON. Pyodide, SQLite WASM y Roslyn pueden aumentar descargas y consumo de memoria: se evaluarán y cargarán bajo demanda en etapas 30–34. Un Web Worker no constituye aislamiento absoluto de código arbitrario: antes de habilitarlo se deberán revisar CSP, red, límites de ejecución y finalización del Worker. La PWA estará sujeta a cuotas de caché y Render gratuito tiene límites de uso.

## 6. Glosario samurái

| Concepto | Definición en SAMURAI |
| --- | --- |
| Dojo | Pantalla principal de aprendizaje. |
| Sensei | Guía narrativa y pedagógica. |
| Camino | Itinerario académico de 1000 niveles. |
| Ciclo / región | Bloque curricular de unos 100 niveles. |
| Misión / pergamino | Lección o reto concreto. |
| Jefe final | Evaluación al cerrar un ciclo. |
| Proyecto integrador | Actividad que combina aprendizajes del ciclo. |
| Clan | Especialidad profesional. |
| Rango / cinturón | Avance por dominio; no es título oficial. |
| XP / ryō / vidas | Experiencia, moneda cosmética y oportunidades. |

## 7. Criterio de aprobación

La etapa 1 termina cuando se aprueban: visión, público, MVP y exclusiones; estructura de los dos recorridos y 16 clanes; glosario; política de seguridad; riesgos; y **un único emblema SVG** reutilizable para web y futura PWA. El documento queda **pendiente de aprobación** hasta recibir una confirmación expresa. No se inicia la etapa 2 hasta que el usuario indique **«continúa»**.

**Fuentes técnicas:** https://dotnet.microsoft.com/en-us/platform/support/policy · https://learn.microsoft.com/en-us/nuget/concepts/auditing-packages · https://render.com/docs/static-sites
