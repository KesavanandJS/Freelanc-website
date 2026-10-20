/* Quote form: validates, then logs the enquiry to a Google Sheet via Apps Script (no server needed) */
(function () {
  var form = document.querySelector('[data-quote-form]');
  if (!form) return;
  var status = form.querySelector('.form__status');
  var sheetUrl = form.getAttribute('data-sheet-url'); // Apps Script Web App URL, see _dev/leads-apps-script.gs

  function isWeakPhone(raw) {
    var core = raw.replace(/\D/g, '').slice(-10);
    if (core.length < 10) return false; // let "required"/pattern handle short input
    if (/^(\d)\1{9}$/.test(core)) return true; // e.g. 9999999999
    var ascending = true, descending = true;
    for (var i = 1; i < core.length; i++) {
      var diff = (Number(core[i]) - Number(core[i - 1]) + 10) % 10; // wraps 9->0 and 0->9
      if (diff !== 1) ascending = false;
      if (diff !== 9) descending = false;
    }
    return ascending || descending; // e.g. 1234567890 or 9876543210
  }

  var phoneInput = form.querySelector('#f-phone');
  if (phoneInput) {
    phoneInput.addEventListener('input', function () {
      phoneInput.setCustomValidity(isWeakPhone(phoneInput.value) ? 'weak' : '');
    });
  }

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

    // sendBeacon (not fetch) because the page navigates away right after this: fetch
    // requests get cancelled on navigation, sendBeacon is built to survive it.
    if (sheetUrl) {
      try {
        if (navigator.sendBeacon) {
          navigator.sendBeacon(sheetUrl, data);
        } else {
          fetch(sheetUrl, { method: 'POST', mode: 'no-cors', body: new URLSearchParams(data), keepalive: true });
        }
      } catch (err) { /* logging is best-effort; never blocks the enquiry */ }
    }

    status.textContent = 'Sending your enquiry…';
    setTimeout(function () { window.location.href = form.getAttribute('action'); }, 600);
  });
})();
