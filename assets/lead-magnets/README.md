# Lead magnets (gated) — AcademIAS

Estos PDF NO se enlazan público. Se suben a MailerLite y se entregan en el correo de
confirmación (double opt-in), así el sitio sigue 100% estático en Vercel.

## Listo

- `mitos-ia-educacion.pdf` — *6 mitos de la IA en la educación* (9 páginas, estilo de marca).
  Fuente: `tools/mitos/mitos-ia-educacion.html`. Se renderiza con navegador headless
  (Playwright `page.pdf({format:'Letter', printBackground:true})`), no con WeasyPrint,
  porque usa fondos e imágenes de color.
  Re-render: `node` con Playwright apuntando al HTML (ver el script usado en el commit).

## Pendiente de conexión (lo aporta el dueño en MailerLite) — el sitio ya quedó cableado con placeholders

1. Crear en MailerLite un formulario "Webinar + recurso" con **double opt-in ON** (campos: nombre, correo).
2. Subir `mitos-ia-educacion.pdf` y configurar la **automatización** de confirmación para que envíe:
   - el enlace del **webinar** (Zoom/Meet) del día 22, y
   - el **PDF de mitos**.
3. En el sitio, reemplazar `REPLACE_ML_FORM_ACTION` por el endpoint del formulario de MailerLite
   (o pegar el embed de MailerLite) en:
   - `es/servicios/index.html` y `en/servicios/index.html` (sección `#webinar`, `<form class="ml-form">`).
   Los campos ya usan la convención de MailerLite: `name="fields[name]"`, `name="fields[email]"`.
4. Webinar mensual: agendar el Zoom/Meet el **día 22 de cada mes** y dejar que la automatización
   de MailerLite mande la invitación y el recordatorio.
5. Probar el flujo completo: registro → correo de confirmación → descarga del PDF + datos del webinar.

## Nota

Mientras `REPLACE_ML_FORM_ACTION` no se reemplace, el formulario se ve bien pero no envía a ningún
lado. Los CTA "Únete al webinar" apuntan a `#webinar` (la sección con el formulario), así que nada
queda roto en el sitio; solo falta conectar MailerLite para capturar y entregar.
