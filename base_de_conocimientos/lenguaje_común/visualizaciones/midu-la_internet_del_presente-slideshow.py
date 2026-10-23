# -*- coding: utf-8 -*-
import lzstring, json, re, random, string, time, io, sys
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
_HERE=os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(_HERE,'midu-la_internet_del_presente.excalidraw.md')
OUT = os.path.join(_HERE,'midu-la_internet_del_presente-slideshow.excalidraw.md')

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

imgs=defaultdict(list)
for e in scene:
    if e['type']=='image': imgs[iname(e)].append(e['id'])
texts=[(e['id'],e.get('text',''),e.get('fontSize',20)) for e in scene if e['type']=='text']
groups=defaultdict(set)
for e in scene:
    for g in e.get('groupIds',[]): groups[g].add(e['id'])
abind={}
for e in scene:
    if e['type']=='arrow':
        s=e.get('startBinding',{}).get('elementId') if e.get('startBinding') else None
        t=e.get('endBinding',{}).get('elementId') if e.get('endBinding') else None
        abind[e['id']]=(s,t)

def one(name):
    ids=imgs.get(name,[]); assert len(ids)==1, f'expected 1 {name}, got {len(ids)}'; return ids[0]
def txt(pred):
    hit=[i for i,t,fs in texts if pred(t,fs)]; assert hit,'no text'; return hit[0]
def dist(a,b): return (a[0]-b[0])**2+(a[1]-b[1])**2

# router/switch stacks via routes (unaffected by wrapper groups)
routers=imgs['router']; switches=imgs['switch']
def out_target_name(rid):
    for aid,(s,t) in abind.items():
        if s==rid and t in byid: return iname(byid[t])
    return None
router1=router2=None
for r in routers:
    tn=out_target_name(r)
    if tn=='computer_shopping_online': router1=r
    elif tn=='computer_graphic_design': router2=r
assert router1 and router2,(router1,router2)
def partner_switch(rid):
    r0=byid[rid]['groupIds'][0]
    for s in switches:
        if byid[s]['groupIds'] and byid[s]['groupIds'][0]==r0: return s
    raise AssertionError('no switch partner')
switch1=partner_switch(router1); switch2=partner_switch(router2)

# dotted boxes by size/position
drects=[e for e in scene if e['type']=='rectangle' and e.get('strokeStyle')=='dotted']
box_internet=max(drects,key=lambda e:e['width'])['id']
box_centros=[e['id'] for e in drects if 1500<e['width']<2000][0]
box_indisp=[e['id'] for e in drects if 400<e['width']<700 and e['height']>700][0]
userboxes=[e for e in drects if e['width']<300]
assert len(userboxes)==4,len(userboxes)
compboxes=[e['id'] for e in userboxes if e['x']<4700]   # columna x~4455 = Computadores
txboxes  =[e['id'] for e in userboxes if e['x']>=4700]   # columna x~4923 = Transmisores
assert len(compboxes)==2 and len(txboxes)==2,(compboxes,txboxes)
def contains_center(boxid,elid):
    b=byid[boxid]; cx,cy=center(byid[elid])
    return b['x']<=cx<=b['x']+b['width'] and b['y']<=cy<=b['y']+b['height']
boxTx1=next((b for b in txboxes if contains_center(b,router1)),txboxes[0])
boxTx2=[b for b in txboxes if b!=boxTx1][0]

# title / banner / frame
titulo=txt(lambda t,fs: 'del presente' in t)
banner=[e['id'] for e in scene if e['type']=='rectangle' and e.get('strokeStyle')=='solid'][0]
marco =[e['id'] for e in scene if e['type']=='rectangle' and e.get('strokeStyle')=='dashed'][0]

# data_center clusters
dc=imgs['data_center']
clusters=[(g,ms) for g,ms in groups.items() if len(ms)==4 and all(i in dc for i in ms)]
def meanx(ms): return sum(byid[i]['x'] for i in ms)/len(ms)
clusters.sort(key=lambda gm:meanx(gm[1])); assert len(clusters)>=3,len(clusters)
clA,clB,clC=list(clusters[0][1]),list(clusters[1][1]),list(clusters[2][1])
lone=[i for i in dc if i not in (set(clA)|set(clB)|set(clC))]; assert len(lone)==1; dcLone=lone[0]

RES={
 'man_white':[one('person_c')],'woman_black':[one('person')],'lblPersonas':[txt(lambda t,fs:'Personas' in t)],
 'shop':[one('computer_shopping_online')],'phone':[one('smartphone_apps')],'graphic':[one('computer_graphic_design')],
 'lblComp':[txt(lambda t,fs:'Computadores' in t)],'boxComp':list(compboxes),
 'router1':[router1],'switch1':[switch1],'antenna':[one('antenna')],'router2':[router2],'switch2':[switch2],
 'boxTx1':[boxTx1],'boxTx2':[boxTx2],'lblTx':[txt(lambda t,fs:'Antenas' in t or 'enrutadores' in t)],
 'isp_a':[one('isp_a')],'isp_c':[one('isp_c')],'lblIspC':[txt(lambda t,fs:'conocidos' in t and 'desconocidos' not in t)],
 'global':[one('global_network')],
 'domain_name':[one('domain_name')],'dns':[one('dns')],
 'lblIcann':[txt(lambda t,fs:'Registradores' in t)],'lblSistema':[txt(lambda t,fs:'Sistemas de nombres' in t)],
 'lblIndisp':[txt(lambda t,fs:'Actores indispensables' in t)],'boxIndisp':[box_indisp],
 'isp_b':[one('isp_b')],'satellite':[one('satellite')],'lblIspD':[txt(lambda t,fs:'desconocidos' in t)],
 'lblPublicos':[txt(lambda t,fs:'Actores públicos' in t)],'democracy':[one('democracy')],'rich':[one('rich')],
 'dcLone':[dcLone],
 'lblPrivados':[txt(lambda t,fs:'Actores privados' in t)],'google':[one('google')],'clA':clA,
 'amazon':[one('amazon')],'aws':[one('aws')],'clB':clB,
 'ai':[one('artificial_intelligence')],'theft':[one('theft')],
 'fake_news':[one('fake_news')],'show':[one('show')],'cryptobro':[one('cryptobro')],
 'social':[one('social_network')],'news':[one('news')],'hacker':[one('hacker')],'bug':[one('bug')],'clC':clC,
 'lblDc':[txt(lambda t,fs:'Centros de datos' in t)],'boxDc':[box_centros],
 'infantry':[one('infantry')],'fossil_fuel':[one('fossil_fuel')],'lblNube':[txt(lambda t,fs:'nube' in t)],
 'lblInternet':[txt(lambda t,fs:t.strip().startswith('Internet'))],'boxInternet':[box_internet],
 'banner':[banner],'titulo':[titulo],
}
# --- indispensables consolidation: identify the two area arrows ---
_gid=RES['global'][0]; _dnsid=RES['dns'][0]; _ilbl=RES['lblIndisp'][0]; _ibox=RES['boxIndisp'][0]
_ag=[aid for aid,(s,t) in abind.items() if {s,t}=={_gid,_dnsid}]
_aa=[aid for aid,(s,t) in abind.items() if _ilbl in (s,t) and _ibox in (s,t)]
assert len(_ag)==1 and len(_aa)==1, ('global-dns',_ag,'annot',_aa)
RES['arrowIndisp']=_aa
# flechas de anotación de los conjuntos nube e internet (recuadro ↔ etiqueta)
_nbox=RES['boxDc'][0]; _nlbl=RES['lblNube'][0]; _ibx=RES['boxInternet'][0]; _ilb=RES['lblInternet'][0]
_an=[aid for aid,(s,t) in abind.items() if _nbox in (s,t) and _nlbl in (s,t)]
_ai=[aid for aid,(s,t) in abind.items() if _ibx in (s,t) and _ilb in (s,t)]
assert len(_an)==1 and len(_ai)==1, ('nube',_an,'internet',_ai)
RES['arrowNube']=_an; RES['arrowInternet']=_ai
EXCLUDE_ARROWS=set(_aa)|set(_an)|set(_ai)  # annot indispensables/nube/internet van en sus conjuntos; global↔dns SÍ tiene frame propio
def resolve(ref): return RES[ref]

P=[
 ('00.1 · apertura — todos los elementos',[],['ALL']),
 ('00.2 · título — La internet del presente',[],['banner','titulo']),
 ('01.1 · etiqueta Personas',['lblPersonas'],[]),
 ('01.2 · man_white',['man_white'],[]),
 ('01.3 · woman_black',['woman_black'],[]),
 ('01.4 · personas (conjunto)',[],['man_white','woman_black','lblPersonas']),
 ('02.1 · computador (shopping)',['shop'],[]),
 ('02.2 · smartphone',['phone'],[]),
 ('02.3 · computador (graphic design)',['graphic'],[]),
 ('02.4 · computadores (conjunto)',['boxComp','lblComp'],['shop','phone','graphic']),
 ('03.1 · router+switch (stack 1)',['router1','switch1'],[]),
 ('03.2 · antenna',['antenna'],[]),
 ('03.4 · router+switch (stack 2)',['router2','switch2'],[]),
 ('03.6 · antenas y enrutadores (conjunto: cuadros + etiqueta)',['boxTx1','boxTx2','lblTx'],['router1','switch1','antenna','router2','switch2']),
 ('04.1 · isp_a',['isp_a'],[]),
 ('04.2 · isp_c',['isp_c'],[]),
 ('04.3 · etiqueta ISP conocidos',['lblIspC'],[]),
 ('04.4 · ISP conocidos (conjunto)',[],['isp_a','isp_c','lblIspC']),
 ('05.1 · red global',['global'],[]),
 ('06.1 · domain_name + ICANN',['domain_name','lblIcann'],[]),
 ('06.2 · dns + sistemas de nombres',['dns','lblSistema'],[]),
 ('06.3 · indispensables (conjunto: recuadro + flecha + etiqueta)',['boxIndisp','arrowIndisp','lblIndisp'],['global','domain_name','dns','lblIcann','lblSistema']),
 ('07.1 · isp_b',['isp_b'],[]),
 ('07.2 · satellite',['satellite'],[]),
 ('07.3 · ISP desconocidos (conjunto)',['lblIspD'],['isp_b','satellite']),
 ('08.1 · etiqueta actores públicos',['lblPublicos'],[]),
 ('08.2 · democracy',['democracy'],[]),
 ('08.3 · rich',['rich'],[]),
 ('09.1 · servidor conocido',['dcLone'],[]),
 ('10.1 · etiqueta actores privados',['lblPrivados'],[]),
 ('10.2 · google',['google'],[]),
 ('10.3 · servidores grupo 1',['clA'],[]),
 ('11.1 · amazon',['amazon'],[]),
 ('11.2 · aws',['aws'],[]),
 ('11.3 · servidores grupo 2',['clB'],[]),
 ('12.1 · inteligencia artificial',['ai'],[]),
 ('12.2 · theft',['theft'],[]),
 ('12.3 · aws',['aws'],[]),
 ('12.4 · servidores grupo 2',['clB'],[]),
 ('13.1 · news',['news'],[]),
 ('13.2 · rich',['rich'],[]),
 ('13.3 · bug',['bug'],[]),
 ('13.4 · show',['show'],[]),
 ('13.5 · cryptobro',['cryptobro'],[]),
 ('13.6 · social_network',['social'],[]),
 ('13.7 · fake_news',['fake_news'],[]),
 ('13.8 · hacker',['hacker'],[]),
 ('13.9 · servidores grupo 3',['clC'],[]),
 ('15.1 · públicos + privados (recap)',[],['democracy','rich','google','amazon','aws','ai','theft','fake_news','bug','show','cryptobro','social','news','hacker','lblPublicos','lblPrivados']),
 ('16.1 · servidores grupo 1',['clA'],[]),
 ('16.2 · servidores grupo 2',['clB'],[]),
 ('16.3 · servidores grupo 3',['clC'],[]),
 ('16.4 · servidor suelto',['dcLone'],[]),
 ('16.5 · etiqueta centros de datos',['lblDc'],[]),
 ('17.1 · grupo de centros de datos',[],['clA','clB','clC','dcLone','boxDc']),
 ('17.2 · infantry',['infantry'],[]),
 ('17.3 · fossil_fuel',['fossil_fuel'],[]),
 ('17.5 · la nube (conjunto)',['lblNube','boxDc','arrowNube'],['clA','clB','clC','dcLone','infantry','fossil_fuel']),
 ('18.2 · la internet (conjunto)',['lblInternet','boxInternet','arrowInternet'],[]),
 ('99.1 · cierre — todos los elementos',[],['ALL']),
]

revealed=set(); intro={}
def nid(n=21): return ''.join(random.choice(string.ascii_letters+string.digits+'-_') for _ in range(n))
def fstep(ids,dur): return {'id':nid(10),'targets':[{'type':'element','id':i} for i in ids],'effect':'fade','trigger':'after-delay','delayMs':200,'durationMs':dur}
ALLIDS=[e['id'] for e in scene]
def bbox(ids,pad):
    xs=[byid[i]['x'] for i in ids]; ys=[byid[i]['y'] for i in ids]
    xe=[byid[i]['x']+byid[i]['width'] for i in ids]; ye=[byid[i]['y']+byid[i]['height'] for i in ids]
    return (min(xs)-pad,min(ys)-pad,max(xe)-min(xs)+2*pad,max(ye)-min(ys)+2*pad)

frames=[]
for idx,(name,appear,extra) in enumerate(P):
    cam=[]; new=[]
    for ref in appear:
        ids=resolve(ref); cam+=ids
        for i in ids:
            if i not in revealed: new.append(i); revealed.add(i); intro[i]=idx
    is_all='ALL' in extra
    for ref in extra:
        if ref=='ALL': continue
        cam+=resolve(ref)
    steps=[fstep(new,600)] if new else []
    if is_all: r=bbox(ALLIDS,130)
    else:
        single=len(appear)==1 and not extra and len(resolve(appear[0]))==1
        r=bbox(cam,40 if single else 75)
    frames.append([name,r,steps])

# per-arrow frames
def group_unit(eid):
    # unidad de grupo más interna (imagen+etiquetas / cluster de servidores / par router+switch);
    # tope de tamaño para no agarrar el grupo global que envuelve el diagrama ni la cadena del ecosistema
    e=byid.get(eid)
    if not e: return []
    # personas y dispositivos son individuos/dispositivos distintos, no una unidad de grupo
    if e['type']=='image' and iname(e) in ('person','person_c','computer_shopping_online','smartphone_apps','computer_graphic_design'):
        return [e]
    g=e.get('groupIds',[])
    if g:
        g0=g[0]
        mem=[m for m in scene if m.get('groupIds') and m['groupIds'][0]==g0]
        if 2<=len(mem)<=6: return mem
    return [e]
def enm(eid):
    e=byid.get(eid)
    if not e: return '?'
    if e['type']=='image': return iname(e)
    if e['type']=='text':
        sib=[m for m in group_unit(eid) if m['type']=='image']
        if sib: return iname(sib[0])
    return e['type']
arrow_specs=defaultdict(list)
for aid,(s,t) in abind.items():
    if aid in EXCLUDE_ARROWS: continue
    # mostrar la flecha en el extremo que se revela MÁS TARDE (independiente de la
    # dirección del binding): así se agrupa donde ambos extremos ya están presentes
    ep=[intro[x] for x in (s,t) if x in intro]
    if not ep: continue
    after=max(ep)
    rects=[rect(byid[aid])]
    for x in (s,t):
        if x in byid: rects+=[rect(m) for m in group_unit(x)]
    xs=[q[0] for q in rects]; ys=[q[1] for q in rects]; xe=[q[0]+q[2] for q in rects]; ye=[q[1]+q[3] for q in rects]
    ar=(min(xs)-70,min(ys)-70,max(xe)-min(xs)+140,max(ye)-min(ys)+140)
    nm=f'→ {enm(s)} ↔ {enm(t)}' if s else f'→ {enm(t)}'
    arrow_specs[after].append((center(byid[aid])[0],aid,ar,nm))

final=[]
for i,(name,r,steps) in enumerate(frames):
    final.append((name,r,steps))
    for _,aid,ar,nm in sorted(arrow_specs.get(i,[]),key=lambda z:z[0]):
        s,t=abind[aid]
        tg=[aid]
        for x in (s,t):
            tg+=[m['id'] for m in group_unit(x) if m['type']!='arrow']
        tg=list(dict.fromkeys(tg))  # flecha + unidad de grupo de los elementos que une
        final.append((nm,ar,[fstep(tg,500)]))

base=data['elements'][-1].get('index','a0')
ts=int(time.time()*1000)
for i,(name,r,steps) in enumerate(final):
    x,y,w,h=r
    data['elements'].append({'id':nid(),'type':'frame','x':round(x,2),'y':round(y,2),'width':round(w,2),'height':round(h,2),
      'angle':0,'strokeColor':'#a89984','backgroundColor':'transparent','fillStyle':'solid','strokeWidth':1,
      'strokeStyle':'solid','roughness':0,'opacity':100,'groupIds':[],'frameId':None,'index':base+f'{i:04d}',
      'roundness':None,'seed':random.randint(1,2**31),'version':1,'versionNonce':random.randint(1,2**31),
      'isDeleted':False,'boundElements':None,'updated':ts,'link':None,'locked':False,'name':name,
      'customData':{'slideshow':{'schemaVersion':2,'kind':'frame','order':i,**({'animation':{'steps':steps}} if steps else {})}}})

new=lz.compressToBase64(json.dumps(data,separators=(',',':'),ensure_ascii=False))
open(OUT,'w',encoding='utf-8').write(content[:m.start(1)]+new+content[m.end(1):])

poster={banner,titulo,marco}
notrev=[e for e in scene if e['id'] not in revealed and e['type']!='arrow' and e['id'] not in poster]
print(f'clusters(x): A={meanx(clA):.0f} B={meanx(clB):.0f} C={meanx(clC):.0f}')
print(f'element frames={len(frames)} | arrow frames={sum(len(v) for v in arrow_specs.values())} | TOTAL={len(final)}')
print(f'revealed(non-arrow)={len(revealed)} | poster(no fade)={len(poster)} | unexpected not-revealed={[ (e["type"],iname(e) or e.get("text","")[:12]) for e in notrev]}')
print('boxes: internet',box_internet[:5],'centros',box_centros[:5],'indisp',box_indisp[:5],'| comp',[b[:5] for b in compboxes],'tx',[b[:5] for b in txboxes])
print('OUT:',OUT)
