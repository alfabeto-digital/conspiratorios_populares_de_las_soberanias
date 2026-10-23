# -*- coding: utf-8 -*-
import lzstring, json, re, random, string, time, io, sys, glob
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
base=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
SRC=glob.glob(base+'/*/visualizaciones/midu-una_red_local_soberana.excalidraw.md')[0]
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
imgs=defaultdict(list)
for e in scene:
    if e['type']=='image': imgs[iname(e)].append(e['id'])
texts=[(e['id'],e.get('text','')) for e in scene if e['type']=='text']
abind={}
for e in scene:
    if e['type']=='arrow':
        s=e.get('startBinding',{}).get('elementId') if e.get('startBinding') else None
        t=e.get('endBinding',{}).get('elementId') if e.get('endBinding') else None
        abind[e['id']]=(s,t)
def one(n):
    assert len(imgs.get(n,[]))==1, (n,len(imgs.get(n,[]))); return imgs[n][0]
def txt(pred):
    hit=[i for i,t in texts if pred(t)]; assert hit,'no text'; return hit[0]

drects=[e for e in scene if e['type']=='rectangle' and e.get('strokeStyle')=='dotted']
boxOS=max(drects,key=lambda e:e['width'])['id']
boxRouter=min(drects,key=lambda e:e['width'])['id']
banner=[e['id'] for e in scene if e['type']=='rectangle' and e.get('strokeStyle')=='solid'][0]
marco=[e['id'] for e in scene if e['type']=='rectangle' and e.get('strokeStyle')=='dashed'][0]

RES={
 'person_b':[one('person_b')],'person_h':[one('person_y')],'driver':[one('person_f')],'infra3':[one('infrastructure_3')],
 'lblInfra':[txt(lambda t:'Infraestructura' in t)],
 'laptop':[one('computer_laptop')],'smartphone':[one('smartphone')],
 'local_server':[one('computer_local_server')],'lblMidu':[txt(lambda t:t.strip()=='midu')],'lblServicios':[txt(lambda t:'Servicios' in t)],
 'memory':[one('memory')],'lblDatos':[txt(lambda t:'Datos locales' in t)],
 'ext_hd':[one('external_hard_drive')],'lblDiscos':[txt(lambda t:'Discos' in t)],
 'digital_brain':[one('digital_brain')],'lblMemorias':[txt(lambda t:'Memorias' in t)],
 'renewable':[one('renewable_energy')],
 'os_android':[one('operating_system_android')],'degoogled':[one('degoogled')],'lblAndroid':[txt(lambda t:t.strip()=='android')],
 'os_graphene':[one('operating_system_graphene_os')],'lblGraphene':[txt(lambda t:'graphene' in t)],
 'os_lineage':[one('operating_system_lineage_os')],'lblLineage':[txt(lambda t:'lineage' in t)],
 'os_linux':[one('operating_system_linux')],'lblLinux':[txt(lambda t:t.strip()=='linux')],
 'os_nixos':[one('operating_system_nixos')],'lblNixos':[txt(lambda t:'nixos' in t)],
 'lblSO':[txt(lambda t:'Sistemas operativos' in t)],'boxOS':[boxOS],
 'dns':[one('dns')],'lblDns':[txt(lambda t:'Sistema de nombres' in t)],
 'router':[one('router')],'switch':[one('switch')],'boxRouter':[boxRouter],
 'isp_a':[one('isp_a')],'global_network':[one('global_network')],
 'banner':[banner],'titulo':[txt(lambda t:'Una red local' in t)],
}
POSTER={banner, RES['titulo'][0], marco}
# flechas de anotación de datos (se funden en su frame) + flecha a mover + flechas isp/global (se eliminan)
def _ab(a,b): return [aid for aid,(s,t) in abind.items() if {s,t}=={a,b}]
_mem=RES['memory'][0]; _db=RES['digital_brain'][0]; _ls=RES['local_server'][0]
RES['arrowDatos']=_ab(_mem,RES['lblDatos'][0])
RES['arrowDiscos']=_ab(RES['ext_hd'][0],RES['lblDiscos'][0])
RES['arrowMemorias']=_ab(_db,RES['lblMemorias'][0])
_arrowLsMem=set(_ab(_ls,_mem))
assert RES['arrowDatos'] and RES['arrowDiscos'] and RES['arrowMemorias'] and _arrowLsMem, 'falta alguna flecha de datos'
_isp=RES['isp_a'][0]; _gn=RES['global_network'][0]
EXCLUDE_ARROWS=set(RES['arrowDatos'])|set(RES['arrowDiscos'])|set(RES['arrowMemorias'])|{aid for aid,(s,t) in abind.items() if _isp in (s,t) or _gn in (s,t)}
def resolve(ref): return RES[ref]

P=[
 ('00.1 · apertura — todos los elementos',[],['ALL']),
 ('00.2 · título — Una red local soberana',[],['banner','titulo']),
 ('01.1 · person_b',['person_b'],[]),
 ('01.2 · person_y',['person_h'],[]),
 ('01.3 · person_f',['driver'],[]),
 ('01.4 · infraestructura humana (conjunto)',['infra3','lblInfra'],['person_b','person_h','driver']),
 ('02.1 · laptop',['laptop'],[]),
 ('02.2 · smartphone',['smartphone'],[]),
 ('02.3 · la midu',['local_server','lblMidu','lblServicios'],[]),
 ('02.4 · datos locales',['memory','lblDatos','arrowDatos'],[]),
 ('02.5 · discos duros',['ext_hd','lblDiscos','arrowDiscos'],[]),
 ('02.6 · memorias',['digital_brain','lblMemorias','arrowMemorias'],[]),
 ('02.7 · energía renovable',['renewable'],[]),
 ('02.8 · midu + memorias (conjunto)',[],['local_server','lblMidu','lblServicios','memory','lblDatos','ext_hd','lblDiscos','digital_brain','lblMemorias']),
 ('02.9 · transición — android / graphene / lineage',[],['os_android','os_graphene','os_lineage']),
 ('03.1 · android (degoogled)',['os_android','degoogled','lblAndroid'],[]),
 ('03.2 · graphene',['os_graphene','lblGraphene'],[]),
 ('03.3 · lineage',['os_lineage','lblLineage'],[]),
 ('03.35 · transición — linux / nixos',[],['os_linux','os_nixos']),
 ('03.4 · linux',['os_linux','lblLinux'],[]),
 ('03.5 · nixos',['os_nixos','lblNixos'],[]),
 ('03.6 · sistemas operativos (conjunto)',['lblSO','boxOS'],['os_android','degoogled','os_graphene','os_lineage','os_linux','os_nixos']),
 ('04.1 · dns',['dns','lblDns'],[]),
 ('04.2 · router + switch',['router','switch'],[]),
 ('04.4 · enrutador (conjunto)',['boxRouter'],['router','switch']),
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

def group_unit(eid):
    # el extremo se expande a su UNIDAD de grupo más interna (imagen + etiquetas del grupo),
    # para que las flechas apunten al grupo y no al elemento individual
    e=byid.get(eid)
    if not e: return []
    # smartphone y laptop comparten un grupo de layout pero son dispositivos distintos (de
    # personas distintas): no son una unidad, se tratan individualmente
    if e['type']=='image' and iname(e) in ('smartphone','computer_laptop'):
        return [e]
    g=e.get('groupIds',[])
    if g:
        g0=g[0]
        mem=[m for m in scene if m.get('groupIds') and m['groupIds'][0]==g0]
        if mem: return mem
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
    ep=[intro[x] for x in (s,t) if x in intro]
    if not ep: continue
    after=max(ep)
    if aid in _arrowLsMem: after=intro[_db]  # mover local_server↔memory a justo antes de energía renovable
    rects=[rect(byid[aid])]
    for x in (s,t):
        if x in byid:
            rects+=[rect(m) for m in group_unit(x)]
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
            tg+=[mm['id'] for mm in group_unit(x) if mm['type']!='arrow']
        tg=list(dict.fromkeys(tg))  # flecha + elementos (unidad de grupo) que une, hacen fade juntos
        final.append((nm,ar,[fstep(tg,500)]))

# ===== ediciones solicitadas sobre `final` (por índice 0-based original) =====
renew=RES['renewable'][0]; aDatos=RES['arrowDatos'][0]; aDiscos=RES['arrowDiscos'][0]; aMemorias=RES['arrowMemorias'][0]
a_renew_ls=_ab(renew,_ls)[0]; a_ls_mem=list(_arrowLsMem)[0]
osL=RES['os_linux'][0]; lblL=RES['lblLinux'][0]; lblMidu=RES['lblMidu'][0]; lblServ=RES['lblServicios'][0]
exthd=RES['ext_hd'][0]; lblDatos=RES['lblDatos'][0]; lblDiscos=RES['lblDiscos'][0]; lblMem=RES['lblMemorias'][0]; sm=RES['smartphone'][0]
def _fade_of(fr): return [t['id'] for s in fr[2] for t in s['targets']]
def _with_fade(fr,add_ids,pad=70):
    name,r,steps=fr
    ids=list(dict.fromkeys(_fade_of(fr)+[i for i in add_ids if i in byid]))
    xs=[r[0]]; ys=[r[1]]; xe=[r[0]+r[2]]; ye=[r[1]+r[3]]
    for i in add_ids:
        if i in byid:
            e=byid[i]; xs.append(e['x']-pad); ys.append(e['y']-pad); xe.append(e['x']+e['width']+pad); ye.append(e['y']+e['height']+pad)
    return (name,(min(xs),min(ys),max(xe)-min(xs),max(ye)-min(ys)),[fstep(ids,500)])
# 1. frame 15 (idx14): local_server↔memory + renewable + flechas de memorias + flecha renewable↔local_server
final[14]=_with_fade(final[14],[renew,aDatos,aDiscos,aMemorias,a_renew_ls])
# 3. frame 19 (idx18): transición + smartphone
final[18]=_with_fade(final[18],[sm])
# 6. frame 34 (idx33): nixos↔dns + linux + midu + renewable + grupo de memorias + flechas (todo fade in)
final[33]=_with_fade(final[33],[osL,lblL,_ls,lblMidu,lblServ,renew,_mem,_db,exthd,lblDatos,lblDiscos,lblMem,aDatos,aDiscos,aMemorias,a_ls_mem,a_renew_ls])
# reordenar: eliminar 15,16,17 (idx15,16,17), 20 (idx19), 39 (idx38);
# invertir 28/29 (idx27,28); mover 36 (idx35) antes de 30 (idx29); invertir 37/38 (idx36,37)
order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,18,20,21,22,23,24,25,26,28,27,35,29,30,31,32,33,34,37,36,39,40]
final=[final[i] for i in order]

# ===== segunda pasada de ediciones (índices 0-based sobre la lista ya reordenada de 36) =====
osA=RES['os_android'][0]; deg=RES['degoogled'][0]; lblA=RES['lblAndroid'][0]
osG=RES['os_graphene'][0]; lblG=RES['lblGraphene'][0]; osLin=RES['os_lineage'][0]; lblLin=RES['lblLineage'][0]
router=RES['router'][0]; switch=RES['switch'][0]
def _is_rect(i): return i in byid and byid[i]['type']=='rectangle'
def _edit_fade(fr,add=(),drop_rect=False,drop=()):
    ids=_fade_of(fr)
    if drop_rect: ids=[i for i in ids if not _is_rect(i)]
    ids=[i for i in ids if i not in set(drop)]
    ids=list(dict.fromkeys(ids+[i for i in add if i in byid]))
    xs=[byid[i]['x'] for i in ids]; ys=[byid[i]['y'] for i in ids]
    xe=[byid[i]['x']+byid[i]['width'] for i in ids]; ye=[byid[i]['y']+byid[i]['height'] for i in ids]
    return (fr[0],(min(xs)-70,min(ys)-70,max(xe)-min(xs)+140,max(ye)-min(ys)+140),[fstep(ids,500)])
# frame 16 (idx15): fade a todos los elementos (smartphone + grupos android/graphene/lineage)
final[15]=_edit_fade(final[15],add=[osA,deg,lblA,osG,lblG,osLin,lblLin])
# frame 34 (idx33): lineage↔switch + grupo degoogled android + smartphone
final[33]=_edit_fade(final[33],add=[osA,deg,lblA,sm])
# frame 35 (idx34): graphene + grupo degoogled android + smartphone; fade a switch+router (no el rectángulo)
final[34]=_edit_fade(final[34],add=[osA,deg,lblA,sm,router,switch],drop_rect=True)
# eliminar 18 (idx17 graphene), 20 (idx19 lineage), 32 (idx31 router+switch)
final=[fr for i,fr in enumerate(final) if i not in (17,19,31)]

# ===== tercera pasada (índices 0-based sobre la lista de 33) =====
pb=RES['person_b'][0]; py=RES['person_h'][0]; pf=RES['driver'][0]; infra3=RES['infra3'][0]; lblInfra=RES['lblInfra'][0]
laptop=RES['laptop'][0]; osN=RES['os_nixos'][0]; lblN=RES['lblNixos'][0]; dns=RES['dns'][0]; lblDns=RES['lblDns'][0]
def _arr(ia,ib):  # flecha entre los grupos de dos imágenes (los extremos pueden ligar a imagen o etiqueta)
    ga={m['id'] for m in group_unit(ia)}; gb={m['id'] for m in group_unit(ib)}
    for aid,(s,t) in abind.items():
        if (s in ga and t in gb) or (s in gb and t in ga): return aid
    return None
a_laptop_linux=_arr(laptop,osL); a_linux_switch=_arr(osL,switch); a_linux_nixos=_arr(osL,osN)
a_nixos_dns=_arr(osN,dns); a_dns_router=_arr(dns,router)
assert all([a_laptop_linux,a_linux_switch,a_linux_nixos,a_nixos_dns,a_dns_router]),'arrows OS'
def _mk(name,ids,pad=75):
    ids=[i for i in dict.fromkeys(ids) if i in byid]
    xs=[byid[i]['x'] for i in ids]; ys=[byid[i]['y'] for i in ids]
    xe=[byid[i]['x']+byid[i]['width'] for i in ids]; ye=[byid[i]['y']+byid[i]['height'] for i in ids]
    return (name,(min(xs)-pad,min(ys)-pad,max(xe)-min(xs)+2*pad,max(ye)-min(ys)+2*pad),[fstep(ids,500)])
# frame 15 (idx14): quitar el fade de la midu (local_server + etiquetas)
final[14]=_edit_fade(final[14],drop=[_ls,lblMidu,lblServ])
# frame 20 (idx19): todos los elementos conectados con nixos, con fade in
final[19]=_edit_fade(final[19],add=[osN,lblN,osL,lblL,dns,lblDns,a_linux_nixos,a_nixos_dns])
# frame final (idx32 cierre) -> volver a la infraestructura humana: cámara sobre todo el grupo,
# pero el fade resalta sólo a las personas (infrastructure_3 + etiqueta quedan fuera del fade)
final[32]=('99.1 · volver a la infraestructura humana',bbox([pb,py,pf,infra3,lblInfra],75),[fstep([pb,py,pf],500)])
# tres frames antes del final
new1=_mk('→ laptop + linux + switch + router',[laptop,osL,lblL,switch,router,a_laptop_linux,a_linux_switch])
new2=_mk('→ midu + renewable + memorias + linux + nixos + dns + switch + router',
         [_ls,lblMidu,lblServ,renew,_mem,_db,exthd,lblDatos,lblDiscos,lblMem,osL,lblL,osN,lblN,dns,lblDns,switch,router,
          aDatos,aDiscos,aMemorias,a_ls_mem,a_renew_ls,a_linux_nixos,a_nixos_dns,a_dns_router,a_linux_switch])
new3=_mk('→ midu + laptop + smartphone',[_ls,lblMidu,lblServ,laptop,sm])
# eliminar 8 (idx7), 10 (idx9), 21 (idx20), 26 (idx25); insertar new1/2/3 antes del final
keep=[fr for i,fr in enumerate(final) if i not in (7,9,20,25)]
final=keep[:-1]+[new1,new2,new3]+[keep[-1]]
# frame 18 (idx17): linux + midu + laptop + router + switch + flechas
a_ls_linux=_arr(_ls,osL)
final[17]=_mk('03.35 · linux + midu + laptop + router + switch',
              [osL,lblL,_ls,lblMidu,lblServ,laptop,router,switch,a_laptop_linux,a_ls_linux,a_linux_switch])
# frame 22 (idx21): linux + nixos + flecha
final[21]=_mk('03.5 · linux + nixos',[osL,lblL,osN,lblN,a_linux_nixos])
# último frame: todo el conjunto
final.append(('99.2 · todo el conjunto',bbox(ALLIDS,130),[]))

# ===== reveal de personas una por una (estilo soberana): fusionar 01.1-01.4 en un frame multipaso =====
_pnames=['01.1 · person_b','01.2 · person_y','01.3 · person_f','01.4 · infraestructura humana (conjunto)']
_ppos=[i for i,fr in enumerate(final) if fr[0] in _pnames]
assert _ppos==list(range(_ppos[0],_ppos[0]+4)),'frames de personas no consecutivos'
_ppl=sorted([pb,py,pf],key=lambda i:byid[i]['x'])
_psteps=[fstep([i],600) for i in _ppl]+[fstep([infra3,lblInfra],600)]
_merged=('01 · personas (una por una) + infraestructura humana',bbox([pb,py,pf,infra3,lblInfra],80),_psteps)
final=final[:_ppos[0]]+[_merged]+final[_ppos[-1]+1:]

# ===== correcciones de flechas (índices de salida, tras la fusión de personas) =====
osA=RES['os_android'][0]; osG=RES['os_graphene'][0]; osLin=RES['os_lineage'][0]
a_lineage_android=_arr(osLin,osA); a_android_smart=_arr(osA,sm); a_graphene_android=_arr(osG,osA)
assert all([a_lineage_android,a_android_smart,a_graphene_android]),'flechas lineage/graphene/android/smartphone'
def _ext(e):
    if e['type']=='arrow' and e.get('points'):
        xs=[e['x']+p[0] for p in e['points']]; ys=[e['y']+p[1] for p in e['points']]; return (min(xs),min(ys),max(xs),max(ys))
    return (e['x'],e['y'],e['x']+e['width'],e['y']+e['height'])
def _bbx(ids,pad):
    q=[_ext(byid[i]) for i in ids if i in byid]
    return (min(a[0] for a in q)-pad,min(a[1] for a in q)-pad,max(a[2] for a in q)-min(a[0] for a in q)+2*pad,max(a[3] for a in q)-min(a[1] for a in q)+2*pad)
def _patch(idx,expect,add=(),drop=()):
    name,r,steps=final[idx]; assert expect in name,(idx,name)
    ids=[t['id'] for s in steps for t in s['targets']]
    ids=[i for i in ids if i not in set(drop)]
    ids=list(dict.fromkeys(ids+[i for i in add if i in byid]))
    final[idx]=(name,_bbx(ids,75),[fstep(ids,500)])
_patch(10,'02.9',add=[a_android_smart,a_graphene_android,a_lineage_android])  # frame 11: + flechas smartphone↔android, android↔graphene, android↔lineage
_patch(21,'nixos ↔ dns',add=[a_ls_linux,a_linux_nixos])                 # frame 22: + ls↔linux, + linux↔nixos
_patch(23,'lineage',add=[a_lineage_android,a_android_smart])            # frame 24: + lineage↔android, + android↔smartphone
_patch(24,'graphene',add=[a_graphene_android,a_android_smart])          # frame 25: + graphene↔android, + android↔smartphone
_patch(25,'laptop + linux',add=[osN,lblN,dns,lblDns,a_linux_nixos,a_nixos_dns,a_dns_router],drop=[a_linux_switch])  # frame 26: -linux↔enrutador, +nixos +dns + flechas (linux↔nixos↔dns↔router)
_patch(26,'midu + renewable',add=[a_ls_linux])                          # frame 27: + ls↔linux

base_idx=data['elements'][-1].get('index','a0')
ts=int(time.time()*1000)
for i,(name,r,steps) in enumerate(final):
    x,y,w,h=r
    data['elements'].append({'id':nid(),'type':'frame','x':round(x,2),'y':round(y,2),'width':round(w,2),'height':round(h,2),
      'angle':0,'strokeColor':'#a89984','backgroundColor':'transparent','fillStyle':'solid','strokeWidth':1,
      'strokeStyle':'solid','roughness':0,'opacity':100,'groupIds':[],'frameId':None,'index':base_idx+f'{i:04d}',
      'roundness':None,'seed':random.randint(1,2**31),'version':1,'versionNonce':random.randint(1,2**31),
      'isDeleted':False,'boundElements':None,'updated':ts,'link':None,'locked':False,'name':name,
      'customData':{'slideshow':{'schemaVersion':2,'kind':'frame','order':i,**({'animation':{'steps':steps}} if steps else {})}}})

new=lz.compressToBase64(json.dumps(data,separators=(',',':'),ensure_ascii=False))
open(OUT,'w',encoding='utf-8').write(content[:m.start(1)]+new+content[m.end(1):])

notrev=[e for e in scene if e['id'] not in revealed and e['type']!='arrow' and e['id'] not in POSTER]
print(f'element frames={len(frames)} | arrow frames={sum(len(v) for v in arrow_specs.values())} | TOTAL={len(final)}')
print(f'revelados={len(revealed)} | poster={len(POSTER)} | no revelados inesperados={[(e["type"],iname(e) or e.get("text","")[:12]) for e in notrev]}')
print('OUT:',OUT.split('/')[-1])
