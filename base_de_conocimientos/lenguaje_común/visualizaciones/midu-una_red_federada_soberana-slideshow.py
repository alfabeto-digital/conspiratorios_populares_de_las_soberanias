# -*- coding: utf-8 -*-
import lzstring, json, re, random, string, time, io, sys, glob
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os
base=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
SRC=glob.glob(base+'/*/visualizaciones/midu-una_red_federada_soberana.excalidraw.md')[0]
OUT=SRC.replace('.excalidraw.md','-slideshow.excalidraw.md')
content=open(SRC,encoding='utf-8').read()
fmap={fid:nm.split('/')[-1] for fid,nm in re.findall(r'^([0-9a-f]{40}): \[\[assets/image/attachments/(.+?)\.png\]\]',content,re.M)}
m=re.search(r'```compressed-json\n([\s\S]+?)\n```',content)
lz=lzstring.LZString()
data=json.loads(lz.decompressFromBase64(m.group(1).replace('\n','')))
scene=[e for e in data['elements'] if not e.get('isDeleted') and e['type']!='frame']
byid={e['id']:e for e in scene}
def iname(e): return fmap.get(e.get('fileId','')) if e['type']=='image' else None
def ctr(e): return (e['x']+e.get('width',0)/2, e['y']+e.get('height',0)/2)
def one(n):
    h=[e['id'] for e in scene if iname(e)==n]; assert len(h)==1,(n,len(h)); return h[0]
def txt(pred):
    h=[e['id'] for e in scene if e['type']=='text' and pred(e.get('text',''))]; assert h,'no text'; return h[0]
def img_at(n,x,y):
    cs=[(e['id'],(ctr(e)[0]-x)**2+(ctr(e)[1]-y)**2) for e in scene if iname(e)==n]; assert cs,n; return min(cs,key=lambda z:z[1])[0]
def txt_at(sub,x,y):
    cs=[(e['id'],(ctr(e)[0]-x)**2+(ctr(e)[1]-y)**2) for e in scene if e['type']=='text' and sub in e.get('text','')]; assert cs,sub; return min(cs,key=lambda z:z[1])[0]
groups=defaultdict(list)
for e in scene:
    for gi in (e.get('groupIds') or []): groups[gi].append(e['id'])
def members(gid): return groups.get(gid,[])
def grp_with(a,b):
    common=set(byid[a].get('groupIds',[]))&set(byid[b].get('groupIds',[]))
    return min(common,key=lambda g:len(members(g))) if common else None
def unit(eid):
    g=byid[eid].get('groupIds',[]); return members(g[0]) if g else [eid]
abind={e['id']:((e.get('startBinding') or {}).get('elementId'),(e.get('endBinding') or {}).get('elementId')) for e in scene if e['type']=='arrow'}

# --- título / banner ---
banner=[e['id'] for e in scene if e['type']=='rectangle' and e.get('strokeStyle')=='solid'][0]
titulo=txt(lambda t:'Una red federada soberana' in t)

# --- comunidades humanas (4 grupos) ---
G1=members(grp_with(one('person_j'),one('person_r')))   # l3Gg8C -> Node A
G2=members(grp_with(one('person_d'),one('person_f')))   # sSLxv1 -> Node C
G3=members(grp_with(one('person_v'),one('person_t')))   # VCwucH -> Node B
G4=members(grp_with(one('person_m'),one('person_l')))   # qobSpD -> cliente
# personas (solo iconos de persona, sin icono/etiqueta de infraestructura) para las intros de rutas
P1=[one('person_j'),one('person_z'),one('person_r'),one('person')]
P2=[one('person_d'),one('person_f'),one('person_s')]
P3=[one('person_v'),one('person_t'),one('person_y')]
P4=[one('person_m'),one('person_l')]

# --- dispositivos (computadores y teléfonos) ---
dev1=members(grp_with(one('computer_laptop'),one('smartphone')))        # Ih3kz
dev2=members(grp_with(one('computer_gaming'),one('smartphone_apps_a'))) # B8seJG
dev3=members(grp_with(one('smartphone_chat'),one('computer_desktop')))  # ITfHlN
dev4=members(grp_with(one('smartphone_simple'),one('computer_vintage')))# ye7Hks

# --- conectividad (enrutadores, antenas, túnel cifrado) ---
cn1=unit(img_at('router',-2522,-2486))+unit(img_at('vpn',-2281,-2400))                  # router+switch + túnel
cn2=unit(img_at('antenna',-1514,-3117))+unit(img_at('vpn',-1441,-2936))                 # antena+satélite + túnel
_ant3=img_at('antenna',-1264,-1421)                                                     # antena del grupo de person_t (suThS2)
cn3=members(byid[_ant3]['groupIds'][0])+unit(img_at('vpn',-1443,-1618))                 # router+switch+antena + túnel
cn4=[img_at('antenna',-128,-2213)]+unit(img_at('vpn',-417,-2265))                       # antena + túnel

# --- midus (nodos servidor) ---
nodeA=members(grp_with(one('computer_local_server_a'),one('renewable_energy')))  # mNAZTn (morado, IA)
nodeB=members(grp_with(one('computer_local_server_b'),one('solar_energy')))      # tIRq-3 (azul)
scC=one('computer_local_server'); nodeC=list(members(byid[scC]['groupIds'][0]))  # 4tvGT3 + sueltos
nodeC+=[one('electric_tower'),img_at('memory',-395,-3102),img_at('external_hard_drive',-510,-2970),img_at('digital_brain',-348,-2940)]
nodeC+=[txt_at('Datos locales',13,-3102),txt_at('Memorias',-21,-2940),txt_at('Discos Duros',2,-2779)]
def midu_lbl(nodeids): return [i for i in nodeids if byid[i]['type']=='text' and byid[i].get('text','').strip()=='midu']
def serv_lbl(nodeids): return [i for i in nodeids if byid[i]['type']=='text' and 'Servicios' in byid[i].get('text','')]
miduA=[one('computer_local_server_a')]+midu_lbl(nodeA)+serv_lbl(nodeA)  # servidor + midu + servicios soberanos
miduB=[one('computer_local_server_b')]+midu_lbl(nodeB)
gcard=one('graphic_card')  # IA (nodo A)

# --- centro soberano (registros colectivos + dns soberano + memorias colectivas + sistemas soberanos) ---
glb=one('global_network')
dom=one('domain_name'); domlbl=txt(lambda t:'Registros de dominios' in t)
dns=one('dns'); dnslbl=txt(lambda t:'Sistemas de nombres' in t)
memcol=one('memorias_colectivas'); memcollbl=txt(lambda t:'Memorias colectivas' in t)
infosys=one('information_system'); infolbl=txt(lambda t:'informaci' in t and 'soberanos' in t)
qtext=txt(lambda t:'Qu' in t and 'internet' in t)
boxZ=[e['id'] for e in scene if e['type']=='rectangle' and e.get('strokeColor')=='#1e1e1e'][0]
R_center=[glb,dom,domlbl,dns,dnslbl,memcol,memcollbl,infosys,infolbl,qtext,boxZ]

# --- regiones de acceso (lado humano) y de grupo completo ---
A1=G1+dev1+cn1; A2=G2+dev2+cn2; A3=G3+dev3+cn3; A4=G4+dev4+cn4
RG1=A1+nodeA; RG2=A2+nodeC; RG3=A3+nodeB; RG4=A4

def nid(n=21): return ''.join(random.choice(string.ascii_letters+string.digits+'-_') for _ in range(n))
def fstep(ids,dur=600): return {'id':nid(10),'targets':[{'type':'element','id':i} for i in ids],'effect':'fade','trigger':'after-delay','delayMs':200,'durationMs':dur}
ALLIDS=[e['id'] for e in scene]
def extent(e):
    if e['type']=='arrow' and e.get('points'):
        xs=[e['x']+p[0] for p in e['points']]; ys=[e['y']+p[1] for p in e['points']]
        return (min(xs),min(ys),max(xs),max(ys))
    return (e['x'],e['y'],e['x']+e.get('width',0),e['y']+e.get('height',0))
def bbox(ids,pad):
    exts=[extent(byid[i]) for i in ids if i in byid]
    x0=min(q[0] for q in exts); y0=min(q[1] for q in exts); x1=max(q[2] for q in exts); y1=max(q[3] for q in exts)
    return (x0-pad,y0-pad,(x1-x0)+2*pad,(y1-y0)+2*pad)
def arrs(ids):
    s=set(ids); return [a for a,(x,y) in abind.items() if x in s and y in s]
def F(name,ids,pad=90):
    ids=list(dict.fromkeys([i for i in ids if i in byid])); ids=ids+[a for a in arrs(ids) if a not in ids]
    return (name,bbox(ids,pad),[fstep(ids)])
def Fstatic(name,ids,pad=130): return (name,bbox(ids,pad),[])
def Ffull(name,ids):
    ids=list(dict.fromkeys([i for i in ids if i in byid])); ids=ids+[a for a in arrs(ids) if a not in ids]
    return (name,bbox(ALLIDS,130),[fstep(ids,300)])
def Fzoom(name,ids,pad=60):
    ids=list(dict.fromkeys([i for i in ids if i in byid])); ids=ids+[a for a in arrs(ids) if a not in ids]
    return (name,bbox(ids,pad),[fstep(ids,300)])
def Fseq(name,G,pad=80):  # presentación: revela las personas una por una, luego su infraestructura humana
    ps=sorted([i for i in G if (iname(byid[i]) or '').startswith('person')],key=lambda i:byid[i]['x'])
    rest=[i for i in G if i not in ps]
    cam=list(dict.fromkeys(G)); cam=cam+[a for a in arrs(cam) if a not in cam]
    steps=[fstep([i]) for i in ps]
    if rest: steps.append(fstep(rest))
    return (name,bbox(cam,pad),steps)

frames=[]
frames.append(Fstatic('00.1 · apertura — todos los elementos',ALLIDS))
frames.append(Fstatic('00.2 · título — Una red federada soberana',[banner,titulo],120))

# ===== GRUPO 1 (comunidad l3Gg8C -> nodo A: energía renovable + IA, morado) =====
frames.append(Fseq('G1.1 · personas (una por una)',G1,80))
frames.append(F('G1.2 · computadores y teléfonos',dev1,80))
frames.append(F('G1.3 · enrutadores y túnel cifrado',cn1,80))
frames.append(F('G1.4 · midu (energía renovable + IA)',nodeA,90))
frames.append(F('G1.5 · paneo: grupo completo',RG1))

# ===== GRUPO 2 (comunidad sSLxv1 -> nodo C: torre eléctrica + satélite, rosa) =====
frames.append(Fseq('G2.1 · personas (una por una)',G2,80))
frames.append(F('G2.2 · computadores y teléfonos',dev2,80))
frames.append(F('G2.3 · antena, satélite y túnel cifrado',cn2,80))
frames.append(F('G2.4 · midu (torre eléctrica + satélite)',nodeC,90))
frames.append(F('G2.5 · paneo: grupo completo',RG2))

# ===== GRUPO 3 (comunidad VCwucH -> nodo B: energía solar, azul) =====
frames.append(Fseq('G3.1 · personas (una por una)',G3,80))
frames.append(F('G3.2 · computadores y teléfonos',dev3,80))
frames.append(F('G3.3 · enrutadores, antena y túnel cifrado',cn3,80))
frames.append(F('G3.4 · midu (energía solar)',nodeB,90))
frames.append(F('G3.5 · paneo: grupo completo',RG3))

# ===== GRUPO 4 (comunidad qobSpD -> cliente sin midu, verde) =====
frames.append(Fseq('G4.1 · personas (una por una)',G4,80))
frames.append(F('G4.2 · computadores y teléfonos',dev4,80))
frames.append(F('G4.3 · antena y túnel cifrado',cn4,80))
frames.append(F('G4.4 · paneo: grupo completo',RG4))

# ===== SERIE DE RUTAS (conexiones directas, sin centro) =====
# cada conexión: personas (solo personas) -> personas/midu del segundo grupo -> los dos grupos funden en el paneo
frames.append(Fstatic('— rutas: conexiones directas —',ALLIDS))
# 1 · servicio en la midu PROPIA (grupo 1) — acceso local soberano
frames.append(Fzoom('R1.0a · conecta: personas (grupo 1)',P1))
frames.append(Fzoom('R1.0b · con: su propia midu (nodo A)',miduA))
frames.append(Ffull('R1.1 · paneo: grupo 1 (conexión local directa)',RG1))
# 2 · conexión directa entre infraestructuras (grupo 1 <-> grupo 3)
frames.append(Fzoom('R2.0a · conecta: personas (grupo 1)',P1))
frames.append(Fzoom('R2.0b · con: personas (grupo 3)',P3))
frames.append(Ffull('R2.1 · paneo: grupos 1 y 3 funden (conexión directa)',RG1+RG3))
# 3 · conexión directa entre infraestructuras (grupo 2 <-> grupo 3)
frames.append(Fzoom('R3.0a · conecta: personas (grupo 2)',P2))
frames.append(Fzoom('R3.0b · con: personas (grupo 3)',P3))
frames.append(Ffull('R3.1 · paneo: grupos 2 y 3 funden (conexión directa)',RG2+RG3))
# 4 · cliente (grupo 4, sin midu) <-> IA de la midu del grupo 1
frames.append(Fzoom('R4.0a · conecta: personas (grupo 4)',P4))
frames.append(Fzoom('R4.0b · con: IA de la midu (nodo A)',miduA+[gcard]))
frames.append(Ffull('R4.1 · paneo: grupo 4 y nodo A funden (conexión directa)',RG4+nodeA))

# ===== CENTRO SOBERANO (presentado después de las rutas) =====
frames.append(Fstatic('— el centro soberano —',R_center))
frames.append(F('C.1 · red soberana (¿qué puede llegar a ser la internet?)',[glb,qtext,boxZ],90))
frames.append(F('C.2 · registros de dominios colectivo',[dom,domlbl],80))
frames.append(F('C.3 · sistemas de nombres de dominios',[dns,dnslbl],80))
frames.append(F('C.4 · memorias colectivas',[memcol,memcollbl],80))
frames.append(F('C.5 · sistemas de información soberanos',[infosys,infolbl],80))
frames.append(F('C.6 · paneo: centro soberano completo',R_center))

frames.append(Fstatic('99.1 · cierre — todos los elementos',ALLIDS))

base_idx=data['elements'][-1].get('index','a0'); ts=int(time.time()*1000)
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
print(f'frames={len(frames)}')
print(f'G1={len(G1)} G2={len(G2)} G3={len(G3)} G4={len(G4)} | nodeA={len(nodeA)} nodeB={len(nodeB)} nodeC={len(nodeC)} | R_center={len(R_center)}')
print(f'cn1={len(cn1)} cn2={len(cn2)} cn3={len(cn3)} cn4={len(cn4)} | dev1={len(dev1)} dev2={len(dev2)} dev3={len(dev3)} dev4={len(dev4)}')
for i,(name,r,steps) in enumerate(frames): print(f'  {i+1:2} {name}')
