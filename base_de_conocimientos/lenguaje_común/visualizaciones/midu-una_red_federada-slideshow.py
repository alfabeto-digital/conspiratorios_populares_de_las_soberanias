# -*- coding: utf-8 -*-
import lzstring, json, re, random, string, time, io, sys, glob
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os
base=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
SRC=glob.glob(base+'/*/visualizaciones/midu-una_red_federada.excalidraw.md')[0]
OUT=SRC.replace('.excalidraw.md','-slideshow.excalidraw.md')
content=open(SRC,encoding='utf-8').read()
fmap={fid:nm.split('/')[-1] for fid,nm in re.findall(r'^([0-9a-f]{40}): \[\[assets/image/attachments/(.+?)\.png\]\]',content,re.M)}
m=re.search(r'```compressed-json\n([\s\S]+?)\n```',content)
lz=lzstring.LZString()
data=json.loads(lz.decompressFromBase64(m.group(1).replace('\n','')))
scene=[e for e in data['elements'] if not e.get('isDeleted') and e['type']!='frame']
byid={e['id']:e for e in scene}
def iname(e): return fmap.get(e.get('fileId','')) if e['type']=='image' else None
def ctr(e): return (e['x']+e['width']/2, e['y']+e['height']/2)
def one(n):
    h=[e['id'] for e in scene if iname(e)==n]; assert len(h)==1,(n,len(h)); return h[0]
def txt(pred):
    h=[e['id'] for e in scene if e['type']=='text' and pred(e.get('text',''))]; assert h,'no text'; return h[0]
def img_at(n,x,y):
    cs=[(e['id'],(ctr(e)[0]-x)**2+(ctr(e)[1]-y)**2) for e in scene if iname(e)==n]; assert cs,n; return min(cs,key=lambda z:z[1])[0]
groups=defaultdict(list)
for e in scene:
    for gi in (e.get('groupIds') or []): groups[gi].append(e['id'])
def members(gid): return groups.get(gid,[])
def grp_with(a,b):
    common=set(byid[a].get('groupIds',[]))&set(byid[b].get('groupIds',[]))
    return min(common,key=lambda g:len(members(g))) if common else None
def gcenter(ids):
    xs=[byid[i]['x']+byid[i]['width']/2 for i in ids]; ys=[byid[i]['y']+byid[i]['height']/2 for i in ids]
    return (sum(xs)/len(xs),sum(ys)/len(ys))
def conn_unit(x,y):  # grupo con vpn+router+switch cuyo centro esté más cerca de (x,y)
    best=None; bd=1e18
    for gi,ids in groups.items():
        nms={iname(byid[i]) for i in ids if byid[i]['type']=='image'}
        if {'vpn','router','switch'}<=nms:
            cx,cy=gcenter(ids); dd=(cx-x)**2+(cy-y)**2
            if dd<bd: bd=dd; best=ids
    return list(best)
abind={e['id']:((e.get('startBinding') or {}).get('elementId'),(e.get('endBinding') or {}).get('elementId')) for e in scene if e['type']=='arrow'}

# --- título / banner ---
banner=[e['id'] for e in scene if e['type']=='rectangle' and e.get('strokeStyle')=='solid'][0]
titulo=txt(lambda t:'Una red federada' in t)

# --- personas / grupos humanos ---
pq=one('person_q'); pw=one('person_w'); po=one('person_o'); pp=one('person_p')
pg=one('person_g'); pk=one('person_k'); pn=one('person_n'); pu=one('person_u')
hg1=members(grp_with(pq,pw)); hg2=members(grp_with(po,pp)); hg3=members(grp_with(pg,pu))
# --- grupos servidor ---
ls_b=one('computer_local_server_b'); gen=one('generator')
ls_a=one('computer_local_server_a'); etw=one('electric_tower')
sgL=grp_with(ls_b,gen); sgR=grp_with(ls_a,etw)
SL=members(sgL); SR=members(sgR)
def server_core(gid):  # grupo servidor sin dns ni su etiqueta
    out=[]
    for i in members(gid):
        e=byid[i]
        if iname(e)=='dns': continue
        if e['type']=='text' and 'Sistema de nombres' in e.get('text',''): continue
        out.append(i)
    return out
coreL=server_core(sgL); coreR=server_core(sgR)
# --- dispositivos ---
laptop=one('computer_laptop'); sm1=one('smartphone')
cgd=one('computer_graphic_design'); sch=one('smartphone_chat')
cso=one('computer_shopping_online'); smd=one('smartphone_development')
# --- isps ---
isp_a=one('isp_a'); isp_b=one('isp_b'); isp_c=one('isp_c')
def isp_grp(i):  # isp_a+etiqueta y isp_b+satellite son grupos conjuntos
    g=byid[i].get('groupIds',[]); return members(g[0]) if g else [i]
ispA=isp_grp(isp_a); ispB=isp_grp(isp_b); ispC=isp_grp(isp_c)
def no_antenna(unit): return [i for i in unit if iname(byid[i])!='antenna']
# --- unidades de conectividad (vpn+router+switch(+antena)) por posición ---
cnL_dev=conn_unit(4230,-3200)   # izquierda, camino de dispositivos
cnL_srv=conn_unit(4199,-4010)   # izquierda, camino del servidor (par extra)
cnR2=conn_unit(6821,-2790)      # derecha-abajo (grupo 2)
cnR3=conn_unit(7236,-4937)      # derecha-arriba (grupo 3)
_rects=[e['id'] for e in scene if e['type']=='rectangle']
box_g3=min(_rects,key=lambda i:(byid[i]['x']+byid[i]['width']/2-7341)**2+(byid[i]['y']+byid[i]['height']/2+4922)**2)  # recuadro enrutadores/antenas -> isp_b

def nid(n=21): return ''.join(random.choice(string.ascii_letters+string.digits+'-_') for _ in range(n))
def fstep(ids,dur=600): return {'id':nid(10),'targets':[{'type':'element','id':i} for i in ids],'effect':'fade','trigger':'after-delay','delayMs':200,'durationMs':dur}
ALLIDS=[e['id'] for e in scene]
def extent(e):  # extensión real: las flechas guardan puntos relativos que pueden ir en negativo
    if e['type']=='arrow' and e.get('points'):
        xs=[e['x']+p[0] for p in e['points']]; ys=[e['y']+p[1] for p in e['points']]
        return (min(xs),min(ys),max(xs),max(ys))
    return (e['x'],e['y'],e['x']+e['width'],e['y']+e['height'])
def bbox(ids,pad):
    exts=[extent(byid[i]) for i in ids if i in byid]
    x0=min(q[0] for q in exts); y0=min(q[1] for q in exts); x1=max(q[2] for q in exts); y1=max(q[3] for q in exts)
    return (x0-pad,y0-pad,(x1-x0)+2*pad,(y1-y0)+2*pad)
def arrs(ids):  # todas las flechas cuyos dos extremos estén en el conjunto
    s=set(ids); return [a for a,(x,y) in abind.items() if x in s and y in s]
def F(name,ids,pad=90):
    ids=list(dict.fromkeys([i for i in ids if i in byid]))
    ids=ids+[a for a in arrs(ids) if a not in ids]
    return (name,bbox(ids,pad),[fstep(ids)])
def Fstatic(name,ids,pad=130): return (name,bbox(ids,pad),[])
def Ffull(name,ids):  # cámara fija sobre todo el diagrama; solo fade in (rápido) de la región
    ids=list(dict.fromkeys([i for i in ids if i in byid]))
    ids=ids+[a for a in arrs(ids) if a not in ids]
    return (name,bbox(ALLIDS,130),[fstep(ids,300)])
def Fzoom(name,ids,pad=60):  # intro: zoom al sujeto (quién conecta), fade rápido
    ids=list(dict.fromkeys([i for i in ids if i in byid]))
    ids=ids+[a for a in arrs(ids) if a not in ids]
    return (name,bbox(ids,pad),[fstep(ids,300)])
def Fseq(name,G,pad=80):  # presentación: revela las personas una por una, luego su infraestructura humana
    ps=sorted([i for i in G if (iname(byid[i]) or '').startswith('person')],key=lambda i:byid[i]['x'])
    rest=[i for i in G if i not in ps]
    cam=list(dict.fromkeys(G)); cam=cam+[a for a in arrs(cam) if a not in cam]
    steps=[fstep([i]) for i in ps]
    if rest: steps.append(fstep(rest))
    return (name,bbox(cam,pad),steps)

# --- partes de cada nodo servidor (midu ancla / memorias / energía / IA) ---
def node(gid,power_name,ai=False):
    ms=members(gid)
    def pick(cond): return [i for i in ms if cond(byid[i])]
    ls=pick(lambda e:iname(e) in ('computer_local_server_a','computer_local_server_b'))[0]
    lblmidu=pick(lambda e:e['type']=='text' and e.get('text','').strip()=='midu')[0]
    lblserv=pick(lambda e:e['type']=='text' and 'Servicios' in e.get('text',''))[0]
    memimg=pick(lambda e:iname(e) in ('memory','digital_brain','external_hard_drive'))
    memlbl=pick(lambda e:e['type']=='text' and any(k in e.get('text','') for k in ('Datos locales','Memorias','Discos Duros')))
    d=dict(midu=[ls,lblmidu,lblserv],mem=memimg+memlbl,power=pick(lambda e:iname(e)==power_name)[0])
    if ai:
        d['gcard']=pick(lambda e:iname(e)=='graphic_card')[0]
        d['gcardlbl']=pick(lambda e:e['type']=='text' and 'Tarjeta' in e.get('text',''))[0]
    return d
NL=node(sgL,'generator'); NR=node(sgR,'electric_tower',ai=True)
def vpn_only(unit): return [i for i in unit if iname(byid[i]) not in ('router','switch','antenna')]
# --- elementos para la serie de rutas (tráfico IP real) ---
dns_C=img_at('dns',6306,-4016); domain=one('domain_name'); cloud=one('cloud_server'); cf=one('cloudflare')
lblDnsC=txt(lambda t:'Sistemas de nombres' in t); lblDom=txt(lambda t:'Registradores' in t)
lblZT=txt(lambda t:'ZeroTrust' in t); lblRutaC=txt(lambda t:'ruta C' in t)
dnsL_b=[i for i in members(sgL) if iname(byid[i])=='dns'][0]
dnsLb_lbl=[i for i in members(sgL) if byid[i]['type']=='text' and 'Sistema de nombres' in byid[i].get('text','')][0]
vpn1=[i for i in cnL_srv if iname(byid[i])=='vpn'][0]; vpn2=[i for i in cnR2 if iname(byid[i])=='vpn'][0]
midu1=NL['midu']; midu2=NR['midu']; gcard=NR['gcard']; gcardlbl=NR['gcardlbl']
dnsC_set=[dns_C,lblDnsC,domain,lblDom]; cf_set=[cf,lblZT,lblRutaC]
lblVPS=txt(lambda t:'Servidor virtual' in t); lblRutaAB=txt(lambda t:'ruta A/B' in t)
# --- REGIONES (conjuntos exactos de los frames zoom-out 6/10/14/19/25 + el centro) ---
R_center=[glob,domain,lblDom,cloud,lblVPS,lblRutaAB,cf,lblZT,lblRutaC]  # domain+cloud+cloudflare (sin dns: nunca se activa)
R6=hg1+[laptop,sm1]+cnL_dev+ispA            # grupo 1: personas + dispositivos + isp
R10=SL+cnL_srv+ispA                          # grupo 1: midu (servidor)
R14=hg2+[sch,cgd]+cnR2+ispC                  # grupo 2: personas + dispositivos + isp
R19=SR+no_antenna(cnR2)+ispC                 # grupo 2: midu (servidor + IA)
R25=hg3+[cso,smd]+cnR3+[box_g3]+ispB         # grupo 3 (cliente)

frames=[]
frames.append(Fstatic('00.1 · apertura — todos los elementos',ALLIDS))
frames.append(Fstatic('00.2 · título — Una red federada',[banner,titulo],120))

# ===== GRUPO 1 (izquierda, servidor local_server_b + generator, isp_a) =====
frames.append(Fseq('G1.1 · personas (una por una) + infraestructura humana',hg1,80))
frames.append(F('G1.4 · zoom out: grupo + dispositivos + isp',hg1+[laptop,sm1]+cnL_dev+ispA))
frames.append(F('G1.5 · midu',NL['midu'],80))
frames.append(F('G1.6 · midu + memorias',NL['midu']+NL['mem'],80))
frames.append(F('G1.7 · midu + generador',NL['midu']+[NL['power']],80))
frames.append(F('G1.8 · zoom out: midu + dns + vpn + switch + router + isp',SL+cnL_srv+ispA))

# ===== GRUPO 2 (derecha-abajo, servidor local_server_a + IA, isp_c) =====
frames.append(Fseq('G2.1 · personas (una por una) + infraestructura humana',hg2,80))
frames.append(F('G2.4 · zoom out: grupo + dispositivos + isp',hg2+[sch,cgd]+cnR2+ispC))
frames.append(F('G2.5 · midu',NR['midu'],80))
frames.append(F('G2.6 · midu + tarjeta gráfica (IA)',NR['midu']+[NR['gcard'],NR['gcardlbl']],80))
frames.append(F('G2.7 · midu + memorias',NR['midu']+NR['mem'],80))
frames.append(F('G2.8 · midu + torre eléctrica',NR['midu']+[NR['power']],80))
frames.append(F('G2.9 · zoom out: midu + dns + vpn + switch + router + isp',SR+no_antenna(cnR2)+ispC))

# ===== GRUPO 3 (derecha-arriba, cliente sin servidor, isp_b) =====
frames.append(Fseq('G3.1 · personas (una por una) + infraestructura humana',hg3,80))
frames.append(F('G3.6 · zoom out: grupo + dispositivos + isp',hg3+[cso,smd]+cnR3+[box_g3]+ispB))

# ===== SERIE DE RUTAS (tráfico IP real) =====
frames.append(Fstatic('— rutas: tráfico IP —',ALLIDS))
# A · servicio en la midu PROPIA (grupo 1)
frames.append(Fzoom('RA.0a · conecta: personas (grupo 1)',[pq,pw]))
frames.append(Fzoom('RA.0b · con: su propia midu (grupo 1)',midu1))
frames.append(Ffull('RA.1 · personas (grupo 1)',R6))
frames.append(Ffull('RA.2 · → internet: domain + cloud + cloudflare',R_center))
frames.append(Ffull('RA.3 · → midu propia (grupo 1)',R10))
frames.append(Ffull('RA.4 · regreso: internet',R_center))
frames.append(Ffull('RA.5 · regreso: personas (grupo 1)',R6))
# B · servicio en OTRA midu (grupo 1 → midu del grupo 2)
frames.append(Fzoom('RB.0a · conecta: personas (grupo 1)',[pq,pw]))
frames.append(Fzoom('RB.0b · con: midu del grupo 2',midu2+[gcard,gcardlbl]))
frames.append(Ffull('RB.1 · personas (grupo 1)',R6))
frames.append(Ffull('RB.2 · → internet: domain + cloud + cloudflare',R_center))
frames.append(Ffull('RB.3 · → midu del grupo 2',R19))
frames.append(Ffull('RB.4 · regreso: internet',R_center))
frames.append(Ffull('RB.5 · regreso: personas (grupo 1)',R6))
# C · persona ↔ persona entre nodos (grupo 1 ↔ grupo 2)
frames.append(Fzoom('RC.0a · conecta: personas (grupo 1)',[pq,pw]))
frames.append(Fzoom('RC.0b · con: personas (grupo 2)',[po,pp]))
frames.append(Ffull('RC.1 · personas (grupo 1)',R6))
frames.append(Ffull('RC.2 · → internet',R_center))
frames.append(Ffull('RC.3 · → midu del grupo 2',R19))
frames.append(Ffull('RC.4 · → personas (grupo 2)',R14))
frames.append(Ffull('RC.5 · regreso: internet',R_center))
frames.append(Ffull('RC.6 · regreso: personas (grupo 1)',R6))
# D · cliente (grupo 3, sin midu) → IA de la midu del grupo 2
frames.append(Fzoom('RD.0a · conecta: personas (grupo 3)',[pg,pk,pn,pu]))
frames.append(Fzoom('RD.0b · con: IA de la midu (grupo 2)',midu2+[gcard,gcardlbl]))
frames.append(Ffull('RD.1 · personas (grupo 3)',R25))
frames.append(Ffull('RD.2 · → internet',R_center))
frames.append(Ffull('RD.3 · → midu del grupo 2 (IA)',R19))
frames.append(Ffull('RD.4 · regreso: internet',R_center))
frames.append(Ffull('RD.5 · regreso: personas (grupo 3)',R25))

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
print(f'frames={len(frames)} | cnL_dev={len(cnL_dev)} cnL_srv={len(cnL_srv)} cnR2={len(cnR2)} cnR3={len(cnR3)}')
for i,(name,r,steps) in enumerate(frames): print(f'  {i+1:2} {name}')
