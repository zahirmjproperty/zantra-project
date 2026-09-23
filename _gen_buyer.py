#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_gen_buyer.py — penjana BUYER PORTAL (versi pembeli) untuk mock-up ZENTRA PROJECT.

Hasil: ~/mockup-hartanah/zentra-launch/buyer/{index,payments,progress,documents}.html
Shell mudah alih (top bar + tab), bukan sidebar admin. English (US) — ini permukaan sistem.
Data contoh; noindex; jelas ditanda sebagai mock-up.
"""
import os

OUT = "/home/ubuntu/mockup-hartanah/zantra-project/buyer"
os.makedirs(OUT, exist_ok=True)

BUYER = "Ahmad Faiz"
UNIT = "A-12-03"
PROJECT = "Avalon @ Cybersouth"
REF = "LAU-2608-0113"
PRICE = 468000
PAID = 108900

TABS = [("index.html", "My Booking"), ("payments.html", "Payments"),
        ("progress.html", "Progress"), ("documents.html", "Documents")]

PV = ('<div class="pv">PREVIEW MOCK-UP — sample data · not a live system · Zentra Project buyer portal</div>')


def shell(active, content):
    tabs = "".join(
        '<a href="%s"%s>%s</a>' % (h, ' class="on"' if h == active else "", t) for h, t in TABS)
    label = [t for h, t in TABS if h == active][0]
    head_title = '<title>Zentra Project — %s</title>\n' % label          # % pada literal tunggal sahaja
    tail = ('<div class="wrap">\n%s\n</div>\n'
            '<div class="foot">Zentra Project — buyer portal (mock-up) · Zentra Property Group<br>'
            'Documents &amp; invoices are issued by ZMJ Solutions (002093603-H)</div>\n'
            '</body>\n</html>\n') % content
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        + head_title +
        '<meta name="robots" content="noindex, nofollow">\n'
        '<link rel="preload" href="../assets/PlusJakartaSans-var.woff2" as="font" type="font/woff2" crossorigin>\n'
        '<link rel="stylesheet" href="../assets/zl-buyer.css">\n</head>\n<body>\n'
        + PV +
        '\n<div class="topbar"><div class="inner">'
        '<div class="brand"><span class="mark"></span>ZENTRA <em>PROJECT</em></div>'
        '<div class="spacer"></div>'
        '<div class="who"><span>Signed in as <b>%s</b></span><span class="av">AF</span></div>'
        '</div></div>\n' % BUYER
        + '<div class="tabs"><div class="inner">' + tabs + '</div></div>\n'
        + tail
    )


def write(fname, active, content):
    open(os.path.join(OUT, fname), "w", encoding="utf-8").write(shell(active, content))
    return fname


def card(title, inner, more=""):
    return ('<div class="card"><div class="hd"><h2>%s</h2>%s</div><div class="bd">%s</div></div>\n'
            % (title, ('<span class="more">%s</span>' % more) if more else "", inner))


def stats(items):
    out = ['<div class="stats">']
    for v, l, t, cls in items:
        out.append('<div class="stat"><div class="v">%s</div><div class="l">%s</div><div class="t %s">%s</div></div>'
                   % (v, l, cls, t))
    out.append('</div>')
    return "".join(out) + "\n"


def steps(items):
    out = ['<ul class="steps">']
    for state, title, meta in items:
        out.append('<li class="%s"><div class="st">%s</div><div class="mt">%s</div></li>' % (state, title, meta))
    out.append('</ul>')
    return "".join(out) + "\n"


def rows(items):
    out = ['<ul class="rows">']
    for ic, a, b, right in items:
        out.append('<li><span class="ic">%s</span><span class="tx"><span class="a">%s</span><br>'
                   '<span class="b">%s</span></span><span class="rt">%s</span></li>' % (ic, a, b, right))
    out.append('</ul>')
    return "".join(out) + "\n"


def bars(items):
    out = []
    for label, right, pct in items:
        out.append('<div class="bar"><div class="bl"><span>%s</span><span>%s</span></div>'
                   '<div class="bw"><div class="bf" style="width:%s%%"></div></div></div>' % (label, right, pct))
    return "".join(out) + "\n"


def table(headers, rows_):
    th = "".join("<th>%s</th>" % h for h in headers)
    body = ""
    for r in rows_:
        sel = []
        for i, c in enumerate(r):
            atr = c[1] if isinstance(c, tuple) else ""
            txt = c[0] if isinstance(c, tuple) else c
            lab = headers[i] if i < len(headers) else ""
            sel.append('<td%s data-label="%s">%s</td>' % (atr, lab, txt))
        body += "<tr>" + "".join(sel) + "</tr>\n"
    return ('<div class="table-wrap"><table class="t"><thead><tr>%s</tr></thead><tbody>\n%s</tbody></table></div>\n'
            % (th, body))


money = lambda n: "RM " + format(n, ",.0f")

# ───────────────────────────────────────────────────────────── 1. My Booking
booking = (
    '<h1>My Booking</h1>\n<p class="sub">%s · %s · %s</p>\n' % (PROJECT, UNIT, REF)
    + stats([
        (money(PRICE), "Purchase price", "SPA signed 18 Sep 2026", "up"),
        (money(PAID), "Paid to date", "23% of price", "up"),
        (money(PRICE - PAID), "Outstanding", "9 payments remaining", "due"),
        ("2 of 10", "Progress payments", "Next due 30 Sep 2026", "due"),
    ])
    + card("Your unit", rows([
        ("🏢", "Block A · Level 12 · Unit %s" % UNIT, "3 rooms · 2 baths · 1,050 sq ft", '<span class="badge b-gold">Booked</span>'),
        ("📄", "Sale &amp; Purchase Agreement", "Signed 18 Sep 2026 · digital signature", '<span class="badge b-ok">Signed</span>'),
        ("🤝", "Sales agent", "Aina Zulkifli · Zentra Property Group (COA partner)", '<a class="btn ghost" href="#agent">WhatsApp</a>'),
        ("🏦", "End-financing", "Maybank · RM 374,400 (80%) · 35 years", '<span class="badge b-due">In progress</span>'),
    ]))
    + card("Your journey", steps([
        ("done", "Expression of interest", "Received 14 Aug 2026 · reference LAU-2608-E014"),
        ("done", "Unit locked", "Block A-12-03 held for 48 hours on 16 Aug 2026"),
        ("done", "Booking confirmed", "Deposit RM 46,800 (10%) paid 25 Aug 2026 · receipt R-2608-0412"),
        ("done", "Sale &amp; Purchase Agreement signed", "Signed digitally on 18 Sep 2026 · stamped copy in Documents"),
        ("now", "End-financing approval", "Maybank panel · offer letter issued, awaiting acceptance"),
        ("", "Progressive payments", "2 of 10 paid · next milestone: foundation completed"),
        ("", "Vacant possession", "Estimated Q4 2027 · defects liability period 24 months"),
    ]))
    + card("Next action", (
        '<p style="margin:0 0 10px"><b>Payment 3 — Foundation completed · %s</b><br>'
        '<span class="sub" style="margin:0">Due 30 Sep 2026 · invoice INV-2609-0142 · pay by transfer or cheque into the '
        'developer\u2019s Housing Development Account (or the solicitor\u2019s client account for SPA-stage payments)</span></p>'
        '<div class="cta"><a class="btn gold" href="payments.html">View payment schedule</a>'
        '<a class="btn ghost" href="documents.html">Download invoice</a></div>' % money(70200)))
    + card("Need help?", rows([
        ("💬", "Message your sales agent", "Aina Zulkifli · replies within 1 working day", '<a class="btn ghost" href="#agent">Open</a>'),
        ("🛠", "Report a defect", "Available after vacant possession (Phase 2)", '<span class="badge b-info">Phase 2</span>'),
        ("📞", "Zentra Project support", "016-311 9076 · Mon–Fri 9am–6pm", '<a class="btn ghost" href="#support">Call</a>'),
    ]))
    + '<div class="note">Your booking data is held by Zentra Property Group. '
      'The Sale &amp; Purchase Agreement and all invoices are issued by the registered entity '
      '<b>ZMJ Solutions (002093603-H)</b> — this cannot be replaced by a trade name.</div>\n'
)

# ───────────────────────────────────────────────────────────── 2. Payments
schedule = [
    [("1", "strong"), "Booking / deposit", "10%", ("46,800", "num"), "25 Aug 2026", '<span class="badge b-ok">Paid</span>'],
    [("2", "strong"), "SPA signing (within 14 days)", "10%", ("46,800", "num"), "18 Sep 2026", '<span class="badge b-ok">Paid</span>'],
    [("3", "strong"), "Foundation completed", "15%", ("70,200", "num"), "30 Sep 2026", '<span class="badge b-due">Due</span>'],
    [("4", "strong"), "Frame completed", "10%", ("46,800", "num"), "Feb 2027", '<span class="badge b-info">Upcoming</span>'],
    [("5", "strong"), "Walls &amp; roof", "10%", ("46,800", "num"), "May 2027", '<span class="badge b-info">Upcoming</span>'],
    [("6", "strong"), "Windows, doors, plumbing", "15%", ("70,200", "num"), "Aug 2027", '<span class="badge b-info">Upcoming</span>'],
    [("7", "strong"), "Internal &amp; external finishes", "10%", ("46,800", "num"), "Nov 2027", '<span class="badge b-info">Upcoming</span>'],
    [("8", "strong"), "Car park &amp; access", "5%", ("23,400", "num"), "Jan 2028", '<span class="badge b-info">Upcoming</span>'],
    [("9", "strong"), "Drainage &amp; roads", "5%", ("23,400", "num"), "Feb 2028", '<span class="badge b-info">Upcoming</span>'],
    [("10", "strong"), "Vacant possession", "10%", ("46,800", "num"), "Q4 2027 / 2028", '<span class="badge b-info">Upcoming</span>'],
]

payments = (
    '<h1>Payments</h1>\n<p class="sub">Schedule of payments under the Third Schedule, Housing Development Act 1966</p>\n'
    + stats([
        (money(PRICE), "Total price", "3 rooms · 2 baths · 1,050 sq ft", "up"),
        (money(PAID), "Paid to date (23%)", "2 of 10 payments", "up"),
        (money(PRICE - PAID), "Outstanding", "8 remaining milestones", "due"),
        (money(70200), "Due 30 Sep 2026", "Foundation completed", "due"),
    ])
    + card("Payment schedule", table(["#", "Milestone", "Share", "Amount (RM)", "Due", "Status"], schedule),
           more="Interest on late payment: 10% p.a.")
    + card("Receipts &amp; e-invoices", rows([
        ("🧾", "INV-2608-0391 · Booking deposit", "Receipt R-2608-0412 · e-invoice ref 2026-08-31142", '<a class="btn ghost" href="#dl1">PDF</a>'),
        ("🧾", "INV-2609-0108 · SPA signing", "Receipt R-2609-0055 · e-invoice ref 2026-09-40218", '<a class="btn ghost" href="#dl2">PDF</a>'),
        ("🧾", "INV-2609-0142 · Foundation completed", "Issued 19 Sep 2026 · due 30 Sep 2026", '<span class="badge b-due">Unpaid</span>'),
    ]))
    + card("How to pay", rows([
        ("🏦", "Transfer / cheque — developer's account",
         "Avalon Cybersouth Housing Development Account (HDA 1966 s.7A) · Maybank 5144 2233 8891 · ref LAU-2608-0113",
         '<span class="badge b-info">Project account</span>'),
        ("⚖️", "Transfer / cheque — solicitor's client account",
         "For SPA-stage payments, per the payment clause in your SPA · ref LAU-2608-0113",
         '<span class="badge b-info">Per SPA</span>'),
        ("📎", "Upload your payment slip",
         "Bank-in slip or cheque copy — the sales office reconciles it and issues your receipt",
         '<a class="btn ghost" href="#upload">Upload</a>'),
    ]))
    + '<div class="note"><b>No payment is collected before your SPA is signed</b> '
      '(Regulation 11(2), Housing Development Regulations 1989). Every payment you make appears here '
      'within 24 hours with a receipt and an e-invoice reference (LHDN MyInvois).<br>'
      '<b>Zentra Project never holds your money:</b> payments are made straight to the developer\u2019s '
      'Housing Development Account or the solicitor\u2019s client account — the system only records them, '
      'issues receipts and tracks your balance.</div>\n'
)

# ───────────────────────────────────────────────────────────── 3. Progress
progress = (
    '<h1>Construction progress</h1>\n<p class="sub">%s · Block A · updated 19 Sep 2026 by the project team</p>\n' % PROJECT
    + stats([
        ("34%", "Overall progress", "Site started Mar 2026", "up"),
        ("Q4 2027", "Est. vacant possession", "DLP 24 months after VP", "up"),
        ("100%", "Foundation", "Verified 12 Sep 2026", "up"),
        ("74%", "Frame", "Block A · level 13 of 18", "up"),
    ])
    + card("Milestones", bars([
        ("Foundation", "100%", 100), ("Frame", "74%", 74), ("Walls &amp; roof", "61%", 61),
        ("Windows, doors &amp; plumbing", "48%", 48), ("Internal &amp; external finishes", "35%", 35),
        ("Car park &amp; access", "22%", 22), ("Drainage &amp; roads", "14%", 14),
    ]), more="Certified by the project architect")
    + card("Latest site updates", rows([
        ("📸", "Level 13 slab completed", "19 Sep 2026 · photos issued with the monthly report", '<span class="badge b-ok">New</span>'),
        ("📸", "Block A lift core to level 15", "12 Sep 2026 · on schedule", '<span class="badge b-info">Report</span>'),
        ("📄", "Architect certificate 04 issued", "10 Sep 2026 · released payment milestone 3", '<a class="btn ghost" href="#ac4">PDF</a>'),
        ("⚠️", "Temporary water supply interruption", "08 Sep 2026 · resolved same day, no cost impact", '<span class="badge b-late">Closed</span>'),
    ]))
    + card("What is verified before you are billed", rows([
        ("✅", "A milestone is billed only after certification", "Architect / engineer certificate must be uploaded first", '<span class="badge b-ok">Enforced</span>'),
        ("📏", "Only the scheduled share is charged", "Third Schedule percentages · no early collection", '<span class="badge b-ok">Enforced</span>'),
        ("🔔", "You are notified 7 days before each due date", "Email and portal notification", '<span class="badge b-info">Automatic</span>'),
    ]))
    + '<div class="note">Progress percentages are issued by the project team and certified by the architect. '
      'They are shown here for information and are not a valuation of your unit.</div>\n'
)

# ───────────────────────────────────────────────────────────── 4. Documents
documents = (
    '<h1>Documents</h1>\n<p class="sub">Everything for %s · %s · %s</p>\n' % (PROJECT, UNIT, REF)
    + stats([
        ("8", "Documents", "2 signed digitally", "up"),
        ("2", "Receipts &amp; e-invoices", "August–September 2026", "up"),
        ("1", "Pending signature", "Loan agreement with Maybank", "due"),
    ])
    + card("Agreements", rows([
        ("📜", "Sale &amp; Purchase Agreement", "Signed 18 Sep 2026 · digitally signed copy", '<a class="btn ghost" href="#spa">Open</a>'),
        ("🏦", "Loan agreement (Maybank)", "Awaiting your signature at the branch", '<span class="badge b-due">Pending</span>'),
        ("📋", "Schedule of payments (Third Schedule)", "Attached to your SPA", '<a class="btn ghost" href="payments.html">View</a>'),
    ]))
    + card("Developer &amp; project documents", rows([
        ("🏗", "Development licence (DL)", "DL 2026/0418 · issued by the local authority", '<a class="btn ghost" href="#dl">Open</a>'),
        ("🏗", "Advertising &amp; selling permit (APDL)", "APDL 2026/1042 · valid to 31 Dec 2027", '<a class="btn ghost" href="#apdl">Open</a>'),
        ("🗺", "Approved site &amp; floor plans", "Unit %s highlighted" % UNIT, '<a class="btn ghost" href="#plan">Open</a>'),
        ("📕", "House rules &amp; DMC", "Issued at vacant possession", '<span class="badge b-info">Later</span>'),
    ]))
    + card("Receipts &amp; e-invoices", rows([
        ("🧾", "Receipt R-2608-0412", "Booking deposit RM 46,800 · 25 Aug 2026", '<a class="btn ghost" href="#r1">PDF</a>'),
        ("🧾", "Receipt R-2609-0055", "SPA signing RM 46,800 · 18 Sep 2026", '<a class="btn ghost" href="#r2">PDF</a>'),
        ("🧾", "e-invoice 2026-09-40218", "LHDN MyInvois validated · 18 Sep 2026", '<a class="btn ghost" href="#e1">PDF</a>'),
    ]))
    + '<div class="note">Documents are stored in your name only. The Sale &amp; Purchase Agreement, the '
      'transfer instrument and any charge must be completed on paper or by a registered e-signature provider — '
      'a simple digital signature is not valid for land instruments (Electronic Commerce Act 2006). '
      'Your data is processed under the Personal Data Protection Act 2010 and retained 7 years after vacant possession.</div>\n'
)

if __name__ == "__main__":
    done = [write("index.html", "index.html", booking),
            write("payments.html", "payments.html", payments),
            write("progress.html", "progress.html", progress),
            write("documents.html", "documents.html", documents)]
    print("buyer portal:", done, "| fail dalam folder:", sorted(os.listdir(OUT)))
