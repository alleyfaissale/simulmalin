# Génère les pages du site à partir de modèles. Lancer : python3 src/build.py
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "SimulMalin"
DOMAIN = "https://simulmalin.fr"  # À remplacer par le vrai domaine
AD = '<div class="ad-slot" aria-hidden="true">Publicité</div>'

def fr(n,d=0): return f"{n:,.{d}f}".replace(",","\u202f").replace(".",",")

PAGES = []
def page(slug, title, desc, body, faq=None, script=""):
    if slug not in ("index","mentions-legales","confidentialite","contact","a-propos"):
        PAGES.append({"u": slug + ".html", "t": re.split(r" : | – ", title)[0].strip(), "d": (desc if len(desc)<=110 else desc[:110].rsplit(" ",1)[0]+"…")})
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
    rel = ((f'<p class="sources">Sources : {SOURCES[slug]}. Barèmes vérifiés en novembre 2026.</p>' if slug in SOURCES else "") + related(slug)) if tool else ""
    if slug in ("salaire-brut-net","frais-de-notaire","credit-immobilier","capacite-emprunt","indemnite-licenciement","calcul-tva"):
        body = body.replace('<div class="card">', '<div class="card calc">', 1)
    url = f"{DOMAIN}/{'' if slug=='index' else slug+'.html'}"
    html = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,600;0,9..144,700;1,9..144,600&family=Inter:wght@400;600&display=swap"><link rel="stylesheet" href="style.css"><link rel="icon" href="favicon.svg" type="image/svg+xml"><meta name="theme-color" content="#1d5c45">{ld_html}
<!-- Emplacement du code AdSense / Ezoic : à coller ici une fois le compte validé -->
</head><body>
<header><div class="wrap"><a class="logo" href="index.html"><img src="favicon.svg" alt="" width="28" height="28">Simul<span>Malin</span></a>
<form class="search" role="search" onsubmit="return false"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg><input id="q" type="search" placeholder="Rechercher un calcul…" aria-label="Rechercher un calcul" autocomplete="off"><div id="sr" role="listbox"></div></form>
<nav><a href="salaire-brut-net.html">Salaire</a><a href="frais-de-notaire.html">Notaire</a><a href="credit-immobilier.html">Crédit</a><a href="index.html#outils">Tous les outils</a></nav></div></header>
<main class="wrap">{crumb}{body}{faq_html}{rel}{AD if slug not in ('mentions-legales','confidentialite','a-propos','contact') else ''}</main>
<footer><div class="wrap"><div class="fcols">{FOOT}<div><h3>SimulMalin</h3><a href="a-propos.html">À propos</a><a href="contact.html">Contact</a><a href="mentions-legales.html">Mentions légales</a><a href="confidentialite.html">Confidentialité et cookies</a></div></div>
<p class="fine">© 2026 {SITE}. Les résultats sont des estimations indicatives et ne remplacent pas l'avis d'un professionnel. Barèmes vérifiés en novembre 2026.</p></div></footer>
<script>const eur=n=>n.toLocaleString('fr-FR',{{style:'currency',currency:'EUR',maximumFractionDigits:0}}).replace(/\u202f/g,'\u00a0');const eur2=n=>n.toLocaleString('fr-FR',{{style:'currency',currency:'EUR'}}).replace(/\u202f/g,'\u00a0');</script>
<script src="search.js" defer></script><script src="ui.js"></script>
{script}</body></html>"""
    open(os.path.join(ROOT, slug + ".html"), "w", encoding="utf-8").write(html)
    return url

TOOLS = [
 ("Emploi et salaire", [
  ("salaire-brut-net","💶","Salaire brut → net","Convertissez votre salaire mensuel, annuel ou horaire.","#e8f0fe"),
  ("indemnite-licenciement","📄","Indemnité de licenciement","Minimum légal, aussi valable en rupture conventionnelle.","#fdecea")]),
 ("Immobilier", [
  ("frais-de-notaire","🏠","Frais de notaire","Estimez les frais d'achat dans l'ancien ou le neuf.","#e6f4ea"),
  ("credit-immobilier","🏦","Crédit immobilier","Mensualités, coût total et tableau d'amortissement.","#fef7e0"),
  ("capacite-emprunt","💰","Capacité d'emprunt","Combien pouvez-vous emprunter selon vos revenus ?","#e8f5e9")]),
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
 "capacite-emprunt":('<circle cx="12" cy="12" r="9"/><path d="M15 9.5a3 3 0 0 0-3-1.5c-1.7 0-3 .9-3 2s1.3 1.7 3 2 3 .9 3 2-1.3 2-3 2a3 3 0 0 1-3-1.5M12 6v2M12 16v2"/>',"#2e7d32","#e8f5e9"),
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

SOURCES = {
 "salaire-brut-net":'<a href="https://www.urssaf.fr" rel="nofollow">urssaf.fr</a> et <a href="https://www.service-public.gouv.fr" rel="nofollow">service-public.gouv.fr</a>',
 "indemnite-licenciement":'<a href="https://www.service-public.gouv.fr" rel="nofollow">service-public.gouv.fr</a> (Code du travail)',
 "frais-de-notaire":'<a href="https://www.service-public.gouv.fr" rel="nofollow">service-public.gouv.fr</a>, <a href="https://www.notaires.fr" rel="nofollow">notaires.fr</a> et <a href="https://www.impots.gouv.fr" rel="nofollow">impots.gouv.fr</a>',
 "credit-immobilier":'<a href="https://www.banque-france.fr" rel="nofollow">Banque de France</a> et recommandations du HCSF',
 "capacite-emprunt":'<a href="https://www.banque-france.fr" rel="nofollow">Banque de France</a> et recommandations du HCSF',
 "calcul-tva":'<a href="https://www.impots.gouv.fr" rel="nofollow">impots.gouv.fr</a>',
}

FOOT = "".join('<div><h3>'+c+'</h3>'+"".join(f'<a href="{t[0]}.html">{t[2]}</a>' for t in l)+'</div>' for c,l in TOOLS)
urls = []

# ---------- SALAIRE ----------
# Barèmes 2026 (sources : URSSAF, Agirc-Arrco, service-public.fr). PMSS 2026 = 4 005 €.
PMSS = 4005
SMIC = 1867.02  # SMIC mensuel brut 35 h depuis le 1er juin 2026
def cotis(b, st):
    """Cotisations salariales mensuelles (hors mutuelle) pour un brut mensuel b.
    st : 'nc' non-cadre, 'c' cadre, 'fp' fonctionnaire titulaire (primes = 20 % du brut)."""
    csg = 0.097 * (0.9825 * min(b, 4*PMSS) + max(b - 4*PMSS, 0))  # CSG 9,20 % + CRDS 0,50 %
    if st == 'fp':
        ti = 0.8 * b  # traitement indiciaire
        return 0.111 * ti + 0.05 * min(b - ti, 0.2 * ti) + csg  # pension civile/CNRACL 11,10 % + RAFP 5 %
    t1 = min(b, PMSS); t2 = min(max(b - PMSS, 0), 7*PMSS)
    c = 0.069*t1 + 0.004*b + (0.0315 + 0.0086)*t1 + (0.0864 + 0.0108)*t2 + csg
    if b > PMSS: c += 0.0014 * (t1 + t2)  # CET
    if st == 'c': c += 0.00024 * min(b, 4*PMSS)  # APEC
    return c
def net(b, st): return b - cotis(b, st)
COTIS_JS = """const P=4005;function cotis(b,st){const csg=0.097*(0.9825*Math.min(b,4*P)+Math.max(b-4*P,0));
if(st==='fp'){const ti=0.8*b;return 0.111*ti+0.05*Math.min(b-ti,0.2*ti)+csg}
const t1=Math.min(b,P),t2=Math.min(Math.max(b-P,0),7*P);let c=0.069*t1+0.004*b+0.0401*t1+0.0972*t2+csg;
if(b>P)c+=0.0014*(t1+t2);if(st==='c')c+=0.00024*Math.min(b,4*P);return c}"""

urls.append(page("salaire-brut-net", "Salaire brut en net 2026 : calculateur gratuit et instantané",
 "Convertissez votre salaire brut en net (et net en brut) avec les taux de cotisations 2026 : cadre, non-cadre, fonction publique. Mensuel, annuel, horaire, avec prélèvement à la source.",
 """<h1>Calcul salaire brut en net 2026</h1>
<p class="lead">Saisissez un montant brut ou net : l'autre se calcule automatiquement avec les taux de cotisations 2026.</p>
<div class="card">
<div class="row"><div><label for="statut">Statut</label><select id="statut">
<option value="nc">Salarié non-cadre (privé)</option><option value="c">Salarié cadre (privé)</option>
<option value="fp">Fonctionnaire titulaire</option></select></div>
<div><label for="periode">Période</label><select id="periode"><option value="1">Mensuel</option><option value="12">Annuel</option><option value="h">Horaire (35 h)</option></select></div></div>
<div class="row"><div><label for="brut">Salaire brut (€)</label><input id="brut" type="number" inputmode="decimal" value="2500" data-range="1000,10000,50" data-suffix="€"></div>
<div><label for="net">Salaire net avant impôt (€)</label><input id="net" type="number" inputmode="decimal" data-suffix="€"></div></div>
<div class="row"><div><label for="mut">Mutuelle et prévoyance, part salariale (€ / mois)</label><input id="mut" type="number" step="1" value="0"></div>
<div><label for="pas">Taux de prélèvement à la source (%)</label><input id="pas" type="number" step="0.1" value="0"></div></div>
<div class="result" aria-live="polite"><div>Net après impôt</div><div class="big" id="apres">–</div>
<div class="bar" id="bar"></div><div class="kv"><span>Net mensuel avant impôt</span><b id="nm">–</b></div>
<div class="kv"><span>Net annuel avant impôt</span><b id="na">–</b></div>
<div class="kv"><span>Cotisations salariales</span><b id="cot">–</b></div></div>
</div>
""" + AD + """
<h2>Montants les plus recherchés</h2><p class="chips">""" + "".join(f'<a href="salaire-{m}-euros-brut-en-net.html">{m} € brut</a>' for m in range(1500,5001,100)) + """</p>
<h2>Comment passer du brut au net ?</h2>
<p>Le salaire net correspond au salaire brut diminué des cotisations salariales. Dans le privé en 2026, elles comprennent l'assurance vieillesse (6,90 % jusqu'au plafond de la Sécurité sociale de 4 005 € par mois, plus 0,40 % sur tout le salaire), la retraite complémentaire Agirc-Arrco (3,15 % + 0,86 % jusqu'au plafond, 8,64 % + 1,08 % au-delà) et la CSG-CRDS (9,70 % sur 98,25 % du brut). Cela représente environ 21 % du brut, auxquels s'ajoute la part salariale de votre mutuelle et de votre prévoyance.</p>
<p>Un cadre paie en plus la cotisation APEC (0,024 %) : sous le plafond de 4 005 €, son net est donc presque identique à celui d'un non-cadre. Pour un fonctionnaire titulaire, la retenue pour pension (11,10 % du traitement indiciaire), la retraite additionnelle sur les primes (5 %) et la CSG-CRDS représentent environ 19 % du brut.</p>
<p>Depuis 2019, l'impôt sur le revenu est en plus prélevé à la source. Le montant versé sur votre compte est donc le « net après impôt ».</p>
<p class="note">Estimation indicative avec les taux 2026 du régime général, hors mutuelle si vous ne la renseignez pas. Pour la fonction publique, le calcul suppose des primes égales à 20 % du brut. Votre fiche de paie peut différer selon votre convention collective, votre prévoyance et vos avantages en nature.</p>""",
 faq=[("Combien fait 2 000 € brut en net ?",f"Pour un salarié du privé, cadre ou non-cadre, 2 000 € brut par mois donnent environ {fr(net(2000,'nc'))} € net avant impôt en 2026, avant la part salariale de la mutuelle d'entreprise."),
      ("Quelle différence entre net avant et après impôt ?","Le net avant impôt sert de base au prélèvement à la source. Le net après impôt est ce que vous recevez réellement sur votre compte."),
      ("Un cadre touche-t-il moins de net qu'un non-cadre pour le même brut ?","Presque pas sous le plafond de la Sécurité sociale (4 005 € brut par mois en 2026) : seule la cotisation APEC de 0,024 % s'ajoute. Au-delà, la part du salaire qui dépasse le plafond supporte des cotisations de retraite complémentaire plus élevées, pour les cadres comme pour les non-cadres, et la prévoyance des cadres est souvent plus chère.")],
 script="""<script>
const $=id=>document.getElementById(id);let src='brut';
""" + COTIS_JS + """
function per(){const p=$('periode').value;return p==='h'?151.67:(+p===12?1/12:1)}
function brutDe(n,st){let lo=0,hi=n*2+100;for(let i=0;i<60;i++){const m=(lo+hi)/2;(m-cotis(m,st)<n)?lo=m:hi=m}return (lo+hi)/2}
function calc(){const st=$('statut').value,f=per(),mut=+$('mut').value||0;
 if(src==='brut'){const b=+$('brut').value*f;$('net').value=$('brut').value?((b-cotis(b,st)-mut)/f).toFixed(2):''}
 else{const n=+$('net').value*f;$('brut').value=$('net').value?(brutDe(n+mut,st)/f).toFixed(2):''}
 const bm=+$('brut').value*f,nm=bm-cotis(bm,st)-mut,pas=+$('pas').value/100;
 $('nm').textContent=eur2(nm);bar('bar',[{l:'Net versé',v:nm*(1-pas),c:'var(--accent)'},{l:'Impôt à la source',v:nm*pas,c:'#c9a227'},{l:'Cotisations',v:cotis(bm,st),c:'#b9b3a5'},{l:'Mutuelle',v:mut,c:'#8c8577'}]);$('na').textContent=eur(nm*12);$('cot').textContent=eur2(bm-nm)+' / mois';$('apres').textContent=eur2(nm*(1-pas))+' / mois'}
$('brut').oninput=()=>{src='brut';calc()};$('net').oninput=()=>{src='net';calc()};['statut','periode','pas','mut'].forEach(i=>$(i).oninput=calc);calc();
</script>"""))

# ---------- NOTAIRE ----------
urls.append(page("frais-de-notaire", "Calcul frais de notaire 2026 : simulateur ancien et neuf",
 "Estimez vos frais de notaire 2026 pour un achat immobilier dans l'ancien ou le neuf : droits de mutation, émoluments, débours. Détail complet et gratuit.",
 """<h1>Calcul des frais de notaire 2026</h1>
<p class="lead">Environ 7 à 8 % du prix dans l'ancien, 2 à 3 % dans le neuf. Obtenez le détail exact.</p>
<div class="card"><div class="row">
<div><label for="prix">Prix d'achat du bien (€)</label><input id="prix" type="number" value="250000" data-range="50000,1000000,5000" data-suffix="€"></div>
<div><label for="type">Type de bien</label><select id="type"><option value="ancien">Ancien</option><option value="neuf">Neuf (VEFA)</option></select></div></div>
<div class="row"><div><label for="dmto">Taux du département (ancien)</label><select id="dmto">
<option value="0.0631850">Taux relevé (5 %) – 88 départements en 2026</option><option value="0.0580665">Taux de 4,5 % – autres départements et primo-accédants</option><option value="0.0509006">Taux de 3,8 % – Indre</option></select></div>
<div><label for="mob">Mobilier inclus (€, déductible)</label><input id="mob" type="number" value="0"></div></div>
<div class="result" aria-live="polite"><div>Frais de notaire estimés</div><div class="big" id="tot">–</div>
<div class="bar" id="bar"></div><div class="kv"><span>Droits de mutation (taxes)</span><b id="d">–</b></div>
<div class="kv"><span>Émoluments du notaire (TTC)</span><b id="e">–</b></div>
<div class="kv"><span>Contribution de sécurité immobilière</span><b id="c">–</b></div>
<div class="kv"><span>Formalités et débours (estimation)</span><b id="f">–</b></div>
<div class="kv"><span>Part du prix</span><b id="pct">–</b></div></div></div>
""" + AD + """
<h2>Frais de notaire par prix</h2><p class="chips">""" + "".join(f'<a href="frais-de-notaire-{p}-euros.html">{p//1000} 000 €</a>' for p in range(100000,500001,25000)) + """</p>
<h2>De quoi se composent les frais de notaire ?</h2>
<p>Malgré leur nom, près de 80 % des « frais de notaire » sont des taxes reversées à l'État et aux collectivités (droits de mutation). Le reste comprend la rémunération réglementée du notaire (émoluments, selon un barème national), la contribution de sécurité immobilière (0,10 %) et les débours avancés pour votre compte.</p>
<p>Depuis avril 2025, les départements peuvent relever leur taux de 4,5 % à 5 % jusqu'au 31 mars 2028. Au 1er juin 2026, 88 départements l'ont fait. Les 11 autres restent à 4,5 % (Hautes-Alpes, Alpes-Maritimes, Ardèche, Charente, Drôme, Lozère, Oise, Hautes-Pyrénées, Saône-et-Loire, Guadeloupe et Mayotte) et l'Indre applique 3,8 %. À ces taux s'ajoutent la taxe communale de 1,20 % et les frais d'assiette de l'État (2,37 % du droit départemental).</p>
<p>La hausse à 5 % ne s'applique pas aux primo-accédants, c'est-à-dire aux acheteurs qui n'ont pas été propriétaires de leur résidence principale au cours des deux dernières années et qui achètent leur future résidence principale : choisissez alors le taux de 4,5 %.</p>
<p>Les émoluments du notaire suivent le barème national reconduit à l'identique jusqu'au 29 février 2028 : 3,870 % jusqu'à 6 500 €, 1,596 % de 6 500 à 17 000 €, 1,064 % de 17 000 à 60 000 € et 0,799 % au-delà, hors TVA de 20 %. Pour un prix d'au moins 100 000 €, le notaire peut accorder une remise de 20 % au maximum sur la part de ses émoluments calculée au-delà de 100 000 €. Les formalités et débours (cadastre, urbanisme, état hypothécaire…) sont estimés ici à 1 200 € ; le montant exact figure dans le décompte de votre notaire.</p>
<p class="note">Estimation indicative. Seul votre notaire peut vous communiquer le montant définitif.</p>""",
 faq=[("Comment réduire ses frais de notaire ?","Vous pouvez déduire du prix la valeur du mobilier vendu avec le logement (cuisine équipée, électroménager), dans une limite raisonnable d'environ 5 % du prix."),
      ("Les frais de notaire peuvent-ils être financés par le prêt ?","Certaines banques acceptent de les financer, mais la plupart demandent qu'ils soient couverts par votre apport personnel."),
      ("Pourquoi les frais sont-ils plus bas dans le neuf ?","Dans le neuf, l'acheteur paie la TVA incluse dans le prix ; les droits de mutation sont donc réduits à environ 0,7 %.")],
 script="""<script>
const $=id=>document.getElementById(id);
function emol(p){const t=[[6500,.0387],[17000,.01596],[60000,.01064],[Infinity,.00799]];let r=0,prev=0;for(const[l,x]of t){if(p>prev)r+=(Math.min(p,l)-prev)*x;prev=l}return r*1.2}
function calc(){const prix=Math.max(0,+$('prix').value-+$('mob').value),neuf=$('type').value==='neuf';$('dmto').disabled=neuf;
 const d=prix*(neuf?0.00715:+$('dmto').value),e=emol(prix),c=Math.max(15,prix*0.001),f=1200,t=d+e+c+f;
 $('d').textContent=eur(d);$('e').textContent=eur(e);$('c').textContent=eur(c);$('f').textContent=eur(f);$('tot').textContent=eur(t);bar('bar',[{l:'Taxes',v:d,c:'#b9b3a5'},{l:'Notaire',v:e,c:'var(--accent)'},{l:'Débours',v:f,c:'#c9a227'},{l:'Sécurité immo.',v:c,c:'#8c8577'}]);
 $('pct').textContent=(+$('prix').value?(t/+$('prix').value*100).toFixed(2).replace('.',','):0)+' %'}
['prix','type','dmto','mob'].forEach(i=>$(i).oninput=calc);calc();
</script>"""))

# ---------- CRÉDIT ----------
urls.append(page("credit-immobilier", "Simulateur crédit immobilier 2026 : mensualités et coût total",
 "Calculez gratuitement vos mensualités de crédit immobilier, le coût total des intérêts et de l'assurance, et votre tableau d'amortissement année par année.",
 """<h1>Simulateur de crédit immobilier</h1>
<p class="lead">Mensualité, coût total et tableau d'amortissement, mis à jour en direct.</p>
<div class="card"><div class="row">
<div><label for="cap">Montant emprunté (€)</label><input id="cap" type="number" value="200000" data-range="20000,800000,5000" data-suffix="€"></div>
<div><label for="duree">Durée (années)</label><input id="duree" type="number" value="25" min="1" max="30" data-range="5,30,1" data-suffix="ans"></div></div>
<div class="row"><div><label for="taux">Taux nominal annuel (%)</label><input id="taux" type="number" step="0.01" value="3.70" data-range="1,7,0.05" data-suffix="%"></div>
<div><label for="ass">Taux d'assurance annuel (%)</label><input id="ass" type="number" step="0.01" value="0.30"></div></div>
<label for="rev">Revenus nets mensuels du foyer (€, optionnel)</label><input id="rev" type="number" value="">
<div class="result" aria-live="polite"><div>Mensualité (assurance incluse)</div><div class="big" id="m">–</div>
<div class="bar" id="bar"></div><div class="kv"><span>Dont assurance</span><b id="ma">–</b></div>
<div class="kv"><span>Coût total des intérêts</span><b id="ci">–</b></div>
<div class="kv"><span>Coût total de l'assurance</span><b id="ca">–</b></div>
<div class="kv"><span>Coût total du crédit</span><b id="ct">–</b></div>
<div class="kv"><span>Taux d'endettement</span><b id="te">–</b></div></div></div>
""" + AD + """
<h2>Tableau d'amortissement annuel</h2><div class="tablewrap"><table id="tab"><thead><tr><th>Année</th><th>Capital remboursé</th><th>Intérêts</th><th>Capital restant</th></tr></thead><tbody></tbody></table></div>
<h2>Simulations les plus recherchées</h2><p class="chips">""" + "".join(f'<a href="emprunter-{c}-euros-sur-{y}-ans.html">{c//1000} 000 € sur {y} ans</a>' for c in range(100000,400001,50000) for y in (20,25)) + """</p>
<h2>Comment est calculée la mensualité ?</h2>
<p>La mensualité d'un prêt amortissable est constante : au début, elle rembourse surtout des intérêts, puis de plus en plus de capital. L'assurance emprunteur est ici calculée sur le capital initial, comme dans la plupart des contrats bancaires.</p>
<p>Les banques limitent le taux d'endettement à 35 % des revenus, assurance comprise, et la durée à 25 ans (27 ans pour certains achats dans le neuf).</p>
<p>En novembre 2026, les taux moyens hors assurance se situent autour de 3,5 à 3,9 % sur 20 à 25 ans selon les courtiers. Le taux proposé par défaut (3,70 %) est donc un point de départ : remplacez-le par celui de votre offre.</p>""",
 faq=[("Quelle mensualité pour 200 000 € sur 25 ans ?","À 3,70 % hors assurance, la mensualité est d'environ 1 025 €. Avec une assurance à 0,30 %, comptez environ 1 075 €."),
      ("Qu'est-ce que le taux d'endettement ?","C'est la part de vos revenus consacrée au remboursement de vos crédits. Le Haut Conseil de stabilité financière le plafonne à 35 %."),
      ("Peut-on changer d'assurance emprunteur ?","Oui, depuis la loi Lemoine de 2022, vous pouvez changer d'assurance à tout moment, ce qui permet souvent d'économiser plusieurs milliers d'euros.")],
 script="""<script>
const $=id=>document.getElementById(id);
function calc(){const C=+$('cap').value,n=Math.round(+$('duree').value*12),r=+$('taux').value/100/12,a=C*(+$('ass').value/100)/12;
 if(!C||!n)return;const m=r?C*r/(1-Math.pow(1+r,-n)):C/n,tot=m+a;
 $('m').textContent=eur2(tot);$('ma').textContent=eur2(a);$('ci').textContent=eur(m*n-C);$('ca').textContent=eur(a*n);$('ct').textContent=eur(m*n-C+a*n);bar('bar',[{l:'Capital',v:C,c:'var(--accent)'},{l:'Intérêts',v:m*n-C,c:'#c9a227'},{l:'Assurance',v:a*n,c:'#b9b3a5'}]);
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
 faq=[("L'indemnité de rupture conventionnelle est-elle imposable ?","Elle est exonérée d'impôt sur le revenu à hauteur du plus élevé de ces montants : l'indemnité légale ou conventionnelle, deux fois votre rémunération brute de l'année précédente, ou la moitié de l'indemnité versée, dans la limite de 6 plafonds annuels de la Sécurité sociale (288 360 € en 2026). Elle est entièrement imposable si vous pouvez déjà toucher une pension de retraite."),
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
STATUTS = [("Non-cadre (privé)","nc"),("Cadre (privé)","c"),("Fonctionnaire titulaire","fp")]
MONTANTS = list(range(1500,5001,100))
def sal_slug(m): return f"salaire-{m}-euros-brut-en-net"
for m in MONTANTS:
    rows="".join(f"<tr><td>{st}</td><td>{fr(net(m,k))}&nbsp;€</td><td>{fr(net(m,k)*12)}&nbsp;€</td><td>{fr(net(m,k)/151.67,2)}&nbsp;€</td></tr>" for st,k in STATUTS)
    nc=net(m,'nc'); ca=net(m,'c'); fp=net(m,'fp')
    pct=cotis(m,'nc')/m*100
    voisins=" · ".join(f'<a href="{sal_slug(v)}.html">{fr(v)} € brut</a>' for v in (m-200,m-100,m+100,m+200) if v in MONTANTS)
    smic = (f"<p>À noter : {fr(m)} € brut est inférieur au SMIC mensuel à temps plein ({fr(SMIC,2)} € brut depuis le 1er juin 2026). "
            f"Ce montant correspond donc à un temps partiel, à un contrat d'apprentissage ou à un salaire d'avant la dernière revalorisation.</p>") if m < SMIC else ""
    if m <= PMSS:
        cadre_txt = (f"Pour un cadre, la seule cotisation en plus est l'APEC (0,024 %), soit environ {fr(ca)} € net : sous le plafond de la Sécurité sociale "
                     f"({fr(PMSS)} € par mois en 2026), cadres et non-cadres touchent quasiment le même net.")
    else:
        cadre_txt = (f"Comme ce salaire dépasse le plafond de la Sécurité sociale ({fr(PMSS)} € par mois en 2026), la part au-delà supporte des cotisations "
                     f"de retraite complémentaire plus élevées (8,64 % + 1,08 % + 0,14 %). Un cadre, qui paie aussi l'APEC (0,024 %), touche environ {fr(ca)} € net.")
    urls.append(page(sal_slug(m), f"{fr(m)} € brut en net : combien touche-t-on en 2026 ?",
     f"{fr(m)} € brut par mois correspondent à environ {fr(nc)} € net avant impôt en 2026 dans le privé. Détail cadre, fonction publique, annuel et horaire.",
     f"""<nav class="crumb"><a href="index.html">Accueil</a> › <a href="salaire-brut-net.html">Salaire brut en net</a> › <span>{fr(m)} € brut</span> <em class="upd">Mis à jour : novembre 2026</em></nav>
<h1>{fr(m)} € brut en net</h1>
<p class="lead">Un salaire de <b>{fr(m)} € brut par mois</b> correspond à environ <b>{fr(nc)} € net</b> avant impôt pour un salarié non-cadre du privé en 2026.</p>
<div class="card"><div class="tablewrap"><table><thead><tr><th>Statut</th><th>Net mensuel</th><th>Net annuel</th><th>Net horaire</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="note">Base de 35 heures par semaine (151,67 h par mois), avant prélèvement à la source et avant la part salariale de la mutuelle d'entreprise (souvent 20 à 60 € par mois).</p></div>
""" + AD + f"""
<h2>Combien touche-t-on réellement avec {fr(m)} € brut ?</h2>
<p>Sur un salaire brut de {fr(m)} €, un non-cadre du privé paie environ {fr(m-nc)} € de cotisations salariales, soit {fr(pct,1)} % : assurance vieillesse, retraite complémentaire Agirc-Arrco et CSG-CRDS. {cadre_txt}</p>
<p>Un fonctionnaire titulaire paie la retenue pour pension (11,10 % du traitement indiciaire), la retraite additionnelle sur ses primes et la CSG-CRDS, soit environ {fr(fp)} € net si ses primes représentent 20 % de son brut.</p>
{smic}<p>Sur une année, {fr(m)} € brut mensuels représentent {fr(m*12)} € brut, soit environ {fr(nc*12)} € net pour un non-cadre, hors primes et treizième mois.</p>
<p>Pour un calcul personnalisé (temps partiel, mutuelle, taux de prélèvement à la source), utilisez notre <a href="salaire-brut-net.html">calculateur de salaire brut en net</a>.</p>
<h2>Montants proches</h2><p>{voisins}</p>
<p class="note">Estimation indicative avec les taux de cotisations 2026 du régime général. Le montant exact dépend de votre convention collective, de votre mutuelle, de votre prévoyance et de vos avantages.</p>""",
     faq=[(f"{fr(m)} € brut, ça fait combien en net ?",f"Environ {fr(nc)} € net par mois pour un non-cadre, {fr(ca)} € pour un cadre et {fr(fp)} € pour un fonctionnaire titulaire, avant impôt et avant mutuelle."),
          (f"Quel est le salaire net annuel pour {fr(m)} € brut par mois ?",f"Environ {fr(nc*12)} € net par an pour un non-cadre, sur 12 mois.")]))

# ---------- CAPACITÉ D'EMPRUNT ----------
urls.append(page("capacite-emprunt", "Capacité d'emprunt 2026 : combien pouvez-vous emprunter ?",
 "Calculez gratuitement votre capacité d'emprunt immobilier 2026 selon vos revenus, vos charges, la durée et le taux, avec la règle des 35 % d'endettement.",
 """<h1>Calcul de capacité d'emprunt</h1>
<p class="lead">Combien la banque peut-elle vous prêter ? Estimation instantanée selon la règle des 35 % d'endettement.</p>
<div class="card"><div class="row">
<div><label for="rev">Revenus nets mensuels du foyer (€)</label><input id="rev" type="number" value="4000" data-range="1000,15000,100" data-suffix="€"></div>
<div><label for="chg">Crédits en cours (€ / mois)</label><input id="chg" type="number" value="0"></div></div>
<div class="row"><div><label for="duree">Durée (années)</label><input id="duree" type="number" value="25" min="5" max="27" data-range="5,27,1" data-suffix="ans"></div>
<div><label for="taux">Taux nominal (%)</label><input id="taux" type="number" step="0.01" value="3.70"></div>
<div><label for="ass">Assurance (% par an)</label><input id="ass" type="number" step="0.01" value="0.30"></div></div>
<div class="result" aria-live="polite"><div>Vous pouvez emprunter environ</div><div class="big" id="cap">–</div>
<div class="bar" id="bar"></div><div class="kv"><span>Mensualité maximale (assurance incluse)</span><b id="mm">–</b></div>
<div class="kv"><span>Reste à vivre après mensualités</span><b id="rav">–</b></div>
<div class="kv"><span>Budget total avec 10 % d'apport</span><b id="bud">–</b></div></div></div>
""" + AD + """
<h2>Comment les banques calculent-elles votre capacité d'emprunt ?</h2>
<p>Depuis 2022, le Haut Conseil de stabilité financière (HCSF) impose aux banques deux règles : le taux d'endettement ne doit pas dépasser <b>35 % des revenus nets</b>, assurance comprise, et la durée est limitée à <b>25 ans</b> (27 ans pour un achat dans le neuf ou avec travaux importants). Les banques peuvent déroger à ces règles pour 20 % de leurs dossiers, en priorité pour la résidence principale.</p>
<p>La mensualité maximale correspond donc à 35 % de vos revenus, moins vos crédits en cours. On en déduit le capital empruntable avec la formule d'un prêt amortissable à mensualités constantes.</p>
<p>Le « reste à vivre » (ce qu'il vous reste une fois les crédits payés) compte aussi : avec des revenus modestes, une banque peut refuser un dossier même sous 35 %.</p>
<p>Pour connaître le coût total et le détail année par année, utilisez notre <a href="credit-immobilier.html">simulateur de crédit immobilier</a>, puis estimez vos <a href="frais-de-notaire.html">frais de notaire</a>.</p>
<p class="note">Estimation indicative : l'accord final dépend de votre apport, de votre stabilité professionnelle et de la politique de la banque.</p>""",
 faq=[("Combien emprunter avec 3 000 € de salaire ?","Avec 3 000 € de revenus nets et sans autre crédit, la mensualité maximale est de 1 050 €. Sur 25 ans à 3,70 % avec 0,30 % d'assurance, cela permet d'emprunter environ 196 000 €."),
      ("Faut-il un apport personnel ?","La plupart des banques demandent au moins 10 % du prix, pour couvrir les frais de notaire et de garantie. Sans apport, l'accord est possible mais plus difficile."),
      ("Les revenus locatifs sont-ils pris en compte ?","Oui, en général à hauteur de 70 % des loyers perçus, pour tenir compte de la vacance et des charges.")],
 script="""<script>
const $=id=>document.getElementById(id);
function calc(){const R=+$('rev').value,ch=+$('chg').value,n=Math.round(+$('duree').value*12),r=+$('taux').value/100/12,a=+$('ass').value/100/12;
 const mm=Math.max(0,R*0.35-ch);if(!n){return}const f=r?(r/(1-Math.pow(1+r,-n))):1/n,C=mm/(f+a);
 $('cap').textContent=eur(Math.round(C/1000)*1000);$('mm').textContent=eur2(mm);$('rav').textContent=eur(R-mm-ch)+' / mois';bar('bar',[{l:'Crédit immobilier',v:mm,c:'var(--accent)'},{l:'Autres crédits',v:ch,c:'#c9a227'},{l:'Reste à vivre',v:R-mm-ch,c:'#b9b3a5'}]);$('bud').textContent=eur(Math.round(C/0.9/1000)*1000)}
['rev','chg','duree','taux','ass'].forEach(i=>$(i).oninput=calc);calc();
</script>"""))

# ---------- PAGES « FRAIS DE NOTAIRE POUR X € » ----------
def emol(p):
    r,prev=0,0
    for l,x in [(6500,.0387),(17000,.01596),(60000,.01064),(float('inf'),.00799)]:
        if p>prev: r+=(min(p,l)-prev)*x
        prev=l
    return r*1.2
def notaire(p, taux):
    d=p*taux; e=emol(p); c=max(15,p*0.001); f=1200
    return d,e,c,f,d+e+c+f
PRIX = list(range(100000,500001,25000))
def not_slug(p): return f"frais-de-notaire-{p}-euros"
for p in PRIX:
    d5,e,c,f,t5 = notaire(p,0.0631850)
    d45,_,_,_,t45 = notaire(p,0.0580665)
    dn,_,_,_,tn = notaire(p,0.00715)
    voisins=" · ".join(f'<a href="{not_slug(v)}.html">{fr(v)} €</a>' for v in (p-50000,p-25000,p+25000,p+50000) if v in PRIX)
    urls.append(page(not_slug(p), f"Frais de notaire pour {fr(p)} € : montant exact en 2026",
     f"Pour un achat à {fr(p)} € dans l'ancien, les frais de notaire s'élèvent à environ {fr(t5)} € en 2026 ({fr(t5/p*100,1)} %). Détail ancien, neuf et primo-accédant.",
     f"""<nav class="crumb"><a href="index.html">Accueil</a> › <a href="frais-de-notaire.html">Frais de notaire</a> › <span>{fr(p)} €</span> <em class="upd">Mis à jour : novembre 2026</em></nav>
<h1>Frais de notaire pour un bien à {fr(p)} €</h1>
<p class="lead">Pour un achat à <b>{fr(p)} €</b> dans l'ancien, comptez environ <b>{fr(t5)} €</b> de frais de notaire en 2026, soit {fr(t5/p*100,1)} % du prix.</p>
<div class="card"><div class="tablewrap"><table><thead><tr><th>Situation</th><th>Frais estimés</th><th>Part du prix</th></tr></thead><tbody>
<tr><td>Ancien, département à 5 % (cas général)</td><td>{fr(t5)}&nbsp;€</td><td>{fr(t5/p*100,1)}&nbsp;%</td></tr>
<tr><td>Ancien, primo-accédant ou département à 4,5 %</td><td>{fr(t45)}&nbsp;€</td><td>{fr(t45/p*100,1)}&nbsp;%</td></tr>
<tr><td>Neuf (VEFA)</td><td>{fr(tn)}&nbsp;€</td><td>{fr(tn/p*100,1)}&nbsp;%</td></tr></tbody></table></div></div>
""" + AD + f"""
<h2>Détail des frais dans l'ancien</h2>
<div class="card"><div class="kv"><span>Droits de mutation (taxes)</span><b>{fr(d5)} €</b></div>
<div class="kv"><span>Émoluments du notaire (TTC)</span><b>{fr(e)} €</b></div>
<div class="kv"><span>Contribution de sécurité immobilière</span><b>{fr(c)} €</b></div>
<div class="kv"><span>Formalités et débours (estimation)</span><b>{fr(f)} €</b></div></div>
<p>Sur les {fr(t5)} € payés, {fr(d5)} € (soit {fr(d5/t5*100,0)} %) sont des taxes reversées au département, à la commune et à l'État. La rémunération du notaire, fixée par un barème national, ne représente que {fr(e)} € TTC.</p>
<p>Si vous achetez votre première résidence principale, vous échappez à la hausse des droits à 5 % : les frais tombent alors à environ {fr(t45)} €, soit {fr(t5-t45)} € d'économie. Dans le neuf, les droits de mutation sont réduits et les frais passent à environ {fr(tn)} €.</p>
<p>Pour un calcul avec votre département ou du mobilier déductible, utilisez notre <a href="frais-de-notaire.html">calculateur de frais de notaire</a>. Pour savoir si vous pouvez financer ce projet, testez votre <a href="capacite-emprunt.html">capacité d'emprunt</a>.</p>
<h2>Autres prix</h2><p>{voisins}</p>
<p class="note">Estimation indicative fondée sur les barèmes 2026. Seul votre notaire peut communiquer le montant définitif.</p>""",
     faq=[(f"Quels sont les frais de notaire pour {fr(p)} € ?",f"Environ {fr(t5)} € dans l'ancien (cas général), {fr(t45)} € pour un primo-accédant et {fr(tn)} € dans le neuf."),
          ("Les frais de notaire sont-ils négociables ?","Les taxes ne le sont pas. Le notaire peut seulement accorder une remise de 20 % au maximum sur la part de ses émoluments calculée au-delà de 100 000 €.")]))

# ---------- PAGES « EMPRUNTER X € SUR Y ANS » ----------
TAUX_D={15:3.45,20:3.60,25:3.70}
CAPITAUX=list(range(100000,400001,50000))
def cred_slug(c,y): return f"emprunter-{c}-euros-sur-{y}-ans"
for c in CAPITAUX:
    for y in (15,20,25):
        t=TAUX_D[y]; r=t/100/12; n=y*12; m=c*r/(1-(1+r)**-n); a=c*0.003/12; tot=m+a
        interets=m*n-c; revmin=tot/0.35
        autres=" · ".join(f'<a href="{cred_slug(c,yy)}.html">sur {yy} ans</a>' for yy in (15,20,25) if yy!=y)
        voisins=" · ".join(f'<a href="{cred_slug(v,y)}.html">{fr(v)} €</a>' for v in (c-50000,c+50000) if v in CAPITAUX)
        urls.append(page(cred_slug(c,y), f"Emprunter {fr(c)} € sur {y} ans : mensualité et salaire nécessaire",
         f"Pour emprunter {fr(c)} € sur {y} ans en 2026, comptez environ {fr(tot)} € par mois assurance comprise. Salaire nécessaire, coût total et intérêts.",
         f"""<nav class="crumb"><a href="index.html">Accueil</a> › <a href="credit-immobilier.html">Crédit immobilier</a> › <span>{fr(c)} € sur {y} ans</span> <em class="upd">Mis à jour : novembre 2026</em></nav>
<h1>Emprunter {fr(c)} € sur {y} ans</h1>
<p class="lead">Au taux moyen de <b>{fr(t,2)} %</b> constaté en novembre 2026, la mensualité est d'environ <b>{fr(tot)} € par mois</b>, assurance comprise.</p>
<div class="card"><div class="kv"><span>Mensualité hors assurance</span><b>{fr(m)} €</b></div>
<div class="kv"><span>Assurance (0,30 % par an)</span><b>{fr(a)} €</b></div>
<div class="kv"><span>Coût total des intérêts</span><b>{fr(interets)} €</b></div>
<div class="kv"><span>Coût total de l'assurance</span><b>{fr(a*n)} €</b></div>
<div class="kv"><span>Revenus nets minimum (35 %)</span><b>{fr(revmin)} € / mois</b></div></div>
""" + AD + f"""
<h2>Quel salaire pour emprunter {fr(c)} € sur {y} ans ?</h2>
<p>Les banques limitent le taux d'endettement à 35 % des revenus nets, assurance comprise. Pour une mensualité de {fr(tot)} €, il faut donc des revenus d'au moins <b>{fr(revmin)} € net par mois</b> pour le foyer, sans autre crédit en cours.</p>
<p>Sur {y} ans, ce prêt vous coûtera environ {fr(interets+a*n)} € au total (intérêts et assurance), soit {fr((interets+a*n)/c*100,0)} % du montant emprunté. Allonger la durée baisse la mensualité mais augmente fortement ce coût : comparez avec {autres}.</p>
<p>Ces calculs utilisent un taux indicatif. Pour simuler votre propre taux et voir le tableau d'amortissement, utilisez notre <a href="credit-immobilier.html">simulateur de crédit immobilier</a>.</p>
<h2>Autres montants sur {y} ans</h2><p>{voisins}</p>
<p class="note">Taux moyens indicatifs hors assurance en novembre 2026 : {fr(TAUX_D[15],2)} % sur 15 ans, {fr(TAUX_D[20],2)} % sur 20 ans, {fr(TAUX_D[25],2)} % sur 25 ans. Votre taux réel dépend de votre profil et de votre banque.</p>""",
         faq=[(f"Quelle mensualité pour {fr(c)} € sur {y} ans ?",f"Environ {fr(tot)} € par mois avec une assurance à 0,30 %, au taux de {fr(t,2)} %."),
              (f"Quel salaire pour emprunter {fr(c)} € sur {y} ans ?",f"Au moins {fr(revmin)} € net par mois pour le foyer, pour respecter le plafond d'endettement de 35 %.")]))

# ---------- ACCUEIL ----------
urls.append(page("index", "SimulMalin : simulateurs gratuits salaire, notaire, crédit",
 "Calculateurs gratuits et instantanés : salaire brut en net, frais de notaire, mensualités de crédit immobilier. Simple, rapide, sans inscription.",
 """<section class="hero"><div><p class="kicker">Simulateurs indépendants · barèmes 2026 vérifiés</p>
<h1>Le bon chiffre, <em>avant</em> de signer.</h1>
<p class="lead">Salaire, achat immobilier, prêt, rupture de contrat : on fait le calcul avec vous, en détaillant chaque ligne et en citant nos sources.</p></div>
<div class="ticket live"><p>Essayez : votre salaire en net</p>
<label for="hb">Salaire brut mensuel</label><span class="suffix" data-s="€"><input id="hb" type="number" inputmode="decimal" value="2500"></span>
<div class="seg" role="radiogroup" aria-label="Statut"><button type="button" data-st="nc" aria-pressed="true">Non-cadre</button><button type="button" data-st="c" aria-pressed="false">Cadre</button><button type="button" data-st="fp" aria-pressed="false">Fonctionnaire</button></div>
<div class="l"><span>Cotisations</span><span id="hc">–</span></div>
<div class="l"><span>Net avant impôt</span><span class="t" id="hn">–</span></div>
<a href="salaire-brut-net.html">Calcul détaillé (mutuelle, impôt, annuel) →</a></div></section>
""" + "".join('<h2 class="cat"'+(' id="outils"' if i==0 else '')+'>'+c+'</h2><div class="grid">'+"".join(card(t) for t in l)+'</div>' for i,(c,l) in enumerate(TOOLS)) + """
<h2>Recherches populaires</h2><p class="chips">""" + "".join(f'<a href="{u}.html">{t}</a>' for u,t in [("salaire-2000-euros-brut-en-net","2 000 € brut en net"),("salaire-2500-euros-brut-en-net","2 500 € brut en net"),("salaire-3000-euros-brut-en-net","3 000 € brut en net"),("frais-de-notaire-200000-euros","Frais de notaire 200 000 €"),("frais-de-notaire-300000-euros","Frais de notaire 300 000 €"),("emprunter-200000-euros-sur-25-ans","Emprunter 200 000 € sur 25 ans"),("emprunter-250000-euros-sur-20-ans","Emprunter 250 000 € sur 20 ans"),("capacite-emprunt","Combien puis-je emprunter ?")]) + """</p>
<h2>Notre méthode</h2>
<div class="method"><p><b>Des barèmes officiels.</b> Chaque taux vient d'une source publique (Urssaf, service-public.gouv.fr, impots.gouv.fr) et la date de vérification figure en bas de page.</p>
<p><b>Un calcul qu'on peut refaire.</b> Nous affichons le détail ligne par ligne : vous voyez d'où vient chaque euro, et vous pouvez le vérifier vous-même.</p>
<p><b>Rien n'est enregistré.</b> Les montants que vous saisissez restent dans votre navigateur. Pas de compte, pas de formulaire, pas de rappel commercial.</p>
<p><b>Une erreur ?</b> Écrivez-nous à <a href="mailto:contact@simulmalin.fr">contact@simulmalin.fr</a> : nous corrigeons et indiquons la date de mise à jour.</p></div>""", script="""<script>""" + COTIS_JS + """
let hst='nc';const hb=document.getElementById('hb');
function h(){const b=+hb.value||0,c=cotis(b,hst);document.getElementById('hc').textContent='− '+eur(c);document.getElementById('hn').textContent=eur(b-c)}
hb.oninput=h;document.querySelectorAll('.seg button').forEach(x=>x.onclick=()=>{hst=x.dataset.st;document.querySelectorAll('.seg button').forEach(y=>y.setAttribute('aria-pressed',y===x));h()});h();
</script>"""))


page("a-propos","À propos de SimulMalin","SimulMalin propose des simulateurs gratuits et pédagogiques pour les calculs du quotidien : salaire, immobilier, crédit, TVA.",
 """<h1>À propos de SimulMalin</h1><div class="card"><p>SimulMalin est né d'un constat simple : les calculs du quotidien (salaire net, frais de notaire, mensualités de crédit…) sont souvent mal expliqués, éparpillés ou noyés sous la publicité.</p>
<p>Notre objectif est de proposer des outils <b>gratuits, rapides et pédagogiques</b>. Chaque simulateur s'appuie sur les barèmes publics en vigueur, détaille son calcul et répond aux questions les plus fréquentes.</p>
<p>Nos outils fournissent des estimations : pour une décision importante, rapprochez-vous toujours d'un professionnel (notaire, banque, conseiller). Une erreur ou une suggestion ? <a href="contact.html">Écrivez-nous</a>, nous corrigeons rapidement.</p></div>""")
page("contact","Contact – SimulMalin","Contactez l'équipe SimulMalin pour signaler une erreur, proposer un nouveau simulateur ou toute autre demande.",
 """<h1>Contact</h1><div class="card"><p>Une erreur dans un calcul, une idée de nouveau simulateur, une demande de partenariat ? Écrivez-nous :</p>
<p class="big" style="font-size:1.3rem"><a href="mailto:contact@simulmalin.fr">contact@simulmalin.fr</a></p><p class="note">Nous répondons généralement sous 48 heures ouvrées.</p></div>""")

# ---------- LÉGAL ----------
page("mentions-legales","Mentions légales – SimulMalin","Mentions légales du site SimulMalin.",
 """<h1>Mentions légales</h1><div class="card"><p><b>Éditeur du site :</b> SimulMalin. Contact : <a href="mailto:contact@simulmalin.fr">contact@simulmalin.fr</a>.</p>
<p><b>Directeur de la publication :</b> l'équipe SimulMalin, joignable à la même adresse.</p>
<p><b>Propriété intellectuelle :</b> les textes et outils de ce site sont la propriété de SimulMalin. Toute reproduction sans autorisation est interdite.</p><p><b>Hébergeur :</b> GitHub, Inc. (GitHub Pages), 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>
<p><b>Responsabilité :</b> les calculs proposés sont fournis à titre indicatif. Ils ne constituent ni un conseil juridique, ni un conseil financier.</p></div>""")
page("confidentialite","Confidentialité et cookies – SimulMalin","Politique de confidentialité et de cookies de SimulMalin.",
 """<h1>Confidentialité et cookies</h1><div class="card"><p>Les données saisies dans nos calculateurs restent dans votre navigateur et ne sont jamais transmises à nos serveurs.</p>
<p>Ce site affiche de la publicité via des partenaires (par exemple Google AdSense) qui peuvent déposer des cookies pour personnaliser les annonces. Conformément au RGPD, votre consentement est demandé via le bandeau de gestion des cookies, et vous pouvez le retirer à tout moment.</p>
<p>Pour toute question : contact@simulmalin.fr.</p></div>""")

urls += [f"{DOMAIN}/a-propos.html", f"{DOMAIN}/contact.html"]
SEARCH_JS = r"""
(function(){var P=__PAGES__;var q=document.getElementById('q'),r=document.getElementById('sr');if(!q)return;
function n(s){return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/(\d)[\s\u00a0\u202f](?=\d{3}\b)/g,'$1')}
P.forEach(function(p){p.k=n(p.t+' '+p.d+' '+p.u.replace(/-/g,' '));p.h=n(p.t+' '+p.u.replace(/-/g,' '))});
function show(){var w=n(q.value).split(/\s+/).filter(Boolean);if(!w.length){r.innerHTML='';r.className='';return}
var res=P.filter(function(p){return w.every(function(x){return p.k.indexOf(x)>=0})}).sort(function(a,b){return w.filter(function(x){return b.h.indexOf(x)>=0}).length-w.filter(function(x){return a.h.indexOf(x)>=0}).length}).slice(0,8);
r.className='open';r.innerHTML=res.length?res.map(function(p){return '<a href="'+p.u+'"><b>'+p.t+'</b><small>'+p.d+'</small></a>'}).join(''):'<p>Aucun résultat. Essayez « salaire », « notaire » ou « crédit ».</p>'}
q.addEventListener('input',show);q.addEventListener('focus',show);
document.addEventListener('click',function(e){if(!e.target.closest('.search')){r.innerHTML='';r.className=''}});
q.addEventListener('keydown',function(e){if(e.key==='Enter'){var a=r.querySelector('a');if(a)location.href=a.getAttribute('href')}if(e.key==='Escape'){q.value='';show()}});})();
"""
open(os.path.join(ROOT,"search.js"),"w",encoding="utf-8").write(SEARCH_JS.replace("__PAGES__", json.dumps(PAGES, ensure_ascii=False)))
open(os.path.join(ROOT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{u}</loc></url>" for u in urls)+"</urlset>\n")
open(os.path.join(ROOT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
open(os.path.join(ROOT,"ads.txt"),"w").write("# Ajouter ici la ligne fournie par Google AdSense, ex. : google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0\n")
print("ok", len(urls))
