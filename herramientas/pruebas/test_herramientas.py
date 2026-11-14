import datetime as dt
import sys
from pathlib import Path

import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galeria  # noqa: E402
import proyectos  # noqa: E402

FICHA = """\
titulo: Taza procedimental
fecha: 2026-11-20
software: [Blender 4.2]
motor: Cycles
descripcion: Una taza hecha solo con nodos.
tecnicas: [Geometry Nodes, Materiales procedimentales]
destacado: true
"""


def crear_trabajo(base: Path, nombre: str, ficha: str = FICHA, imagenes=("render.png",)) -> Path:
    carpeta = base / nombre
    carpeta.mkdir(parents=True)
    (carpeta / "ficha.yml").write_text(ficha, encoding="utf-8")
    for img in imagenes:
        Image.new("RGB", (1920, 1080), (120, 100, 160)).save(carpeta / img)
    return carpeta


def test_ficha_valida(tmp_path):
    carpeta = crear_trabajo(tmp_path, "2026-11-taza")
    trabajo, errores, avisos = galeria.leer_trabajo(carpeta)
    assert errores == [] and avisos == []
    assert trabajo.titulo == "Taza procedimental"
    assert trabajo.fecha == dt.date(2026, 11, 20)
    assert trabajo.destacado is True
    assert trabajo.principal.name == "render.png"


def test_faltan_campos_y_motor_invalido(tmp_path):
    carpeta = crear_trabajo(tmp_path, "2026-11-mal", ficha="titulo: X\nmotor: Unreal\n")
    trabajo, errores, _ = galeria.leer_trabajo(carpeta)
    assert trabajo is None
    texto = " ".join(errores)
    for campo in ("fecha", "software", "descripcion"):
        assert campo in texto
    assert "motor" in texto


def test_sin_imagenes_ni_ficha(tmp_path):
    sin_img = crear_trabajo(tmp_path, "a", imagenes=())
    assert "no hay imágenes" in " ".join(galeria.leer_trabajo(sin_img)[1])
    (tmp_path / "b").mkdir()
    assert "falta ficha.yml" in galeria.leer_trabajo(tmp_path / "b")[1][0]


def test_imagen_principal_inexistente(tmp_path):
    carpeta = crear_trabajo(tmp_path, "c", ficha=FICHA + "imagen_principal: otra.png\n")
    assert "imagen_principal" in " ".join(galeria.leer_trabajo(carpeta)[1])


def test_orden_e_ignora_carpetas_con_guion_bajo(tmp_path):
    crear_trabajo(tmp_path, "vieja", ficha=FICHA.replace("2026-11-20", "2025-01-01"))
    crear_trabajo(tmp_path, "nueva")
    crear_trabajo(tmp_path, "_plantilla")
    trabajos, errores, _ = galeria.cargar_trabajos(tmp_path)
    assert errores == []
    assert [t.nombre for t in trabajos] == ["nueva", "vieja"]


def test_miniatura_reduce_a_640(tmp_path):
    carpeta = crear_trabajo(tmp_path, "d")
    trabajo, _, _ = galeria.leer_trabajo(carpeta)
    salida = galeria.crear_miniatura(trabajo, tmp_path / "_miniaturas")
    with Image.open(salida) as img:
        assert img.format == "WEBP"
        assert img.size == (640, 360)


def test_tabla_galeria_rutas_y_vacia(tmp_path, monkeypatch):
    monkeypatch.setattr(galeria, "RAIZ", tmp_path)
    monkeypatch.setattr(galeria, "RENDERS", tmp_path / "renders")
    monkeypatch.setattr(galeria, "MINIATURAS", tmp_path / "renders" / "_miniaturas")
    carpeta = crear_trabajo(tmp_path / "renders", "2026-11-taza")
    trabajo, _, _ = galeria.leer_trabajo(carpeta)
    tabla = galeria.tabla_galeria([trabajo], tmp_path)
    assert 'src="renders/_miniaturas/2026-11-taza.webp"' in tabla
    assert 'href="renders/2026-11-taza/"' in tabla
    tabla_interna = galeria.tabla_galeria([trabajo], tmp_path / "renders")
    assert 'src="_miniaturas/2026-11-taza.webp"' in tabla_interna
    assert "Próximamente" in galeria.tabla_galeria([], tmp_path)


def test_reemplazar_bloque():
    texto = "a\n<!-- GALERIA:INICIO -->\nviejo\n<!-- GALERIA:FIN -->\nb"
    nuevo = galeria.reemplazar_bloque(texto, "nuevo")
    assert "nuevo" in nuevo and "viejo" not in nuevo and nuevo.startswith("a\n") and nuevo.endswith("\nb")
    with pytest.raises(ValueError):
        galeria.reemplazar_bloque("sin marcadores", "x")


def test_tabla_proyectos_con_y_sin_api():
    config = {
        "usuario": "Usuario",
        "proyectos": [
            {"repo": "uno", "nombre": "Uno", "descripcion": "Hace algo.", "stack": "Python"},
            {"repo": "privado", "nombre": "Privado"},
            {"repo": "dos", "nombre": "Dos"},
        ],
    }
    respuestas = {
        "repos/Usuario/uno": {"html_url": "https://github.com/Usuario/uno", "pushed_at": "2026-11-10T15:00:00Z"},
        "repos/Usuario/privado": {"private": True},
        "repos/Usuario/dos": None,  # la API falló
    }
    tabla = proyectos.tabla_proyectos(config, consultar=respuestas.get)
    assert "[**Uno**](https://github.com/Usuario/uno) | Hace algo. | Python | nov 2026 |" in tabla
    assert "Privado" not in tabla
    assert "[**Dos**](https://github.com/Usuario/dos) | — | — | — |" in tabla
