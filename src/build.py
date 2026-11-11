# Génère les pages du site à partir de modèles. Lancer : python3 src/build.py
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "SimulMalin"
DOMAIN = "https://simulmalin.fr"  # À remplacer par le vrai domaine
AD = '<div class="ad-slot" aria-hidden="true">Publicité</div>'

def page(slug, title, desc, body, faq=None, script=""):
    ld = []
    if faq:
        ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]})
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>' for x in ld)
    faq_html = ""
    if faq:
        faq_html = "<h2>Questions fréquentes</h2>" + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in faq)
    tool = slug in ICONS
    crumb = f'<nav class="crumb"><a href="index.html">Accueil</a> › <span>{title.split(":")[0].split("–")[0].strip()}</span> <em class="upd">Mis à jour : novembre 2026</em></nav>' if tool else ""
    rel = related(slug) if tool else ""
    url = f"{DOMAIN}/{'' if slug=='index' else slug+'.html'}"
    html = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website">
<link rel="stylesheet" href="style.css"><link rel="icon" href="favicon.svg" type="image/svg+xml"><meta name="theme-color" content="#1f6feb">{ld_html}
<!-- Emplacement du code AdSense / Ezoic : à coller ici une fois le compte validé -->
</head><body>
<header><div class="wrap"><a class="logo" href="index.html"><img src="favicon.svg" alt="" width="28" height="28">Simul<span>Malin</span></a>
<nav><a href="salaire-brut-net.html">Salaire</a><a href="frais-de-notaire.html">Notaire</a><a href="credit-immobilier.html">Crédit</a><a href="index.html#outils">Tous les outils</a></nav></div></header>
<main class="wrap">{crumb}{body}{faq_html}{rel}{AD if slug not in ('mentions-legales','confidentialite','a-propos','contact') else ''}</main>
<footer><div class="wrap"><p>© 2026 {SITE}. Les résultats sont des estimations indicatives et ne remplacent pas l'avis d'un professionnel.</p>
<a href="a-propos.html">À propos</a><a href="contact.html">Contact</a><a href="mentions-legales.html">Mentions légales</a><a href="confidentialite.html">Confidentialité et cookies</a></div></footer>
<script>const eur=n=>n.toLocaleString('fr-FR',{{style:'currency',currency:'EUR',maximumFractionDigits:0}});const eur2=n=>n.toLocaleString('fr-FR',{{style:'currency',currency:'EUR'}});</script>
{script}</body></html>"""
    open(os.path.join(ROOT, slug + ".html"), "w", encoding="utf-8").write(html)
    return url

TOOLS = [
 ("Emploi et salaire", [
  ("salaire-brut-net","💶","Salaire brut → net","Convertissez votre salaire mensuel, annuel ou horaire.","#e8f0fe"),
  ("indemnite-licenciement","📄","Indemnité de licenciement","Minimum légal, aussi valable en rupture conventionnelle.","#fdecea")]),
 ("Immobilier", [
  ("frais-de-notaire","🏠","Frais de notaire","Estimez les frais d'achat dans l'ancien ou le neuf.","#e6f4ea"),
  ("credit-immobilier","🏦","Crédit immobilier","Mensualités, coût total et tableau d'amortissement.","#fef7e0")]),
 ("Outils du quotidien", [
  ("calcul-tva","🧾","Calcul de TVA","Passez du HT au TTC et inversement.","#f3e8fd"),
  ("calcul-pourcentage","📊","Pourcentages","Remise, augmentation, taux d'évolution.","#e0f7fa"),
  ("jours-entre-deux-dates","📅","Jours entre deux dates","Jours calendaires et jours ouvrés.","#fce8f3")]),
]
ICONS = {
 "salaire-brut-net":('<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18M16 15h2"/>',"#1f6feb","#e8f0fe"),
 "indemnite-licenciement":('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',"#d93025","#fdecea"),
 "frais-de-notaire":('<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z"/>',"#0f9d58","#e6f4ea"),
 "credit-immobilier":('<path d="M3 21h18M5 21V10M19 21V10M9.5 21V10M14.5 21V10M2 10l10-6 10 6z"/>',"#b06000","#fef7e0"),
 "calcul-tva":('<path d="M5 3h14v18l-3-2-2 2-2-2-2 2-2-2-3 2z"/><path d="M9 8h6M9 12h6"/>',"#8430ce","#f3e8fd"),
 "calcul-pourcentage":('<path d="M19 5L5 19"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>',"#007b83","#e0f7fa"),
 "jours-entre-deux-dates":('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',"#c5221f","#fce8f3"),
}
def icon(slug):
    d,fg,bg=ICONS[slug]
    return f'<span class="ico" style="background:{bg};color:{fg}"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg></span>'
def card(t): return f'<a class="tool" href="{t[0]}.html">{icon(t[0])}<span><strong>{t[2]}</strong><small>{t[3]}</small></span></a>'
def related(slug):
    allt=[t for _,l in TOOLS for t in l if t[0]!=slug][:3]
    return '<h2>Autres simulateurs utiles</h2><div class="grid">'+"".join(card(t) for t in allt)+'</div>'

urls = []

# ---------- ACCUEIL ----------
urls.append(page("index", "SimulMalin : simulateurs gratuits salaire, notaire, crédit",
 "Calculateurs gratuits et instantanés : salaire brut en net, frais de notaire, mensualités de crédit immobilier. Simple, rapide, sans inscription.",
 """<section class="hero"><h1>Vos calculs du quotidien, <span>en quelques secondes</span></h1>
<p class="lead">Des simulateurs gratuits et sans inscription pour décider en toute confiance : salaire, achat immobilier, crédit, démarches.</p>
<div class="badges"><span>✓ 100 % gratuit</span><span>✓ Barèmes 2026</span><span>✓ Aucune donnée enregistrée</span></div></section>
""" + "".join('<h2 class="cat"'+(' id="outils"' if i==0 else '')+'>'+c+'</h2><div class="grid">'+"".join(card(t) for t in l)+'</div>' for i,(c,l) in enumerate(TOOLS)) + """
<h2>Pourquoi utiliser SimulMalin ?</h2>
<div class="grid why"><div class="card"><strong>Instantané</strong><p>Les résultats se mettent à jour pendant que vous tapez, sans bouton ni rechargement.</p></div>
<div class="card"><strong>Expliqué</strong><p>Chaque outil détaille son calcul et répond aux questions les plus fréquentes.</p></div>
<div class="card"><strong>Confidentiel</strong><p>Vos chiffres restent dans votre navigateur : rien n'est envoyé ni enregistré.</p></div></div>"""))

# ---------- SALAIRE ----------
urls.append(page("salaire-brut-net", "Salaire brut en net 2026 : calculateur gratuit et instantané",
 "Convertissez votre salaire brut en net (et net en brut) pour 2026 : cadre, non-cadre, fonction publique. Mensuel, annuel, horaire, avec prélèvement à la source.",
 """<h1>Calcul salaire brut en net 2026</h1>
<p class="lead">Saisissez un montant brut ou net : l'autre se calcule automatiquement.</p>
<div class="card">
<div class="row"><div><label for="statut">Statut</label><select id="statut">
<option value="0.22">Salarié non-cadre (≈ 22 %)</option><option value="0.25">Salarié cadre (≈ 25 %)</option>
<option value="0.15">Fonction publique (≈ 15 %)</option></select></div>
<div><label for="periode">Période</label><select id="periode"><option value="1">Mensuel</option><option value="12">Annuel</option><option value="h">Horaire (35 h)</option></select></div></div>
<div class="row"><div><label for="brut">Salaire brut (€)</label><input id="brut" type="number" inputmode="decimal" value="2500"></div>
<div><label for="net">Salaire net avant impôt (€)</label><input id="net" type="number" inputmode="decimal"></div></div>
<label for="pas">Taux de prélèvement à la source (%)</label><input id="pas" type="number" step="0.1" value="0">
<div class="result" aria-live="polite"><div>Net après impôt</div><div class="big" id="apres">–</div>
<div class="kv"><span>Net mensuel avant impôt</span><b id="nm">–</b></div>
<div class="kv"><span>Net annuel avant impôt</span><b id="na">–</b></div>
<div class="kv"><span>Cotisations salariales</span><b id="cot">–</b></div></div>
</div>
""" + AD + """
<h2>Montants les plus recherchés</h2><p class="chips">""" + "".join(f'<a href="salaire-{m}-euros-brut-en-net.html">{m} € brut</a>' for m in range(1500,5001,100)) + """</p>
<h2>Comment passer du brut au net ?</h2>
<p>Le salaire net correspond au salaire brut diminué des cotisations salariales (sécurité sociale, retraite, CSG/CRDS, chômage…). Leur poids dépend du statut : environ 22 % pour un non-cadre, 25 % pour un cadre et 15 % dans la fonction publique.</p>
<p>Depuis 2019, l'impôt sur le revenu est en plus prélevé à la source. Le montant versé sur votre compte est donc le « net après impôt ».</p>
<p class="note">Estimation indicative : les taux réels varient selon la convention collective, la mutuelle et les avantages en nature.</p>""",
 faq=[("Combien fait 2 000 € brut en net ?","Pour un salarié non-cadre du privé, 2 000 € brut mensuel donnent environ 1 560 € net avant impôt. Pour un cadre, environ 1 500 €."),
      ("Quelle différence entre net avant et après impôt ?","Le net avant impôt sert de base au prélèvement à la source. Le net après impôt est ce que vous recevez réellement sur votre compte."),
      ("Pourquoi un cadre touche-t-il moins de net pour le même brut ?","Les cadres cotisent davantage pour la retraite complémentaire et la prévoyance, ce qui augmente leurs cotisations salariales d'environ 3 points.")],
 script="""<script>
const $=id=>document.getElementById(id);let src='brut';
function per(){const p=$('periode').value;return p==='h'?151.67:(+p===12?1/12:1)}
function calc(){const t=+$('statut').value,f=per();
 if(src==='brut'){$('net').value=$('brut').value?(+$('brut').value*(1-t)).toFixed(2):''}else{$('brut').value=$('net').value?(+$('net').value/(1-t)).toFixed(2):''}
 const bm=+$('brut').value*(f===151.67?151.67:f),nm=bm*(1-t),pas=+$('pas').value/100;
 $('nm').textContent=eur2(nm);$('na').textContent=eur(nm*12);$('cot').textContent=eur2(bm-nm)+' / mois';$('apres').textContent=eur2(nm*(1-pas))+' / mois'}
$('brut').oninput=()=>{src='brut';calc()};$('net').oninput=()=>{src='net';calc()};['statut','periode','pas'].forEach(i=>$(i).oninput=calc);calc();
</script>"""))

# ---------- NOTAIRE ----------
urls.append(page("frais-de-notaire", "Calcul frais de notaire 2026 : simulateur ancien et neuf",
 "Estimez vos frais de notaire 2026 pour un achat immobilier dans l'ancien ou le neuf : droits de mutation, émoluments, débours. Détail complet et gratuit.",
 """<h1>Calcul des frais de notaire 2026</h1>
<p class="lead">Environ 7 à 8 % du prix dans l'ancien, 2 à 3 % dans le neuf. Obtenez le détail exact.</p>
<div class="card"><div class="row">
<div><label for="prix">Prix d'achat du bien (€)</label><input id="prix" type="number" value="250000"></div>
<div><label for="type">Type de bien</label><select id="type"><option value="ancien">Ancien</option><option value="neuf">Neuf (VEFA)</option></select></div></div>
<div class="row"><div><label for="dmto">Taux du département (ancien)</label><select id="dmto">
<option value="0.0631850">Taux relevé (5 %) – majorité des départements depuis 2025</option><option value="0.0580665">Taux normal (4,5 %)</option></select></div>
<div><label for="mob">Mobilier inclus (€, déductible)</label><input id="mob" type="number" value="0"></div></div>
<div class="result" aria-live="polite"><div>Frais de notaire estimés</div><div class="big" id="tot">–</div>
<div class="kv"><span>Droits de mutation (taxes)</span><b id="d">–</b></div>
<div class="kv"><span>Émoluments du notaire (TTC)</span><b id="e">–</b></div>
<div class="kv"><span>Contribution de sécurité immobilière</span><b id="c">–</b></div>
<div class="kv"><span>Débours et frais divers</span><b id="f">–</b></div>
<div class="kv"><span>Part du prix</span><b id="pct">–</b></div></div></div>
""" + AD + """
<h2>De quoi se composent les frais de notaire ?</h2>
<p>Malgré leur nom, près de 80 % des « frais de notaire » sont des taxes reversées à l'État et aux collectivités (droits de mutation). Le reste comprend la rémunération réglementée du notaire (émoluments, selon un barème national), la contribution de sécurité immobilière (0,10 %) et les débours avancés pour votre compte.</p>
<p>Depuis avril 2025, la plupart des départements ont relevé leur taux de 4,5 % à 5 %. Les primo-accédants en sont exonérés dans de nombreux cas : choisissez alors le taux normal.</p>
<p class="note">Estimation indicative. Seul votre notaire peut vous communiquer le montant définitif.</p>""",
 faq=[("Comment réduire ses frais de notaire ?","Vous pouvez déduire du prix la valeur du mobilier vendu avec le logement (cuisine équipée, électroménager), dans une limite raisonnable d'environ 5 % du prix."),
      ("Les frais de notaire peuvent-ils être financés par le prêt ?","Certaines banques acceptent de les financer, mais la plupart demandent qu'ils soient couverts par votre apport personnel."),
      ("Pourquoi les frais sont-ils plus bas dans le neuf ?","Dans le neuf, l'acheteur paie la TVA incluse dans le prix ; les droits de mutation sont donc réduits à environ 0,7 %.")],
 script="""<script>
const $=id=>document.getElementById(id);
function emol(p){const t=[[6500,.0387],[17000,.01596],[60000,.01064],[Infinity,.00799]];let r=0,prev=0;for(const[l,x]of t){if(p>prev)r+=(Math.min(p,l)-prev)*x;prev=l}return r*1.2}
function calc(){const prix=Math.max(0,+$('prix').value-+$('mob').value),neuf=$('type').value==='neuf';$('dmto').disabled=neuf;
 const d=prix*(neuf?0.00715:+$('dmto').value),e=emol(prix),c=Math.max(15,prix*0.001),f=1200,t=d+e+c+f;
 $('d').textContent=eur(d);$('e').textContent=eur(e);$('c').textContent=eur(c);$('f').textContent=eur(f);$('tot').textContent=eur(t);
 $('pct').textContent=(+$('prix').value?(t/+$('prix').value*100).toFixed(2).replace('.',','):0)+' %'}
['prix','type','dmto','mob'].forEach(i=>$(i).oninput=calc);calc();
</script>"""))

# ---------- CRÉDIT ----------
urls.append(page("credit-immobilier", "Simulateur crédit immobilier 2026 : mensualités et coût total",
 "Calculez gratuitement vos mensualités de crédit immobilier, le coût total des intérêts et de l'assurance, et votre tableau d'amortissement année par année.",
 """<h1>Simulateur de crédit immobilier</h1>
<p class="lead">Mensualité, coût total et tableau d'amortissement, mis à jour en direct.</p>
<div class="card"><div class="row">
<div><label for="cap">Montant emprunté (€)</label><input id="cap" type="number" value="200000"></div>
<div><label for="duree">Durée (années)</label><input id="duree" type="number" value="25" min="1" max="30"></div></div>
<div class="row"><div><label for="taux">Taux nominal annuel (%)</label><input id="taux" type="number" step="0.01" value="3.30"></div>
<div><label for="ass">Taux d'assurance annuel (%)</label><input id="ass" type="number" step="0.01" value="0.30"></div></div>
<label for="rev">Revenus nets mensuels du foyer (€, optionnel)</label><input id="rev" type="number" value="">
<div class="result" aria-live="polite"><div>Mensualité (assurance incluse)</div><div class="big" id="m">–</div>
<div class="kv"><span>Dont assurance</span><b id="ma">–</b></div>
<div class="kv"><span>Coût total des intérêts</span><b id="ci">–</b></div>
<div class="kv"><span>Coût total de l'assurance</span><b id="ca">–</b></div>
<div class="kv"><span>Coût total du crédit</span><b id="ct">–</b></div>
<div class="kv"><span>Taux d'endettement</span><b id="te">–</b></div></div></div>
""" + AD + """
<h2>Tableau d'amortissement annuel</h2><div class="tablewrap"><table id="tab"><thead><tr><th>Année</th><th>Capital remboursé</th><th>Intérêts</th><th>Capital restant</th></tr></thead><tbody></tbody></table></div>
<h2>Comment est calculée la mensualité ?</h2>
<p>La mensualité d'un prêt amortissable est constante : au début, elle rembourse surtout des intérêts, puis de plus en plus de capital. L'assurance emprunteur est ici calculée sur le capital initial, comme dans la plupart des contrats bancaires.</p>
<p>Les banques limitent le taux d'endettement à 35 % des revenus, assurance comprise, et la durée à 25 ans (27 ans pour certains achats dans le neuf).</p>""",
 faq=[("Quelle mensualité pour 200 000 € sur 25 ans ?","À 3,30 % hors assurance, la mensualité est d'environ 980 €. Avec une assurance à 0,30 %, comptez environ 1 030 €."),
      ("Qu'est-ce que le taux d'endettement ?","C'est la part de vos revenus consacrée au remboursement de vos crédits. Le Haut Conseil de stabilité financière le plafonne à 35 %."),
      ("Peut-on changer d'assurance emprunteur ?","Oui, depuis la loi Lemoine de 2022, vous pouvez changer d'assurance à tout moment, ce qui permet souvent d'économiser plusieurs milliers d'euros.")],
 script="""<script>
const $=id=>document.getElementById(id);
function calc(){const C=+$('cap').value,n=Math.round(+$('duree').value*12),r=+$('taux').value/100/12,a=C*(+$('ass').value/100)/12;
 if(!C||!n)return;const m=r?C*r/(1-Math.pow(1+r,-n)):C/n,tot=m+a;
 $('m').textContent=eur2(tot);$('ma').textContent=eur2(a);$('ci').textContent=eur(m*n-C);$('ca').textContent=eur(a*n);$('ct').textContent=eur(m*n-C+a*n);
 const rev=+$('rev').value;$('te').textContent=rev?(tot/rev*100).toFixed(1)+' %'+(tot/rev>0.35?' (au-delà de 35 %)':''):'Renseignez vos revenus';
 let k=C,rows='';for(let y=1;y*12<=n+11&&k>0.5;y++){let cp=0,it=0;for(let i=0;i<12&&k>0.5;i++){const x=k*r,p=m-x;it+=x;cp+=p;k-=p}rows+=`<tr><td>${y}</td><td>${eur(cp)}</td><td>${eur(it)}</td><td>${eur(Math.max(0,k))}</td></tr>`}
 document.querySelector('#tab tbody').innerHTML=rows}
['cap','duree','taux','ass','rev'].forEach(i=>$(i).oninput=calc);calc();
</script>"""))

# ---------- TVA ----------
urls.append(page("calcul-tva", "Calcul TVA : convertir HT en TTC et TTC en HT (20 %, 10 %, 5,5 %)",
 "Calculateur de TVA gratuit : passez du prix HT au prix TTC et inversement avec les taux français 20 %, 10 %, 5,5 % et 2,1 %. Montant de TVA détaillé.",
 """<h1>Calcul de la TVA : HT ↔ TTC</h1>
<p class="lead">Saisissez un montant HT ou TTC, l'autre se calcule instantanément.</p>
<div class="card"><label for="t">Taux de TVA</label><select id="t"><option value="20">20 % (taux normal)</option><option value="10">10 % (taux intermédiaire)</option><option value="5.5">5,5 % (taux réduit)</option><option value="2.1">2,1 % (taux particulier)</option></select>
<div class="row"><div><label for="ht">Montant HT (€)</label><input id="ht" type="number" value="100"></div><div><label for="ttc">Montant TTC (€)</label><input id="ttc" type="number"></div></div>
<div class="result" aria-live="polite"><div>Montant de la TVA</div><div class="big" id="tva">–</div></div></div>
""" + AD + """
<h2>Les formules de la TVA</h2>
<p><b>HT vers TTC :</b> TTC = HT × (1 + taux). Avec 20 %, on multiplie par 1,2.<br><b>TTC vers HT :</b> HT = TTC ÷ (1 + taux). Avec 20 %, on divise par 1,2.</p>
<h2>Quel taux de TVA appliquer ?</h2>
<p>Le taux normal de 20 % s'applique à la majorité des biens et services. Le taux de 10 % concerne notamment la restauration, les transports et certains travaux de rénovation. Le taux de 5,5 % s'applique aux produits alimentaires, aux livres et aux travaux de rénovation énergétique. Le taux de 2,1 % est réservé à certains médicaments remboursés et à la presse.</p>""",
 faq=[("Comment calculer 20 % de TVA ?","Multipliez le montant HT par 0,2 pour obtenir la TVA, ou par 1,2 pour obtenir directement le prix TTC."),
      ("Pourquoi ne pas retirer 20 % d'un prix TTC ?","Parce que la TVA est calculée sur le prix HT. Pour retrouver le HT, il faut diviser le TTC par 1,2 et non retirer 20 %.")],
 script="""<script>
const $=id=>document.getElementById(id);let src='ht';
function calc(){const t=+$('t').value/100;if(src==='ht'){$('ttc').value=$('ht').value?(+$('ht').value*(1+t)).toFixed(2):''}else{$('ht').value=$('ttc').value?(+$('ttc').value/(1+t)).toFixed(2):''}
$('tva').textContent=eur2(+$('ttc').value-+$('ht').value)}
$('ht').oninput=()=>{src='ht';calc()};$('ttc').oninput=()=>{src='ttc';calc()};$('t').oninput=calc;calc();
</script>"""))

# ---------- POURCENTAGE ----------
urls.append(page("calcul-pourcentage", "Calcul de pourcentage : augmentation, réduction, évolution",
 "Calculez facilement un pourcentage, une remise, une augmentation ou un taux d'évolution entre deux valeurs. Outil gratuit avec explications.",
 """<h1>Calcul de pourcentage</h1><p class="lead">Quatre calculs courants, résultats instantanés.</p>
<div class="card"><h2 style="margin-top:0">Combien font X % de Y ?</h2><div class="row"><div><label for="a1">Pourcentage (%)</label><input id="a1" type="number" value="15"></div><div><label for="a2">Valeur</label><input id="a2" type="number" value="80"></div></div><div class="result"><div class="big" id="r1">–</div></div></div>
<div class="card"><h2 style="margin-top:0">Prix après remise ou augmentation</h2><div class="row"><div><label for="b1">Prix initial</label><input id="b1" type="number" value="50"></div><div><label for="b2">Variation (%, négatif pour une remise)</label><input id="b2" type="number" value="-30"></div></div><div class="result"><div class="big" id="r2">–</div></div></div>
""" + AD + """
<div class="card"><h2 style="margin-top:0">Taux d'évolution entre deux valeurs</h2><div class="row"><div><label for="c1">Valeur de départ</label><input id="c1" type="number" value="1200"></div><div><label for="c2">Valeur d'arrivée</label><input id="c2" type="number" value="1500"></div></div><div class="result"><div class="big" id="r3">–</div></div></div>
<div class="card"><h2 style="margin-top:0">X représente quel pourcentage de Y ?</h2><div class="row"><div><label for="d1">Partie</label><input id="d1" type="number" value="45"></div><div><label for="d2">Total</label><input id="d2" type="number" value="180"></div></div><div class="result"><div class="big" id="r4">–</div></div></div>
<h2>Les formules à retenir</h2><p>X % de Y = Y × X ÷ 100. Taux d'évolution = (arrivée − départ) ÷ départ × 100. Attention : une baisse de 50 % suivie d'une hausse de 50 % ne ramène pas au prix de départ (100 → 50 → 75).</p>""",
 faq=[("Comment calculer une réduction de 30 % ?","Multipliez le prix par 0,7. Par exemple, 50 € avec 30 % de remise donnent 35 €."),
      ("Comment calculer un pourcentage d'augmentation ?","Soustrayez l'ancienne valeur de la nouvelle, divisez par l'ancienne valeur, puis multipliez par 100.")],
 script="""<script>
const $=id=>document.getElementById(id),fr=n=>isFinite(n)?n.toLocaleString('fr-FR',{maximumFractionDigits:2}):'–';
function calc(){$('r1').textContent=fr(+$('a1').value*+$('a2').value/100);$('r2').textContent=fr(+$('b1').value*(1+ +$('b2').value/100));
const e=(+$('c2').value-+$('c1').value)/+$('c1').value*100;$('r3').textContent=(e>0?'+':'')+fr(e)+' %';$('r4').textContent=fr(+$('d1').value/+$('d2').value*100)+' %'}
document.querySelectorAll('input').forEach(i=>i.oninput=calc);calc();
</script>"""))

# ---------- INDEMNITÉ ----------
urls.append(page("indemnite-licenciement", "Indemnité de licenciement et rupture conventionnelle 2026 : calcul",
 "Calculez le montant minimum légal de votre indemnité de licenciement ou de rupture conventionnelle selon votre ancienneté et votre salaire de référence.",
 """<h1>Calcul de l'indemnité de licenciement ou de rupture conventionnelle</h1>
<p class="lead">Montant minimum légal, applicable aussi à la rupture conventionnelle.</p>
<div class="card"><div class="row"><div><label for="sal">Salaire brut mensuel de référence (€)</label><input id="sal" type="number" value="2800"></div>
<div><label for="ans">Ancienneté (années)</label><input id="ans" type="number" value="6"></div><div><label for="mois">+ mois</label><input id="mois" type="number" value="0" min="0" max="11"></div></div>
<div class="result" aria-live="polite"><div>Indemnité légale minimum</div><div class="big" id="ind">–</div><p class="note" id="msg"></p></div></div>
""" + AD + """
<h2>Comment est calculée l'indemnité légale ?</h2>
<p>Le salarié doit justifier d'au moins 8 mois d'ancienneté. L'indemnité est égale à 1/4 de mois de salaire par année d'ancienneté jusqu'à 10 ans, puis à 1/3 de mois par année au-delà. Les années incomplètes sont comptées au prorata des mois.</p>
<p>Le salaire de référence est le plus avantageux entre la moyenne des 12 derniers mois et celle des 3 derniers mois. Votre convention collective peut prévoir un montant plus élevé : c'est alors lui qui s'applique.</p>
<p class="note">Estimation du minimum légal hors faute grave ou lourde. Vérifiez votre convention collective.</p>""",
 faq=[("L'indemnité de rupture conventionnelle est-elle imposable ?","Elle est exonérée d'impôt sur le revenu dans la limite du montant légal ou conventionnel, sauf si vous pouvez déjà toucher une pension de retraite."),
      ("Peut-on négocier plus que le minimum ?","Oui. Dans une rupture conventionnelle, le montant légal est un plancher : rien n'empêche de négocier davantage.")],
 script="""<script>
const $=id=>document.getElementById(id);
function calc(){const s=+$('sal').value,a=+$('ans').value+ +$('mois').value/12;
if(a<8/12){$('ind').textContent=eur(0);$('msg').textContent="Moins de 8 mois d'ancienneté : pas d'indemnité légale.";return}
const i=s*(Math.min(a,10)/4+Math.max(0,a-10)/3);$('ind').textContent=eur(i);$('msg').textContent='Soit '+(i/s).toLocaleString('fr-FR',{maximumFractionDigits:2})+' mois de salaire.'}
['sal','ans','mois'].forEach(i=>$(i).oninput=calc);calc();
</script>"""))

# ---------- DATES ----------
urls.append(page("jours-entre-deux-dates", "Nombre de jours entre deux dates : calculateur gratuit",
 "Calculez le nombre de jours, de semaines et de jours ouvrés entre deux dates, ou ajoutez des jours à une date. Outil gratuit et instantané.",
 """<h1>Nombre de jours entre deux dates</h1><p class="lead">Jours calendaires, semaines et jours ouvrés (hors week-ends).</p>
<div class="card"><div class="row"><div><label for="d1">Date de début</label><input id="d1" type="date"></div><div><label for="d2">Date de fin</label><input id="d2" type="date"></div></div>
<div class="result" aria-live="polite"><div>Écart</div><div class="big" id="j">–</div>
<div class="kv"><span>En semaines</span><b id="s">–</b></div><div class="kv"><span>Jours ouvrés (lundi au vendredi)</span><b id="o">–</b></div></div></div>
""" + AD + """
<div class="card"><h2 style="margin-top:0">Ajouter ou retirer des jours</h2><div class="row"><div><label for="b">Date</label><input id="b" type="date"></div><div><label for="n">Nombre de jours (négatif pour retirer)</label><input id="n" type="number" value="90"></div></div>
<div class="result"><div class="big" id="res">–</div></div></div>
<p class="note">Les jours fériés ne sont pas déduits du nombre de jours ouvrés.</p>""",
 faq=[("La date de fin est-elle comptée ?","Non, le calcul donne l'écart entre les deux dates. Ajoutez 1 si vous voulez inclure les deux jours."),
      ("Quelle différence entre jours ouvrés et ouvrables ?","Les jours ouvrés vont du lundi au vendredi. Les jours ouvrables incluent aussi le samedi.")],
 script="""<script>
const $=id=>document.getElementById(id),D=864e5,iso=d=>d.toISOString().slice(0,10);const t=new Date();$('d1').value=iso(t);$('d2').value=iso(new Date(t.getFullYear(),11,31,12));$('b').value=iso(t);
function calc(){const a=new Date($('d1').value+'T12:00'),b=new Date($('d2').value+'T12:00');if(!isNaN(a)&&!isNaN(b)){const n=Math.round((b-a)/D);
$('j').textContent=n.toLocaleString('fr-FR')+' jours';$('s').textContent=(n/7).toLocaleString('fr-FR',{maximumFractionDigits:1});
let o=0,s=Math.sign(n);for(let i=0;i<Math.abs(n);i++){const d=new Date(+a+s*(i+(s>0?1:0))*D).getDay();if(d%6)o++}$('o').textContent=o}
const c=new Date($('b').value+'T12:00');if(!isNaN(c)){const r=new Date(+c+ +$('n').value*D);$('res').textContent=r.toLocaleDateString('fr-FR',{weekday:'long',day:'numeric',month:'long',year:'numeric'})}}
document.querySelectorAll('input').forEach(i=>i.oninput=calc);calc();
</script>"""))

# ---------- PAGES « X € BRUT EN NET » ----------
STATUTS = [("Non-cadre (privé)",0.22),("Cadre (privé)",0.25),("Fonction publique",0.15)]
def fr(n,d=0): return f"{n:,.{d}f}".replace(",","\u202f").replace(".",",")
MONTANTS = list(range(1500,5001,100))
def sal_slug(m): return f"salaire-{m}-euros-brut-en-net"
for m in MONTANTS:
    rows="".join(f"<tr><td>{st}</td><td>{fr(m*(1-t))}&nbsp;€</td><td>{fr(m*12*(1-t))}&nbsp;€</td><td>{fr(m*(1-t)/151.67,2)}&nbsp;€</td></tr>" for st,t in STATUTS)
    nc=m*0.78
    voisins=" · ".join(f'<a href="{sal_slug(v)}.html">{fr(v)} € brut</a>' for v in (m-200,m-100,m+100,m+200) if v in MONTANTS)
    urls.append(page(sal_slug(m), f"{fr(m)} € brut en net : combien touche-t-on en 2026 ?",
     f"{fr(m)} € brut par mois correspondent à environ {fr(nc)} € net pour un non-cadre en 2026. Détail cadre, fonction publique, annuel et horaire.",
     f"""<nav class="crumb"><a href="index.html">Accueil</a> › <a href="salaire-brut-net.html">Salaire brut en net</a> › <span>{fr(m)} € brut</span> <em class="upd">Mis à jour : novembre 2026</em></nav>
<h1>{fr(m)} € brut en net</h1>
<p class="lead">Un salaire de <b>{fr(m)} € brut par mois</b> correspond à environ <b>{fr(nc)} € net</b> avant impôt pour un salarié non-cadre du privé.</p>
<div class="card"><div class="tablewrap"><table><thead><tr><th>Statut</th><th>Net mensuel</th><th>Net annuel</th><th>Net horaire</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="note">Base de 35 heures par semaine (151,67 h par mois), avant prélèvement à la source.</p></div>
""" + AD + f"""
<h2>Combien touche-t-on réellement avec {fr(m)} € brut ?</h2>
<p>Sur un salaire brut de {fr(m)} €, environ {fr(m*0.22)} € de cotisations salariales sont prélevées pour un non-cadre, et environ {fr(m*0.25)} € pour un cadre, qui cotise davantage pour sa retraite complémentaire. Dans la fonction publique, les cotisations sont plus faibles, autour de {fr(m*0.15)} €.</p>
<p>Sur une année, {fr(m)} € brut mensuels représentent {fr(m*12)} € brut, soit environ {fr(m*12*0.78)} € net pour un non-cadre, hors primes et treizième mois.</p>
<p>Pour un calcul personnalisé (temps partiel, taux de prélèvement à la source), utilisez notre <a href="salaire-brut-net.html">calculateur de salaire brut en net</a>.</p>
<h2>Montants proches</h2><p>{voisins}</p>
<p class="note">Estimation indicative fondée sur des taux moyens. Le montant exact dépend de votre convention collective, de votre mutuelle et de vos avantages.</p>""",
     faq=[(f"{fr(m)} € brut, ça fait combien en net ?",f"Environ {fr(nc)} € net par mois pour un non-cadre, {fr(m*0.75)} € pour un cadre et {fr(m*0.85)} € dans la fonction publique."),
          (f"Quel est le salaire net annuel pour {fr(m)} € brut par mois ?",f"Environ {fr(m*12*0.78)} € net par an pour un non-cadre, sur 12 mois.")]))

# ---------- À PROPOS / CONTACT ----------
page("a-propos","À propos de SimulMalin","SimulMalin propose des simulateurs gratuits et pédagogiques pour les calculs du quotidien : salaire, immobilier, crédit, TVA.",
 """<h1>À propos de SimulMalin</h1><div class="card"><p>SimulMalin est né d'un constat simple : les calculs du quotidien (salaire net, frais de notaire, mensualités de crédit…) sont souvent mal expliqués, éparpillés ou noyés sous la publicité.</p>
<p>Notre objectif est de proposer des outils <b>gratuits, rapides et pédagogiques</b>. Chaque simulateur s'appuie sur les barèmes publics en vigueur, détaille son calcul et répond aux questions les plus fréquentes.</p>
<p>Nos outils fournissent des estimations : pour une décision importante, rapprochez-vous toujours d'un professionnel (notaire, banque, conseiller). Une erreur ou une suggestion ? <a href="contact.html">Écrivez-nous</a>, nous corrigeons rapidement.</p></div>""")
page("contact","Contact – SimulMalin","Contactez l'équipe SimulMalin pour signaler une erreur, proposer un nouveau simulateur ou toute autre demande.",
 """<h1>Contact</h1><div class="card"><p>Une erreur dans un calcul, une idée de nouveau simulateur, une demande de partenariat ? Écrivez-nous :</p>
<p class="big" style="font-size:1.3rem"><a href="mailto:contact@simulmalin.fr">contact@simulmalin.fr</a></p><p class="note">Nous répondons généralement sous 48 heures ouvrées.</p></div>""")

# ---------- LÉGAL ----------
page("mentions-legales","Mentions légales – SimulMalin","Mentions légales du site SimulMalin.",
 """<h1>Mentions légales</h1><div class="card"><p><b>Éditeur :</b> [Nom et prénom ou raison sociale], [adresse], contact@simulmalin.fr. Statut : [particulier / micro-entreprise, SIRET].</p>
<p><b>Directeur de la publication :</b> [Nom].</p><p><b>Hébergeur :</b> GitHub, Inc. (GitHub Pages), 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>
<p><b>Responsabilité :</b> les calculs proposés sont fournis à titre indicatif. Ils ne constituent ni un conseil juridique, ni un conseil financier.</p></div>""")
page("confidentialite","Confidentialité et cookies – SimulMalin","Politique de confidentialité et de cookies de SimulMalin.",
 """<h1>Confidentialité et cookies</h1><div class="card"><p>Les données saisies dans nos calculateurs restent dans votre navigateur et ne sont jamais transmises à nos serveurs.</p>
<p>Ce site affiche de la publicité via des partenaires (par exemple Google AdSense) qui peuvent déposer des cookies pour personnaliser les annonces. Conformément au RGPD, votre consentement est demandé via le bandeau de gestion des cookies, et vous pouvez le retirer à tout moment.</p>
<p>Pour toute question : contact@simulmalin.fr.</p></div>""")

urls += [f"{DOMAIN}/a-propos.html", f"{DOMAIN}/contact.html"]
open(os.path.join(ROOT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{u}</loc></url>" for u in urls)+"</urlset>\n")
open(os.path.join(ROOT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
open(os.path.join(ROOT,"ads.txt"),"w").write("# Ajouter ici la ligne fournie par Google AdSense, ex. : google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0\n")
print("ok", len(urls))
