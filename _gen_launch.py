#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_gen_launch.py — penjana set penuh mock-up ZENTRA LAUNCH (Zentra Property Group).

Hasil: 8 halaman dalam ~/mockup-hartanah/zentra-launch/
  index.html · projects.html · inventory.html · leads.html · sales.html · commission.html · billing.html · settings.html

Gaya selamat (arahan projek): kepingan HTML sebagai string biasa, gelung/julat ringkas untuk nav & kad.
Halaman sedia ada (index/projects/inventory/leads) DIPELIHARA kandungannya — skrip hanya menulis semula
blok sidebar + header supaya nav seragam, dan membetulkan sisa jenama lama (ZB → ZL, badge 'hot' → 'red').
"""
import os
import re

OUT = "/home/ubuntu/mockup-hartanah/zentra-launch"
os.makedirs(OUT, exist_ok=True)

ICON = {
    "dash": '<rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/>',
    "projects": '<path d="M3 9.5 12 4l9 5.5"/><path d="M5 8.5V19h14V8.5"/><path d="M10 19v-5h4v5"/>',
    "inventory": '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.29 7 12 12 20.71 7"/><line x1="12" y1="22" x2="12" y2="12"/>',
    "leads": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "sales": '<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    "commission": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
    "billing": '<rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/><line x1="6" y1="15" x2="11" y2="15"/>',
    "settings": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9 17 7M7 17l-2.1 2.1"/>',
    "guide": '<path d="M9 4h6a2 2 0 0 1 2 2v14l-5-3-5 3V6a2 2 0 0 1 2-2z"/><path d="M9 9h6M9 13h4"/>',
}

# (fail, label, ikon, tajuk carian, breadcrumb, ada_dalam_nav)
NAV = [
    ("index.html", "Dashboard", "dash", "Search projects, units, buyers...", "Dashboard", True),
    ("projects.html", "Projects", "projects", "Search projects...", "All Projects", True),
    ("inventory.html", "Inventory", "inventory", "Search units...", "Unit Inventory", True),
    ("leads.html", "Leads", "leads", "Search leads...", "Buyers &amp; Inquiries", True),
    ("sales.html", "Sales", "sales", "Search bookings...", "Bookings &amp; Pipeline", True),
    ("commission.html", "Commission", "commission", "Search agents...", "Agent Commission", True),
    ("billing.html", "Billing", "billing", "Search invoices...", "Progressive Billing", True),
    ("settings.html", "Settings", "settings", "Search settings...", "System Settings", True),
    ("guide.html", "Guide", "guide", "Search the guide...", "Guide &amp; Review Notes", True),
    # halaman drill-down — TIADA dalam sidebar (dibuka dengan klik kad/unit)
    ("project.html", "Project detail", "projects", "Search units in this project...", "Project detail", False),
    ("unit.html", "Unit detail", "inventory", "Search units...", "Unit detail", False),
]


def sidebar(active):
    links = []
    for i, (href, label, icon, _s, _b, in_nav) in enumerate(NAV):
        if not in_nav:
            continue
        if i == 4:
            links.append('<div class="section-label">Money</div>')
        if i == 7:
            links.append('<div class="section-label">System</div>')
        cls = ' class="active"' if href == active else ""
        links.append(
            '<a href="%s"%s><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">%s</svg><span>%s</span></a>'
            % (href, cls, ICON[icon], label)
        )
    return (
        '<div class="sidebar">\n'
        '  <div class="brand">\n'
        '    <span class="mark" aria-hidden="true"></span>\n'
        '    <span class="wordmark">ZENTRA <em>LAUNCH</em></span>\n'
        '  </div>\n'
        '  <nav class="nav" aria-label="Main">\n    ' + "\n    ".join(links) + '\n  </nav>\n'
        '  <div class="user-foot">\n'
        '    <div class="avatar">ZL</div>\n'
        '    <div class="info">\n'
        '      <div class="name">Zahir Admin</div>\n'
        '      <div class="role">Developer</div>\n'
        '    </div>\n'
        '  </div>\n'
        '</div>\n'
    )


def header(search_placeholder):
    return (
        '<header class="header">\n'
        '    <button class="nav-toggle" aria-label="Menu" onclick="document.body.classList.toggle(\'sidebar-collapsed\')">'
        '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>\n'
        '    <div class="search"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'
        '<input type="text" placeholder="%s" aria-label="Search"></div>\n'
        '    <div class="actions">\n'
        '      <button class="icon-btn" id="themeToggle" title="Toggle theme" onclick="toggleTheme()">\n'
        '        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" id="sunIcon"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>\n'
        '        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" id="moonIcon" style="display:none"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>\n'
        '      </button>\n'
        '      <button class="icon-btn" title="Notifications"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg><span class="dot"></span></button>\n'
        '      <div class="avatar">ZL</div>\n'
        '    </div>\n'
        '  </header>\n'
    ) % search_placeholder


THEME_JS = """<script>
function toggleTheme() {
  const html = document.documentElement;
  const isLight = html.classList.toggle('theme-light');
  document.getElementById('sunIcon').style.display = isLight ? 'none' : '';
  document.getElementById('moonIcon').style.display = isLight ? '' : 'none';
  localStorage.setItem('zl-theme', isLight ? 'light' : 'dark');
}
(function() {
  var theme = localStorage.getItem('zl-theme') || 'dark';
  if (window.location.search.indexOf('theme=light') > -1) theme = 'light';
  if (theme === 'light') {
    document.documentElement.classList.add('theme-light');
    document.getElementById('sunIcon').style.display = 'none';
    document.getElementById('moonIcon').style.display = '';
  }
})();
</script>"""


def page(fname, title, body, title_block=True):
    """title_block=False → halaman bina kepala sendiri (tajuk dinamik melalui JS)."""
    nav = [n for n in NAV if n[0] == fname][0]
    head_title = '<title>Zentra Launch — %s</title>\n' % title          # % pada literal tunggal sahaja
    crumb = ('    <div class="page-title">\n      <h1>%s</h1>\n'
             '      <div class="breadcrumb"><span>Zentra Launch</span> · <span>%s</span></div>\n    </div>\n'
             % (title, nav[4])) if title_block else ''
    html = (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        + head_title +
        '<meta name="robots" content="noindex, nofollow">\n'
        '<link rel="stylesheet" href="assets/zl.css?v=20260920b">\n</head>\n<body>\n'
        + sidebar(fname)
        + '\n<div class="main">\n  ' + header(nav[3]) + '\n  <div class="content">\n'
        + crumb
        + body
        + '\n  </div>\n</div>\n\n' + THEME_JS + '\n</body>\n</html>\n'
    )
    open(os.path.join(OUT, fname), "w", encoding="utf-8").write(html)
    return len(html)


def stats(items):
    out = ['    <div class="stat-row">']
    for value, label, trend, cls in items:
        out.append('      <div class="stat-card"><div class="value">%s</div><div class="label">%s</div>'
                   '<div class="trend %s">%s</div></div>' % (value, label, cls, trend))
    out.append('    </div>')
    return "\n".join(out) + "\n"


def card(title, inner, more=""):
    hd = '      <div class="card-hd"><h2>%s</h2>%s</div>\n' % (title, more)
    return '    <div class="card">\n' + hd + '      <div class="card-bd">\n' + inner + '\n      </div>\n    </div>\n'


def table(headers, rows, wrapper=True):
    th = "".join("<th>%s</th>" % h for h in headers)
    body = ""
    for r in rows:
        sel = []
        for i, c in enumerate(r):
            atr = c[1] if isinstance(c, tuple) else ""
            txt = c[0] if isinstance(c, tuple) else c
            lab = headers[i] if i < len(headers) else ""
            sel.append('<td%s data-label="%s">%s</td>' % (atr, lab, txt))
        body += "            <tr>" + "".join(sel) + "</tr>\n"
    t = ('        <table class="dash-table">\n          <thead><tr>%s</tr></thead>\n          <tbody>\n%s'
         '          </tbody>\n        </table>\n') % (th, body)
    return '      <div class="table-wrap">\n' + t + '      </div>\n' if wrapper else t


def bars(items):
    """Portfolio bar list: label, count text, peratus."""
    out = ['      <div class="portfolio-list">']
    for label, count, pct in items:
        out.append('        <div class="portfolio-item"><div class="plabel">%s</div>'
                   '<div class="pcount">%s</div><div class="bar-wrap"><div class="bar-fill" style="width:%s%%"></div></div></div>'
                   % (label, count, pct))
    out.append('      </div>')
    return "\n".join(out) + "\n"


def activities(items):
    """Activity list: (tajuk, meta, jumlah, warna ikon)."""
    out = ['      <div class="activity-list">']
    for title, meta, amount, tone in items:
        out.append(
            '        <div class="activity-item"><div class="act-icon"%s><svg viewBox="0 0 24 24" width="16" height="16" '
            'fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div>'
            '<div class="act-body"><div class="act-title">%s</div><div class="act-meta">%s</div></div>'
            '<div class="act-amount%s">%s</div></div>'
            % ((' style="background:%s"' % tone) if tone else "", title, meta,
               " gold" if amount.startswith("RM") else "", amount)
        )
    out.append('      </div>')
    return "\n".join(out) + "\n"


BADGE = {"paid": "green", "issued": "blue", "overdue": "red", "booked": "gold",
         "locked": "amber", "spa": "green", "eoi": "blue", "cancelled": "red", "loan": "amber"}


def b(kind, text):
    return '<span class="badge %s">%s</span>' % (BADGE.get(kind, "blue"), text)


# ─────────────────────────────────────────────────── sales.html
sales = (
    stats([
        ("24", "Bookings (MTD)", "↑ 6 this month", "up"),
        ("18", "SPA Signed", "↑ 4 this month", "up"),
        ("22", "Locks Active", "3 expire &lt; 24h", "down"),
        ("3", "Cancelled / NTU", "↓ 1 this month", "up"),
    ])
    + '<div class="filter-row">'
      '<button class="phase-btn active">All projects <span class="count">6</span></button>'
      '<button class="phase-btn">Avalon @ Cybersouth <span class="count">2</span></button>'
      '<button class="phase-btn">Setia Seraya P15 <span class="count">1</span></button>'
      '<button class="phase-btn">Allamanda KLIA <span class="count">1</span></button>'
      '<button class="phase-btn">Expiring locks <span class="count">3</span></button>'
      '</div>\n'
    + card("Unit pipeline", table(
        ["Unit", "Project", "Buyer", "Stage", "Price (RM)", "Agent", "Updated"],
        [
            [("A-12-03", "strong"), "Avalon @ Cybersouth", "Ahmad Faiz", b("booked", "Booked"), ("468,000", "num"), "Aina (COA)", "19 Sep"],
            [("B-04-11", "strong"), "Avalon @ Cybersouth", "Lim Wei Hong", b("spa", "SPA signed"), ("612,000", "num"), "Fadilah", "18 Sep"],
            [("C-08-02", "strong"), "Setia Seraya P15", "Ravi Kumar", b("locked", "Locked · 20h left"), ("385,000", "num"), "Aina (COA)", "19 Sep"],
            [("D-02-07", "strong"), "Allamanda KLIA", "Fatin Amira", b("eoi", "EOI"), ("—", "num"), "Fadilah", "17 Sep"],
            [("A-09-07", "strong"), "Senna Presint 12", "Siti Nurhaliza", b("loan", "Loan submitted"), ("540,000", "num"), "Aina (COA)", "16 Sep"],
            [("E-11-05", "strong"), "Terra Residences", "—", b("locked", "Unit locked"), ("720,000", "num"), "Fadilah", "19 Sep"],
        ], ), more='<span class="more">Export CSV →</span>')
    + card("Conversion funnel", bars([
        ("EOI captured", "86", 100), ("Unit locked", "42", 49), ("Booked", "24", 28),
        ("SPA signed", "18", 21), ("Loan approved", "12", 14),
    ]))
    + card("Exceptions &amp; alerts", activities([
        ("Lock expiring in 20h — C-08-02, Setia Seraya P15", "Ravi Kumar · agent Aina (COA)", "20h", "#B7791F"),
        ("Document missing — B-04-11 (buyer IC copy)", "Required before SPA release", "1 item", "#B23A34"),
        ("Loan offer lapsing — A-09-07 in 5 days", "Maybank · RM 432,000 (80%)", "5 days", "#B7791F"),
        ("Bumi release pending — D-02-07", "Developer consent not yet issued", "—", "#1F5F8B"),
    ]))
)

# ─────────────────────────────────────────────────── commission.html
commission = (
    stats([
        ("RM 128,400", "Commission earned (MTD)", "↑ RM 18,200", "up"),
        ("RM 42,600", "Awaiting release", "released after disbursement", "down"),
        ("RM 385,200", "Released (YTD)", "↑ 4% vs LY", "up"),
        ("12", "Active agents", "3 COA partners", "up"),
    ])
    + card("Release rules — decision 19 Sep 2026", table(
        ["Trigger event", "Share released", "Evidence required"],
        [
            ["End-financing disbursed", ("100%", "strong"), "Bank advice — release only when the money reaches the developer"],
            ["Cash purchase — full settlement", ("100%", "strong"), "Final receipt + developer confirmation"],
            ["Co-agency sale (MT + COA agent)", ("50 : 50 split", "gold"), "Co-agency agreement"],
            ["Sale cancelled before disbursement (NTU)", ("none", "strong"), "Nothing is released — no partial payout on booking or SPA"],
        ]))
    + card("Why a single release", (
        '<div class="note" style="margin:0"><b>One release event, not three.</b> Booking and SPA no longer trigger a payout — '
        'commission is released <b>once</b>, after the end-financier disburses (or the buyer settles in full for a cash purchase). '
        'The system tracks the entitlement from booking, but the ledger keeps it <b>held</b> until the bank advice is attached. '
        'Cancellation before disbursement releases nothing.</div>'))
    + card("Agent ledger", table(
        ["Agent", "Role", "Bookings", "Rate", "Earned (MTD)", "Awaiting", "Status"],
        [
            [("Aina Zulkifli", "strong"), "COA partner", ("6", "num"), "2.0%", ("RM 42,800", "num"), ("RM 12,400", "num"), b("issued", "Statement sent")],
            [("Fadilah Ismail", "strong"), "Internal agent", ("5", "num"), "2.5%", ("RM 38,600", "num"), ("RM 9,300", "num"), b("paid", "Partially released")],
            [("Hafiz Rahman", "strong"), "COA partner", ("4", "num"), "2.0%", ("RM 21,700", "num"), ("RM 8,600", "num"), b("issued", "Statement sent")],
            [("Nurul Izzah", "strong"), "Internal agent", ("3", "num"), "2.5%", ("RM 15,900", "num"), ("RM 7,000", "num"), b("locked", "Pending SPA")],
            [("Kumar Raj", "strong"), "COA partner", ("2", "num"), "2.0%", ("RM 9,400", "num"), ("RM 5,300", "num"), b("locked", "Pending loan")],
        ]), more='<span class="more">Payout run →</span>')
    + card("Recent releases", activities([
        ("Released 100% — B-04-11 Avalon @ Cybersouth", "Fadilah Ismail · loan disbursed 18 Sep (bank advice attached)", "RM 15,300", None),
        ("Released 100% — A-09-07 Senna Presint 12", "Aina Zulkifli · cash settlement 15 Sep", "RM 10,800", None),
        ("Held — A-12-03 Avalon @ Cybersouth", "Aina Zulkifli · entitlement earned at booking, waiting for disbursement", "RM 9,360 held", "#C9A227"),
        ("Hold placed — C-08-02 Setia Seraya P15", "Lock expired without booking", "RM 0", "#B23A34"),
    ]))
)

# ─────────────────────────────────────────────────── billing.html
milestones = [
    ("1 · Booking / deposit", "10%", 100), ("2 · SPA signing (within 14 days)", "10%", 100),
    ("3 · Foundation completed", "15%", 92), ("4 · Frame completed", "10%", 74),
    ("5 · Walls &amp; roof", "10%", 61), ("6 · Windows, doors, plumbing", "15%", 48),
    ("7 · Internal &amp; external finishes", "10%", 35), ("8 · Car park &amp; access", "5%", 22),
    ("9 · Drainage &amp; roads", "5%", 14), ("10 · Vacant possession", "10%", 8),
]
billing = (
    stats([
        ("RM 12.4M", "Billed to date", "342 units · 6 projects", "up"),
        ("RM 9.8M", "Collected (79%)", "↑ RM 640K this month", "up"),
        ("RM 2.6M", "Outstanding", "84 invoices open", "down"),
        ("RM 380K", "Overdue &gt; 60 days", "11 invoices · 4 units", "down"),
    ])
    + card("Schedule of payments — Third Schedule, HDA 1966", bars(milestones),
           more='<span class="more">Template: 10-10-15-10-10-15-10-5-5-10</span>')
    + card("Invoices", table(
        ["Invoice", "Unit", "Buyer", "Milestone", "Amount (RM)", "Due", "Status"],
        [
            [("INV-2609-0142", "strong"), "A-12-03", "Ahmad Faiz", "3 · Foundation", ("70,200", "num"), "30 Sep 2026", b("issued", "Issued")],
            [("INV-2609-0139", "strong"), "B-04-11", "Lim Wei Hong", "4 · Frame", ("61,200", "num"), "22 Sep 2026", b("paid", "Paid 18 Sep")],
            [("INV-2608-0118", "strong"), "C-08-02", "Ravi Kumar", "2 · SPA signing", ("38,500", "num"), "12 Sep 2026", b("overdue", "Overdue 7d")],
            [("INV-2608-0104", "strong"), "D-02-07", "Fatin Amira", "1 · Deposit", ("0", "num"), "—", b("eoi", "Pending SPA")],
            [("INV-2607-0093", "strong"), "A-09-07", "Siti Nurhaliza", "3 · Foundation", ("81,000", "num"), "05 Sep 2026", b("paid", "Paid 03 Sep")],
        ]), more='<span class="more">e-invoice (MyInvois) →</span>')
    + card("Billing rules enforced by the system", activities([
        ("No payment collected before SPA is signed", "Regulation 11(2), Housing Development Regulations 1989", "blocked", "#B23A34"),
        ("Late payment interest capped at 10% p.a.", "Computed per SPA clause, not compounded", "auto", "#1F5F8B"),
        ("Buyer receipts issued automatically on payment", "Emailed with e-invoice reference", "auto", None),
        ("Progressive claim requires architect / engineer certificate", "Uploaded before the invoice can be issued", "1 doc", "#B7791F"),
    ]))
    + card("Payment route — record only (decision 19 Sep 2026)", activities([
        ("Buyer pays into the developer's Housing Development Account",
         "HDA 1966 s.7A — project account. Zentra Launch never holds client money", "record-only", "#C9A227"),
        ("Or into the solicitor's client account for SPA-stage payments",
         "Per the payment clause in the SPA — the system records what the solicitor confirms", "per SPA", "#1F5F8B"),
        ("Buyer uploads the bank-in slip or cheque copy",
         "Sales office reconciles it, then the receipt and e-invoice are issued from here", "reconcile", None),
    ]), more='<span class="more">No card, e-wallet or QR collection</span>')
)

# ─────────────────────────────────────────────────── settings.html
def opts(items):
    return "".join("<option>%s</option>" % i for i in items)


settings_body = (
    '    <div class="card">\n      <div class="card-hd"><h2>Project setup</h2><span class="more">6 projects</span></div>\n'
    '      <div class="card-bd">\n'
    '        <div class="form-group"><label>Project profile</label><input type="text" value="Avalon @ Cybersouth" aria-label="Project"></div>\n'
    '        <div class="form-group"><label>Phases / blocks</label><input type="text" value="Phase 1 · Block A, Block B" aria-label="Phases"></div>\n'
    '        <div class="form-group"><label>Unit types &amp; price list</label><input type="text" value="3R2B RM 385K–489K · 4R3B RM 612K–742K" aria-label="Price list"></div>\n'
    '        <div class="form-group"><label>Development licence (DL) / APDL</label><input type="text" value="DL 2026/0418 · APDL 2026/1042" aria-label="Licence"></div>\n'
    '      </div>\n    </div>\n'
    '    <div class="card">\n      <div class="card-hd"><h2>Sales rules</h2></div>\n      <div class="card-bd">\n'
    '        <div class="form-group"><label>Unit lock duration</label><select aria-label="Lock">' + opts(["24 hours", "48 hours (default)", "72 hours"]) + '</select></div>\n'
    '        <div class="form-group"><label>Lock buffer between bookings</label><select aria-label="Buffer">' + opts(["1 hour", "2 hours (default)", "4 hours"]) + '</select></div>\n'
    '        <div class="form-group"><label>EOI validity</label><select aria-label="EOI">' + opts(["3 days", "7 days (default)", "14 days"]) + '</select></div>\n'

    '        <div class="form-group"><label>SPA signing window</label><select aria-label="SPA window">' + opts(["14 days from booking (default)", "21 days", "30 days"]) + '</select></div>\n'
    '        <div class="form-group"><label>Discount policy (decision 19/9/2026)</label><select aria-label="Discount">' + opts(["No discounts — published launch packages only", "Agent up to 2%, manager up to 5%", "Manager approves all discounts"]) + '</select></div>\n'
    '        <div class="form-group"><label>Bumi quota control (decision 19/9/2026)</label><select aria-label="Bumi">' + opts(["System holds bumi units until the release date", "Warning only — management releases manually", "No bumi quota for this project", "Follow the state authority's conditions per project"]) + '</select></div>\n'
    '        <div class="form-group"><label>Max active locks per buyer</label><select aria-label="Max locks">' + opts(["1 unit", "2 units (default)", "3 units"]) + '</select></div>\n'
    '      </div>\n    </div>\n'
    '    <div class="card">\n      <div class="card-hd"><h2>Commission rules</h2></div>\n      <div class="card-bd">\n'
    '        <div class="form-group"><label>Internal agent rate</label><select aria-label="Internal rate">' + opts(["2.0%", "2.5% (default)", "3.0%"]) + '</select></div>\n'
    '        <div class="form-group"><label>Co-agency split (MT : partner)</label><select aria-label="Split">' + opts(["40 : 60", "50 : 50 (default)", "60 : 40"]) + '</select></div>\n'
    '        <div class="form-group"><label>Release trigger (decision 19/9/2026)</label><select aria-label="Triggers">' + opts(["Single release after end-financing disbursement (100%)", "Single release after full cash settlement (100%)", "Staggered release (booking / SPA / disbursement)"]) + '</select></div>\n'
    '        <div class="form-group"><label>Entitlement held until disbursement</label><select aria-label="Held">' + opts(["Yes — no payout on booking or SPA (default)", "No — release on SPA"]) + '</select></div>\n'
    '        <div class="form-group"><label>Evidence required before release</label><input type="text" value="Bank advice (end-financier) or final receipt + developer confirmation" aria-label="Evidence"></div>\n'
    '        <div class="form-group"><label>Cancellation before disbursement</label><select aria-label="Cancellation">' + opts(["Release nothing (default)", "Release pro-rated share"]) + '</select></div>\n'
    '        <div class="form-group"><label>Clawback on cancellation (NTU)</label><select aria-label="Clawback">' + opts(["Full recall of unreleased share", "Pro-rated by stage (default)", "No clawback"]) + '</select></div>\n'
    '      </div>\n    </div>\n'
    '    <div class="card">\n      <div class="card-hd"><h2>Billing &amp; e-invoice</h2></div>\n      <div class="card-bd">\n'
    '        <div class="form-group"><label>Payment schedule template</label><select aria-label="Schedule">' + opts(["Third Schedule (HDA 1966) — 10-10-15-10-10-15-10-5-5-10", "Custom per project"]) + '</select></div>\n'
    '        <div class="form-group"><label>Invoice prefix</label><input type="text" value="INV-YYMM-" aria-label="Prefix"></div>\n'
    '        <div class="form-group"><label>Issuing entity (e-invoice)</label><input type="text" value="ZMJ Solutions (002093603-H) · TIN 202301234567" aria-label="Entity"></div>\n'
    '        <div class="form-group"><label>Late payment interest</label><select aria-label="Interest">' + opts(["10% p.a. (SPA standard)", "8% p.a.", "None"]) + '</select></div>\n'
    '        <div class="form-group"><label>Payment route (per project — decision 19/9/2026)</label><select aria-label="Payment route">' + opts(["Developer's Housing Development Account (HDA 1966 s.7A) — record only by Zentra Launch", "Solicitor's client account (SPA-stage payments)", "Operator's own account (non-licensed project)"]) + '</select></div>\n'
    '        <div class="form-group"><label>Buyer proof of payment</label><select aria-label="Proof">' + opts(["Upload bank-in slip / cheque copy — sales office reconciles (default)", "Record only, no upload", "Require bank confirmation letter"]) + '</select></div>\n'
    '        <div class="form-group"><label>Online collection (card / e-wallet / QR)</label><select aria-label="Collection">' + opts(["Disabled — Zentra Launch never holds client money (default)", "Enabled for non-licensed projects only"]) + '</select></div>\n'
    '      </div>\n    </div>\n'
    '    <div class="card">\n      <div class="card-hd"><h2>Data ownership — system of record</h2><span class="more">decision 19/9/2026</span></div>\n      <div class="card-bd">\n'
    '        <div class="form-group"><label>System of record</label><select aria-label="System of record">' + opts(["Zentra Launch — from cutover (decision B)", "Notion 'Projek Baharu MT' — until freeze"]) + '</select></div>\n'
    '        <div class="form-group"><label>Notion \'Projek Baharu MT\'</label><select aria-label="Notion role">' + opts(["Read-only archive after one-time import", "Still editable (pre-freeze)", "Retired"]) + '</select></div>\n'
    '        <div class="form-group"><label>Write lock on Notion fields</label><select aria-label="Write lock">' + opts(["Units, prices, locks and bookings (default)", "All fields", "None"]) + '</select></div>\n'
    '        <div class="form-group"><label>Import status</label><input type="text" value="Not started — scheduled in F1a (import → verify → freeze)" aria-label="Import"></div>\n'
    '        <div class="form-group"><label>Audit trail retention</label><select aria-label="Audit">' + opts(["Every change, who and when (default)", "Status changes only"]) + '</select></div>\n'
    '      </div>\n    </div>\n'
    '    <div class="card">\n      <div class="card-hd"><h2>Agents &amp; access</h2></div>\n      <div class="card-bd">\n'
    '        <div class="form-group"><label>Agent roster</label><input type="text" value="9 internal · 3 COA partners" aria-label="Roster"></div>\n'
    '        <div class="form-group"><label>Agent sees (decision 19/9/2026)</label><select aria-label="Agent access">' + opts(["Own leads, locks and commission only (default)", "All units, own buyers and commission", "Full read access"]) + '</select></div>\n'
    '        <div class="form-group"><label>Developer portal</label><select aria-label="Developer access">' + opts(["Sales board + reports (read only)", "Sales board + approve prices", "No access"]) + '</select></div>\n'
    '      </div>\n    </div>\n'
    '    <div class="card">\n      <div class="card-hd"><h2>Compliance &amp; brand</h2></div>\n      <div class="card-bd">\n'
    '        <div class="form-group"><label>DL / APDL fields on public microsite</label><select aria-label="DL gate">' + opts(["Mandatory — page stays noindex if incomplete (default)", "Warning only"]) + '</select></div>\n'
    '        <div class="form-group"><label>eSPA / HIMS KPKT export</label><select aria-label="HIMS">' + opts(["Enabled (required from 1 Jan 2026)", "Disabled"]) + '</select></div>\n'
    '        <div class="form-group"><label>Record retention (PDPA)</label><select aria-label="Retention">' + opts(["7 years after vacant possession (default)", "7 years after handover + 1"]) + '</select></div>\n'
    '        <div class="form-group"><label>Client-facing system name</label><input type="text" value="Zentra Launch" aria-label="Brand"></div>\n'
    '      </div>\n    </div>\n'
)
settings = settings_body

NEW_PAGES = [("sales.html", "Sales", sales), ("commission.html", "Commission", commission),
             ("billing.html", "Billing", billing), ("settings.html", "Settings", settings)]


def patch_existing():
    """Tulis semula blok sidebar + header halaman sedia ada supaya nav seragam (kandungan dikekalkan)."""
    changed = []
    for fname, _label, _icon, _s, _b, _in_nav in NAV[:4]:
        p = os.path.join(OUT, fname)
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        a = s.index('<div class="sidebar">')
        b = s.index('<div class="main">')
        s = s[:a] + sidebar(fname) + "\n" + s[b:]
        # header
        h1 = s.index('<header class="header">')
        h2 = s.index('</header>') + len('</header>')
        ph = [n for n in NAV if n[0] == fname][0][3]
        s = s[:h1] + header(ph).rstrip("\n") + s[h2:]
        # sisa jenama lama + kelas badge tak wujud
        s = s.replace(">ZB<", ">ZL<").replace('class="badge hot"', 'class="badge red"').replace('class="badge gold">Warm', 'class="badge amber">Warm')
        s = s.replace("localStorage.getItem('za-theme')", "localStorage.getItem('zl-theme')").replace("localStorage.setItem('za-theme'", "localStorage.setItem('zl-theme'")
        # notis punca kebenaran (keputusan B, 19/9/2026) — disisip sekali sahaja
        if fname == "index.html" and "System of record:" not in s:
            notis = ('<div class="banner">System of record: <b>Zentra Launch</b>. '
                     'Notion \'Projek Baharu MT\' becomes a read-only archive after the one-time import '
                     '(decision 19/9/2026).</div>\n    ')
            s = s.replace('<div class="content">\n', '<div class="content">\n    ' + notis, 1)
        open(p, "w", encoding="utf-8").write(s)
        changed.append(fname)
    return changed


if __name__ == "__main__":
    sizes = {}
    for fname, title, body in NEW_PAGES:
        sizes[fname] = page(fname, title, body)
    print("halaman baharu:", sizes)
    print("halaman dikemas (nav seragam):", patch_existing())
    print("jumlah fail:", len(os.listdir(OUT)))
