# Renders y trabajo en Blender

Todos mis trabajos en Blender, del más reciente al más antiguo. Haz clic en una imagen para ver la ficha completa.

<!-- GALERIA:INICIO -->
> **Próximamente.** Todavía no hay trabajos publicados.

<!-- GALERIA:FIN -->

---

## Cómo publicar un trabajo nuevo

1. Crea una carpeta dentro de `renders/` con el formato `AAAA-MM-nombre-del-trabajo`, todo en minúsculas y con guiones. Ejemplo: `2026-11-taza-procedimental`.
2. Copia ahí [`_plantilla/ficha.yml`](_plantilla/ficha.yml) y llénala.
3. Agrega tus imágenes en `.png`, `.jpg` o `.webp`. La primera en orden alfabético es la portada, salvo que indiques otra en `imagen_principal`.
4. Haz commit y push. El flujo **Galería de renders** valida la ficha, crea la miniatura y actualiza esta página y la portada del repositorio.

### Recomendaciones

- **Exporta para web:** 1920 px de ancho como máximo y menos de 5 MB por imagen. El sistema avisa a partir de 20 MB y rechaza más de 90 MB, porque GitHub no acepta archivos de más de 100 MB.
- **No subas archivos `.blend` pesados aquí.** Si quieres compartir uno, súbelo como adjunto en un *Release* o enlázalo desde la ficha.
- **Varias vistas cuentan una historia:** el render final, la malla en modo alámbrico, los nodos y, si aplica, un antes y después.
- **Marca `destacado: true`** en tus mejores trabajos para que aparezcan en la portada (máximo seis).

Las carpetas que empiezan con `_` (como `_plantilla` y `_miniaturas`) no son trabajos y el sistema las ignora.

Las imágenes de esta carpeta están bajo licencia [CC BY-NC-ND 4.0](LICENCIA.md).
