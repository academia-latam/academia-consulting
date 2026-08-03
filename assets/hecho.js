/* AcademIAS — Hecho con IA. Botón de copiar prompts. Progressive enhancement:
   el botón nace con [hidden] en el HTML y solo aparece si este script corre. */
(function () {
  'use strict';

  function copiarLegacy(texto) {
    var ta = document.createElement('textarea');
    ta.value = texto;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.top = '-1000px';
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }

  function marcar(btn, texto) {
    var previo = btn.dataset.previo || btn.textContent;
    btn.dataset.previo = previo;
    btn.textContent = texto;
    clearTimeout(btn.__t);
    btn.__t = setTimeout(function () { btn.textContent = previo; }, 1600);
  }

  document.querySelectorAll('.prompt').forEach(function (fig) {
    var btn = fig.querySelector('.prompt__copy');
    var pre = fig.querySelector('.prompt__body');
    if (!btn || !pre) return;

    btn.hidden = false;
    btn.setAttribute('aria-live', 'polite');

    btn.addEventListener('click', function () {
      var texto = pre.innerText;
      // La Clipboard API pide contexto seguro: existe en https y en localhost, no en file://
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(texto).then(
          function () { marcar(btn, 'Copiado'); },
          function () { marcar(btn, copiarLegacy(texto) ? 'Copiado' : 'Copia a mano'); }
        );
      } else {
        marcar(btn, copiarLegacy(texto) ? 'Copiado' : 'Copia a mano');
      }
    });
  });
})();
