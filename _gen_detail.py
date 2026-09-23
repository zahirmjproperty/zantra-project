#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_gen_detail.py — penjana halaman drill-down ZANTRA PROJECT: project.html + unit.html.

- project.html?p=<slug>  : butiran satu projek (fasa/blok, senarai harga, prestasi jualan, pasukan, aktiviti)
- unit.html?u=<id>       : butiran satu unit (spesifikasi, pelan lantai, status, tempahan, dokumen, log audit)
Klik dari kad projek (projects.html) dan grid unit (inventory.html) dijahit oleh skrip ini juga.
Semua data = SAMPEL (mock-up); halaman ditanda jelas dan kekal noindex.
Gaya selamat: HTML sebagai string + token @@KEY@@ (JANGAN gabungan f-string/% panjang).
"""
import json
import os
import re
import sys

sys.path.insert(0, "/home/ubuntu/mockup-hartanah/zantra-project")
import _gen_project as G  # sidebar/header/page yang sama → nav seragam

OUT = "/home/ubuntu/mockup-hartanah/zantra-project"

# ───────────────────────────────────────────────────────────────── data projek (SAMPEL)
PROJECTS = [
    {
        "slug": "avalon-cybersouth", "name": "Avalon Cybersouth", "type": "High-Rise",
        "location": "Cyberjaya, Selangor", "storeys": "17 storeys", "units": 120,
        "sold": 68, "reserved": 12, "launch": "Jan 2026", "completion": "Dec 2028",
        "avg_price": 486000, "land": "4.2 acres", "tenure": "Freehold",
        "dl": "DL 2026/0418", "apdl": "APDL 2026/1042 (valid to 31 Dec 2027)",
        "blocks": [["Block A", 60, 34], ["Block B", 60, 34]],
        "prices": [["3R2B", "1,050 sq ft", "RM 385,000 – 489,000"], ["4R3B", "1,320 sq ft", "RM 612,000 – 742,000"]],
        "team": [["Aina Zulkifli", "COA partner", 12], ["Fadilah Ismail", "Internal agent", 9], ["Hafiz Rahman", "COA partner", 6]],
        "activity": [
            ["19 Sep 2026", "A-12-03 booked — Ahmad Faiz (RM 468,000)"],
            ["18 Sep 2026", "B-04-11 SPA signed — Lim Wei Hong"],
            ["17 Sep 2026", "Price list revision approved — Block B +2%"],
            ["12 Sep 2026", "Block A foundation certified (milestone 3)"],
        ],
    },
    {
        "slug": "setia-seraya-p15", "name": "Setia Seraya P15", "type": "Landed",
        "location": "Shah Alam, Selangor", "storeys": "2-storey terraces", "units": 86,
        "sold": 52, "reserved": 8, "launch": "Mar 2026", "completion": "Dec 2027",
        "avg_price": 845000, "land": "11.4 acres", "tenure": "Freehold",
        "dl": "DL 2025/0912", "apdl": "APDL 2025/2288 (valid to 30 Jun 2027)",
        "blocks": [["Phase 1", 40, 31], ["Phase 2", 46, 21]],
        "prices": [["4R3B terrace", "2,150 sq ft", "RM 780,000 – 920,000"], ["4R4B corner", "2,480 sq ft", "RM 960,000 – 1,120,000"]],
        "team": [["Fadilah Ismail", "Internal agent", 14], ["Nurul Izzah", "Internal agent", 8]],
        "activity": [
            ["18 Sep 2026", "C-08-02 locked — Ravi Kumar (48-hour hold)"],
            ["15 Sep 2026", "Phase 2 bumi release approved for 6 units"],
            ["02 Sep 2026", "Frame completed — phase 1 (milestone certified)"],
        ],
    },
    {
        "slug": "allamanda-saujana-klia", "name": "Allamanda Saujana KLIA", "type": "Serviced",
        "location": "Sepang, Selangor", "storeys": "12 storeys", "units": 48,
        "sold": 41, "reserved": 4, "launch": "Sep 2025", "completion": "Jun 2027",
        "avg_price": 712000, "land": "2.1 acres", "tenure": "Leasehold (99 years)",
        "dl": "DL 2025/0344", "apdl": "APDL 2025/0771 (valid to 30 Sep 2026)",
        "blocks": [["Tower 1", 48, 41]],
        "prices": [["Studio", "560 sq ft", "RM 648,000 – 690,000"], ["3R2B", "1,110 sq ft", "RM 812,000 – 880,000"]],
        "team": [["Aina Zulkifli", "COA partner", 10], ["Kumar Raj", "COA partner", 7]],
        "activity": [
            ["17 Sep 2026", "D-02-07 EOI received — Fatin Amira"],
            ["08 Sep 2026", "Tower 1 topping-up certified"],
            ["29 Aug 2026", "Bumi quota fulfilled — 4 units released"],
        ],
    },
    {
        "slug": "senna-presint-12", "name": "Senna Presint 12", "type": "High-Rise",
        "location": "Putrajaya", "storeys": "25 storeys", "units": 200,
        "sold": 45, "reserved": 18, "launch": "Jun 2026", "completion": "Mar 2030",
        "avg_price": 742000, "land": "5.6 acres", "tenure": "Freehold",
        "dl": "DL 2026/0788", "apdl": "APDL 2026/1509 (valid to 31 Dec 2028)",
        "blocks": [["Block A", 100, 24], ["Block B", 100, 21]],
        "prices": [["3R2B", "1,140 sq ft", "RM 520,000 – 610,000"], ["4R3B", "1,480 sq ft", "RM 880,000 – 980,000"]],
        "team": [["Aina Zulkifli", "COA partner", 8], ["Nurul Izzah", "Internal agent", 5]],
        "activity": [
            ["16 Sep 2026", "A-09-07 loan submitted — Siti Nurhaliza (Maybank)"],
            ["10 Sep 2026", "Launch weekend: 22 EOIs captured"],
            ["28 Aug 2026", "Show unit opened for viewing"],
        ],
    },
    {
        "slug": "astana-residence-p8", "name": "Astana Residence P8", "type": "Landed",
        "location": "Cyberjaya, Selangor", "storeys": "Semi-D", "units": 32,
        "sold": 28, "reserved": 2, "launch": "Jan 2025", "completion": "Sep 2026",
        "avg_price": 1480000, "land": "6.8 acres", "tenure": "Freehold",
        "dl": "DL 2024/1122", "apdl": "APDL 2024/2011 (expired — renewal in progress)",
        "blocks": [["Phase 1", 20, 20], ["Phase 2", 12, 8]],
        "prices": [["Semi-D 40×80", "3,200 sq ft", "RM 1,280,000 – 1,480,000"], ["Semi-D 45×90", "3,600 sq ft", "RM 1,520,000 – 1,820,000"]],
        "team": [["Fadilah Ismail", "Internal agent", 11], ["Hafiz Rahman", "COA partner", 6]],
        "activity": [
            ["14 Sep 2026", "Phase 1 vacant possession inspection scheduled"],
            ["30 Aug 2026", "APDL renewal submitted (expiry risk flagged)"],
            ["12 Jul 2026", "CCC application lodged"],
        ],
        "risk": "APDL expired — new bookings blocked until renewal is approved (Regulation 6).",
    },
    {
        "slug": "terra-residences", "name": "Terra Residences", "type": "High-Rise",
        "location": "Kajang, Selangor", "storeys": "15 storeys", "units": 42,
        "sold": 36, "reserved": 3, "launch": "Jul 2025", "completion": "Jun 2027",
        "avg_price": 668000, "land": "2.9 acres", "tenure": "Freehold",
        "dl": "DL 2025/0219", "apdl": "APDL 2025/0618 (valid to 31 Mar 2027)",
        "blocks": [["Block A", 42, 36]],
        "prices": [["3R2B", "1,060 sq ft", "RM 600,000 – 690,000"], ["3R3B", "1,240 sq ft", "RM 720,000 – 900,000"]],
        "team": [["Aina Zulkifli", "COA partner", 9], ["Fadilah Ismail", "Internal agent", 7]],
        "activity": [
            ["19 Sep 2026", "E-11-05 locked — hold expires in 24 hours"],
            ["06 Sep 2026", "Windows &amp; doors installation 48% complete"],
            ["21 Aug 2026", "Bumi release approved — 3 units"],
        ],
    },
]

# Unit yang ada cerita penuh (padan dengan sales.html + buyer portal)
UNIT_DETAILS = {
    "A-12-03": {"status": "Booked", "cls": "sold", "buyer": "Ahmad Faiz", "agent": "Aina Zulkifli (COA)",
                "ref": "LAU-2608-0113", "paid": 108900, "booking_date": "25 Aug 2026", "spa": "18 Sep 2026",
                "microsite": "buyer/index.html", "stage": 4},
    "B-04-11": {"status": "SPA signed", "cls": "sold", "buyer": "Lim Wei Hong", "agent": "Fadilah Ismail",
                "ref": "LAU-2605-0088", "paid": 122400, "booking_date": "12 May 2026", "spa": "18 Sep 2026",
                "microsite": "buyer/index.html", "stage": 5},
    "A-09-07": {"status": "Loan submitted", "cls": "reserved", "buyer": "Siti Nurhaliza", "agent": "Aina Zulkifli (COA)",
                "ref": "LAU-2607-0101", "paid": 108000, "booking_date": "21 Jul 2026", "spa": "30 Aug 2026",
                "microsite": "buyer/index.html", "stage": 5},
    "A-11-05": {"status": "Reserved", "cls": "reserved", "buyer": "—", "agent": "Fadilah Ismail",
                "ref": "LAU-2609-0121", "paid": 0, "booking_date": "—", "spa": "—",
                "microsite": "", "stage": 2},
    "E-11-05": {"status": "Reserved", "cls": "reserved", "buyer": "—", "agent": "Fadilah Ismail",
                "ref": "LAU-2609-0126", "paid": 0, "booking_date": "—", "spa": "—", "microsite": "", "stage": 2},
    "C-08-02": {"status": "Reserved", "cls": "reserved", "buyer": "Ravi Kumar", "agent": "Aina Zulkifli (COA)",
                "ref": "LAU-2609-0119", "paid": 0, "booking_date": "—", "spa": "—", "microsite": "", "stage": 2},
    "A-12-05": {"status": "Sold", "cls": "sold", "buyer": "Tan Mei Ling", "agent": "Hafiz Rahman (COA)",
                "ref": "LAU-2604-0044", "paid": 233000, "booking_date": "09 Apr 2026", "spa": "02 Jun 2026",
                "microsite": "buyer/index.html", "stage": 6},
}

# Grid unit Blok A (halaman inventory) — status mesti padan dengan UNIT_DETAILS
GRID = [("A-12-01", "Sold"), ("A-12-02", "Sold"), ("A-12-03", "Booked"), ("A-12-04", "Sold"),
        ("A-12-05", "Sold"), ("A-12-06", "Reserved"), ("A-12-07", "Available"), ("A-12-08", "Sold"),
        ("A-12-09", "Sold"), ("A-12-10", "Reserved"), ("A-12-11", "Sold"), ("A-12-12", "Available"),
        ("A-11-01", "Sold"), ("A-11-02", "Available"), ("A-11-03", "Sold"), ("A-11-04", "Sold"),
        ("A-11-05", "Reserved"), ("A-11-06", "Available"), ("A-11-07", "Sold"), ("A-11-08", "Sold"),
        ("A-11-09", "Reserved"), ("A-11-10", "Sold"), ("A-11-11", "Available"), ("A-11-12", "Sold")]

STATUS_CLS = {"Booked": "sold", "Sold": "sold", "SPA signed": "sold", "Reserved": "reserved",
              "Loan submitted": "reserved", "Available": "available"}

PROJECT_JSON = json.dumps(PROJECTS, ensure_ascii=False).replace("</", "<\\/")
UNIT_JSON = json.dumps(UNIT_DETAILS, ensure_ascii=False).replace("</", "<\\/")

# ───────────────────────────────────────────────────────────────── floor plan (SVG 3R2B)
FLOORPLAN = """<div class="plan">
<svg viewBox="0 0 420 300" role="img" aria-label="Sample 3R2B floor plan">
  <g fill="none" stroke="#c9a227" stroke-opacity=".55" stroke-width="1.4">
    <rect x="10" y="10" width="400" height="280" rx="3"/>
    <path d="M10 150h240M250 10v90M250 150v140M360 150v140M10 210h240"/>
  </g>
  <g fill="#f0ead6" fill-opacity=".80" font-family="Plus Jakarta Sans, sans-serif" font-size="9.5">
    <text x="22" y="30">MASTER BEDROOM 14'0" x 12'0"</text>
    <text x="22" y="170">LIVING / DINING 14'0" x 13'0"</text>
    <text x="262" y="30">BEDROOM 2 10'0" x 10'0"</text>
    <text x="262" y="170">BEDROOM 3 10'0" x 9'0"</text>
    <text x="370" y="30">BATH 1</text>
    <text x="370" y="170">BATH 2</text>
    <text x="22" y="230">KITCHEN + YARD</text>
  </g>
  <g stroke="#94a3b8" stroke-width="1" fill="none">
    <path d="M250 128a12 12 0 0 1 22 0" />
    <path d="M360 128a12 12 0 0 1 22 0" />
    <path d="M80 205a12 12 0 0 1 0 22" />
  </g>
  <g fill="#e8ce86" font-family="Plus Jakarta Sans, sans-serif" font-size="9">
    <text x="196" y="294">BUILT-UP 1,050 SQ FT</text>
    <text x="18" y="8">N</text>
  </g>
</svg>
<div class="cap">Sample layout — 3R2B · 1,050 sq ft · layout varies by stack (mock-up)</div>
</div>"""

# ───────────────────────────────────────────────────────────────── project.html
PROJECT_JS = r"""
<script>
var PROJECTS = @@DATA@@;
function fmt(n){ return 'RM ' + Number(n).toLocaleString('en-MY'); }
function el(id, html){ var e = document.getElementById(id); if (e) e.innerHTML = html; }
function kv(rows){ return rows.map(function(r){
  return '<div class="row"><span class="k">' + r[0] + '</span><span class="v">' + r[1] + '</span></div>'; }).join(''); }

function render(){
  var slug = new URLSearchParams(location.search).get('p') || PROJECTS[0].slug;
  var p = PROJECTS.filter(function(x){ return x.slug === slug; })[0] || PROJECTS[0];
  var soldPct = Math.round(p.sold / p.units * 100);
  var value = p.sold * p.avg_price;

  document.title = 'Zantra Project — ' + p.name;
  el('crumb', '<a class="back" href="projects.html">&larr; All projects</a> · <span>' + p.name + '</span>');
  el('title', p.name);
  el('sub', p.type + ' · ' + p.location + ' · ' + p.storeys + ' · ' + p.units + ' units');
  el('chips', PROJECTS.map(function(x){
    return '<a class="chip' + (x.slug === p.slug ? ' on' : '') + '" href="project.html?p=' + x.slug + '">' + x.name + '</a>';
  }).join(''));
  el('risk', p.risk ? '<div class="banner" style="border-color:rgba(232,119,106,.35);color:var(--danger)">⚠️ ' + p.risk + '</div>' : '');
  el('stats',
    '<div class="stat-card"><div class="value">' + p.units + '</div><div class="label">Total units</div><div class="trend up">' + p.blocks.length + ' block(s)</div></div>' +
    '<div class="stat-card"><div class="value">' + p.sold + '</div><div class="label">Sold</div><div class="trend up">' + soldPct + '% take-up</div></div>' +
    '<div class="stat-card"><div class="value">' + p.reserved + '</div><div class="label">Reserved / locked</div><div class="trend down">locks expire in 48h</div></div>' +
    '<div class="stat-card"><div class="value">' + fmt(value).replace('RM ', 'RM ') + '</div><div class="label">Sales value (booked)</div><div class="trend up">avg ' + fmt(p.avg_price) + '</div></div>');
  el('spec', kv([
    ['Project', p.name], ['Type', p.type], ['Location', p.location], ['Land area', p.land],
    ['Tenure', p.tenure], ['Launch', p.launch], ['Est. completion', p.completion],
    ['Development licence', p.dl], ['Advertising &amp; selling permit', p.apdl],
    ['Buyer microsite (publish path)', 'launch.zentrapropertygroup.com/' + p.slug],
    ['Payment route', 'Developer\u2019s Housing Development Account (HDA 1966 s.7A), or the solicitor\u2019s client account per SPA']
  ]));
  el('blocks', '<div class="table-wrap"><table class="dash-table"><thead><tr><th>Block / phase</th><th>Units</th><th>Sold</th><th>Take-up</th><th></th></tr></thead><tbody>' +
    p.blocks.map(function(b){
      var pct = Math.round(b[2] / b[1] * 100);
      return '<tr><td class="strong">' + b[0] + '</td><td class="num">' + b[1] + '</td><td class="num">' + b[2] + '</td><td class="num gold">' + pct + '%</td>' +
             '<td><a class="back" href="inventory.html">Open grid &rarr;</a></td></tr>';
    }).join('') + '</tbody></table></div>');
  el('prices', '<div class="table-wrap"><table class="dash-table"><thead><tr><th>Unit type</th><th>Built-up</th><th>Price range</th></tr></thead><tbody>' +
    p.prices.map(function(r){ return '<tr><td class="strong">' + r[0] + '</td><td>' + r[1] + '</td><td class="num gold">' + r[2] + '</td></tr>'; }).join('') +
    '</tbody></table></div>');
  el('team', '<div class="activity-list">' + p.team.map(function(t){
      return '<div class="activity-item"><div class="act-body"><div class="act-title">' + t[0] + '</div>' +
             '<div class="act-meta">' + t[1] + '</div></div><div class="act-amount">' + t[2] + ' bookings</div></div>';
    }).join('') + '</div>');
  el('activity', '<div class="activity-list">' + p.activity.map(function(a){
      return '<div class="activity-item"><div class="act-body"><div class="act-title">' + a[1] + '</div>' +
             '<div class="act-meta">' + a[0] + '</div></div></div>';
    }).join('') + '</div>');
  el('links',
    '<a class="btn btn-gold" href="inventory.html">Unit inventory</a> ' +
    '<a class="btn" href="sales.html">Sales board</a> ' +
    '<a class="btn btn-ghost" href="buyer/index.html">Buyer portal preview &rarr;</a>');
}
render();
</script>
"""

PROJECT_BODY = """
    <div class="page-title">
      <h1 id="title">Project</h1>
      <div class="breadcrumb" id="crumb"></div>
      <div class="sub" id="sub" style="color:var(--text-dim);font-size:13.5px;margin-top:4px"></div>
    </div>
    <div class="banner">PREVIEW MOCK-UP — sample data. The public buyer microsite, price approval and eSPA/HIMS
      submission are shown here as designed screens, not live features.</div>
    <div class="chips" id="chips"></div>
    <div id="risk"></div>
    <div class="stat-row" id="stats"></div>
    <div class="split">
      <div>
        <div class="card"><div class="card-hd"><h2>Phases &amp; blocks</h2><span class="more">take-up</span></div>
          <div class="card-bd" id="blocks"></div></div>
        <div class="card"><div class="card-hd"><h2>Price list</h2><span class="more">approved</span></div>
          <div class="card-bd" id="prices"></div></div>
        <div class="card"><div class="card-hd"><h2>Recent activity</h2></div>
          <div class="card-bd" id="activity"></div></div>
      </div>
      <div>
        <div class="card"><div class="card-hd"><h2>Project profile</h2><span class="more">edit</span></div>
          <div class="card-bd kv" id="spec"></div></div>
        <div class="card"><div class="card-hd"><h2>Sales team</h2></div>
          <div class="card-bd" id="team"></div></div>
        <div class="card"><div class="card-hd"><h2>Open in</h2></div>
          <div class="card-bd"><div class="cta-row" id="links"></div>
            <div class="note" style="font-size:12.5px;color:var(--text-muted);margin-top:10px">
              Buyer-facing microsite is published only when the DL and APDL fields are complete (Regulation 6, HDR 1989).</div></div></div>
      </div>
    </div>
"""

# ───────────────────────────────────────────────────────────────── unit.html
UNIT_JS = r"""
<script>
var UNITS = @@DATA@@;
function fmt(n){ return 'RM ' + Number(n).toLocaleString('en-MY'); }
function el(id, html){ var e = document.getElementById(id); if (e) e.innerHTML = html; }
function kv(rows){ return rows.map(function(r){
  return '<div class="row"><span class="k">' + r[0] + '</span><span class="v">' + r[1] + '</span></div>'; }).join(''); }

function parseUnit(id){
  var m = /^([A-Z])-(\d+)-(\d+)$/.exec(id);
  if (!m) return null;
  var block = m[1], level = parseInt(m[2], 10), no = parseInt(m[3], 10);
  var corner = (no === 3 || no === 9 || no === 12);
  var built = corner ? 1150 : 1050;
  var price = 361000 + (level - 1) * 6000 + (corner ? 41000 : 0);
  return { id: id, block: block, level: level, no: no, built: built, price: price };
}

function render(){
  var id = (new URLSearchParams(location.search).get('u') || 'A-12-03').toUpperCase();
  var u = parseUnit(id) || parseUnit('A-12-03');
  var d = UNITS[u.id] || null;
  var status = d ? d.status : (u.no % 4 === 0 ? 'Reserved' : 'Available');
  var cls = d ? d.cls : (status === 'Reserved' ? 'reserved' : 'available');
  var paid = d ? d.paid : 0;
  var outstanding = u.price - paid;

  document.title = 'Zantra Project — Unit ' + u.id;
  el('crumb', '<a class="back" href="inventory.html">&larr; Unit inventory</a> · <a class="back" href="project.html?p=avalon-cybersouth">Avalon Cybersouth</a> · Block ' + u.block);
  el('title', 'Unit ' + u.id);
  el('sub', 'Avalon Cybersouth · Block ' + u.block + ' · Level ' + u.level + ' · 3R2B · ' + u.built + ' sq ft');
  el('badge', '<span class="badge ' + (cls === 'sold' ? 'green' : cls === 'reserved' ? 'amber' : 'blue') + '">' + status + '</span>');
  el('stats',
    '<div class="stat-card"><div class="value">' + fmt(u.price) + '</div><div class="label">List price</div><div class="trend up">nett after discount below</div></div>' +
    '<div class="stat-card"><div class="value">' + (paid ? fmt(paid) : '—') + '</div><div class="label">Paid to date</div><div class="trend ' + (paid ? 'up' : 'down') + '">' + (paid ? Math.round(paid / u.price * 100) + '% of price' : 'no payment yet') + '</div></div>' +
    '<div class="stat-card"><div class="value">' + (paid ? fmt(outstanding) : '—') + '</div><div class="label">Outstanding</div><div class="trend down">progressive billing</div></div>' +
    '<div class="stat-card"><div class="value">' + (d ? d.agent.split(' ')[0] : '—') + '</div><div class="label">Assigned agent</div><div class="trend up">' + (d ? d.agent : 'unassigned') + '</div></div>');
  el('spec', kv([
    ['Unit', u.id], ['Block / level', 'Block ' + u.block + ' · Level ' + u.level],
    ['Type', '3R2B'], ['Built-up', u.built + ' sq ft (' + (u.built > 1050 ? 'corner' : 'intermediate') + ')'],
    ['Bedrooms / baths', '3 / 2'], ['Car park bays', u.level >= 11 ? '2 (covered)' : '1 (covered)'],
    ['Facing', u.no <= 6 ? 'Pool / city view' : 'Garden view'], ['Tenure', 'Freehold'],
    ['Est. completion', 'Dec 2028'], ['DL / APDL', 'DL 2026/0418 · APDL 2026/1042']
  ]));
  el('price_history', '<div class="table-wrap"><table class="dash-table"><thead><tr><th>Date</th><th>Entry</th><th>Amount</th></tr></thead><tbody>' +
    '<tr><td>02 Jan 2026</td><td>Launch price list</td><td class="num">' + fmt(u.price - 30000) + '</td></tr>' +
    '<tr><td>17 Mar 2026</td><td>Revision +2% (Block A)</td><td class="num">' + fmt(u.price) + '</td></tr>' +
    (d ? '<tr><td>' + d.booking_date + '</td><td>Launch discount — booking</td><td class="num gold">- ' + fmt(10000) + '</td></tr>' +
         '<tr><td>—</td><td><b>Nett selling price</b></td><td class="num gold">' + fmt(u.price - 10000) + '</td></tr>' : '') +
    '</tbody></table></div>');
  el('plan', @@PLAN@@);

  if (d) {
    el('status', '<div class="card"><div class="card-hd"><h2>Booking</h2><span class="more">' + d.ref + '</span></div><div class="card-bd">' +
      '<div class="kv">' + kv([
        ['Status', status], ['Buyer', d.buyer], ['Agent', d.agent],
        ['Booking date', d.booking_date], ['SPA signed', d.spa], ['Stage', 'Stage ' + d.stage + ' of 7']
      ]) + '</div>' +
      (d.microsite ? '<div style="margin-top:12px"><a class="btn btn-gold" href="' + d.microsite + '">Open buyer portal &rarr;</a> ' +
        '<a class="btn btn-ghost" href="sales.html">Sales board</a></div>' : '') +
      '</div></div>' +
      '<div class="card"><div class="card-hd"><h2>Documents</h2></div><div class="card-bd">' +
      '<div class="activity-list">' +
      '<div class="activity-item"><div class="act-body"><div class="act-title">Booking form (signed)</div><div class="act-meta">' + (d.booking_date === '—' ? 'pending' : d.booking_date) + '</div></div><div class="act-amount">PDF</div></div>' +
      '<div class="activity-item"><div class="act-body"><div class="act-title">Sale &amp; Purchase Agreement</div><div class="act-meta">' + (d.spa === '—' ? 'not signed yet' : 'signed ' + d.spa) + '</div></div><div class="act-amount">PDF</div></div>' +
      '<div class="activity-item"><div class="act-body"><div class="act-title">Receipts &amp; e-invoices</div><div class="act-meta">' + (paid ? 'issued with each payment' : 'none yet') + '</div></div><div class="act-amount">' + (paid ? 'PDF' : '—') + '</div></div>' +
      '</div></div></div>');
  } else {
    el('status', '<div class="card"><div class="card-hd"><h2>Availability</h2><span class="more">no contract</span></div><div class="card-bd">' +
      '<div class="kv">' + kv([['Status', status], ['Price', fmt(u.price)], ['Lock duration', '48 hours, once booked'],
      ['Max locks per buyer', '2 units'], ['Next step', 'Issue EOI &rarr; book deposit 10%']]) + '</div>' +
      '<div style="margin-top:12px"><a class="btn btn-gold" href="#">Lock unit (48h)</a> ' +
      '<a class="btn btn-ghost" href="#">Issue EOI</a></div>' +
      '<div style="font-size:12.5px;color:var(--text-muted);margin-top:10px">No payment may be collected before the SPA is signed (Regulation 11(2), HDR 1989).</div>' +
      '</div></div>' +
      '<div class="card"><div class="card-hd"><h2>Documents</h2></div><div class="card-bd"><div class="activity-list">' +
      '<div class="activity-item"><div class="act-body"><div class="act-title">Floor plan &amp; price list</div><div class="act-meta">approved revision, 17 Mar 2026</div></div><div class="act-amount">PDF</div></div>' +
      '<div class="activity-item"><div class="act-body"><div class="act-title">DL / APDL copy</div><div class="act-meta">for buyer disclosure</div></div><div class="act-amount">PDF</div></div>' +
      '</div></div></div>');
  }

  el('audit', '<div class="activity-list">' +
    '<div class="activity-item"><div class="act-body"><div class="act-title">Viewed in inventory grid</div><div class="act-meta">Zahir Admin · today</div></div></div>' +
    (d ? '<div class="activity-item"><div class="act-body"><div class="act-title">Booked — ' + d.buyer + '</div><div class="act-meta">' + d.agent + ' · ' + d.booking_date + '</div></div></div>' : '') +
    '<div class="activity-item"><div class="act-body"><div class="act-title">Price revision +2% applied</div><div class="act-meta">by Approval · 17 Mar 2026</div></div></div>' +
    '<div class="activity-item"><div class="act-body"><div class="act-title">Created with project import</div><div class="act-meta">system · 02 Jan 2026</div></div></div>' +
    '</div>');
}
render();
</script>
"""

UNIT_BODY = """
    <div class="page-title">
      <h1 id="title">Unit</h1>
      <div class="breadcrumb" id="crumb"></div>
      <div id="badge" style="margin:8px 0 0"></div>
      <div id="sub" style="color:var(--text-dim);font-size:13.5px;margin-top:6px"></div>
    </div>
    <div class="banner">PREVIEW MOCK-UP — sample data. Locking, booking and SPA records are designed screens,
      not live features. Buyer documents shown here are the same views the buyer sees in the buyer portal.</div>
    <div class="stat-row" id="stats"></div>
    <div class="split">
      <div>
        <div id="status"></div>
        <div class="card"><div class="card-hd"><h2>Unit specification</h2></div>
          <div class="card-bd kv" id="spec"></div></div>
        <div class="card"><div class="card-hd"><h2>Price &amp; discount history</h2><span class="more">audit kept</span></div>
          <div class="card-bd" id="price_history"></div></div>
      </div>
      <div>
        <div class="card"><div class="card-hd"><h2>Floor plan</h2><span class="more">sample</span></div>
          <div class="card-bd" id="plan"></div></div>
        <div class="card"><div class="card-hd"><h2>Activity log</h2></div>
          <div class="card-bd" id="audit"></div></div>
      </div>
    </div>
"""


# ───────────────────────────────────────────────────────────────── penulisan + jahitan klik
def tulis_detail():
    pj = PROJECT_JS.replace("@@DATA@@", PROJECT_JSON)
    uj = UNIT_JS.replace("@@DATA@@", UNIT_JSON).replace("@@PLAN@@", json.dumps(FLOORPLAN))
    n1 = G.page("project.html", "Project detail", PROJECT_BODY + pj, title_block=False)
    n2 = G.page("unit.html", "Unit detail", UNIT_BODY + uj, title_block=False)
    return n1, n2


def jahit_klik():
    """Kad projek → project.html?p=slug ; sel unit → unit.html?u=ID (idempotent)."""
    out = []
    # 1) projects.html — bungkus setiap kad dalam <a>
    p = os.path.join(OUT, "projects.html")
    s = open(p, encoding="utf-8").read()
    if '<a class="project-card"' not in s:
        slugs = [pr["slug"] for pr in PROJECTS]

        def ganti(m, _c=[0]):
            slug = slugs[_c[0]] if _c[0] < len(slugs) else slugs[-1]
            _c[0] += 1
            return '<a class="project-card" href="project.html?p=%s">%s\n      </a>' % (slug, m.group(1))
        s2, n = re.subn(r'<div class="project-card">(.*?)\n      </div>', ganti, s, flags=re.S)
        if n == len(slugs):
            open(p, "w", encoding="utf-8").write(s2)
            out.append("projects.html: %d kad dijahit" % n)
        else:
            out.append("projects.html: GAGAL (padanan %d, jangka %d) — tiada perubahan" % (n, len(slugs)))
    else:
        out.append("projects.html: sudah dijahit")

    # 2) inventory.html — grid unit baharu dengan id penuh + pautan
    q = os.path.join(OUT, "inventory.html")
    t = open(q, encoding="utf-8").read()
    cells = "\n".join(
        '      <a class="unit-cell %s" href="unit.html?u=%s"><div class="uc-label">%s</div>'
        '<div class="uc-status %s">%s</div></a>'
        % (STATUS_CLS.get(st, "available"), uid, uid, STATUS_CLS.get(st, "available"), st)
        for uid, st in GRID)
    grid = '<div class="unit-grid">\n' + cells + '\n    </div>'
    t2, n2 = re.subn(r'<div class="unit-grid">.*?\n    </div>', grid, t, flags=re.S)
    if n2 == 1:
        # kemas kini ringkasan supaya padan dengan grid yang dipaparkan
        t2 = re.sub(r'<div class="inv-summary">.*?</div>',
                    '<div class="inv-summary"><span>Showing: <strong>24</strong> of 48</span>'
                    '<span>Available: <strong style="color:var(--success)">5</strong></span>'
                    '<span>Reserved: <strong style="color:var(--warning)">5</strong></span>'
                    '<span>Sold / booked: <strong style="color:var(--danger)">14</strong></span></div>', t2, flags=re.S)
        open(q, "w", encoding="utf-8").write(t2)
        out.append("inventory.html: grid 24 unit dijahit dengan pautan unit.html")
    else:
        out.append("inventory.html: GAGAL (padanan %d) — tiada perubahan" % n2)
    return out


if __name__ == "__main__":
    a, b = tulis_detail()
    print("project.html:", a, "aksara | unit.html:", b, "aksara")
    for line in jahit_klik():
        print(" ", line)
