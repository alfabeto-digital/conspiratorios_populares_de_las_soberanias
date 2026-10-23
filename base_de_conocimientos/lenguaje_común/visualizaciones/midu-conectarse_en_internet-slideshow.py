# -*- coding: utf-8 -*-
import lzstring, json, re, random, string, time, io, sys, glob
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
base=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
SRC=glob.glob(base+'/*/visualizaciones/midu-conectarse_en_internet.excalidraw.md')[0]
OUT=SRC.replace('.excalidraw.md','-slideshow.excalidraw.md')

content=open(SRC,encoding='utf-8').read()
fmap={fid:nm.split('/')[-1] for fid,nm in re.findall(r'^([0-9a-f]{40}): \[\[assets/image/attachments/(.+?)\.png\]\]',content,re.M)}
m=re.search(r'```compressed-json\n([\s\S]+?)\n```',content)
lz=lzstring.LZString()
data=json.loads(lz.decompressFromBase64(m.group(1).replace('\n','')))
scene=[e for e in data['elements'] if not e.get('isDeleted') and e['type']!='frame']
byid={e['id']:e for e in scene}
def rect(e): return (e['x'],e['y'],e['width'],e['height'])
def center(e): x,y,w,h=rect(e); return (x+w/2,y+h/2)
def iname(e): return fmap.get(e.get('fileId','')) if e['type']=='image' else None
def one(n):
    hits=[e['id'] for e in scene if iname(e)==n]; assert len(hits)==1,(n,len(hits)); return hits[0]
def txt(pred):
    hits=[e['id'] for e in scene if e['type']=='text' and pred(e.get('text',''))]; assert hits,'no text'; return hits[0]
abind={}
for e in scene:
    if e['type']=='arrow':
        s=e.get('startBinding',{}).get('elementId') if e.get('startBinding') else None
        t=e.get('endBinding',{}).get('elementId') if e.get('endBinding') else None
        abind[e['id']]=(s,t)
def arrow_between(a,b):
    for aid,(s,t) in abind.items():
        if {s,t}=={a,b}: return aid
    return None
def _is_green(hexc):
    h=(hexc or '').lstrip('#')
    if len(h)!=6: return False
    r,g,b=int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return g>r and g>=b
def green_arrow(a,b):
    cands=[aid for aid,(s,t) in abind.items() if {s,t}=={a,b}]
    for aid in cands:
        if _is_green(byid[aid].get('strokeColor','')): return aid
    return cands[0] if cands else None
def end_from(start_id):
    for aid,(s,t) in abind.items():
        if s==start_id and t in byid: return t
    return None
def dist(a,b): c1=center(byid[a]); c2=center(byid[b]); return (c1[0]-c2[0])**2+(c1[1]-c2[1])**2

# imágenes que SIEMPRE son un grupo junto con sus etiquetas: la flecha y el fade apuntan al grupo
CANON={'dns','vpn','cloud_server','cloudflare','domain_name','computer_local_server','router','switch'}
GROUP_PAIR={'isp_b','satellite'}   # isp_b y satellite se tratan como un grupo
def _innermost(e):
    g=e.get('groupIds',[])
    if not g: return None
    g0=g[0]
    mem=[m for m in scene if m.get('groupIds') and m['groupIds'][0]==g0]
    return mem if 2<=len(mem)<=6 else None
def group_unit(eid):
    # unidad de grupo canónica: imagen canónica (o etiqueta que comparte su grupo interno) -> grupo
    # completo imagen+etiquetas; cualquier otro elemento (antena, personas, dispositivos, isp) -> él solo
    e=byid.get(eid)
    if not e: return []
    nm=iname(e) if e['type']=='image' else None
    if nm in CANON or nm in GROUP_PAIR:
        mem=_innermost(e)
        if mem: return mem
    if e['type']=='text':
        mem=_innermost(e)
        if mem and any(iname(m) in CANON for m in mem if m['type']=='image'): return mem
    return [e]
def gu(eid): return [m['id'] for m in group_unit(eid)]
def _is_infra(i):
    # las imágenes de infraestructura humana no se revelan en los frames de personas
    e=byid.get(i); return bool(e) and e['type']=='image' and (iname(e) or '').startswith('infrastructure')

# --- resolver elementos del camino (escenario 1) ---
px=one('person_x'); pza=one('person_za'); laptop=one('computer_laptop'); smartphone=one('smartphone')
isp_a=one('isp_a'); glob=one('global_network'); isp_c=one('isp_c'); cloud=one('cloud_server'); cf=one('cloudflare')
infra2=one('infrastructure_2')               # infraestructura humana junto a las personas
arr_dev_laptop=arrow_between(infra2,laptop)   # flecha persona↔laptop (lado emisor)
arr_dev_smart=arrow_between(infra2,smartphone)# flecha persona↔smartphone (lado receptor)
assert arr_dev_laptop and arr_dev_smart,(arr_dev_laptop,arr_dev_smart)
sw_x=end_from(laptop)              # switch del laptop (binding)
assert byid[sw_x] and iname(byid[sw_x])=='switch', sw_x
sw_x_groups=set(byid[sw_x].get('groupIds',[]))
rt_x=[e['id'] for e in scene if iname(e)=='router' and set(e.get('groupIds',[]))&sw_x_groups][0]
ant=end_from(smartphone)           # antena del smartphone (binding)
assert iname(byid[ant])=='antenna', ant
vpns=[e['id'] for e in scene if iname(e)=='vpn']
vpn=min(vpns,key=lambda v:dist(v,sw_x))   # vpn del túnel inferior (más cerca del laptop/antena)
vpn_groups=set(byid[vpn].get('groupIds',[]))
tun=[e['id'] for e in scene if e['type']=='text' and 'Túnel' in e.get('text','') and set(e.get('groupIds',[]))&vpn_groups][0]
lbl_conocido=txt(lambda t:'conocido' in t and 'desconocidos' not in t)
lbl_vps=txt(lambda t:'Servidor virtual privado' in t)
lbl_rutaAB=txt(lambda t:'ruta A/B' in t)
lbl_zt=txt(lambda t:'ZeroTrust' in t)
lbl_rutaC=txt(lambda t:'ruta C' in t)

# --- actores indispensables (lado de internet): dns + domain_name + centros de datos ---
dc_all={e['id'] for e in scene if iname(e)=='data_center'}
dns_i=[e['id'] for e in scene if iname(e)=='dns' and end_from(e['id']) in dc_all][0]  # dns del área de internet
domain=one('domain_name')
domain_dc=end_from(domain); dns_dc=end_from(dns_i)                 # centro de datos que sirve a cada uno
assert domain_dc in dc_all and dns_dc in dc_all,(domain_dc,dns_dc)
def _cluster_of(eid):
    g0=byid[eid].get('groupIds',[None])[0]
    return [e['id'] for e in scene if iname(e)=='data_center' and e.get('groupIds',[None])[0]==g0]
dc_cluster=_cluster_of(domain_dc)                                  # grupo de 4 centros de datos
assert len(dc_cluster)==4 and dns_dc in dc_cluster,(len(dc_cluster),dns_dc in dc_cluster)
domain_lbl=[m['id'] for m in group_unit(domain) if m['type']=='text'][0]
dns_lbl=[m['id'] for m in group_unit(dns_i) if m['type']=='text'][0]
a_g_dom=arrow_between(glob,domain_lbl); a_g_dns=arrow_between(glob,dns_lbl)  # global↔dns/domain
assert a_g_dom and a_g_dns,(a_g_dom,a_g_dns)

# --- midu core (red local soberana): stack superior + dns local + túnel + servidor + memorias ---
def _g0(e): return (e.get('groupIds') or [None])[0]
dns_m=[e['id'] for e in scene if iname(e)=='dns' and e['id']!=dns_i][0]        # dns local (no el de internet)
switch_m=end_from(dns_m); assert iname(byid[switch_m])=='switch',switch_m      # switch que recibe del dns local
sm_g=_g0(byid[switch_m])
router_m=[e['id'] for e in scene if iname(e)=='router' and _g0(byid[e['id']])==sm_g][0]
vpn_m=[v for v in vpns if v!=vpn][0]                                           # túnel superior (del midu)
ls=one('computer_local_server'); mem_img=one('memory')
mem_g=_g0(byid[mem_img]); memorias=[e['id'] for e in scene if _g0(e)==mem_g]   # grupo de memorias (imgs+etiquetas+flechas)
def _contains(box,eid):
    b=byid[box]; cx,cy=center(byid[eid]); return b['x']<=cx<=b['x']+b['width'] and b['y']<=cy<=b['y']+b['height']
box_m=[e['id'] for e in scene if e['type']=='rectangle' and e.get('strokeStyle')=='dotted' and e['width']<300 and _contains(e['id'],switch_m)][0]
a_ls_dns=arrow_between(ls,dns_m); a_ls_mem=arrow_between(ls,mem_img); a_sw_isp=arrow_between(switch_m,isp_a)
assert a_ls_dns and a_ls_mem and a_sw_isp,(a_ls_dns,a_ls_mem,a_sw_isp)
et=one('electric_tower'); a_et_ls=arrow_between(et,ls); a_dns_sw=arrow_between(dns_m,switch_m)
assert a_et_ls and a_dns_sw,(a_et_ls,a_dns_sw)

# --- data centers + energía detrás de los servidores (VPS + Cloudflare) ---
def _img_target(src,name):
    for aid,(s,t) in abind.items():
        if s==src and t in byid and iname(byid[t])==name: return t
    return None
dc_srv=_img_target(cloud,'data_center')                 # data center de cloud/cloudflare
srv_cluster=_cluster_of(dc_srv)                          # grupo de 4 data centers
fossil=one('fossil_fuel'); solar=one('solar_energy')
dc_fossil=_img_target(fossil,'data_center')              # data center alimentado por combustible fósil
dc_solar=[s for aid,(s,t) in abind.items() if t==solar and s in byid and iname(byid[s])=='data_center'][0]
a_cloud_dc=arrow_between(cloud,dc_srv); a_cf_dc=arrow_between(cf,dc_srv)
a_fossil=arrow_between(fossil,dc_fossil); a_solar=arrow_between(dc_solar,solar)
assert all([dc_srv,len(srv_cluster)==4,dc_fossil,dc_solar,a_cloud_dc,a_cf_dc,a_fossil,a_solar]),'data centers/energía'

# --- actores públicos (servicios no soberanos): datacenter de un actor público ---
democracy=one('democracy'); lbl_publicos=txt(lambda t:'Actores públicos' in t)
dc_pub=_img_target(democracy,'data_center')                  # datacenter del actor público
a_dem_dc=arrow_between(democracy,dc_pub); a_dcpub_fossil=arrow_between(dc_pub,fossil)
red_ig=[aid for aid,(s,t) in abind.items() if {s,t}=={isp_a,glob} and not _is_green(byid[aid].get('strokeColor',''))][0]
isp_b=one('isp_b'); infantry=one('infantry'); rich=one('rich')   # isp_b conecta a los actores públicos
a_ispb_dem=arrow_between(isp_b,democracy); a_ispb_glob=arrow_between(isp_b,glob); a_dem_rich=arrow_between(democracy,rich)
assert all([democracy,dc_pub,a_dem_dc,a_dcpub_fossil,red_ig,isp_b,infantry,rich,a_ispb_dem,a_ispb_glob,a_dem_rich]),'actores públicos'

# --- plan de recorrido: (nombre, [nuevos a fade], [pares de flecha a fade], [extra cámara], [flechas explícitas]) ---
green_ig=green_arrow(isp_a,glob)   # conexión verde isp_a↔global (no la roja)
H=[
 ('01 · person_za',[pza],[],[],[]),
 ('02 · person_x',[px],[],[],[]),
 ('03 · person_za usa el laptop',[pza,laptop],[],[],[arr_dev_laptop]),
 ('04 · laptop → router + vpn + túnel + switch',[rt_x,vpn,sw_x],[(laptop,sw_x)],[laptop],[]),
 ('05 · → ISP "conocido" (isp_a)',[isp_a,lbl_conocido],[(sw_x,isp_a)],[sw_x],[]),
 ('06 · → internet (global, conexión verde) → isp_c',[glob,isp_c],[(glob,isp_c)],[],[green_ig]),
 ('08 · ruta A/B → servidor VPS',[cloud,lbl_rutaAB],[(cloud,isp_c)],[isp_c],[]),
 ('09 · ruta C → Cloudflare (ZeroTrust)',[cf,lbl_rutaC],[(cf,isp_c)],[isp_c],[]),
 ('10 · regreso: servidores + data centers + energía → isp_c',[cloud,cf,lbl_rutaAB,lbl_rutaC]+list(srv_cluster)+[fossil,solar],[(cloud,isp_c),(cf,isp_c)],[isp_c],[a_cloud_dc,a_cf_dc,a_fossil,a_solar]),
 ('11 · regreso: isp_c → global',[glob],[(glob,isp_c)],[isp_c],[]),
 ('12 · regreso: global → isp_a (verde)',[isp_a],[],[glob],[green_ig]),
 ('12.1 · isp + router + switch',[switch_m,router_m,isp_a],[(switch_m,isp_a)],[],[]),
 ('12.2 · router + switch + vpn + dns',[switch_m,router_m,vpn_m,dns_m],[(dns_m,switch_m)],[],[]),
 ('12.3 · dns + midu',[dns_m,ls],[(ls,dns_m)],[],[]),
 ('12.4 · midu + grupo de memorias + electric tower',[ls,et]+list(memorias),[(ls,mem_img),(et,ls)],[],[]),
 ('12.5 · midu + dns + vpn + switch + router',[ls,dns_m,vpn_m,switch_m,router_m],[(ls,dns_m)],[],[]),
 ('12.6 · → isp',[isp_a],[(switch_m,isp_a)],[switch_m,router_m,box_m],[]),
 ('13 · → antena (lado de person_x)',[ant],[(ant,isp_a)],[isp_a],[]),
 ('14 · → vpn + túnel + smartphone',[vpn,smartphone],[(smartphone,ant)],[ant],[]),
 ('15 · person_x recibe',[px,smartphone],[],[],[arr_dev_smart]),
]

# === grupo 2: servicios soberanos — ruta person_x <-> midu (vía VPS, ruta A/B) ===
H2=[
 # ida: person_x -> smartphone+vpn -> antena -> isp_a -> global -> isp_c -> VPS+data centers+solar
 ('SS 01 · person_x',[px],[],[],[]),
 ('SS 02 · person_x usa smartphone',[smartphone],[],[px],[arr_dev_smart]),
 ('SS 03 · → vpn + antena',[vpn,ant],[(smartphone,ant)],[smartphone],[]),
 ('SS 04 · → ISP "conocido" (isp_a)',[isp_a,lbl_conocido],[(ant,isp_a)],[ant],[]),
 ('SS 05 · → internet (global, conexión verde)',[glob],[],[isp_a],[green_ig]),
 ('SS 06 · → isp_c',[isp_c],[(glob,isp_c)],[glob],[]),
 ('SS 07 · ruta A/B + VPS + data centers + solar',[cloud,lbl_rutaAB]+list(srv_cluster)+[solar],[(cloud,isp_c)],[isp_c],[a_cloud_dc,a_solar]),
 # vuelta: isp_c -> global -> isp_a -> midu (red local soberana) -> person_x
 ('SS 08 · regreso: isp_c → global',[glob],[(glob,isp_c)],[isp_c],[]),
 ('SS 09 · regreso: global → isp_a (verde)',[isp_a],[],[glob],[green_ig]),
 ('SS 10 · isp + router + switch',[switch_m,router_m,isp_a],[(switch_m,isp_a)],[],[]),
 ('SS 11 · router + switch + vpn + dns',[switch_m,router_m,vpn_m,dns_m],[(dns_m,switch_m)],[],[]),
 ('SS 12 · dns + midu',[dns_m,ls],[(ls,dns_m)],[],[]),
 ('SS 13 · midu + grupo de memorias + electric tower',[ls,et]+list(memorias),[(ls,mem_img),(et,ls)],[],[]),
 ('SS 14 · midu + dns + vpn + switch + router',[ls,dns_m,vpn_m,switch_m,router_m],[(ls,dns_m)],[],[]),
 ('SS 15 · → isp',[isp_a],[(switch_m,isp_a)],[switch_m,router_m,box_m],[]),
 ('SS 16 · → antena (lado de person_x)',[ant],[(ant,isp_a)],[isp_a],[]),
 ('SS 17 · → vpn + túnel + smartphone',[vpn,smartphone],[(smartphone,ant)],[ant],[]),
 ('SS 18 · person_x recibe',[px,smartphone],[],[],[arr_dev_smart]),
]

# === grupo 3: servicios no soberanos (actores públicos y privados) — person_za ===
nube_lbl=txt(lambda t:'nube' in t)
satellite=one('satellite'); a_sat_glob=arrow_between(satellite,glob)   # flecha satellite↔global
lbl_privados=txt(lambda t:'Actores privados' in t); aws=one('aws')
dc_news=_cluster_of(_img_target(one('show'),'data_center'))    # cluster de show/fake_news/social (yqw51Y)
dc_aws=_cluster_of(_img_target(aws,'data_center'))             # cluster de aws (SsPhX3)
dc_goog=_cluster_of(_img_target(one('google'),'data_center'))  # cluster de google (R4lQtO)
def arrows_within(ids):
    s=set(ids); return [a for a,(x,y) in abind.items() if x in s and y in s]
# conjuntos de elementos por frame de actores privados (isp_b incluido -> arrastra satellite y la flecha isp_b→actor)
_ovset=[isp_b,lbl_privados,one('news'),one('ai_cloud'),one('amazon'),one('google')]
_newsset=[isp_b,one('news'),rich,one('bug'),one('show'),one('social_network'),one('fake_news'),one('cryptobro'),one('hacker'),infantry]+list(dc_news)+[fossil]
_aiset=[isp_b,one('ai_cloud'),one('amazon'),aws,one('theft'),infantry]+list(dc_aws)+[fossil]
_googset=[isp_b,one('google'),infantry]+list(dc_goog)+[fossil]
priv_frames=[
 ('NS · actores privados (vista general)',_ovset,[],[],arrows_within(_ovset)),
 ('NS · actor privado: news + desinformación + daños',_newsset+[nube_lbl],[],[],arrows_within(_newsset)),
 ('NS · actores privados: ai_cloud + amazon',_aiset+[nube_lbl],[],[],arrows_within(_aiset)),
 ('NS · actor privado: google',_googset+[nube_lbl],[],[],arrows_within(_googset)),
]
_recap=[isp_b,lbl_publicos,democracy,rich,infantry,lbl_privados]+[one(x) for x in ('news','ai_cloud','amazon','google','theft','cryptobro','bug','hacker')]

H3=([
 # ida: person_za -> laptop -> red local -> isp_a -> global -> dns/datacenters -> isp_b+satellite -> actores
 ('NS 01 · person_za',[pza],[],[],[]),
 ('NS 02 · person_za usa el laptop',[pza,laptop],[],[],[arr_dev_laptop]),
 ('NS 03 · laptop → router + vpn + switch',[rt_x,vpn,sw_x],[(laptop,sw_x)],[laptop],[]),
 ('NS 04 · → isp_a',[isp_a],[(sw_x,isp_a)],[sw_x],[]),
 ('NS 05 · → internet (global, conexión verde)',[glob],[],[isp_a],[green_ig]),
 ('NS 05b · global → isp_c',[glob,isp_c],[(glob,isp_c)],[],[]),
 ('NS 06 · → rutas A/B y C + data centers + fossil + solar + infantry',[cloud,lbl_rutaAB,cf,lbl_rutaC,infantry]+list(srv_cluster)+[fossil,solar],[(cloud,isp_c),(cf,isp_c)],[],[a_cloud_dc,a_cf_dc,a_fossil,a_solar]),
 # transición completa de vuelta por la midu antes de volver a global (roja)
 ('NS 06b · regreso: isp_c + global + isp_a',[isp_c,glob,isp_a],[(glob,isp_c)],[],[green_ig]),
 ('NS 06c · → isp_a + router + switch + vpn + dns',[isp_a,router_m,switch_m,vpn_m,dns_m],[(switch_m,isp_a),(dns_m,switch_m)],[],[]),
 ('NS 06d · → midu + memorias + tower',[ls,et]+list(memorias),[(ls,mem_img),(et,ls)],[],[]),
 ('NS 06e · → dns + vpn + isp_a',[dns_m,vpn_m,isp_a],[(dns_m,switch_m),(switch_m,isp_a)],[],[]),
 ('NS 06f · de nuevo a global network (conexión roja)',[glob],[],[],[red_ig]),
 ('NS 07 · → isp_b + satellite (conecta a los actores)',[isp_b],[(isp_b,glob)],[glob],[a_sat_glob]),
 ('NS 08 · → actores públicos: democracy + rich + infantry + datacenter + fossil + nube',[democracy,lbl_publicos,rich,infantry,dc_pub,fossil,nube_lbl],[(isp_b,democracy),(democracy,rich),(democracy,dc_pub),(dc_pub,fossil)],[isp_b],[]),
 ('NS 09 · regreso: actores públicos → isp_b',[isp_b,lbl_publicos],[(isp_b,democracy)],[democracy],[]),
 ]
 + priv_frames +
 [
 # recap de todo lo que cuelga de isp_b antes de salir
 ('NS · recap: isp_b + actores públicos + privados',_recap,[],[],arrows_within(_recap)),
 # vuelta: isp_b -> global -> (desvío isp_c + servidores) -> isp_a -> red local -> person_za
 ('NS 10 · regreso: isp_b → global',[glob],[(isp_b,glob)],[isp_b],[a_sat_glob]),
 ('NS 10b · regreso: global → isp_c',[glob,isp_c],[(glob,isp_c)],[],[]),
 ('NS 10c · isp_c + cloud + cloudflare + data centers + fossil + solar + infantry',[isp_c,cloud,lbl_rutaAB,cf,lbl_rutaC,infantry]+list(srv_cluster)+[fossil,solar],[(cloud,isp_c),(cf,isp_c)],[],[a_cloud_dc,a_cf_dc,a_fossil,a_solar]),
 ('NS 10d · regreso: isp_c → global',[glob,isp_c],[(glob,isp_c)],[],[]),
 ('NS 11 · regreso: global → isp_a (verde)',[isp_a],[],[glob],[green_ig]),
 ('NS 12 · regreso: isp_a → switch + router',[sw_x,rt_x],[(sw_x,isp_a)],[isp_a],[]),
 ('NS 13 · regreso: switch → laptop + vpn',[laptop,vpn],[(laptop,sw_x)],[sw_x],[]),
 ('NS 14 · person_za recibe',[pza,laptop],[],[],[arr_dev_laptop]),
])

# === grupo 4: fuera de la red — person_ñ (smartphone_apps + antena propia) ===
pn=one('person_ñ'); sm_n=one('smartphone_apps'); ant_n=[e['id'] for e in scene if iname(e)=='antenna' and e['id']!=ant][0]
box_n=[e['id'] for e in scene if e['type']=='rectangle' and e.get('strokeStyle')=='dotted' and e['width']<300 and _contains(e['id'],sm_n)][0]
a_pn_box=arrow_between(pn,box_n)        # person_ñ → smartphone (vía su recuadro)
a_ant_box=arrow_between(ant_n,box_n)    # antena ↔ smartphone (vía recuadro)
a_ant_isp=arrow_between(ant_n,lbl_conocido)  # antena → isp_a (vía etiqueta "conocido")
assert all([box_n,a_pn_box,a_ant_box,a_ant_isp]),'flechas person_ñ'
all_dc=[e['id'] for e in scene if iname(e)=='data_center']
pub_actors=[democracy,rich,infantry]
priv_actors=[one(x) for x in ('news','ai_cloud','amazon','google','aws','show','fake_news','social_network','bug','cryptobro','hacker','theft')]
_fr07=pub_actors+[dc_pub,lbl_publicos]+priv_actors+[lbl_privados]+[i for i in all_dc if i not in set(srv_cluster)]+[fossil,nube_lbl]
midu_super_g=(byid[vpn_m].get('groupIds') or [None])[-1]           # grupo envolvente de toda la midu
midu_super=[e['id'] for e in scene if midu_super_g in (e.get('groupIds') or [])]
H4=[
 ('FR 01 · person_ñ',[pn],[],[],[]),
 ('FR 02 · person_ñ usa el smartphone',[sm_n],[],[pn],[a_pn_box]),
 ('FR 03 · → antena + smartphone',[ant_n,sm_n],[],[],[a_ant_box]),
 ('FR 04 · → antena + isp_a + global network (roja)',[isp_a,glob,ant_n],[],[],[a_ant_isp,red_ig]),
 ('FR 05 · → dns + domain_name + datacenters',[domain,dns_i]+list(dc_cluster),[(domain,domain_dc),(dns_i,dns_dc)],[glob],[a_g_dom,a_g_dns]),
 ('FR 06 · → global + isp_b + satellite',[isp_b],[(isp_b,glob)],[glob],[a_sat_glob]),
 ('FR 07 · → todos los actores públicos y privados hasta fossil fuel',_fr07,[],[],arrows_within(_fr07)),
 ('FR 08 · isp_b + satellite + global + actores públicos/privados + proveedores desconocidos + isp_c',[isp_b,glob,lbl_privados,lbl_publicos,txt(lambda t:'desconocidos' in t),one('news'),one('ai_cloud'),one('amazon'),one('google'),isp_c],[(isp_b,glob),(isp_b,democracy),(isp_b,one('news')),(isp_b,one('ai_cloud')),(isp_b,one('amazon')),(isp_b,one('google')),(glob,isp_c)],[],[a_sat_glob]),
 ('FR 09 · → ruta A/B + C + datacenters + infantry + fossil + solar',[cloud,lbl_rutaAB,cf,lbl_rutaC,infantry]+list(srv_cluster)+[fossil,solar],[],[],[a_cloud_dc,a_cf_dc,a_fossil,a_solar]),
 ('FR 10 · isp_c + global + isp_a (flecha verde)',[isp_c,glob,isp_a],[(isp_c,glob)],[],[green_ig]),
 ('FR 11 · → switch + router + vpn + dns',[switch_m,router_m,vpn_m,dns_m],[(dns_m,switch_m),(switch_m,isp_a)],[isp_a],[]),
 ('FR 12 · → todo el grupo de la midu',midu_super,[],[],arrows_within(midu_super)),
 ('FR 13 · midu (local_server + etiquetas)',[ls],[],[],[]),
 ('FR 14 · → dns + vpn + switch + router + isp_a',[dns_m,vpn_m,switch_m,router_m,isp_a],[(dns_m,switch_m),(switch_m,isp_a)],[],[]),
 ('FR 15 · → antena',[ant_n],[],[isp_a],[a_ant_isp]),
 ('FR 16 · → antena + smartphone',[sm_n],[],[ant_n],[a_ant_box]),
 ('FR 17 · → smartphone + person_ñ',[pn],[],[sm_n],[a_pn_box]),
]

def nid(n=21): return ''.join(random.choice(string.ascii_letters+string.digits+'-_') for _ in range(n))
def fstep(ids,dur): return {'id':nid(10),'targets':[{'type':'element','id':i} for i in ids],'effect':'fade','trigger':'after-delay','delayMs':200,'durationMs':dur}
def extent(e):
    # extensión real: las flechas guardan puntos relativos que pueden ir en negativo, así que
    # x+width / y+height no es la esquina inferior; se calcula desde los puntos
    if e['type']=='arrow' and e.get('points'):
        xs=[e['x']+p[0] for p in e['points']]; ys=[e['y']+p[1] for p in e['points']]
        return (min(xs),min(ys),max(xs),max(ys))
    return (e['x'],e['y'],e['x']+e['width'],e['y']+e['height'])
def bbox(ids,pad):
    exts=[extent(byid[i]) for i in ids]
    x0=min(q[0] for q in exts); y0=min(q[1] for q in exts)
    x1=max(q[2] for q in exts); y1=max(q[3] for q in exts)
    return (x0-pad,y0-pad,(x1-x0)+2*pad,(y1-y0)+2*pad)

def build_frames(plan):
    out=[]
    for name,newels,arrpairs,extra,exarrows in plan:
        fade=[]                                  # flecha(s) + unidades de grupo que une, funden juntas
        for e in newels: fade+=gu(e)
        arrows=[]
        for a,b in arrpairs:
            aid=arrow_between(a,b)
            if aid:
                arrows.append(aid); fade+=gu(a)+gu(b)
        for aid in exarrows:
            if not aid: continue
            arrows.append(aid)
            s,t=abind.get(aid,(None,None))
            for x in (s,t):
                if x: fade+=gu(x)
        fade=list(dict.fromkeys([i for i in fade if i in byid and not _is_infra(i) and i!=box_n]+arrows))
        cam=list(fade)                            # la cámara encuadra las unidades de grupo + el contexto
        for e in extra: cam+=gu(e)
        cam=list(dict.fromkeys([i for i in cam if i in byid]))
        r=bbox(cam,90)
        steps=[fstep(fade,600)] if fade else []
        out.append((name,r,steps))
    return out

frames_cs=build_frames(H); frames_ss=build_frames(H2); frames_ns=build_frames(H3); frames_fr=build_frames(H4)

# reveal de personas una por una (estilo soberana): el grupo 1 presenta a person_za y person_x,
# los demás grupos introducen a una sola persona, así que ya se revelan de a una
assert frames_cs[0][0].startswith('01 · person') and frames_cs[1][0].startswith('02 · person'),'intro de personas'
_lbl_infra2=txt(lambda t:'nfraestructura' in t)
_pp=sorted([pza,px],key=lambda i:byid[i]['x'])
_pcam=bbox(_pp+[infra2,_lbl_infra2],90)
_psteps=[fstep([i],600) for i in _pp]+[fstep([infra2,_lbl_infra2],600)]  # personas una por una, luego su infraestructura humana
frames_cs=[('01 · personas (una por una) + infraestructura humana',_pcam,_psteps)]+frames_cs[2:]

# apertura + título + dos secciones con su frame divisor (todos estáticos, sin fade)
ALLIDS=[e['id'] for e in scene]
banner=[e['id'] for e in scene if e['type']=='rectangle' and e.get('strokeStyle')=='solid'][0]
titulo=txt(lambda t:'Conectarse en internet' in t)
frames=([('00.1 · apertura — todos los elementos',bbox(ALLIDS,150),[]),
         ('00.2 · título — Conectarse en internet',bbox([banner,titulo],120),[]),
         ('— conexión soberana —',bbox(ALLIDS,150),[])]
        + frames_cs
        + [('— servicios soberanos —',bbox(ALLIDS,150),[])]
        + frames_ss
        + [('— servicios no soberanos (actores públicos y privados) —',bbox(ALLIDS,150),[])]
        + frames_ns
        + [('— fuera de la red —',bbox(ALLIDS,150),[])]
        + frames_fr
        + [('— cierre: todo el conjunto —',bbox(ALLIDS,150),[])])

base_idx=data['elements'][-1].get('index','a0')
ts=int(time.time()*1000)
for i,(name,r,steps) in enumerate(frames):
    x,y,w,h=r
    data['elements'].append({'id':nid(),'type':'frame','x':round(x,2),'y':round(y,2),'width':round(w,2),'height':round(h,2),
      'angle':0,'strokeColor':'#a89984','backgroundColor':'transparent','fillStyle':'solid','strokeWidth':1,
      'strokeStyle':'solid','roughness':0,'opacity':100,'groupIds':[],'frameId':None,'index':base_idx+f'{i:04d}',
      'roundness':None,'seed':random.randint(1,2**31),'version':1,'versionNonce':random.randint(1,2**31),
      'isDeleted':False,'boundElements':None,'updated':ts,'link':None,'locked':False,'name':name,
      'customData':{'slideshow':{'schemaVersion':2,'kind':'frame','order':i,**({'animation':{'steps':steps}} if steps else {})}}})

new=lz.compressToBase64(json.dumps(data,separators=(',',':'),ensure_ascii=False))
open(OUT,'w',encoding='utf-8').write(content[:m.start(1)]+new+content[m.end(1):])
print('resueltos: sw_x',sw_x[:6],'rt_x',rt_x[:6],'ant',ant[:6],'vpn',vpn[:6],'tun',tun[:6])
print(f'frames={len(frames)} | OUT={OUT.split(chr(92))[-1] if chr(92) in OUT else OUT.split("/")[-1]}')
# validación: orders únicos/completos, targets existentes, y volcado del fade por frame
def elab(i):
    e=byid.get(i)
    if not e: return '??'
    if e['type']=='image': return iname(e)
    if e['type']=='text': return 't:'+e.get('text','').replace(chr(10),' ')[:16]
    if e['type']=='arrow': return 'flecha'
    return e['type']
orders=[fr['customData']['slideshow']['order'] for fr in data['elements'] if fr['type']=='frame']
allids={e['id'] for e in data['elements']}
missing=0
for i,(name,r,steps) in enumerate(frames):
    tids=[t['id'] for s in steps for t in s['targets']]
    missing+=sum(1 for t in tids if t not in allids)
    print(f'  {i+1:2} {name}')
    if tids: print('       fade:',[elab(t) for t in tids])
print(f'orders únicos/completos={orders==list(range(len(frames)))} | targets rotos={missing}')
