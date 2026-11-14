<div align="center">

<img src="assets/sello.svg" alt="" width="64">

# Maximiliano Cabello Mata

**Modelado 3D · Animación digital · Análisis y automatización de datos**

Estudiante de Ingeniería en Entornos Virtuales y Negocios Digitales · Estado de México

[![Blender](https://img.shields.io/badge/Blender-Geometry%20Nodes-E87D0D?logo=blender&logoColor=white)](renders/)
[![Python](https://img.shields.io/badge/Python-datos%20y%20automatizaci%C3%B3n-3776AB?logo=python&logoColor=white)](#proyectos)
[![SQL](https://img.shields.io/badge/SQL-DuckDB%20%C2%B7%20MongoDB-4479A1?logo=duckdb&logoColor=white)](#proyectos)
[![Disponible](https://img.shields.io/badge/disponible-estad%C3%ADa%20%C2%B7%20pr%C3%A1cticas%20%C2%B7%20junior-3b3256)](#contacto)

[Proyectos](#proyectos) · [Renders](#renders-y-trabajo-en-blender) · [Cómo trabajo](#cómo-trabajo) · [CV](cv/CV_Maximiliano_Cabello_Mata.pdf) · [Contacto](#contacto)

</div>

---

## Sobre mí

Tengo formación técnica en Animación Digital y estudio Ingeniería en Entornos Virtuales y Negocios Digitales en la Universidad Tecnológica de Nezahualcóyotl. Trabajo en dos áreas que se cruzan seguido:

| 3D | Datos |
|---|---|
| Modelado en Blender, incluido el modelado procedimental con **Geometry Nodes** | Extracción, limpieza y análisis de datos con **Python** y **SQL** |
| Materiales, animación y render (Cycles y EEVEE) | Bases de datos con **DuckDB**, **MongoDB** y archivos **Parquet** |
| Scripts de Python para automatizar tareas en Blender | Automatización con **GitHub Actions** y almacenamiento en **Azure** |
| Escenas 3D para la web con **A-Frame** | Cuadernos de análisis en **Jupyter** y pruebas con **pytest** |

Busco una **estadía profesional, prácticas o un puesto junior** en 3D, entornos virtuales o datos, en la Ciudad de México o a distancia.

## Proyectos

Mi proyecto principal es **[Amatista 3D](https://amatista-3d.tech)**, una plataforma para aprender 3D con Blender y A-Frame. Está dividida en varios repositorios: una API, un motor que evalúa las prácticas dentro de Blender y G7B, el motor de datos que mide cómo corre Blender en equipos reales.

<!-- PROYECTOS:INICIO -->
| Proyecto | Qué hace | Tecnologías | Actualizado |
|---|---|---|---|
| [**Amatista · G7B**](https://github.com/Maximiliano-cabello-mata/amatista-g7b-etl) | Motor de datos de Amatista: extrae 33 fuentes en línea, mide el rendimiento de Blender en distintos equipos y guarda todo en un cubo versionado con 3,003 mediciones. | Python · Scrapy · DuckDB · Parquet · MongoDB · Azure · GitHub Actions | — |
| [**Amatista · Motor**](https://github.com/Maximiliano-cabello-mata/amatista-motor-) | Motor que evalúa lo que el alumno hace en Blender, con un complemento para Blender y prácticas descritas en JSON. | Python · bpy (API de Blender) · pytest | — |
| [**Amatista · API**](https://github.com/Maximiliano-cabello-mata/amatista-api-) | API de la plataforma: cuentas, progreso, contenido, clases, evaluación y base de datos; también sirve el complemento de Blender. | Python · FastAPI · Oracle · SQLite · Caddy | — |
| [**SIDP**](https://github.com/Maximiliano-cabello-mata/sidp-core) | Base técnica de un sistema de gestión escolar para una primaria, pensado para tres equipos en red local sin servidor dedicado. | Python · SQLite · TLS | — |

<sub>Tabla actualizada automáticamente el 14/11/2026.</sub>
<!-- PROYECTOS:FIN -->

## Renders y trabajo en Blender

Mis trabajos en Blender, del más reciente al más antiguo. Cada imagen abre la ficha del trabajo con el motor de render, las técnicas y todas las vistas. La galería completa está en [`renders/`](renders/).

<!-- GALERIA:INICIO -->
> **Próximamente.** Aquí aparecerán mis renders y trabajos en Blender.
> Cada trabajo nuevo en [`renders/`](renders/) se publica automáticamente.
<!-- GALERIA:FIN -->

## Cómo trabajo

- **Con IA, revisando cada resultado.** Mis proyectos actuales los desarrollo con apoyo de inteligencia artificial (Claude y ChatGPT) para programar, documentar y analizar. Reviso, pruebo y corrijo lo que generan antes de integrarlo.
- **Todo documentado y versionado.** Cada proyecto tiene su README, su historial en Git y pruebas donde aplica.
- **Automatizo lo repetitivo.** Si una tarea se repite, la convierto en un script o en un flujo de GitHub Actions.

### Este repositorio se mantiene solo

| Automatización | Qué hace | Estado |
|---|---|---|
| [Galería de renders](.github/workflows/galeria.yml) | Cuando subo un trabajo a `renders/`, valida su ficha, crea miniaturas y actualiza la galería de esta página. | [![Galería](https://github.com/Maximiliano-cabello-mata/Maximiliano_KD/actions/workflows/galeria.yml/badge.svg)](https://github.com/Maximiliano-cabello-mata/Maximiliano_KD/actions/workflows/galeria.yml) |
| [Proyectos](.github/workflows/proyectos.yml) | Cada lunes consulta la API de GitHub y actualiza la tabla de proyectos. | [![Proyectos](https://github.com/Maximiliano-cabello-mata/Maximiliano_KD/actions/workflows/proyectos.yml/badge.svg)](https://github.com/Maximiliano-cabello-mata/Maximiliano_KD/actions/workflows/proyectos.yml) |
| [Calidad](.github/workflows/calidad.yml) | En cada cambio corre las pruebas de los scripts y revisa que las fichas sean válidas. | [![Calidad](https://github.com/Maximiliano-cabello-mata/Maximiliano_KD/actions/workflows/calidad.yml/badge.svg)](https://github.com/Maximiliano-cabello-mata/Maximiliano_KD/actions/workflows/calidad.yml) |

Los scripts están en [`herramientas/`](herramientas/) y están escritos en Python con Pillow y PyYAML.

## Formación

| | | |
|---|---|---|
| Ingeniería en Entornos Virtuales y Negocios Digitales | Universidad Tecnológica de Nezahualcóyotl | 2025 – actual |
| TSU en Tecnologías de la Información, área Entornos Virtuales y Negocios Digitales | Universidad Tecnológica de Nezahualcóyotl | 2023 – 2025 |
| Bachillerato Técnico en Animación Digital (promedio 9.4) | CECyTEM, plantel Chimalhuacán II | 2020 – 2023 |

Idiomas: español nativo · inglés intermedio (B1).

## Contacto

- **Correo:** cabellomaximiliano86@gmail.com
- **CV:** [CV_Maximiliano_Cabello_Mata.pdf](cv/CV_Maximiliano_Cabello_Mata.pdf)
- **Amatista 3D:** [amatista-3d.tech](https://amatista-3d.tech)
- **GitHub:** [@Maximiliano-cabello-mata](https://github.com/Maximiliano-cabello-mata)

Si quieres comentar algún trabajo o proponer una colaboración, también puedes abrir una conversación en [Discussions](https://github.com/Maximiliano-cabello-mata/Maximiliano_KD/discussions).

---

<details>
<summary><b>English summary</b></summary>

I'm a Virtual Environments and Digital Business engineering student from Mexico City's metro area, with a technical background in Digital Animation. I work on **3D modeling in Blender** (including procedural modeling with Geometry Nodes) and on **data extraction, analysis and automation** with Python and SQL. My main project is [Amatista 3D](https://amatista-3d.tech), a platform for learning 3D, whose repositories are listed above. My current projects are developed with AI assistance (Claude and ChatGPT), and I review and test every result. I'm open to internships and junior roles in 3D, virtual environments or data, on-site in Mexico City or remote. English level: intermediate (B1).

</details>

<sub>Código bajo licencia [MIT](LICENSE). Renders e imágenes bajo [CC BY-NC-ND 4.0](renders/LICENCIA.md).</sub>
