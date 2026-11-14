"""Genera la galería de renders del repositorio.

Recorre ``renders/``: cada carpeta que no empiece con ``_`` es un trabajo y debe
tener un ``ficha.yml`` y al menos una imagen. El script:

1. Valida cada ficha (campos obligatorios, fecha, imágenes y tamaños).
2. Crea una miniatura WebP de la imagen principal en ``renders/_miniaturas/``.
3. Escribe un ``README.md`` dentro de cada carpeta con todas sus imágenes.
4. Actualiza la galería completa en ``renders/README.md`` y los trabajos
   destacados en el ``README.md`` principal, entre los marcadores
   ``<!-- GALERIA:INICIO -->`` y ``<!-- GALERIA:FIN -->``.

Uso:
    python herramientas/galeria.py            # genera y escribe
    python herramientas/galeria.py --revisar  # solo valida; falla si algo está mal
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
RENDERS = RAIZ / "renders"
MINIATURAS = RENDERS / "_miniaturas"

EXTENSIONES = {".png", ".jpg", ".jpeg", ".webp"}
OBLIGATORIOS = ("titulo", "fecha", "software", "motor", "descripcion")
MOTORES = {"Cycles", "EEVEE", "Workbench", "Otro"}
ANCHO_MINIATURA = 640
MB = 1024 * 1024
LIMITE_AVISO = 20 * MB   # avisa: conviene comprimir
LIMITE_ERROR = 90 * MB   # GitHub rechaza archivos de más de 100 MB
MAX_DESTACADOS = 6
COLUMNAS = 3

INICIO = "<!-- GALERIA:INICIO -->"
FIN = "<!-- GALERIA:FIN -->"


@dataclass
class Trabajo:
    carpeta: Path
    titulo: str
    fecha: dt.date
    software: list[str]
    motor: str
    descripcion: str
    tecnicas: list[str] = field(default_factory=list)
    tiempo_render: str | None = None
    destacado: bool = False
    imagenes: list[Path] = field(default_factory=list)
    principal: Path | None = None

    @property
    def nombre(self) -> str:
        return self.carpeta.name


def _lista(valor) -> list[str]:
    if valor is None:
        return []
    if isinstance(valor, str):
        return [valor]
    return [str(v) for v in valor]


def leer_trabajo(carpeta: Path) -> tuple[Trabajo | None, list[str], list[str]]:
    """Devuelve (trabajo, errores, avisos) para una carpeta de renders."""
    errores: list[str] = []
    avisos: list[str] = []
    ficha_ruta = carpeta / "ficha.yml"
    if not ficha_ruta.exists():
        return None, [f"{carpeta.name}: falta ficha.yml"], avisos

    try:
        ficha = yaml.safe_load(ficha_ruta.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        return None, [f"{carpeta.name}: ficha.yml no es YAML válido ({exc})"], avisos
    if not isinstance(ficha, dict):
        return None, [f"{carpeta.name}: ficha.yml debe ser un diccionario de campos"], avisos

    for campo in OBLIGATORIOS:
        if ficha.get(campo) in (None, "", []):
            errores.append(f"{carpeta.name}: falta el campo '{campo}'")

    fecha = ficha.get("fecha")
    if isinstance(fecha, str):
        try:
            fecha = dt.date.fromisoformat(fecha)
        except ValueError:
            errores.append(f"{carpeta.name}: 'fecha' debe tener formato AAAA-MM-DD")
    elif fecha is not None and not isinstance(fecha, dt.date):
        errores.append(f"{carpeta.name}: 'fecha' debe tener formato AAAA-MM-DD")

    motor = ficha.get("motor")
    if motor and motor not in MOTORES:
        errores.append(f"{carpeta.name}: 'motor' debe ser uno de {sorted(MOTORES)}")

    imagenes = sorted(
        p for p in carpeta.iterdir() if p.is_file() and p.suffix.lower() in EXTENSIONES
    )
    if not imagenes:
        errores.append(f"{carpeta.name}: no hay imágenes (.png, .jpg, .jpeg o .webp)")

    for img in imagenes:
        tam = img.stat().st_size
        if tam > LIMITE_ERROR:
            errores.append(f"{carpeta.name}/{img.name}: pesa {tam / MB:.0f} MB; el máximo es 90 MB")
        elif tam > LIMITE_AVISO:
            avisos.append(f"{carpeta.name}/{img.name}: pesa {tam / MB:.0f} MB; conviene comprimirla")

    principal = None
    nombre_principal = ficha.get("imagen_principal")
    if nombre_principal:
        candidata = carpeta / str(nombre_principal)
        if candidata in imagenes:
            principal = candidata
        else:
            errores.append(f"{carpeta.name}: 'imagen_principal' ({nombre_principal}) no existe")
    elif imagenes:
        principal = imagenes[0]

    if errores:
        return None, errores, avisos

    trabajo = Trabajo(
        carpeta=carpeta,
        titulo=str(ficha["titulo"]).strip(),
        fecha=fecha,
        software=_lista(ficha["software"]),
        motor=str(motor),
        descripcion=" ".join(str(ficha["descripcion"]).split()),
        tecnicas=_lista(ficha.get("tecnicas")),
        tiempo_render=ficha.get("tiempo_render"),
        destacado=bool(ficha.get("destacado", False)),
        imagenes=imagenes,
        principal=principal,
    )
    return trabajo, errores, avisos


def cargar_trabajos(base: Path = RENDERS) -> tuple[list[Trabajo], list[str], list[str]]:
    trabajos: list[Trabajo] = []
    errores: list[str] = []
    avisos: list[str] = []
    if not base.exists():
        return trabajos, errores, avisos
    for carpeta in sorted(p for p in base.iterdir() if p.is_dir() and not p.name.startswith(("_", "."))):
        trabajo, errs, avs = leer_trabajo(carpeta)
        errores += errs
        avisos += avs
        if trabajo:
            trabajos.append(trabajo)
    trabajos.sort(key=lambda t: (t.fecha, t.nombre), reverse=True)
    return trabajos, errores, avisos


def crear_miniatura(trabajo: Trabajo, destino: Path = MINIATURAS) -> Path:
    destino.mkdir(parents=True, exist_ok=True)
    salida = destino / f"{trabajo.nombre}.webp"
    with Image.open(trabajo.principal) as img:
        img = img.convert("RGB")
        if img.width > ANCHO_MINIATURA:
            alto = round(img.height * ANCHO_MINIATURA / img.width)
            img = img.resize((ANCHO_MINIATURA, alto), Image.LANCZOS)
        img.save(salida, "WEBP", quality=82, method=6)
    return salida


def _rel(ruta: Path, desde: Path) -> str:
    return Path(os.path.relpath(ruta, desde)).as_posix()


def _pie(trabajo: Trabajo) -> str:
    detalles = [trabajo.motor] + trabajo.tecnicas[:2]
    return f"**{trabajo.titulo}**<br><sub>{' · '.join(detalles)} · {trabajo.fecha:%Y}</sub>"


def tabla_galeria(trabajos: list[Trabajo], desde: Path) -> str:
    """Cuadrícula Markdown de miniaturas que enlazan a la carpeta de cada trabajo."""
    if not trabajos:
        return (
            "> **Próximamente.** Aquí aparecerán mis renders y trabajos en Blender.\n"
            "> Cada trabajo nuevo en [`renders/`](renders/) se publica automáticamente."
            if desde == RAIZ
            else "> **Próximamente.** Todavía no hay trabajos publicados.\n"
        )
    celdas = []
    for t in trabajos:
        mini = _rel(MINIATURAS / f"{t.nombre}.webp", desde)
        enlace = _rel(t.carpeta, desde) + "/"
        celdas.append(
            f'<a href="{enlace}"><img src="{mini}" alt="{t.titulo}" width="100%"></a><br>{_pie(t)}'
        )
    filas = []
    for i in range(0, len(celdas), COLUMNAS):
        fila = celdas[i:i + COLUMNAS]
        fila += [""] * (COLUMNAS - len(fila))
        filas.append("| " + " | ".join(fila) + " |")
    encabezado = "| " + " | ".join([" "] * COLUMNAS) + " |\n|" + ":---:|" * COLUMNAS
    return encabezado + "\n" + "\n".join(filas)


def ficha_markdown(trabajo: Trabajo) -> str:
    lineas = [
        "<!-- Archivo generado por herramientas/galeria.py. Edita ficha.yml, no este archivo. -->",
        f"# {trabajo.titulo}",
        "",
        trabajo.descripcion,
        "",
        "| | |",
        "|---|---|",
        f"| **Fecha** | {trabajo.fecha:%d/%m/%Y} |",
        f"| **Software** | {', '.join(trabajo.software)} |",
        f"| **Motor de render** | {trabajo.motor} |",
    ]
    if trabajo.tecnicas:
        lineas.append(f"| **Técnicas** | {', '.join(trabajo.tecnicas)} |")
    if trabajo.tiempo_render:
        lineas.append(f"| **Tiempo de render** | {trabajo.tiempo_render} |")
    lineas.append("")
    orden = [trabajo.principal] + [i for i in trabajo.imagenes if i != trabajo.principal]
    for img in orden:
        lineas.append(f"![{trabajo.titulo}: {img.stem}]({img.name})")
        lineas.append("")
    lineas.append("[← Volver a la galería](../README.md)")
    return "\n".join(lineas) + "\n"


def reemplazar_bloque(texto: str, contenido: str, inicio: str = INICIO, fin: str = FIN) -> str:
    patron = re.compile(re.escape(inicio) + r".*?" + re.escape(fin), re.S)
    if not patron.search(texto):
        raise ValueError(f"No encontré los marcadores {inicio} … {fin}")
    return patron.sub(lambda _: f"{inicio}\n{contenido}\n{fin}", texto)


def escribir_si_cambia(ruta: Path, texto: str) -> bool:
    if ruta.exists() and ruta.read_text(encoding="utf-8") == texto:
        return False
    ruta.write_text(texto, encoding="utf-8")
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--revisar", action="store_true", help="solo valida, sin escribir archivos")
    args = parser.parse_args(argv)

    trabajos, errores, avisos = cargar_trabajos()
    for aviso in avisos:
        print(f"Aviso: {aviso}")
    if errores:
        for error in errores:
            print(f"Error: {error}", file=sys.stderr)
        return 1
    if args.revisar:
        print(f"Todo en orden: {len(trabajos)} trabajo(s) válido(s).")
        return 0

    nombres = {f"{t.nombre}.webp" for t in trabajos}
    MINIATURAS.mkdir(parents=True, exist_ok=True)
    for vieja in MINIATURAS.glob("*.webp"):
        if vieja.name not in nombres:
            vieja.unlink()
    for t in trabajos:
        crear_miniatura(t)
        escribir_si_cambia(t.carpeta / "README.md", ficha_markdown(t))

    destacados = [t for t in trabajos if t.destacado][:MAX_DESTACADOS] or trabajos[:MAX_DESTACADOS]
    readme = RAIZ / "README.md"
    escribir_si_cambia(readme, reemplazar_bloque(readme.read_text(encoding="utf-8"), tabla_galeria(destacados, RAIZ)))
    galeria = RENDERS / "README.md"
    escribir_si_cambia(galeria, reemplazar_bloque(galeria.read_text(encoding="utf-8"), tabla_galeria(trabajos, RENDERS)))
    print(f"Galería actualizada: {len(trabajos)} trabajo(s), {len(destacados)} en la portada.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
