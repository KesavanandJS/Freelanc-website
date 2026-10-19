/* Quote form: validates, then opens WhatsApp with the enquiry pre-filled (no server needed) */
(function () {
  var form = document.querySelector('[data-quote-form]');
  if (!form) return;
  var status = form.querySelector('.form__status');
  var number = form.getAttribute('data-whatsapp'); // e.g. 919876543210

  function check(field) {
    var input = field.querySelector('input, select, textarea');
    var ok = input.checkValidity();
    field.classList.toggle('is-invalid', !ok);
    input.setAttribute('aria-invalid', String(!ok));
    return ok;
  }
  form.querySelectorAll('.field').forEach(function (f) {
    var input = f.querySelector('input, select, textarea');
    input.addEventListener('blur', function () { if (input.value) check(f); });
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var fields = form.querySelectorAll('.field');
    var allOk = true, firstBad = null;
    fields.forEach(function (f) { if (!check(f)) { allOk = false; firstBad = firstBad || f; } });
    if (!allOk) { firstBad.querySelector('input, select, textarea').focus(); status.textContent = 'Fill in the highlighted fields to send your enquiry.'; return; }

    var data = new FormData(form);
    var msg = 'Hi! I would like a website quote.\n' +
      'Name: ' + data.get('name') + '\n' +
      'Phone: ' + data.get('phone') + '\n' +
      'Business: ' + data.get('business') + '\n' +
      'Website type: ' + data.get('type') + '\n' +
      'Budget: ' + data.get('budget') + '\n' +
      'Details: ' + (data.get('message') || '-');
    status.textContent = 'Opening WhatsApp with your enquiry…';
    window.open('https://wa.me/' + number + '?text=' + encodeURIComponent(msg), '_blank', 'noopener');
    setTimeout(function () { window.location.href = form.getAttribute('action'); }, 1200);
  });
})();
