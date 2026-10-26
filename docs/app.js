'use strict';
const RELEASE = '2.2.0';
const $ = id => document.getElementById(id);
const state = {icons: [], style: new URLSearchParams(location.search).get('style') === 'flat' ? 'flat' : 'detailed', domain: 'all', selected: null};
const labels = {Geophysical:'Geophysics',Geological:'Geology',Geochemical:'Geochemistry',Geotechnical:'Geotechnical'};
const featuredIds = ['gp_seismic_reflection','gl_minerals_specimen','gp_magnetic_survey','gc_chemical_elements','gc_temperature_thermo','gl_block_model_3d','gc_aqua_regia_partial_digest','gl_strike_dip_mapping','gp_electromagnetic_em','gl_rock_type_igneous','gc_pressure_gauge','gl_geological_tagging_domain'];
let toastTimer;
function preview(icon,style=state.style){
  if(style==='flat'){const img=document.createElement('img');img.src='assets/'+icon.svg_file+'?v='+RELEASE;img.alt='';img.loading='lazy';img.width=img.height=96;return img;}
  const glyph=document.createElement('span');glyph.className='glyph';glyph.setAttribute('aria-hidden','true');glyph.textContent=String.fromCodePoint(icon.codepoint_int);return glyph;
}
function render(){
  const query=$('search').value.trim().toLowerCase(),category=$('category').value;
  const matches=state.icons.filter(icon=>(state.domain==='all'||icon.domain===state.domain)&&(category==='all'||icon.category===category)&&(!query||[icon.id,icon.name,icon.description,...icon.keywords].join(' ').toLowerCase().includes(query)));
  const fragment=document.createDocumentFragment();
  for(const icon of matches){
    const card=document.createElement('button');card.className='icon-card';card.dataset.id=icon.id;card.setAttribute('aria-label',icon.name+' — view details');
    const sample=document.createElement('span');sample.className='sample';sample.append(preview(icon));
    const title=document.createElement('span');title.className='icon-name';title.textContent=icon.name;
    const meta=document.createElement('span');meta.className='icon-meta';const code=document.createElement('span');code.textContent=icon.codepoint_hex;
    const expand=document.createElement('span');expand.textContent='↗';expand.setAttribute('aria-hidden','true');meta.append(code,expand);
    card.append(sample,title,meta);card.addEventListener('click',()=>openDetail(icon));fragment.append(card);
  }
  $('icons').replaceChildren(fragment);$('result-count').textContent=`${matches.length} of ${state.icons.length} icons`;$('empty').hidden=matches.length!==0;$('style-label').textContent=state.style==='detailed'?'DETAILED LINE / TTF':'FLAT COLOUR / SVG';
}
function snippet(){
  const icon=state.selected;if(!icon)return;const mode=$('snippet-type').value;
  $('detail-snippet').textContent=mode==='unicode'?`${icon.codepoint_hex}\n${String.fromCodePoint(icon.codepoint_int)}\nCSS content: "${icon.css_content}"`:mode==='java'?`GeoScienceIcons.createGlyph(\n    GeoScienceIcons.Glyph.${icon.id.toUpperCase()},\n    24\n);`:state.style==='flat'?`<img src="${icon.svg_file}"\n     alt="${icon.name}"\n     width="32" height="32">`:`<i class="gi ${icon.css_class}"\n   aria-hidden="true"></i>`;
}
function openDetail(icon){
  state.selected=icon;$('detail-preview').replaceChildren(preview(icon));$('detail-title').textContent=icon.name;$('detail-domain').textContent=labels[icon.domain]+' / '+(state.style==='flat'?'Flat colour':'Detailed line');$('detail-description').textContent=icon.description;$('detail-codepoint').textContent=icon.codepoint_hex;$('detail-category').textContent=icon.category;
  const file=state.style==='flat'?icon.svg_file:icon.svg_mono_file;$('download-svg').href='assets/'+file;$('download-svg').download=icon.id+'.svg';$('source-link').href='https://github.com/APethick/EarthScienceIcons/blob/main/dist/'+file;snippet();$('detail').showModal();document.body.classList.add('modal-open');
}
function toast(message){clearTimeout(toastTimer);$('toast').textContent=message;$('toast').classList.add('show');toastTimer=setTimeout(()=>$('toast').classList.remove('show'),2400);}
async function copy(text,label){try{if(navigator.clipboard&&window.isSecureContext)await navigator.clipboard.writeText(text);else{const input=document.createElement('textarea');input.value=text;input.style.position='fixed';input.style.opacity='0';($('detail').open?$('detail'):document.body).append(input);input.select();const success=document.execCommand('copy');input.remove();if(!success)throw new Error('Clipboard unavailable');}toast(label);}catch{toast('Clipboard unavailable. Select and copy the code above.');}}
$('search').addEventListener('input',render);$('category').addEventListener('change',render);
document.querySelectorAll('[data-domain]').forEach(button=>button.addEventListener('click',()=>{state.domain=button.dataset.domain;document.querySelectorAll('[data-domain]').forEach(item=>item.setAttribute('aria-pressed',item===button));render();}));
for(const style of ['detailed','flat'])$(style).addEventListener('click',()=>{state.style=style;for(const id of ['detailed','flat'])$(id).setAttribute('aria-pressed',id===style);const url=new URL(location.href);if(style==='flat')url.searchParams.set('style','flat');else url.searchParams.delete('style');history.replaceState(null,'',url);render();});
for(const id of ['detailed','flat'])$(id).setAttribute('aria-pressed',id===state.style);
$('size').addEventListener('input',event=>{document.documentElement.style.setProperty('--icon-size',event.target.value+'px');$('size-label').value=event.target.value;});
$('theme').addEventListener('click',()=>{const dark=document.body.classList.toggle('dark');$('theme').setAttribute('aria-label',dark?'Use light theme':'Use dark theme');});
$('reset').addEventListener('click',()=>{$('search').value='';$('category').value='all';document.querySelector('[data-domain="all"]').click();});
$('close-detail').addEventListener('click',()=>$('detail').close());$('detail').addEventListener('close',()=>document.body.classList.remove('modal-open'));
$('detail').addEventListener('click',event=>{const box=$('detail').getBoundingClientRect();if(event.target===$('detail')&&(event.clientX<box.left||event.clientX>box.right||event.clientY<box.top||event.clientY>box.bottom))$('detail').close();});
$('snippet-type').addEventListener('change',snippet);$('copy-snippet').addEventListener('click',()=>copy($('detail-snippet').textContent,'Code copied'));$('copy-character').addEventListener('click',()=>copy(String.fromCodePoint(state.selected.codepoint_int),'Glyph copied'));
document.addEventListener('keydown',event=>{if(event.key==='/'&&!$('detail').open&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)){event.preventDefault();$('search').focus();}});
fetch('assets/geoscience-icons.json?v='+RELEASE).then(response=>{if(!response.ok)throw new Error('Unable to load icons');return response.json();}).then(catalog=>{state.icons=catalog.icons;document.querySelectorAll('[data-total]').forEach(item=>item.textContent=state.icons.length);document.querySelectorAll('[data-domain]').forEach(button=>{const count=button.querySelector('span');if(count)count.textContent=state.icons.filter(icon=>button.dataset.domain==='all'||icon.domain===button.dataset.domain).length;});for(const id of featuredIds){const icon=state.icons.find(item=>item.id===id);if(!icon)continue;const tile=document.createElement('div');tile.className='featured-item';tile.title=icon.name;const index=document.createElement('small');index.textContent=String(icon.index).padStart(3,'0');tile.append(index,preview(icon,'detailed'));$('featured').append(tile);}render();}).catch(()=>{$('result-count').textContent='The icon library could not load. Refresh to try again.';$('empty').hidden=false;});
