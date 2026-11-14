"""Actualiza la tabla de proyectos del README con datos de la API de GitHub.

Lee ``proyectos.yml`` y, para cada repositorio, consulta su lenguaje principal y
la fecha de su última actualización. Escribe la tabla en ``README.md`` entre
``<!-- PROYECTOS:INICIO -->`` y ``<!-- PROYECTOS:FIN -->``.

Si la API no responde (sin red o límite de consultas), usa solo los datos del
archivo, para que la tabla nunca quede vacía.

Uso:
    python herramientas/proyectos.py
Variables de entorno opcionales:
    GITHUB_TOKEN  token para tener un límite de consultas más alto
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from galeria import escribir_si_cambia, reemplazar_bloque  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
INICIO = "<!-- PROYECTOS:INICIO -->"
FIN = "<!-- PROYECTOS:FIN -->"
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]

Consulta = Callable[[str], dict | None]


def consultar_api(ruta: str) -> dict | None:
    """GET a la API de GitHub. Devuelve None si falla, sin detener el script."""
    peticion = urllib.request.Request(
        f"https://api.github.com/{ruta}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "portafolio-readme"},
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        peticion.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(peticion, timeout=15) as resp:
            return json.load(resp)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"Aviso: no pude consultar {ruta} ({exc})")
        return None


def _fecha(iso: str | None) -> str:
    if not iso:
        return "—"
    fecha = dt.datetime.fromisoformat(iso.replace("Z", "+00:00")).date()
    return f"{MESES[fecha.month - 1]} {fecha.year}"


def tabla_proyectos(config: dict, consultar: Consulta = consultar_api) -> str:
    usuario = config["usuario"]
    filas = [
        "| Proyecto | Qué hace | Tecnologías | Actualizado |",
        "|---|---|---|---|",
    ]
    for p in config.get("proyectos", []):
        datos = consultar(f"repos/{usuario}/{p['repo']}") or {}
        if datos.get("private") or datos.get("archived"):
            continue
        url = datos.get("html_url") or f"https://github.com/{usuario}/{p['repo']}"
        descripcion = " ".join(str(p.get("descripcion") or datos.get("description") or "").split())
        stack = p.get("stack") or datos.get("language") or "—"
        filas.append(
            f"| [**{p.get('nombre', p['repo'])}**]({url}) | {descripcion or '—'} | {stack} | {_fecha(datos.get('pushed_at'))} |"
        )
    filas.append("")
    filas.append(f"<sub>Tabla actualizada automáticamente el {dt.date.today():%d/%m/%Y}.</sub>")
    return "\n".join(filas)


def main() -> int:
    config = yaml.safe_load((RAIZ / "proyectos.yml").read_text(encoding="utf-8"))
    readme = RAIZ / "README.md"
    texto = readme.read_text(encoding="utf-8")
    nuevo = reemplazar_bloque(texto, tabla_proyectos(config), INICIO, FIN)
    cambio = escribir_si_cambia(readme, nuevo)
    print("Tabla de proyectos actualizada." if cambio else "Sin cambios en la tabla de proyectos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
