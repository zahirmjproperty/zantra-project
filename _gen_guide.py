#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_gen_guide.py — penjana halaman GUIDE (10 soalan semak + 6 keputusan) untuk mock-up ZANTRA PROJECT.

Zahir boleh jawab terus dalam halaman (radio), kemudian salin ringkasan keputusan dan hantar balik.
Gaya selamat: HTML sebagai string; JS ringkas tanpa template literal.
"""
import json
import sys

sys.path.insert(0, "/home/ubuntu/mockup-hartanah/zantra-project")
import _gen_project as G

BASE = "https://zahirmjproperty.github.io/mockup-hartanah/zentra-launch/"

QUESTIONS = [
    ("q1", "Booking flow", "The flow runs EOI &rarr; 48-hour unit lock &rarr; 10% booking &rarr; SPA within 14 days. Does this match how our launches actually run on the ground?"),
    ("q2", "Lock rules", "A lock lasts 48 hours, extends once with a manager override, warns 2 hours before expiry, and caps a buyer at 2 units. Are these the right numbers?"),
    ("q3", "Unit numbering", "Units are identified as Block-Level-Unit (A-12-03). Does this match the developer's own unit numbering, or do we follow the developer's scheme per project?"),
    ("q4", "Progressive billing", "Billing follows the Third Schedule of the HDA (10/10/15/10/10/15/10/5/5/10) and is issued only after architect or engineer certification. Correct for our projects?"),
    ("q5", "Commission release", "Agent commission releases 30% on booking, 40% on SPA signature and 30% when the loan is disbursed; co-agency splits 50:50. Correct, or is the pattern different for COA partners?"),
    ("q6", "Buyer visibility", "The buyer portal shows full stage names (EOI, locked, booked, SPA signed, loan, progressive, vacant possession). Should buyers see every stage name, or simplified milestones?"),
    ("q7", "Wet ink vs e-signature", "Under the ECA 2006, land instruments still need wet ink or a registered digital signature. Which documents in this set must stay wet ink?"),
    ("q8", "Role visibility", "Agents see their own buyers, bookings and commission. The internal team sees price history, discounts and margins. Is that the right line?"),
    ("q9", "Discount control", "Discounts are recorded per unit with an approval trail. Who may approve a discount, and up to what percentage before it needs Zahir?"),
    ("q10", "Bumi quota", "The system tracks bumi units, release approvals and reporting. How strict should enforcement be when the quota is not yet met?"),
]

DECISIONS = [
    ("d1", "Phase 1 scope", [
        "Admin console first (projects, inventory, locks, bookings, billing) — buyer portal in Phase 2",
        "Admin console and buyer portal together",
        "Buyer portal first, admin console follows"]),
    ("d2", "Source of truth (waiting for explanation)", [
        "Notion 'Projek Baharu MT' stays the source of truth; Zantra Project syncs from it",
        "Build a Zantra Project database; Notion becomes a read-only archive",
        "Keep both in parallel and reconcile manually",
        "Explain the three options in detail before I decide"]),
    ("d3", "Payment collection", [
        "Transfer / cheque into the developer's Housing Development Account (system is record-only)",
        "Transfer / cheque into the solicitor's client account for SPA-stage payments",
        "Billplz (FPX + cards) or DuitNow QR collected by the operator"]),
    ("d4", "Buyer identity", [
        "Reuse Zentra Portal accounts (Supabase) so a buyer has one Zentra ID",
        "Separate buyer accounts inside Zantra Project",
        "Email link access with no account (lightest friction)"]),
    ("d5", "Public microsite", [
        "Publish under launch.zentrapropertygroup.com (one path per project)",
        "Publish project pages on mrtanah.com using the existing pipeline",
        "Keep it preview-only until the rebrand cutover"]),
    ("d6", "Launch timing", [
        "After the Zentra Property Group cutover (one build, one switch)",
        "Before the cutover, keeping Mr Tanah branding internally",
        "No date yet — decide after the decisions above"]),
]

GUARDRAILS = [
    ["HDA 1966 — Third Schedule", "Progressive billing percentages are fixed by statute; the system issues each milestone from the template, not from free-text amounts."],
    ["HDA 1966 — Regulation 11(2)", "No payment may be collected before the SPA is signed. The booking screen blocks payment collection until the SPA date is recorded."],
    ["HDA 1966 — Regulation 6", "A project may only be advertised with a valid developer licence (DL) and advertising &amp; selling permit (APDL). Missing fields keep the microsite out of Google."],
    ["HIMS eSPA (KPKT)", "From 1 January 2026 the SPA submission to HIMS expects accurate unit and buyer data — this is why the unit record is the core of the system."],
    ["PDPA 2010", "Buyer data is held as a data user/processor; retention, access control and breach duties apply. Buyer documents are access-controlled per buyer."],
    ["e-Invoice (LHDN MyInvois)", "Receipts and invoices are issued in the registered legal name (ZMJ Solutions) with TIN; the trade brand may appear alongside but cannot replace it."],
    ["ECA 2006", "E-signature is valid for most documents but not for land instruments, which need wet ink or a registered digital signature."],
    ["Bumi quota", "Bumi units, release approvals and reporting are recorded per project; releases follow the state authority's rules."],
]

ROADMAP = [
    ["F0 · Mock-up (done)", "14 designed screens across admin console, drill-down and buyer portal — the basis for this review", "Complete"],
    ["F1 · Admin core", "Projects, phases and unit inventory; timed locks; bookings; progressive billing records; role access", "6–8 weeks (estimate)"],
    ["F1a · Move the record", "One-time import from Notion 'Projek Baharu MT', data check against the live site, then freeze Notion writes (decision B)", "1–2 weeks (estimate)"],
    ["F2 · Buyer portal", "Buyer sign-in, booking status, payments and receipts, documents, site progress", "3–4 weeks (estimate)"],
    ["F3 · Commission &amp; agents", "Release engine, agent ledger, agent view, reporting", "3–4 weeks (estimate)"],
    ["F4 · Channels &amp; statutory", "Public microsite, e-invoice automation, eSPA/HIMS submission pack", "After F1–F3"],
]

SUMMARY_JS = r"""
<script>
var QS = @@QUESTIONS@@;
var DS = @@DECISIONS@@;
function val(name){
  var e = document.querySelector('input[name="' + name + '"]:checked');
  return e ? e.value : '(not answered)';
}
function note(id){
  var e = document.getElementById(id);
  return e && e.value.trim() ? e.value.trim() : '';
}
function build(){
  var lines = ['ZANTRA PROJECT — review summary', ''];
  lines.push('REVIEW QUESTIONS');
  QS.forEach(function(q, i){
    var n = note('n-' + q[0]);
    lines.push((i + 1) + '. ' + q[1] + ': ' + val(q[0]) + (n ? ' — ' + n : ''));
  });
  lines.push('');
  lines.push('DECISIONS');
  DS.forEach(function(d, i){
    lines.push(String.fromCharCode(65 + i) + '. ' + d[1] + ': ' + val(d[0]));
  });
  lines.push('');
  lines.push('Reviewed by: ____________________   Date: ____________');
  return lines.join('\n');
}
function refresh(){ document.getElementById('sum').value = build(); }
function copySum(){
  var t = document.getElementById('sum');
  t.select();
  try {
    navigator.clipboard.writeText(t.value).then(function(){
      document.getElementById('copied').textContent = 'Copied — paste it back to Ali.';
    }, function(){ document.getElementById('copied').textContent = 'Select the text above and copy manually.'; });
  } catch (e) {
    document.getElementById('copied').textContent = 'Select the text above and copy manually.';
  }
}
document.addEventListener('DOMContentLoaded', function(){
  refresh();
  document.querySelectorAll('input[type=radio]').forEach(function(r){ r.addEventListener('change', refresh); });
  document.querySelectorAll('input[type=text], textarea').forEach(function(t){ t.addEventListener('input', refresh); });
});
</script>
"""


def soalans_html():
    out = []
    for i, (qid, label, text) in enumerate(QUESTIONS, 1):
        pilih = ANSWERS.get(qid)   # 0 Ya · 1 Perlu ubah · 2 Perbincangan
        out.append(
            '<div class="q"><div class="qt"><span class="qn">%d</span> <b>%s</b></div>'
            '<div class="qtxt">%s</div>'
            '<div class="opts">'
            '<label class="opt"><input type="radio" name="%s" value="Yes — as designed"%s> Yes — as designed</label>'
            '<label class="opt"><input type="radio" name="%s" value="Needs change"%s> Needs change</label>'
            '<label class="opt"><input type="radio" name="%s" value="Discuss"%s> Discuss</label>'
            '</div>'
            '<input class="notein" type="text" id="n-%s" placeholder="Note (optional) — what should change?">'
            '</div>' % (i, label, text, qid, CK[pilih == 0], qid, CK[pilih == 1], qid, CK[pilih == 2], qid))
    return "\n".join(out)


# Jawapan Zahir 19/9/2026 (mesej Telegram): indeks pilihan yang dipilih; None = belum dijawab
PICK = {"d1": 0, "d2": 1, "d3": 0, "d4": 0, "d5": 0, "d6": 0}   # B dipilih 19/9: Zantra Project = SSOT
# Jawapan 10 soalan semak (Zahir, 19/9/2026): 0 = Ya · 1 = Perlu ubah · 2 = Perbincangan
ANSWERS = {"q1": 0, "q2": 0, "q3": 0, "q4": 0, "q5": 1, "q6": 0, "q7": 0, "q8": 0, "q9": 1, "q10": 0}
CK = {True: " checked", False: ""}
ANSWER_NOTES = {
    "q5": "Needs change — commission is released once, after end-financing disbursement (100%); nothing on booking or SPA",
    "q9": "Needs change — no discounts at all; only the published launch packages",
}


def decisions_html():
    out = []
    for i, (did, label, opts) in enumerate(DECISIONS):
        rows = []
        for j, o in enumerate(opts):
            rec = ' <span class="rec">recommended</span>' if j == 0 else ''
            rows.append('<label class="opt"><input type="radio" name="%s" value="%s"%s> %s%s</label>'
                        % (did, o.replace('"', '&quot;'),
                           ' checked' if PICK.get(did) == j else '', o, rec))
        out.append('<div class="q"><div class="qt"><span class="qn">%s</span> <b>%s</b></div><div class="opts">%s</div></div>'
                   % (chr(65 + i), label, "\n".join(rows)))
    return "\n".join(out)


def guardrails_html():
    return "\n".join('<div class="act"><b>%s</b><span>%s</span></div>' % (a, b) for a, b in GUARDRAILS)


def roadmap_html():
    rows = "\n".join('<tr><td class="strong">%s</td><td>%s</td><td class="num gold">%s</td></tr>' % tuple(r) for r in ROADMAP)
    return ('<div class="table-wrap"><table class="dash-table"><thead><tr><th>Phase</th><th>Scope</th><th>Effort</th></tr></thead>'
            '<tbody>%s</tbody></table></div>' % rows)


def map_html():
    mods = [("Admin console", "Dashboard", "index.html"), ("Admin console", "Projects", "projects.html"),
            ("Admin console", "Inventory", "inventory.html"), ("Admin console", "Leads", "leads.html"),
            ("Admin console", "Sales", "sales.html"), ("Admin console", "Commission", "commission.html"),
            ("Admin console", "Billing", "billing.html"), ("Admin console", "Settings", "settings.html"),
            ("Drill-down", "Project detail", "project.html?p=avalon-cybersouth"),
            ("Drill-down", "Unit detail", "unit.html?u=A-12-03"),
            ("Buyer portal", "My Booking", "buyer/index.html"), ("Buyer portal", "Payments", "buyer/payments.html"),
            ("Buyer portal", "Progress", "buyer/progress.html"), ("Buyer portal", "Documents", "buyer/documents.html")]
    return ' '.join('<a class="chip" href="%s%s">%s</a>' % (BASE, u, l) for _g, l, u in mods)


BODY = """
    <div class="banner">REVIEW GUIDE — read this before signing off the mock-up. Answer the 10 questions, choose the 6
      decisions, then copy the summary at the bottom and send it back. Nothing here is production: every screen is a
      design proposal with sample data.</div>

    <div class="card" style="border-color:rgba(201,162,39,.45)"><div class="card-hd"><h2>Decisions received — 19 Sep 2026</h2>
      <span class="more">from Zahir</span></div>
      <div class="card-bd">
        <div class="kv">
          <div class="row"><span class="k">A · Phase 1 scope</span><span class="v">Admin console first</span></div>
          <div class="row"><span class="k">B · Source of truth</span><span class="v">Zantra Project is the system of record; Notion becomes a read-only archive</span></div>
          <div class="row"><span class="k">C · Payment collection</span><span class="v">Transfer / cheque to the developer's Housing Development Account, or the solicitor's client account</span></div>
          <div class="row"><span class="k">D · Buyer identity</span><span class="v">Zentra ID (Zentra Portal, Supabase)</span></div>
          <div class="row"><span class="k">E · Public microsite</span><span class="v">launch.zentrapropertygroup.com</span></div>
          <div class="row"><span class="k">F · Launch timing</span><span class="v">After the Zentra Property Group cutover</span></div>
        </div>
        <div class="note" style="margin-top:14px"><b>B changes the plan:</b> before F1 can go live the Notion record
          must be imported once and then frozen — <b>one writer only</b> (Zantra Project). Import, freeze and cut-over
          are now part of the F1 scope; until the freeze, Notion stays authoritative for existing records.</div>
        <div class="note"><b>C changes the design:</b> Zantra Project becomes
          <b>record-only</b> for money — it issues payment instructions, records slips that buyers upload, and tracks the
          balance. The system never holds client funds (and no e-wallet or card collection). The buyer portal and the
          admin billing screens have been updated to show the developer's Housing Development Account route.</div>
      </div></div>

    <div class="card"><div class="card-hd"><h2>Review answers — 19 Sep 2026</h2><span class="more">10 of 10</span></div>
      <div class="card-bd">
        <div class="table-wrap"><table class="dash-table">
          <thead><tr><th>#</th><th>Question</th><th>Answer</th></tr></thead>
          <tbody>
            <tr><td class="strong">1</td><td>Booking flow</td><td>Yes — as designed: EOI → 48-hour lock → booking 10% → SPA within 14 days</td></tr>
            <tr><td class="strong">2</td><td>Lock rules</td><td>Yes — 48 hours, warning 2 hours before expiry, max 2 units per buyer</td></tr>
            <tr><td class="strong">3</td><td>Unit ID scheme</td><td>Yes — A-12-03 (Block–Level–Unit)</td></tr>
            <tr><td class="strong">4</td><td>Progressive billing</td><td>Yes — Third Schedule 10-10-15-10-10-15-10-5-5-10, invoiced only after architect/engineer certification</td></tr>
            <tr><td class="strong">5</td><td>Commission release</td><td><b>Needs change</b> — released once, 100% after end-financing disbursement (or full cash settlement); nothing on booking or SPA</td></tr>
            <tr><td class="strong">6</td><td>Buyer portal status</td><td>Yes — full stage names (EOI, Unit Locked, Booked, SPA Signed, Loan, Progressive, VP)</td></tr>
            <tr><td class="strong">7</td><td>Wet ink vs e-signature</td><td>Yes — SPA and land instruments wet ink; other client documents e-signed</td></tr>
            <tr><td class="strong">8</td><td>Agent visibility</td><td>Yes — own leads, locks and commission only</td></tr>
            <tr><td class="strong">9</td><td>Discount policy</td><td><b>Needs change</b> — no discounts; only the published launch packages</td></tr>
            <tr><td class="strong">10</td><td>Bumi quota</td><td>Yes — the system holds bumi units until the release date</td></tr>
          </tbody></table></div>
        <div class="note" style="margin-top:12px">Two answers changed the design: <b>commission is now a single
          release after disbursement</b> (the booking/SPA triggers are removed) and <b>discounts are off</b> except for
          the published launch packages. Both are now reflected in Settings, Commission and the Phase 1 plan
          (W3 record-only collection, W2 discount field locked).</div>
      </div></div>

    <div class="card"><div class="card-hd"><h2>How to use this guide</h2><span class="more">3 steps</span></div>
      <div class="card-bd">
        <div class="activity-list">
          <div class="activity-item"><div class="act-body"><div class="act-title">1 · Walk the screens</div>
            <div class="act-meta">Open the preview map below — 14 screens: admin console, drill-down pages and the buyer portal.</div></div></div>
          <div class="activity-item"><div class="act-body"><div class="act-title">2 · Answer the 10 questions</div>
            <div class="act-meta">Tick <b>Yes</b>, <b>Needs change</b> or <b>Discuss</b>. Add a note where something must change.</div></div></div>
          <div class="activity-item"><div class="act-body"><div class="act-title">3 · Choose the 6 decisions</div>
            <div class="act-meta">Each decision has a recommended option. The summary updates as you choose — copy it and send it back.</div></div></div>
        </div>
        <div class="chips" style="margin-top:14px">@@MAP@@</div>
      </div></div>

    <div class="split">
      <div>
        <div class="card"><div class="card-hd"><h2>10 review questions</h2><span class="more">operation</span></div>
          <div class="card-bd">
@@SOALAN@@
          </div></div>

        <div class="card"><div class="card-hd"><h2>6 decisions needed</h2><span class="more">phase 1</span></div>
          <div class="card-bd">
@@KEPUTUSAN@@
          </div></div>

        <div class="card"><div class="card-hd"><h2>Your summary</h2><span class="more">copy &amp; send</span></div>
          <div class="card-bd">
            <textarea id="sum" class="notein" style="min-height:260px;font-family:ui-monospace,Menlo,monospace;font-size:12.5px"></textarea>
            <div class="cta-row" style="margin-top:10px">
              <button class="btn btn-gold" onclick="copySum()">Copy summary</button>
              <span id="copied" style="font-size:12.5px;color:var(--text-muted)"></span>
            </div>
          </div></div>
      </div>

      <div>
        <div class="card"><div class="card-hd"><h2>Regulatory guardrails</h2><span class="more">built in</span></div>
          <div class="card-bd">@@GUARDRAILS@@</div></div>
        <div class="card"><div class="card-hd"><h2>Roadmap after sign-off</h2><span class="more">estimate</span></div>
          <div class="card-bd">@@ROADMAP@@
            <div style="font-size:12.5px;color:var(--text-muted);margin-top:10px">
              Effort figures are working estimates; they are confirmed after the 6 decisions are made.</div>
          </div></div>
      </div>
    </div>
"""

CSS_EXTRA = """

/* --- Guide (review) 19/9/2026 --- */
.q { padding:14px 0; border-bottom:1px solid rgba(255,255,255,.06); }
.q:last-child { border-bottom:0; }
.q .qt { font-size:13.5px; color:var(--text); }
.q .qt .qn { display:inline-block; min-width:20px; color:var(--gold-light); font-weight:700; }
.q .qtxt { font-size:12.8px; color:var(--text-dim); margin:6px 0 10px; line-height:1.55; }
.q .opts { display:flex; flex-wrap:wrap; gap:8px; }
.opt { display:inline-flex; align-items:center; gap:6px; font-size:12.5px; color:var(--text-dim);
       border:var(--hairline-card); border-radius:999px; padding:6px 12px; background:rgba(255,255,255,.03); cursor:pointer; }
.opt:hover { border-color:var(--gold-core); color:var(--text); }
.opt input { accent-color:#c9a227; }
.opt .rec { font-size:10px; letter-spacing:.06em; text-transform:uppercase; color:var(--gold-deep); }
.notein { width:100%; margin-top:9px; background:rgba(0,0,0,.22); border:var(--hairline-card); border-radius:var(--radius-sm);
          color:var(--text); font-size:12.5px; padding:9px 11px; font-family:inherit; }
.notein:focus { outline:none; border-color:var(--gold-core); }
.act { display:block; padding:9px 0; border-bottom:1px solid rgba(255,255,255,.05); font-size:12.6px; }
.act:last-child { border-bottom:0; }
.act b { display:block; color:var(--text); font-size:12.8px; margin-bottom:3px; }
.act span { color:var(--text-dim); line-height:1.5; }
:root.theme-light .q, :root.theme-light .act { border-bottom-color:rgba(0,0,0,.07); }
:root.theme-light .opt { background:rgba(0,0,0,.02); }
:root.theme-light .notein { background:#fff; }
"""


def main():
    js = (SUMMARY_JS.replace("@@QUESTIONS@@", json.dumps([[q[0], q[1]] for q in QUESTIONS], ensure_ascii=False))
                   .replace("@@DECISIONS@@", json.dumps([[d[0], d[1]] for d in DECISIONS], ensure_ascii=False)))
    body = (BODY.replace("@@SOALAN@@", soalans_html())
                .replace("@@KEPUTUSAN@@", decisions_html())
                .replace("@@GUARDRAILS@@", guardrails_html())
                .replace("@@ROADMAP@@", roadmap_html())
                .replace("@@MAP@@", map_html()))
    n = G.page("guide.html", "Guide", body + js, title_block=False)
    css_path = "/home/ubuntu/mockup-hartanah/zantra-project/assets/zl.css"
    css = open(css_path, encoding="utf-8").read()
    if "Guide (review) 19/9/2026" not in css:
        open(css_path, "w", encoding="utf-8").write(css + CSS_EXTRA)
        print("zl.css += blok guide")
    print("guide.html:", n, "aksara")


if __name__ == "__main__":
    main()
