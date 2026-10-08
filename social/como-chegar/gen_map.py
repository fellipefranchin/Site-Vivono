# -*- coding: utf-8 -*-
import json, math, html

LAT0, LON0 = 38.9340341, -9.3273352
# frame: metres, isotropic. north up.
SCALE = 2.66             # px per metre
VBW, VBH = 1000, 816
# frame centre offset from our point (metres, +E,+N): push view east & slightly south
FCX, FCY = 30.0, -10.0
X0, Y0 = VBW/2.0, VBH/2.0

def proj(lat, lon):
    mx = (lon-LON0)*math.cos(math.radians(LAT0))*111320.0
    my = (lat-LAT0)*110540.0
    X = X0 + (mx-FCX)*SCALE
    Y = Y0 - (my-FCY)*SCALE
    return X, Y

def geom_xy(e):
    return [proj(p['lat'], p['lon']) for p in e.get('geometry',[])]

def centroid(pts):
    if not pts: return (0,0)
    return (sum(p[0] for p in pts)/len(pts), sum(p[1] for p in pts)/len(pts))

def area(pts):
    a=0
    for i in range(len(pts)):
        x1,y1=pts[i]; x2,y2=pts[(i+1)%len(pts)]
        a+=x1*y2-x2*y1
    return abs(a)/2.0

def path_d(pts, close=False):
    if not pts: return ""
    d="M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts)
    if close: d+=" Z"
    return d

roads = json.load(open("overpass.json"))['elements']
extra = json.load(open("overpass2.json"))['elements']

# ---------- collect layers ----------
green=[]; buildings=[]; parking=[]; steps=[]; foot=[]; road_ways=[]; bus_nodes=[]
for e in roads:
    t=e.get('tags',{})
    if e['type']=='way' and t.get('amenity')=='parking': parking.append(e)
    elif e['type']=='way' and t.get('highway')=='steps': steps.append(e)
    elif e['type']=='way' and t.get('highway') in ('footway','path','pedestrian'): foot.append(e)
    elif e['type']=='way' and t.get('highway'): road_ways.append(e)
    elif e['type']=='node' and (t.get('public_transport')=='station' or t.get('amenity')=='bus_station'):
        bus_nodes.append(e)
for e in extra:
    t=e.get('tags',{})
    if t.get('building'): buildings.append(e)
    elif t.get('landuse') or t.get('leisure') or t.get('natural'): green.append(e)

# our building = building polygon whose centroid nearest pin(project of LAT0,LON0)
pinX,pinY = proj(LAT0,LON0)
def dist2(c): return (c[0]-pinX)**2+(c[1]-pinY)**2
our=None; best=1e18
for e in buildings:
    pts=geom_xy(e)
    if len(pts)<3: continue
    c=centroid(pts); dd=dist2(c)
    # must be reasonably close
    if dd<best and dd < (26*SCALE)**2:
        best=dd; our=e

# big back parking = parking with centroid east (X>pinX+30) & largest area
back=None; barea=0; front=None; farea=0
for e in parking:
    pts=geom_xy(e);
    if len(pts)<3: continue
    c=centroid(pts); ar=area(pts)
    if c[0] > pinX+25:
        if ar>barea: barea=ar; back=e
    elif c[0] < pinX-10:
        if ar>farea: farea=ar; front=e

# connecting steps: east of pin, within ~95m
conn_steps=[]
for e in steps:
    pts=geom_xy(e)
    if len(pts)<2: continue
    c=centroid(pts)
    if c[0]>pinX and abs(c[1]-pinY)<150 and (c[0]-pinX)<120:
        conn_steps.append((e,pts,c))

# named road pick nearest-centre segment
def road_label_pos(name):
    best=None; bd=1e18
    for e in road_ways:
        if e.get('tags',{}).get('name','').lower()!=name.lower(): continue
        pts=geom_xy(e)
        for i in range(len(pts)-1):
            mx=(pts[i][0]+pts[i+1][0])/2; my=(pts[i][1]+pts[i+1][1])/2
            d=(mx-X0)**2+(my-Y0)**2
            if d<bd:
                bd=d; ang=math.degrees(math.atan2(pts[i+1][1]-pts[i][1], pts[i+1][0]-pts[i][0]))
                if ang>90: ang-=180
                if ang<-90: ang+=180
                best=(mx,my,ang)
    return best

# ---------- draw ----------
S=[]
def add(s): S.append(s)

# green areas
for e in green:
    pts=geom_xy(e)
    if len(pts)<3: continue
    t=e.get('tags',{})
    fill="#c9d3b0"
    if t.get('natural')=='wood': fill="#b9c79f"
    elif t.get('natural')=='scrub': fill="#c6cfa6"
    elif t.get('leisure')=='garden': fill="#cdd7b6"
    elif t.get('landuse')=='grass': fill="#d0dab7"
    add(f'<path d="{path_d(pts,True)}" fill="{fill}" fill-opacity="0.9"/>')

# buildings (skip our)
bpath=[]
for e in buildings:
    if e is our: continue
    pts=geom_xy(e)
    if len(pts)<3: continue
    bpath.append(path_d(pts,True))
add(f'<path d="{" ".join(bpath)}" fill="#E1D4C1" stroke="#D0BFA6" stroke-width="0.8"/>')

# road casing then fill
def road_style(hw):
    return {'primary':(13,'#E4D6BF',8.5,'#F7F2EA'),
            'secondary':(11,'#E4D6BF',7,'#F7F2EA'),
            'residential':(8.5,'#E0D2BB',5.5,'#F7F2EA'),
            'living_street':(8.5,'#E0D2BB',5.5,'#F7F2EA'),
            'unclassified':(8,'#E0D2BB',5,'#F7F2EA'),
            'service':(4.5,'#E4D8C4',2.8,'#F5F0E7'),
            'track':(3.5,'#E4D8C4',2,'#F0E9DC'),
            }.get(hw,(4.5,'#E4D8C4',2.8,'#F5F0E7'))
# casing pass
for e in road_ways:
    hw=e.get('tags',{}).get('highway')
    pts=geom_xy(e)
    if len(pts)<2: continue
    cw,cc,fw,fc=road_style(hw)
    add(f'<path d="{path_d(pts)}" fill="none" stroke="{cc}" stroke-width="{cw}" stroke-linecap="round" stroke-linejoin="round"/>')
for e in road_ways:
    hw=e.get('tags',{}).get('highway')
    pts=geom_xy(e)
    if len(pts)<2: continue
    cw,cc,fw,fc=road_style(hw)
    add(f'<path d="{path_d(pts)}" fill="none" stroke="{fc}" stroke-width="{fw}" stroke-linecap="round" stroke-linejoin="round"/>')

# footpaths
for e in foot:
    pts=geom_xy(e)
    if len(pts)<2: continue
    add(f'<path d="{path_d(pts)}" fill="none" stroke="#cbb98f" stroke-width="1.6" stroke-dasharray="4 4" stroke-linecap="round"/>')

# parking polygons
for e in parking:
    pts=geom_xy(e)
    if len(pts)<3: continue
    t=e.get('tags',{})
    free = t.get('fee')=='no'
    add(f'<path d="{path_d(pts,True)}" fill="#E9DBBD" stroke="#B79A5F" stroke-width="1.4" fill-opacity="0.95"/>')

# our building highlight + pin done later (labels layer)
if our:
    pts=geom_xy(our)
    add(f'<path d="{path_d(pts,True)}" fill="#54272E" stroke="#3A1A1F" stroke-width="1.2"/>')

# connecting steps emphasised (tread ticks)
for e,pts,c in conn_steps:
    add(f'<path d="{path_d(pts)}" fill="none" stroke="#9a7b3f" stroke-width="6" stroke-linecap="round"/>')
    # ticks
    for i in range(len(pts)-1):
        x1,y1=pts[i]; x2,y2=pts[i+1]
        seg=math.hypot(x2-x1,y2-y1);
        if seg<1: continue
        nx,ny=-(y2-y1)/seg,(x2-x1)/seg
        n=max(1,int(seg/5))
        for k in range(n+1):
            tx=x1+(x2-x1)*k/n; ty=y1+(y2-y1)*k/n
            add(f'<line x1="{tx-nx*4:.1f}" y1="{ty-ny*4:.1f}" x2="{tx+nx*4:.1f}" y2="{ty+ny*4:.1f}" stroke="#F1E8DA" stroke-width="1.4"/>')

core="\n".join(S)

# expose useful coords for label placement
import pickle
ctx=dict(pinX=pinX,pinY=pinY,
         our_c=centroid(geom_xy(our)) if our else None,
         back_c=centroid(geom_xy(back)) if back else None,
         front_c=centroid(geom_xy(front)) if front else None,
         steps_c=(sum(c[0] for _,_,c in conn_steps)/len(conn_steps), sum(c[1] for _,_,c in conn_steps)/len(conn_steps)) if conn_steps else None,
         bus=[proj(b['lat'],b['lon']) for b in bus_nodes],
         jose=road_label_pos('Rua José Silvestre'),
         av=road_label_pos('Avenida Movimento das Forças Armadas'),
         canal=road_label_pos('Rua do Canal'),
         VBW=VBW,VBH=VBH)
open("map_core.svg","w").write(core)
pickle.dump(ctx, open("map_ctx.pkl","wb"))
print("core elements:", len(S))
print("our building found:", our is not None, "dist_px", best**0.5 if our else None)
print("back parking:", ctx['back_c'], "front:", ctx['front_c'])
print("steps cluster:", ctx['steps_c'], "n_conn_steps", len(conn_steps))
print("bus nodes px:", ctx['bus'])
print("jose:", ctx['jose'])
print("av:", ctx['av'])
print("canal:", ctx['canal'])
print("pin px:", (round(pinX),round(pinY)))
