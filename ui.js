/* SimulMalin – curseurs, suffixes et graphiques de répartition */
(function(){
  // Curseurs liés aux champs numériques : <input data-range="min,max,step">
  document.querySelectorAll('input[data-range]').forEach(function(inp){
    var r=inp.getAttribute('data-range').split(','),s=document.createElement('input');
    s.type='range';s.min=r[0];s.max=r[1];s.step=r[2]||1;s.value=inp.value||r[0];s.className='slider';s.setAttribute('aria-label',(inp.labels&&inp.labels[0]?inp.labels[0].textContent:'')+' (curseur)');
    function paint(){var p=(s.value-s.min)/(s.max-s.min)*100;s.style.setProperty('--p',Math.max(0,Math.min(100,p))+'%')}
    s.addEventListener('input',function(){inp.value=s.value;paint();inp.dispatchEvent(new Event('input',{bubbles:true}))});
    inp.addEventListener('input',function(){if(inp.value!==''){s.value=inp.value;paint()}});
    inp.insertAdjacentElement('afterend',s);paint();
  });
  // Suffixe affiché dans le champ : <input data-suffix="€">
  document.querySelectorAll('input[data-suffix]').forEach(function(inp){
    var w=document.createElement('span');w.className='suffix';w.setAttribute('data-s',inp.getAttribute('data-suffix'));
    inp.parentNode.insertBefore(w,inp);w.appendChild(inp);
  });
})();
// Barre de répartition : bar('id',[{l:'Libellé',v:123,c:'var(--accent)'}])
window.bar=function(id,seg){var el=document.getElementById(id);if(!el)return;var t=seg.reduce(function(a,s){return a+Math.max(0,s.v)},0)||1;
  el.innerHTML='<div class="bar-track">'+seg.map(function(s){return '<span style="width:'+(Math.max(0,s.v)/t*100).toFixed(2)+'%;background:'+s.c+'" title="'+s.l+'"></span>'}).join('')+'</div>'+
  '<ul class="bar-legend">'+seg.map(function(s){return '<li><i style="background:'+s.c+'"></i>'+s.l+'<b>'+Math.round(Math.max(0,s.v)/t*100)+' %</b></li>'}).join('')+'</ul>'};
