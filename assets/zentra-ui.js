/* ============================================================================
   ZENTRA UI LAYER (JS) — v20260920
   Dipasang oleh ~/.hermes/scripts/pasang_lapisan_ui.py.
   Tiga tugas, semuanya idempotent (selamat dimuatkan berulang):
     1. Label jadual  — data-label daripada baris <th> (thead ATAU tidak) supaya
                        CSS boleh tukar setiap baris jadi kad berlabel pada telefon
     2. Tindakan demo — setiap kawalan lengai memberi maklum balas JUJUR (toast),
                        tanpa berpura-pura melakukan tindakan sebenar
     3. Tutup panel   — butang ✕, ketukan pada skrim, dan Esc (kekunci)
   Jangan edit salinan dalam mockup — edit fail sumber ini kemudian jalankan semula
   alat pemasang.
   ========================================================================== */
(function () {
  'use strict';
  if (window.__zentraUILayer) { return; }
  window.__zentraUILayer = true;

  /* ---------- 1. LABEL JADUAL ------------------------------------------- */
  function tajuk(t) {
    var th = t.querySelectorAll('thead tr:first-child th');
    if (th.length) { return th; }
    var baris = t.querySelector('tr');
    return baris ? baris.querySelectorAll('th') : [];
  }
  function labelJadual(t) {
    var th = tajuk(t);
    if (!th.length) { return false; }
    if (!t.tHead && th[0] && th[0].parentElement) {
      th[0].parentElement.classList.add('zr-hdr');   /* baris tajuk tanpa thead */
    }
    var baris = [];
    if (t.tBodies && t.tBodies.length) {
      for (var b = 0; b < t.tBodies.length; b++) {
        for (var r = 0; r < t.tBodies[b].rows.length; r++) { baris.push(t.tBodies[b].rows[r]); }
      }
    } else {
      var semua = t.rows;
      for (var i = 1; i < semua.length; i++) { baris.push(semua[i]); }
    }
    var ok = 0;
    baris.forEach(function (tr) {
      var td = tr.querySelectorAll('td');
      if (!td.length) { return; }
      for (var c = 0; c < td.length; c++) {
        if (!td[c].hasAttribute('data-label') && th[c]) {
          td[c].setAttribute('data-label', (th[c].textContent || '').trim());
        }
      }
      ok++;
    });
    if (ok) { t.classList.add('zr-kad'); return true; }
    return false;
  }
  function balutSkrol(t) {
    /* jadual tanpa <th> tidak boleh jadi kad berlabel — sebaliknya balut dalam
       bekas boleh skrol supaya halaman tidak melebar (POC 640px, dsb.) */
    if (t.parentElement && t.parentElement.classList.contains('zr-scroll')) { return; }
    var b = document.createElement('div');
    b.className = 'zr-scroll';
    t.parentNode.insertBefore(b, t);
    b.appendChild(t);
  }
  function labelSemua() {
    var t = document.querySelectorAll('table'), n = 0;
    for (var i = 0; i < t.length; i++) {
      if (labelJadual(t[i])) { n++; } else { balutSkrol(t[i]); }
    }
    return n;
  }

  /* ---------- 2. TINDAKAN DEMO ------------------------------------------ */
  var PETA = [
    [/^(send reminder|remind|chase)/i, 'Would email the owner and record the reminder in the audit trail.', null],
    [/^(open report|view report|report)/i, 'Opens the compliance report for this exception.', 'compliance.html'],
    [/^stamp now/i, 'Would submit the stamping to LHDN and log the stamped date.', null],
    [/^check in/i, 'Would log a check-in with the agent and their team leader.', 'team.html'],
    [/^upload/i, 'Opens the document picker. (Prototype: no file is stored.)', null],
    [/^invite/i, 'Would email an invitation to the new agent.', null],
    [/^(approve|reject|decline)$/i, 'Would record your decision against this item.', null],
    [/^(export|download)/i, 'Would download a CSV of this table.', null],
    [/^(send|submit|issue|notify)/i, 'Would send this and log it in the audit trail.', null],
    [/^(new|add|create|generate)/i, 'Would open the form and generate the document from sample data.', null],
    [/^(view|open)/i, 'Opens the related record.', null]
  ];
  function toast(teks, label, href) {
    var t = document.getElementById('demoToast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'demoToast'; t.className = 'dtoast'; t.setAttribute('role', 'status');
      document.body.appendChild(t);
    }
    t.innerHTML = '<b>Demo action</b><span>' + (label ? '&ldquo;' + label + '&rdquo; &mdash; ' : '') + teks + '</span>' +
      (href ? '<a href="' + href + '">Open the related page &rarr;</a>' : '') +
      '<i>Prototype only &middot; sample data &middot; no real change is made.</i>';
    t.classList.add('on');
    clearTimeout(window.__dtoast);
    window.__dtoast = setTimeout(function () { t.classList.remove('on'); }, 5000);
  }
  document.addEventListener('click', function (e) {
    var el = e.target.closest('button, a.btn, .btn, .flag.a, .flag.g, .chip.act, [data-act]');
    if (!el || el.closest('.drawer') || el.closest('#demoToast')) { return; }
    if (el.closest('.side') || el.closest('.foot') || el.closest('.sidebar') || el.closest('.top')) { return; }
    /* suis tema, loceng, burger dan apa-apa togol BUKAN tindakan demo */
    var tanda = (el.id + ' ' + (el.className || '') + ' ' + (el.getAttribute('aria-label') || '')).toLowerCase();
    if (/tema|theme|toggle|togol|burger|bell|loceng|drawer|nav/.test(tanda) || el.hasAttribute('aria-pressed')) { return; }
    if (el.tagName === 'A' && el.getAttribute('href')) { return; }
    if (el.hasAttribute('onclick') || el.hasAttribute('data-demo-ignore')) { return; }
    var label = (el.textContent || '').replace(/\s+/g, ' ').trim();
    if (!label || label.length > 46) { return; }
    var mesej = 'This is a prototype control &mdash; the live system runs the real action here.', href = null;
    for (var i = 0; i < PETA.length; i++) {
      if (PETA[i][0].test(label)) { mesej = PETA[i][1]; href = PETA[i][2]; break; }
    }
    toast(mesej, label, href);
  }, true);

  /* ---------- 3. TUTUP PANEL (✕ / skrim / Esc) --------------------------- */
  function pasangSkrim() {
    var scrim = document.getElementById('notifScrim');
    if (!scrim) {
      scrim = document.createElement('div');
      scrim.id = 'notifScrim'; scrim.className = 'nscrim';
      document.body.appendChild(scrim);
    }
    function tutup() {
      var d = document.querySelector('.drawer.open, .modal.open, .sheet.open');
      if (d) { d.classList.remove('open'); }
      document.querySelectorAll('.drawer.open, .modal.open, .sheet.open').forEach(function (x) { x.classList.remove('open'); });
      scrim.classList.remove('on');
      document.body.classList.remove('drawer-open');
    }
    scrim.addEventListener('click', tutup);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { tutup(); } });
    document.addEventListener('click', function (e) {
      var b = e.target.closest('.dclose, .dclosebar');
      if (b) { tutup(); return; }
      var panel = e.target.closest('.drawer, .modal, .sheet');
      if (panel && e.target === panel) { tutup(); }
    });
    /* pantau keadaan: skrim + kunci skrol + butang tutup automatik */
    new MutationObserver(function () {
      var terbuka = document.querySelector('.drawer.open, .modal.open, .sheet.open');
      scrim.classList.toggle('on', !!terbuka);
      document.body.classList.toggle('drawer-open', !!terbuka);
      if (terbuka && !terbuka.querySelector('.dclose') && !terbuka.querySelector('.dclosebar')) {
        var kepala = terbuka.querySelector('.dhead, header, .panel-head');
        if (kepala) {
          var b = document.createElement('button');
          b.type = 'button'; b.className = 'dclose'; b.setAttribute('aria-label', 'Close panel');
          b.innerHTML = '&times;';
          kepala.appendChild(b);
        }
      }
    }).observe(document.body, { attributes: true, subtree: true, attributeFilter: ['class'] });
  }

  /* ---------- JALANKAN --------------------------------------------------- */
  function boot() {
    labelSemua();
    if (document.querySelector('.drawer, .modal, .sheet')) { pasangSkrim(); }
    /* jadual yang dibina kemudian (baris JS) */
    if (window.MutationObserver) {
      document.querySelectorAll('table').forEach(function (t) {
        if (t.tBodies && t.tBodies[0]) {
          new MutationObserver(function () { labelJadual(t); })
            .observe(t.tBodies[0], { childList: true, subtree: true });
        }
      });
    }
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', boot); } else { boot(); }
})();
