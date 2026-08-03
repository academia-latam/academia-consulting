# Recursos + webinar — AcademIAS

Dos cosas independientes:

## 1. PDF freebie — descarga directa (pública, sin gate)

- `mitos-ia-educacion.pdf` — *6 mitos de la IA en la educación* (9 páginas, estilo de marca).
- Se sirve directo desde el sitio: `https://www.academias.dev/assets/lead-magnets/mitos-ia-educacion.pdf`.
- Enlazado con un botón "Descargar el PDF" en la sección `#webinar` de `es/` y `en/servicios`
  (`.freebie`, atributo `download`). Sin registro, sin correo.
- Fuente: `tools/mitos/mitos-ia-educacion.html`. Re-render con Playwright
  (`page.pdf({format:'Letter', printBackground:true})`).

## 1b. PDF catálogo — pieza B2B, dos ediciones (públicas, sin gate)

*Catálogo de formación 2026*, 10 páginas Letter. Todo el catálogo presentado como **entrega
síncrona por Zoom**; la palabra "autoguiado" no aparece. Es lo que se manda a una escuela que
va a contratar grupo cerrado. Registro institucional formal, en español.

Estructura: modalidad de impartición · mapa del catálogo · A.D.A.P.T.A. (3 planas: método, seis
capas, cuatro sesiones) · cursos base C1-C3 · línea Claude y paquetes · precios · calendarios.

| Edición | Fuente | PDF | Dónde se enlaza |
|---|---|---|---|
| Ilustrada (principal) | `tools/brochure/catalogo-ilustrado.html` | `catalogo-academias-ilustrado.pdf` | `es\|en/recursos/`, `es\|en/cursos/`, `es/planificacion/`, `en/planning/` |
| Sobria (impresión) | `tools/brochure/catalogo-sobrio.html` | `catalogo-academias.pdf` | solo `es\|en/recursos/` |

**La sobria se genera desde la ilustrada, no se edita a mano.** El script quita los `<img class="etch">`,
los `.disc` y los `.dots`, y neutraliza `.grad` y `.row--star` con CSS. Así la copy y los precios no
se pueden desincronizar. Si editas contenido, edítalo en la ilustrada y vuelve a derivar.

Render con Playwright: `page.pdf({format:'Letter', printBackground:true})`.

**Al editar la fuente, verifica que sigan siendo exactamente 10 páginas** en cada edición. Cada
`.page` debe medir 1056px de alto bajo `emulateMedia({media:'print'})`; si una se pasa, aunque sea
por 1px, el PDF gana una página de sobra.

Cuidado con la especificidad en la ilustrada: las reglas de apilamiento `.page > *:not(...)` deben
seguir excluyendo `.grad`, `.etch`, `.disc`, `.src` y `.pageno`. Si una de esas capas pierde su
`position:absolute`, entra al flujo y la plana crece al doble.

Los precios deben coincidir con `es/planificacion/#precio` y `es/servicios/#curso-precios`.
Si cambia una tarifa, cambia en los tres lados.

## 1c. PDF currículo — pieza académica, sin precios (pública, sin gate)

*Currículo 2026*, 6 páginas Letter. Solo objetivos de aprendizaje por curso, sin cifras de precio.
Diseño instruccional en registro formal español. Dirigida a directivos y equipos pedagógicos que
quieren entender qué aprende cada docente **antes** de hablar de dinero.

Paleta teal (sidecar: no toca DESIGN.md del sitio). Portada con grabado de Atenas en duotono teal.

| Edición | Fuente | PDF | Dónde se enlaza |
|---|---|---|---|
| Única | `tools/brochure/curriculo.html` | `curriculo-academias.pdf` | `es\|en/recursos/` |

Render con Playwright: `page.pdf({format:'Letter', printBackground:true})`.

**Verificación igual que los catálogos**: cada `.page` debe medir 1056px bajo `emulateMedia({media:'print'})`.
Objetivo: exactamente 6 páginas. Copy pasada por deslop-codex (sin "no es X sino Y", sin guiones largos,
lenguaje de Bloom). Cero precios (grep `\$[0-9]` debe salir vacío).

## 2. Webinar mensual — Brevo (aparte del PDF)

- Formulario embebido de Brevo (iframe) en la sección `#webinar` de `es/` y `en/servicios`.
  Form: `https://c841ce0b.sibforms.com/v2/serve/MUIF...` (misma lista para ES y EN).
- Pendiente en Brevo (opcional, para que sirva de verdad):
  1. **Double opt-in ON** en el formulario.
  2. Correo de confirmación / automatización que mande el enlace del **webinar** (Zoom/Meet del día 22).
  3. Agendar el Zoom/Meet el **día 22 de cada mes**.
- El PDF ya NO depende del registro: es descarga directa (ver arriba).

## Nota
- El form de Brevo solo pide correo. Para capturar también el nombre, agrégalo en Brevo
  (Forms → añadir campo); el iframe se actualiza solo.
- Si algún día quieres el formulario con la tipografía/colores de la marca (en vez del iframe),
  pásame el "HTML embed" de Brevo y lo reestilizo.
