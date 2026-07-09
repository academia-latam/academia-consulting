# Lead magnets + webinar — AcademIAS

El registro al webinar y la entrega del freebie se manejan con **Brevo** (formulario embebido +
double opt-in), así el sitio sigue 100% estático en Vercel.

## Estado

- **Formulario Brevo: CONECTADO.** El iframe de Brevo está embebido en la sección `#webinar` de
  `es/servicios/index.html` y `en/servicios/index.html` (clase `.webi__form--embed`).
  Form: `https://c841ce0b.sibforms.com/v2/serve/MUIF...` (misma lista para ES y EN).
- `mitos-ia-educacion.pdf` — *6 mitos de la IA en la educación* (9 páginas, estilo de marca).
  Fuente: `tools/mitos/mitos-ia-educacion.html`, renderizado con Playwright
  (`page.pdf({format:'Letter', printBackground:true})`).

## Lo que falta en Brevo (para que entregue de verdad)

1. **Double opt-in ON** en el formulario (Brevo → Forms → tu form → ajustes de confirmación).
2. **Correo de confirmación / automatización** que al confirmar envíe:
   - el enlace del **webinar** (Zoom/Meet del día 22), y
   - el **enlace de descarga del PDF de mitos**.
3. **Dónde vive el PDF para descargarlo:** dos opciones.
   - (a) Súbelo a la **biblioteca de medios de Brevo** y usa ese enlace en el correo. (Recomendado: mantiene el freebie fuera del sitio público.)
   - (b) Usa el archivo del repo en `https://www.academias.dev/assets/lead-magnets/mitos-ia-educacion.pdf`.
     Ojo: si lo dejas en el repo, es públicamente descargable por quien tenga la URL (gate "suave").
     Si quieres gate "duro", NO lo dejamos desplegado: dímelo y lo saco del deploy y lo alojas solo en Brevo.
4. **Webinar mensual:** agenda el Zoom/Meet el **día 22 de cada mes**; el correo/automatización de Brevo
   manda invitación y recordatorio.

## Notas

- El form actual de Brevo solo pide **correo**. Si quieres capturar también el **nombre**, agrégalo en
  Brevo (Forms → añadir campo) y el iframe se actualiza solo (no hay que tocar el sitio).
- Si algún día prefieres un formulario 100% con nuestra tipografía/colores (en vez del iframe de Brevo),
  pásame el **"HTML embed"** de Brevo (no el iframe) y lo reestilizo a la marca.
