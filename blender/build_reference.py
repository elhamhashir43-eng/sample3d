"""Front + rear reference study; metres, Blender Z up; front faces -Y."""
import bpy, math, random, os, json
from mathutils import Vector
from collections import defaultdict
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
random.seed(37)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.render.threads_mode='FIXED';scene.render.threads=8
M={};B=defaultdict(lambda:[[],[]]);lights=[]
def mat(n,c,r=.6,metal=0,tex=None,alpha=1):
 m=bpy.data.materials.new(n);m.use_nodes=True;m.diffuse_color=(*c,alpha)
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;p.inputs['Alpha'].default_value=alpha
 if alpha<1:m.surface_render_method='DITHERED';m.use_backface_culling=False
 if tex:
  im=bpy.data.images.load(os.path.join(ROOT,'exports','textures',tex+'.png'));im.pack();t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=im;m.node_tree.links.new(t.outputs['Color'],p.inputs['Base Color'])
 M[n]=m;return m
mat('Ivory plaster',(.83,.82,.77),.83,tex='Warm ivory plaster')
mat('Warm teak',(.38,.18,.075),.48,tex='Smoked teak')
mat('Silver limestone',(.43,.44,.41),.83,tex='Honed outdoor limestone')
mat('Slate grey',(.19,.21,.21),.8,tex='Basalt')
mat('Pale travertine',(.65,.61,.52),.63,tex='Travertine')
mat('Charcoal aluminium',(.055,.063,.065),.3,.7)
mat('Brass',(.55,.36,.13),.3,.75)
mat('Window glass',(.70,.79,.80),.12,.1,alpha=.13)
mat('Balustrade glass',(.72,.83,.83),.09,.15,alpha=.18)
mat('Ivory linen',(.78,.75,.67),.92,tex='Linen')
mat('Sage fabric',(.24,.28,.20),.95)
mat('Curtain linen',(.82,.76,.64),.9,tex='Sheer warm linen')
mat('Garden lawn',(.20,.29,.10),1,tex='Sage lawn')
mat('Dark soil',(.065,.048,.027),1)
mat('Ceramic',(.78,.76,.66),.3)
mat('Water',(.08,.13,.14),.18,.5)
mat('Screen',(.018,.023,.025),.2)
for i,c in enumerate([(.06,.16,.033),(.12,.23,.05),(.22,.31,.08),(.075,.21,.12)]):mat('Leaf '+str(i),c,.8)
for i,c in enumerate([(.37,.38,.36),(.42,.43,.41),(.46,.47,.44)]):mat('Stone course '+str(i),c,.84)
mat('Light diffuser',(1,.78,.45),.4)
p=M['Light diffuser'].node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.65,.28,1);p.inputs['Emission Strength'].default_value=.25

def mesh(tag,material,verts,faces):
 v,f=B[(tag,material)];i=len(v);v.extend(verts);f.extend([tuple(a+i for a in face) for face in faces])
def box(tag,loc,size,material='Ivory plaster',ang=0):
 x,y,z=loc;w,d,h=[a/2 for a in size];c,s=math.cos(ang),math.sin(ang)
 vs=[(x+a*c-b*s,y+a*s+b*c,z+q) for a,b,q in [(-w,-d,-h),(w,-d,-h),(w,d,-h),(-w,d,-h),(-w,-d,h),(w,-d,h),(w,d,h),(-w,d,h)]]
 mesh(tag,material,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])
def cyl(tag,loc,r,h,material,r2=None,n=12):
 r2=r if r2 is None else r2;x,y,z=loc
 v=[(x+rr*math.cos(i*2*math.pi/n),y+rr*math.sin(i*2*math.pi/n),z+zz) for rr,zz in [(r,-h/2),(r2,h/2)] for i in range(n)]
 mesh(tag,material,v,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)])
def rod(tag,a,b,r,material,n=10):
 a,b=Vector(a),Vector(b);d=b-a;side=d.cross(Vector((0,0,1)))
 if side.length<.001:side=d.cross(Vector((0,1,0)))
 side.normalize();up=d.normalized().cross(side)
 v=[tuple(p+r*(side*math.cos(i*2*math.pi/n)+up*math.sin(i*2*math.pi/n))) for p in [a,b] for i in range(n)]
 mesh(tag,material,v,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)])
def leaf(a,b,w,idx=0,arch=.2):
 a,b=Vector(a),Vector(b);d=b-a;side=Vector((-d.y,d.x,0)).normalized();v=[];f=[]
 for i in range(7):
  t=i/6;center=a+d*t+Vector((0,0,math.sin(t*math.pi)*arch));ww=w*math.sin(math.pi*t)**.75
  for j in [-1,0,1]:v.append(tuple(center+side*ww*j+Vector((0,0,-abs(j)*ww*.2))))
 for i in range(6):
  for j in range(2):k=i*3+j;f.append((k,k+1,k+4,k+3))
 mesh('Foliage','Leaf '+str(idx%4),v,f)
def plant(x,y,z=.14,s=1):
 for i in range(11):
  a=i*2.4+random.random()*.3;d=random.uniform(.25,.65)*s
  leaf((x,y,z),(x+math.cos(a)*d,y+math.sin(a)*d,z+random.uniform(.35,.85)*s),.09*s,i,.18*s)
def pot(x,y,z,s=.7):
 cyl('Planters',(x,y,z+.22*s),.20*s,.44*s,'Ceramic',.28*s,18);cyl('Planter soil',(x,y,z+.445*s),.25*s,.012,'Dark soil');plant(x,y,z+.46*s,.85*s)
def tree(x,y,h=3):
 rod('Tree trunks',(x,y,0),(x+.12,y,h*.8),.06,'Warm teak')
 for i in range(18):
  a=i*2.4;end=(x+math.cos(a)*random.uniform(.5,1.0),y+math.sin(a)*random.uniform(.5,1),h+random.uniform(-.6,.35))
  rod('Branches',(x+.1,y,h*.65),end,.018,'Warm teak',6)
  for j in range(14):
   aa=j*2.4;leaf(end,(end[0]+.42*math.cos(aa),end[1]+.42*math.sin(aa),end[2]+random.uniform(-.1,.25)),.10,i+j,.09)
def palm(x,y,h=8):
 for i in range(14):
  t=i/14;u=(i+1)/14;rod('Palm trunks',(x+.28*t*t,y,h*t),(x+.28*u*u,y,h*u),.13-.04*t,'Warm teak')
 crown=Vector((x+.28,y,h))
 for i in range(13):
  a=i*2.4;d=Vector((math.cos(a),math.sin(a),0));side=Vector((-d.y,d.x,0));L=random.uniform(2.0,3.3)
  for k in range(14):
   t=.08+k*.062;mid=crown+d*L*t+Vector((0,0,.85*math.sin(math.pi*t)-.9*t*t));reach=.5*math.sin(math.pi*t)+.1
   for sign in [-1,1]:leaf(mid,mid+sign*side*reach+d*.25+Vector((0,0,-.19)),.053,i,.12)
  leaf(crown,crown+d*L+Vector((0,0,-.85)),.025,i,.75)

# Wall panels are built around openings, so interior sightlines are actual apertures.
def wall(tag,x,y,w,z,h,openings=(),ang=0,material='Ivory plaster',thick=.23):
 cuts=sorted(set([-w/2,w/2]+[v for u,ww,zz,hh in openings for v in [u-ww/2,u+ww/2]]))
 for a,b in zip(cuts,cuts[1:]):
  if b-a<.001:continue
  mid=(a+b)/2;ops=sorted([o for o in openings if o[0]-o[1]/2<mid<o[0]+o[1]/2],key=lambda o:o[2])
  spans=[];cursor=z
  for op in ops:
   if op[2]>cursor:spans.append((cursor,min(op[2],z+h)))
   cursor=max(cursor,op[2]+op[3])
  if cursor<z+h:spans.append((cursor,z+h))
  for lo,hi in spans:
   if hi>lo:box(tag,(x+mid*math.cos(ang),y+mid*math.sin(ang),(lo+hi)/2),(b-a,thick,hi-lo),material,ang)
def window(x,y,w,bottom,h,ang=0,panes=3,curtains=True,tag='Windows'):
 z=bottom+h/2
 def local(u,d,zz,sz,m,n=tag):box(n,(x+u*math.cos(ang)-d*math.sin(ang),y+u*math.sin(ang)+d*math.cos(ang),zz),sz,m,ang)
 for u in [-w/2,w/2]:local(u,0,z,(.075,.21,h+.15),'Charcoal aluminium')
 for zz in [bottom,bottom+h]:local(0,0,zz,(w+.15,.21,.075),'Charcoal aluminium')
 for i in range(panes):
  u=-w/2+(i+.5)*w/panes;local(u,0,z,(w/panes-.05,.016,h-.07),'Window glass',tag+' Glass')
  if i:local(-w/2+i*w/panes,0,z,(.042,.10,h),'Charcoal aluminium')
 local(0,-.05,bottom-.08,(w+.3,.37,.075),'Pale travertine')
 if curtains and h>1:
  for sg in [-1,1]:
   for j in range(6):local(sg*(w/2-.05-j*.048),.18+.022*math.sin(j),z,(.061,.04,h-.04),'Curtain linen')
def rail(x,y,w,z,ang=0):
 def loc(u,zz,sz,m):box('Balcony railing',(x+u*math.cos(ang),y+u*math.sin(ang),zz),sz,m,ang)
 loc(0,z+.52,(w,.025,.95),'Balustrade glass');loc(0,z+.055,(w,.07,.07),'Charcoal aluminium');loc(0,z+1.035,(w,.035,.035),'Charcoal aluminium')
 for u in [-w/2,w/2]:loc(u,z+.55,(.035,.045,1.03),'Charcoal aluminium')
def slab(x,y,w,d,z,tag='Slabs',wood=True):
 box(tag,(x,y,z),(w,d,.24),'Ivory plaster');box('Shadow reveals',(x,y,z-.13),(w-.10,d-.1,.036),'Charcoal aluminium')
 if wood:box('Timber soffits',(x,y,z-.155),(w-.22,d-.2,.036),'Warm teak')
def lum(name,pos,power=80,target=None,angle=.9,shadow=False):
 kind='spot' if target else 'point';data=bpy.data.lights.new(name,'SPOT' if target else 'POINT');data.energy=power;data.color=(1,.68,.39);data.shadow_soft_size=.22
 if target:data.spot_size=angle*2;data.spot_blend=.7
 o=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(o);o.location=pos
 if target:o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
 lights.append(dict(name=name,kind=kind,position=[pos[0],pos[2],-pos[1]],target=[target[0],target[2],-target[1]] if target else None,intensity=power*.30,angle=angle,shadow=shadow,distance=8))
def down(x,y,z,p=65):
 cyl('Recessed lights',(x,y,z),.065,.022,'Charcoal aluminium');cyl('Light lenses',(x,y,z-.015),.045,.015,'Light diffuser');lum('Soffit downlight',(x,y,z-.06),p,(x,y,.4),.8)
def bed(x,y,z,ang=0):
 def q(dx,dy,zz,sz,m):box('Bedroom furniture',(x+dx*math.cos(ang)-dy*math.sin(ang),y+dx*math.sin(ang)+dy*math.cos(ang),z+zz),sz,m,ang)
 q(0,0,.23,(1.85,2.05,.3),'Warm teak');q(0,0,.47,(1.78,2,.24),'Ivory linen');q(0,.72,.9,(1.92,.12,1.2),'Warm teak');q(0,-.35,.61,(1.79,1.13,.05),'Sage fabric')
 for sg in [-1,1]:q(sg*.46,.57,.64,(.66,.43,.12),'Ivory linen');q(sg*1.25,.65,.3,(.48,.5,.6),'Warm teak');cyl('Lamp shades',(x+sg*1.25,y+.65,z+.98),.16,.25,'Light diffuser',.11)
def chair(x,y,z,ang=0):
 def q(dx,dy,zz,sz,m):box('Chairs',(x+dx*math.cos(ang)-dy*math.sin(ang),y+dx*math.sin(ang)+dy*math.cos(ang),z+zz),sz,m,ang)
 q(0,0,.45,(.5,.5,.1),'Ivory linen');q(0,.23,.75,(.5,.07,.6),'Warm teak')
 for dx in [-.2,.2]:
  for dy in [-.2,.2]:q(dx,dy,.23,(.035,.035,.44),'Warm teak')
def sofa(x,y,z,w=2.5):
 box('Sofa',(x,y,z+.3),(w,.85,.35),'Sage fabric');box('Sofa',(x,y+.38,z+.7),(w,.16,.65),'Sage fabric')
 for sg in [-1,1]:box('Sofa',(x+sg*(w/2-.1),y,z+.6),(.18,.85,.45),'Warm teak')
 for i in range(3):box('Cushions',(x-w/2+.47+i*(w-.8)/2,y+.22,z+.76),(.5,.18,.4),'Ivory linen')

# October reference. Coordinates follow upright plans: front -Y, rear +Y.
LEVEL='Ground'
original_mesh=mesh
def mesh(tag,material,verts,faces):original_mesh(LEVEL+' / '+tag,material,verts,faces)
mat('Ochre plaster',(.62,.30,.045),.86)
mat('Brick mortar',(.39,.17,.08),.95)
for i,c in enumerate([(.55,.20,.085),(.65,.26,.12),(.48,.15,.065),(.70,.30,.15)]):mat('Clay '+str(i),c,.85)
def rect(tag,x1,x2,y1,y2,z,thick=.18,material='Pale travertine'):
 box(tag,((x1+x2)/2,(y1+y2)/2,z),(x2-x1,y2-y1,thick),material)
def metalrail(x,y,w,z,ang=0,h=1.05):
 for zz in [z+.08,z+h]:box('Metal railing',(x,y,zz),(w,.055,.045),'Charcoal aluminium',ang)
 for i in range(int(w/.14)+1):
  u=-w/2+i*w/int(w/.14);box('Metal railing',(x+u*math.cos(ang),y+u*math.sin(ang),z+h/2),(.025,.025,h),'Charcoal aluminium')
def brick(x,y,w,z,h):
 box('Brick accent',(x,y,z+h/2),(w,.18,h),'Brick mortar')
 for j in range(int(h/.10)):
  for i in range(int(w/.25)):
   xx=x-w/2+.13+i*.25+(j%2)*.05
   if xx+.12<x+w/2:box('Brick courses',(xx,y-.1,z+j*.10+.047),(.235,.023,.086),'Clay '+str((i+j)%4))
def door(x,y,z,w=.85,ang=0):
 box('Timber doors',(x,y,z+1.1),(w,.065,2.2),'Warm teak',ang)
def bath(x,y,z,w=1.2,d=2.4):
 rect('Bathroom tile',x-w/2,x+w/2,y-d/2,y+d/2,z+.015,.04,'Silver limestone')
 cyl('WC',(x,y,z+.27),.23,.42,'Ceramic',.18,16);box('WC cistern',(x,y+.22,z+.6),(.44,.18,.58),'Ceramic')
 box('Basin cabinet',(x,y-d/2+.30,z+.38),(.6,.42,.75),'Warm teak');box('Basin',(x,y-d/2+.30,z+.8),(.58,.41,.12),'Ceramic')
 box('Shower screen',(x,y+d/2-.7,z+1.05),(w,.014,2),'Window glass');rod('Shower',(x,y+d/2-.1,z+1.4),(x,y+d/2-.1,z+2.05),.018,'Brass')
def roof(x,y,w,d,eave,rise,rotate=False):
 global mesh
 saved_mesh=mesh
 if rotate:
  def rotated(tag,material,verts,faces):saved_mesh(tag,material,[(x-(b-y),y+(a-x),z) for a,b,z in verts],faces)
  mesh=rotated
  w,d=d,w
 # Ridge runs front-to-back, with curved clay tile courses on both pitches.
 for side in [-1,1]:
  a=x+side*w/2
  mesh('Pitched roof base','Clay 0',[(a,y-d/2,eave),(a,y+d/2,eave),(x,y+d/2,eave+rise),(x,y-d/2,eave+rise)],[(0,1,2,3)] if side<0 else [(3,2,1,0)])
  rows=max(2,int(w/2/.28));cols=max(2,int(d/.25))
  for r in range(rows):
   for c in range(cols):
    vs=[]
    for t in [r/rows,min(1,(r+1.14)/rows)]:
     for k in range(5):
      v=k/4;vs.append((a+(x-a)*t,y-d/2+(c+v)*d/cols,eave+rise*t+.025+.033*math.sin(v*math.pi)))
    mesh('Clay roof tiles','Clay '+str((r+c)%4),vs,[(k,k+1,k+6,k+5) for k in range(4)])
  for yy in [y-d/2,y+d/2]:rod('White fascia',(a,yy,eave),(x,yy,eave+rise),.10,'Ivory plaster',4)
  box('Eave fascia',(a,y,eave-.055),(.13,d,.22),'Ivory plaster')
 rod('Ridge cap',(x,y-d/2,eave+rise+.04),(x,y+d/2,eave+rise+.04),.085,'Clay 1')
 for yy in [y-d/2+.18,y+d/2-.18]:mesh('Gable infill','Ivory plaster',[(x-w/2,yy,eave-.1),(x+w/2,yy,eave-.1),(x,yy,eave+rise-.15)],[(0,1,2)]) if rotate else None
 mesh=saved_mesh

# Footprint calibrated from room labels; 16.9 x 7.9 m including wall thickness.
rect('Main floor',-8.5,8.5,-.15,4,.40)
rect('Kitchen floor',-8.5,-3.55,-3.55,-.15,.40)
rect('Dining floor',-3.55,.5,-4,-.15,.40)
rect('Sitout floor',.5,4.9,-4,-.15,.40)
for z in [.08,.20,.32]:rect('Entry steps',1.2,3.4,-4.65+z,-3.85,z,.12,'Silver limestone')
for level,z in [('Ground',.5),('First',3.8)]:
 LEVEL=level
 # Rear bedrooms and wet rooms retain the same stacked layout.
 for x1,x2 in [(-8.4,-5.23),(4.45,8.35)]:
  w=x2-x1;xc=(x1+x2)/2
  wall('Bedroom rear',xc,3.85,w,z,3.05,[(0,1.65,z+.85,1.55)])
  window(xc,3.86,1.65,z+.85,1.55,curtains=True)
  wall('Bedroom front',xc,.12,w,z,3.05,[(w/2-.55,.85,z,2.2)])
  door(x2-.55,.12,z,.8,math.pi/5)
  bed(xc,2.35,z)
  box('Wardrobes',(xc,.4,z+1.15),(w-1.05,.52,2.3),'Warm teak')
 for x,sg in [(-8.5,-1),(8.5,1)]:
  wall('Bedroom side',x,1.9,4,z,3.05,[(0,1.45,z+.8,1.6)],math.pi/2)
  window(x,1.9,1.45,z+.8,1.6,math.pi/2)
 for x in [-5.12,4.32]:wall('Bedroom partition',x,2,3.7,z,3.05,[],math.pi/2)
 for xc,w in [(-4.4,1.2),(3.38,1.65)]:
  bath(xc,2.57,z,w,2.4 if xc<0 else 2.75)
  wall('Toilet rear',xc,3.85,w,z,3.05,[(0,.65,z+2.1,.5)]);window(xc,3.86,.65,z+2.1,.5,curtains=False)
  wall('Toilet front',xc,1.15,w,z,3.05,[(0,.7,z,2.1)])
  wall('Toilet side',xc-w/2,2.5,2.7,z,3.05,[],math.pi/2)
  door(xc,1.15,z,.65,math.pi/4)
 for xc in [-6.8,6.3]:lum(level+' bedroom',(xc,2.1,z+2.6),130,shadow=level=='Ground')

LEVEL='Ground'
# Kitchen and breakfast opening facing dining.
wall('Kitchen front',-6,-3.55,4.9,.5,3.05,[(0,2.25,1.3,1.4)]);window(-6,-3.58,2.25,1.3,1.4)
wall('Kitchen side',-8.5,-1.75,3.6,.5,3.05,[(0,.9,.5,2.2)],math.pi/2)
door(-8.5,-1.75,.5,.85,math.pi/2)
wall('Kitchen back',-6,-.02,4.9,.5,3.05,[])
for x,y,w,d in [(-6,-3.12,4.3,.6),(-8.05,-1.8,.6,2.4),(-3.8,-2,.55,2.25)]:
 box('Kitchen cabinetry',(x,y,.95),(w,d,.86),'Warm teak');box('Kitchen stone worktop',(x,y,1.41),(w+.05,d+.05,.055),'Slate grey')
box('Sink',(-7,-3.12,1.45),(.65,.43,.04),'Ceramic');box('Hob',(-5.3,-3.12,1.45),(.65,.45,.035),'Screen')
for x in [-5.5,-5.15]:cyl('Hob rings',(x,-3.12,1.48),.105,.015,'Charcoal aluminium')
box('Refrigerator',(-4.3,-.5,1.45),(.75,.68,1.9),'Silver limestone')
for y in [-2.7,-1.8]:chair(-3.1,y,.5,-math.pi/2)
# Dining: 3.80 x 3.90 m. Gable glazing spans both storeys.
wall('Dining side',-3.5,-2,4,.5,6.35,[],math.pi/2)
wall('Dining front',-1.5,-4,4,.5,6.35,[(0,2.65,.75,5.95)])
window(-1.5,-4.03,2.65,.75,5.95,panes=3,curtains=False)
for z in [2,3.5,4.7,5.8]:box('Glazing grid',(-1.5,-4.1,z),(2.65,.055,.04),'Charcoal aluminium')
box('Dining table',(-1.45,-2.2,1.22),(1.15,2.4,.12),'Pale travertine')
for x in [-1.9,-1]:box('Table base',(x,-2.2,.85),(.08,1.7,.7),'Warm teak')
for y in [-3,-2.2,-1.4]:chair(-2.35,y,.5,math.pi/2);chair(-.55,y,.5,-math.pi/2)
lum('Dining pendant',(-1.5,-2.2,4.5),200,shadow=True)
rod('Pendant suspension',(-1.5,-2.2,6.75),(-1.5,-2.2,4.5),.012,'Brass');cyl('Pendant',(-1.5,-2.2,4.5),.38,.13,'Light diffuser')
# Formal living rear, with projecting bay seat.
wall('Formal rear',.7,3.85,3.3,.5,6.3,[(0,2.5,1.0,2),(0,2.5,4.5,1.8)])
for zz in [1,4.5]:window(.7,4.15,2.5,zz,2 if zz==1 else 1.8)
box('Bay seat',(.7,4.03,1.0),(2.45,.60,.18),'Ivory linen')
sofa(.8,2.8,.5,2.7);cyl('Coffee table',(.7,1.8,1),.48,.13,'Warm teak');chair(-.65,1.5,.5)
box('TV console',(2.23,2,.84),(.32,1.9,.6),'Warm teak');box('TV',(2.19,2,1.65),(.04,1.3,.8),'Screen')
lum('Formal living',(.4,1.7,3.1),150)
box('Utility basin',(-3.0,3.5,1.28),(.85,.52,.18),'Ceramic')
# Foyer / sitout access remains open inside.
wall('Entrance',2.7,-1.35,4.4,.5,3.05,[(0,1.3,.5,2.4)])
door(2.7,-1.38,.5,1.25);rod('Entrance handle',(3.12,-1.45,1.4),(3.12,-1.45,2.0),.016,'Brass')
chair(1.25,-2.9,.5,.2);chair(4,-2.9,.5,-.2);pot(4.4,-3.5,.5)
# U staircase: 20 risers, two flights and half landing. No slab across opening.
for i in range(10):
 box('Stair flight one',(-2.6,.1+i*.27,.5+(i+1)*.165/2),(.9,.28,(i+1)*.165),'Pale travertine')
 box('Stair flight two',(-1.55,2.53-i*.27,2.15+(i+1)*.165/2),(.9,.28,(i+1)*.165),'Pale travertine')
rect('Stair landing',-3.1,-1.05,2.7,3.7,2.08,.15)
for x,z1,z2 in [(-3.08,1.45,2.94),(-1.08,4.04,2.56)]:
 rod('Stair handrail',(x,.1,z1),(x,2.55,z2),.025,'Charcoal aluminium')
 for i in range(10):rod('Stair balusters',(x,.1+i*.27,z1-1+(z2-z1)*i/9),(x,.1+i*.27,z1+(z2-z1)*i/9),.012,'Charcoal aluminium')
lum('Stair light',(-2.1,2,5.1),130)
lum('Kitchen ceiling',(-6,-1.9,3.1),160)
wall('Stair rear',-2.15,3.85,2.15,.5,6.35,[(0,1.55,1.0,5.35)])
window(-2.15,3.88,1.55,1.0,5.35,panes=2,curtains=False)
LEVEL='First'
box('Stair bay seating',(-2.15,3.42,4.3),(1.85,.5,.18),'Ivory linen')
LEVEL='Ground'

LEVEL='First'
# Explicit slab rectangles exclude dining [-3.4,.45]x[-4,-1.4], formal [-.95,2.45]x[.2,3.8], stairs.
for r in [(-8.5,-3.55,-3.55,4),(-3.55,4.4,-1.3,.05),(.55,4.9,-4,-1.3),(2.55,8.5,.05,4),(-3.55,-3.15,.05,4),(-3.15,-1.05,3.75,4)]:rect('Upper floor slab',*r,3.68,.24)
for x,y,w,a in [(-6,-3.55,4.9,0),(-8.5,-1.8,3.5,math.pi/2),(2.7,-4,4.4,0),(4.9,-2.65,2.7,math.pi/2),(-1.5,-1.35,3.8,0),(.7,.12,3.3,0)]:metalrail(x,y,w,3.8,a)
sofa(.4,-.7,3.8,2.4);chair(-2.7,-.6,3.8);cyl('Upper coffee table',(-1.6,-.65,4.3),.3,.10,'Warm teak')
box('Ironing table',(3.65,-.65,4.65),(.5,1,.08),'Ivory linen')
for x,y in [(-7.8,-3.1),(-4,-3.1),(1,-3.55),(4.45,-3.55)]:pot(x,y,3.8,.85)
lum('Upper living',(.5,-.65,6.4),150)

LEVEL='Facade'
# Reference ochre right volume and a slim vertical slit, rather than a generic stone wing.
wall('Ochre feature',6.4,.0,4.15,.5,6.45,[(-1.1,.22,4.1,2.25)],material='Ochre plaster')
window(5.3,-.04,.22,4.1,2.25,panes=1,curtains=False)
for x in [5.1,7.1]:box('Ochre grooves',(x,-.125,5.8),(.045,.015,1.85),'Charcoal aluminium')
brick(.65,-4.04,.9,.5,6.5)
brick(-4.4,-3.7,1.05,.5,2.7)
brick(3.75,-4.04,.35,.5,3.3)
# White central gable frame with a true pentagonal glass crown.
mesh('Gable glass','Window glass',[(-2.83,-4.03,6.7),(-.17,-4.03,6.7),(-.17,-4.03,7.25),(-1.5,-4.03,8.35),(-2.83,-4.03,7.25)],[(0,1,2,3,4)])
for a,b in [((-2.83,-4.08,7.25),(-1.5,-4.08,8.35)),((-1.5,-4.08,8.35),(-.17,-4.08,7.25)),((-1.5,-4.08,6.7),(-1.5,-4.08,8.35))]:rod('Gable glazing frame',a,b,.035,'Charcoal aluminium')
for x in [-3.06,.06]:box('Gable white piers',(x,-4,4.1),(.25,.45,7.2),'Ivory plaster')
box('Window planter',(-1.5,-4.4,3.86),(2.7,.55,.36),'Warm teak')
for i in range(9):plant(-2.65+i*.28,-4.43,4.03,.52)
# Portal around lower glazing: softened shoulders formed by short segments.
for x in [-3.05,.05]:box('Entrance portal',(x,-4.35,1.8),(.19,.23,2.6),'Ivory plaster')
box('Entrance portal',(-1.5,-4.35,3.18),(2.95,.23,.19),'Ivory plaster')

LEVEL='Facade'
# Close rear of central gable while keeping front pentagonal glazing.
mesh('Gable rear','Ivory plaster',[(-3.3,-.4,6.85),(.3,-.4,6.85),(-1.5,-.4,8.55)],[(0,1,2)])
LEVEL='Roof'
roof(-1.5,-2.35,3.9,4.05,7.12,1.6)
roof(-6.3,1.95,5.1,4.45,6.9,1.1,True)
roof(6.4,2.0,4.55,4.55,6.95,1.05,True)
roof(2.7,-3.25,3.25,1.8,3.62,.70,True)
rect('Upper hall roof',-3.3,4.4,-1.35,.2,6.98,.22,'Ivory plaster')
rect('Formal ceiling',-1.05,2.55,.2,4.0,6.98,.22,'Ivory plaster')
rect('Wet area roof',2.55,4.4,.2,4,6.98,.22,'Ivory plaster')
for x in [-2.7,-.3,1.5,3.5,5.2,7.5]:down(x,-.1,6.86,65)
for x in [1.5,3.6]:down(x,-3.3,3.60,80)

LEVEL='Site'
rect('Site lawn',-14,14,-11,12,-.12,.2,'Garden lawn')
rect('Entry path',1.3,3.5,-10,-4.1,.015,.05,'Silver limestone')
rect('Front paving',-10,10,-6.2,-4.8,.005,.05,'Silver limestone')
for x in [-7.6,-5,-2.2,5.8,8.1]:
 rect('Planting bed',x-.8,x+.8,-4.9,-4.25,.06,.1,'Dark soil')
 for i in range(5):plant(x-.65+i*.32,-4.6,.12,.8)
 lum('Garden uplight',(x,-4.8,.25),45,(x,-3.5,2),.65)
for x in [-10.2,10.2]:
 rect('Side path',x-.45,x+.45,-5,5,.02,.08,'Silver limestone')
 for y in [-3,0,3,6]:plant(x+.7,y,.05,1.3)
for x,y,h in [(-11,3,8),(11,4,8.5),(-10,9,9),(10,10,9),(-6,10,8.5),(5,10,9)]:palm(x,y,h)
for x in [-11,-8,-4,0,4,8,11]:tree(x,7.5,6.8)
for x,w in [(-5.0,10),(7,6)]:
 box('Compound wall',(x,-7,.43),(w,.20,.85),'Silver limestone')
 for xx in [x-w/2,x+w/2]:box('Compound piers',(xx,-7,.65),(.4,.4,1.3),'Ivory plaster')
 metalrail(x,-7,w,.85,h=.75)
for y in [-5.7,-7.5,-9]:
 for x in [1.05,3.7]:
  box('Path bollard',(x,y,.3),(.07,.07,.6),'Charcoal aluminium');lum('Path light',(x,y,.58),15,(x,y,0),1)

# Baked batches with level metadata for safe floor inspection.
for (tag,m),(verts,faces) in B.items():
 if not verts:continue
 me=bpy.data.meshes.new(tag+' '+m);me.from_pydata(verts,[],faces);me.update()
 o=bpy.data.objects.new(tag+' | '+m,me);bpy.context.collection.objects.link(o);o.data.materials.append(M[m]);o['level']=tag.split(' / ')[0];o['architectural_group']=tag
 uv=me.uv_layers.new(name='UVMap')
 for poly in me.polygons:
  axis=max(range(3),key=lambda k:abs(poly.normal[k]))
  for li in poly.loop_indices:
   v=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=((v.y,v.z) if axis==0 else (v.x,v.z) if axis==1 else (v.x,v.y))
  if 'Foliage' in tag:poly.use_smooth=True
 bpy.context.view_layer.objects.active=o;o.select_set(True)
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT');o.select_set(False)
scene.world=bpy.data.worlds.new('Tropical sky');scene.world.use_nodes=True
bg=scene.world.node_tree.nodes.get('Background');bg.inputs['Color'].default_value=(.66,.78,1,1);bg.inputs['Strength'].default_value=.4
bpy.ops.object.light_add(type='SUN',location=(-10,-10,16));sun=bpy.context.object;sun.name='Sun';sun.data.energy=2;sun.rotation_euler=(.45,-.45,-.45)
for name,pos in [('Front',(0,-31,5.5)),('Back',(0,30,7)),('Aerial',(17,-20,24)),('Top',(0,0,30))]:
 bpy.ops.object.camera_add(location=pos);cam=bpy.context.object;cam.name='Camera '+name;cam.rotation_euler=(Vector((0,0,3.5))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=45
 if name=='Front':scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1400;scene.render.resolution_y=900;scene.render.resolution_percentage=100
out=os.path.join(ROOT,'exports','two-storey');os.makedirs(out,exist_ok=True)
json.dump(lights,open(os.path.join(out,'lighting.json'),'w'),indent=2)
for o in scene.objects:
 if o.type=='LIGHT' and o.name!='Sun':o.data.energy*=.03
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','house.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.join(out,'house.glb'),export_format='GLB',export_cameras=False,export_lights=False,export_extras=True)
sun.data.energy=.15;sun.data.color=(.43,.62,1);bg.inputs['Color'].default_value=(.1,.19,.35,1);bg.inputs['Strength'].default_value=.25
for o in scene.objects:
 if o.type=='LIGHT' and o.name!='Sun':o.data.energy/=.03
M['Light diffuser'].node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=3
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','house-night.blend'))
print('REFERENCE_COMPLETE',len(B),'batches',len(lights),'lights',flush=True)
