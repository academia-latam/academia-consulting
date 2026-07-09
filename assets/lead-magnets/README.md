# Recursos + webinar — AcademIAS

Dos cosas independientes:

## 1. PDF freebie — descarga directa (pública, sin gate)

- `mitos-ia-educacion.pdf` — *6 mitos de la IA en la educación* (9 páginas, estilo de marca).
- Se sirve directo desde el sitio: `https://www.academias.dev/assets/lead-magnets/mitos-ia-educacion.pdf`.
- Enlazado con un botón "Descargar el PDF" en la sección `#webinar` de `es/` y `en/servicios`
  (`.freebie`, atributo `download`). Sin registro, sin correo.
- Fuente: `tools/mitos/mitos-ia-educacion.html`. Re-render con Playwright
  (`page.pdf({format:'Letter', printBackground:true})`).

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
