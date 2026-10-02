'use strict';
const config=window.ZENTRA_CONFIG||{};
function trustedWebUrl(value){try{const u=new URL(value,location.href);return u.protocol==='https:'||u.origin===location.origin?u.href:null}catch{return null}}
/* Sign-in is wired to the family route only when the deployment actually
   provides it. Until then the UI states the gap: no navigation, no 404,
   no fabricated session. */
const loginUrl=config.loginStatus==='ready'&&config.loginUrl?trustedWebUrl(config.loginUrl):null;
const dialog=document.querySelector('#login-unavailable');
if(config.identityUrl&&dialog){
  const note=dialog.querySelector('[data-identity-note]');
  if(note){
    const a=document.createElement('a');
    a.href=config.identityUrl;a.textContent='ZENTRA-id identity service';
    note.textContent='The identity service is live: ';
    note.append(a);note.append(document.createTextNode('. A client for this system is not registered yet.'));
  }
}
document.querySelectorAll('[data-login]').forEach(a=>{
  if(loginUrl){a.href=loginUrl}
  else{a.href='#';a.addEventListener('click',e=>{e.preventDefault();dialog.showModal()})}
});
document.querySelector('#close-login').addEventListener('click',()=>dialog.close());
const ICONS={"Publish":'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M9 9v11"/></svg>',"Capture":'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>',"Hold":'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg>',"Sell":'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 7h18v13H3z"/><path d="M3 11h18M7 15h3"/><path d="M8 7V4h8v3"/></svg>',"Bill":'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 7h8M8 11h8M8 15h4"/></svg>',"Pay":'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 12h.01M18 12h.01"/></svg>',"Assure":'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 3l8 3v6c0 5-3.5 8.2-8 9.5C7.5 20.2 4 17 4 12V6z"/><path d="M9 12l2.2 2.2L15.5 10"/></svg>'};
const stages=[
['Publish','▤','Showcase your launch','A dedicated project microsite for each launch, with public-facing project information.',['Per-launch microsite','Public project pages'],'Public pages available'],
['Capture','♧','Turn interest into leads','Designed to capture registrations of interest (EOI), agent leads, and walk-in inquiries.',['EOI','Agent leads','Walk-in leads']],
['Hold','◇','Coordinate unit holds','Timed unit locks with buffer windows and an audit trail are part of the designed scope.',['Timed locks','Buffers','Audit trail']],
['Sell','▧','Connect bookings and documents','Unit booking, buyer packs, eKYC, and SPA/HIMS tracking are designed to connect the buyer journey.',['Unit booking','Buyer pack','eKYC','SPA / HIMS']],
['Bill','▥','Follow project progress','Designed scope: Third Schedule progressive billing for applicable HDA projects and e-invoicing. The owner-supplied schedule is 10/10/15/10/10/15/10/5/5/10; verify configuration against the relevant contract before use.',['Progressive billing','Applicable HDA projects','e-invoice']],
['Pay','▱','Coordinate agent commissions','Agent commission release on defined event triggers is part of the designed workflow.',['Agent commissions','Event triggers']],
['Assure','⬡','Keep a complete audit trail','Designed compliance scope includes DL/APDL, HPPH, PDPA, and a full audit log.',['DL / APDL','HPPH','PDPA','Audit log']]];
const tabs=document.querySelector('.workflow-grid');
stages.forEach((s,i)=>{const b=document.createElement('button');b.id='stage-'+i;b.className='stage glow-frame';b.role='tab';b.setAttribute('aria-controls','workflow-detail');b.innerHTML='<span class="symbol">'+(ICONS[s[0]]||'')+'</span><b>'+s[0]+'</b><small>'+s[2]+'</small>';b.addEventListener('click',()=>select(i));b.addEventListener('keydown',e=>{let j=i;if(['ArrowRight','ArrowDown'].includes(e.key))j=(i+1)%7;else if(['ArrowLeft','ArrowUp'].includes(e.key))j=(i+6)%7;else if(e.key==='Home')j=0;else if(e.key==='End')j=6;else return;e.preventDefault();select(j);tabs.children[j].focus()});tabs.append(b)});
function select(i){const s=stages[i];[...tabs.children].forEach((b,j)=>{b.setAttribute('aria-selected',j===i);b.tabIndex=j===i?0:-1});const p=document.querySelector('#workflow-detail');p.setAttribute('aria-labelledby','stage-'+i);p.innerHTML='<div><span class="badge">'+(s[5]||'Designed scope')+'</span><h3>'+s[0]+'</h3><p>'+s[3]+'</p></div><div class="tags">'+s[4].map(t=>'<span>'+t+'</span>').join('')+'</div>'}select(0);
const projectData=[
['XME Business Park 2','industrial','59 industrial units · Phase 3B','xme-business-park-2',config.xmeUrl],
['Pusat Perindustrian Budiman','industrial','15 industrial units · Semenyih','budiman-semenyih',config.budimanUrl],
['Avalon Cybersouth','residential','Registered project','avalon-cybersouth',''],
['Setia Seraya P15','residential','Registered project','setia-seraya-p15',''],
['Allamanda Saujana KLIA','residential','Registered project','allamanda-saujana-klia',''],
['Senna Presint 12','residential','Registered project','senna-presint-12',''],
['Astana Residence P8','residential','Registered project','astana-residence-p8',''],
['Terra Residences','residential','Registered project','terra-residences','']
];
const grid=document.querySelector('.project-grid');projectData.forEach(([name,type,subtitle,slug,url])=>{
  const card=document.createElement('article');card.className='project-card';card.dataset.type=type;
  const figure=document.createElement('div');figure.className='pc-media';
  const img=document.createElement('img');
  img.src='assets/img/projects/'+slug+'.webp';
  img.alt=name+' — illustrative development render';
  img.loading='lazy';img.width=800;img.height=500;
  figure.append(img);
  const body=document.createElement('div');body.className='pc-body';
  const category=document.createElement('span');category.className='eyebrow';category.textContent=type.toUpperCase();
  const h=document.createElement('h3');h.textContent=name;
  const p=document.createElement('p');p.textContent=subtitle||'Registered project';
  body.append(category,h,p);
  const safe=url&&trustedWebUrl(url);
  if(safe){const a=document.createElement('a');a.className='pc-link';a.href=safe;a.textContent='Visit Project Microsite';body.append(a)}
  if(name==='XME Business Park 2'){const l=document.createElement('a');l.className='pc-link';l.href='project.html?p=xme-business-park-2';l.textContent='Project page';body.append(l)}
  if(name==='Pusat Perindustrian Budiman'){const l=document.createElement('a');l.className='pc-link';l.href='project.html?p=budiman-semenyih';l.textContent='Project page';body.append(l)}
  const arrow=document.createElement('span');arrow.className='pc-arrow';arrow.setAttribute('aria-hidden','true');
  arrow.innerHTML='<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h13"/><path d="m12 5 7 7-7 7"/></svg>';
  card.append(figure,body,arrow);
  grid.append(card)});
document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-filter]').forEach(a=>a.setAttribute('aria-pressed',a===b));let count=0;grid.querySelectorAll('article').forEach(c=>{c.hidden=b.dataset.filter!=='all'&&c.dataset.type!==b.dataset.filter;if(!c.hidden)count++});document.querySelector('#project-count').textContent=count+' projects shown'}));
const menu=document.querySelector('#menu'),nav=document.querySelector('#navigation');function closeMenu(){menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Open navigation');nav.classList.remove('open')}
menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',open);menu.setAttribute('aria-label',open?'Close navigation':'Open navigation');nav.classList.toggle('open',open)});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMenu()});
