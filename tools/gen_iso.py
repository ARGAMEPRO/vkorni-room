import math

K = 50
CX, CY = 640, 340

def P(u, v, z=0.0):
    return (CX + (u - v) * K, CY + (u + v) * K * 0.5 - z * K)

def poly(pts, fill, extra=""):
    s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{s}" fill="{fill}"{extra}/>'

def box(u, v, z, du, dv, dz, top, right, left, extra=""):
    out = []
    A = lambda a, b, c: P(u + a, v + b, z + c)
    out.append(poly([A(0,0,dz), A(du,0,dz), A(du,dv,dz), A(0,dv,dz)], top, extra))
    out.append(poly([A(du,0,0), A(du,dv,0), A(du,dv,dz), A(du,0,dz)], right, extra))
    out.append(poly([A(0,dv,0), A(du,dv,0), A(du,dv,dz), A(0,dv,dz)], left, extra))
    return "".join(out)

def face_u(u, v0, v1, z0, z1, fill, extra=""):
    """Грань в плоскости u=const (смотрит вправо)."""
    return poly([P(u,v0,z0), P(u,v1,z0), P(u,v1,z1), P(u,v0,z1)], fill, extra)

def face_v(v, u0, u1, z0, z1, fill, extra=""):
    """Грань в плоскости v=const (смотрит влево-вперёд)."""
    return poly([P(u0,v,z0), P(u1,v,z0), P(u1,v,z1), P(u0,v,z1)], fill, extra)

def disc(u, v, z, rx, ry, fill, extra=""):
    cx, cy = P(u, v, z)
    return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx}" ry="{ry}" fill="{fill}"{extra}/>'

def shadow(u, v, rx, ry, op=".18"):
    return disc(u, v, 0.015, rx, ry, "#4a3524", f' opacity="{op}" filter="url(#soft)"')

W, R, L = "#c08a5e", "#a3704a", "#8c5f3d"      # дерево
W2, R2, L2 = "#d0a276", "#b48054", "#a06f47"   # светлое дерево

s = []
s.append('<svg viewBox="0 0 1280 940" preserveAspectRatio="xMidYMid slice" id="room" aria-label="Изометрическая комната памяти">')
s.append('''<defs>
<linearGradient id="wl" x1="0" y1="0" x2=".7" y2="1"><stop offset="0" stop-color="#f2e0c6"/><stop offset="1" stop-color="#e0c9a9"/></linearGradient>
<linearGradient id="wr" x1="0" y1="0" x2=".7" y2="1"><stop offset="0" stop-color="#e6cfae"/><stop offset="1" stop-color="#d2b58f"/></linearGradient>
<linearGradient id="fl" x1="0" y1="0" x2=".3" y2="1"><stop offset="0" stop-color="#dcba8f"/><stop offset="1" stop-color="#c09a67"/></linearGradient>
<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c3d3d6"/><stop offset=".5" stop-color="#d9dfd2"/><stop offset="1" stop-color="#efe7d3"/></linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2=".8" y2="1"><stop offset="0" stop-color="#fff6dc" stop-opacity=".85"/><stop offset="1" stop-color="#fff6dc" stop-opacity="0"/></linearGradient>
<radialGradient id="lampglow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffce87" stop-opacity=".85"/><stop offset="1" stop-color="#ffce87" stop-opacity="0"/></radialGradient>
<filter id="soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="softer" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="20"/></filter>
</defs>''')

# ---------------------------------------------------------------- пол, стены
s.append('<g id="layer-back">')
s.append(poly([P(0,0), P(10,0), P(10,10), P(0,10)], "url(#fl)"))
for i in range(1, 10):
    a, b = P(i, 0), P(i, 10)
    s.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#a9825a" stroke-width="1.2" opacity=".35"/>')
for i in range(1, 5):
    a, b = P(0, i*2.0), P(10, i*2.0)
    s.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#b08a5f" stroke-width="1" opacity=".2"/>')
s.append(face_u(0, 0, 10, 0, 5.6, "url(#wl)"))
s.append(face_v(0, 0, 10, 0, 5.6, "url(#wr)"))
s.append(face_u(0, 0, 10, 0, .26, "#cfae87"))
s.append(face_v(0, 0, 10, 0, .26, "#c6a67f"))
s.append('</g>')

# ------------------------------------------------------------------- окно
s.append('<g id="layer-window">')
v0, v1, z0, z1 = 1.7, 5.1, 1.85, 4.55
s.append(face_u(0, v0-.16, v1+.16, z0-.16, z1+.16, "#f7f0e1"))
s.append(face_u(0, v0, v1, z0, z1, "url(#night)"))
vm = (v0+v1)/2
s.append(poly([P(0,v0,z0), P(0,v1,z0), P(0,v1,z0+.9), P(0,v0,z0+.9)], "#cbd6c2", ' opacity=".85"'))
s.append(poly([P(0,v0,z0+.9), P(0,v0+1.5,z0+1.5), P(0,v0+2.6,z0+.9), P(0,v1,z0+.75)], "#b7c6b2", ' opacity=".8"'))
s.append(face_u(0, vm-.04, vm+.04, z0, z1, "#f7f0e1"))
zm = (z0+z1)/2
s.append(face_u(0, v0, v1, zm-.04, zm+.04, "#f7f0e1"))
s.append(face_u(0, v0-.45, v0+.02, z0-.3, z1+.25, "#f4e9d6"))
s.append(face_u(0, v1-.02, v1+.45, z0-.3, z1+.25, "#f4e9d6"))
s.append(face_u(0, v0-.5, v1+.5, z0-.34, z0-.14, "#e3c9a6"))
s.append(poly([P(0,v0-.1,z0-.3), P(0,v1+.1,z0-.3), P(5.2,v1+2.4,0), P(3.0,v0-1.4,0)], "url(#beam)", ' opacity=".7" filter="url(#softer)"'))
s.append('</g>')

# ---------------------------------------------------------------- картины
s.append('<g id="layer-wall">')
def frame(u0, u1, zz0, zz1, art="#efe0c2"):
    inner = face_v(0, u0+.09, u1-.09, zz0+.09, zz1-.09, art)
    a, b = P(u0+.12, 0, zz0+.16), P(u1-.12, 0, zz1-.28)
    inner += poly([(a[0], a[1]), (b[0], a[1]), (b[0], b[1]), (a[0], b[1])], "#b9c6a8", ' opacity=".65"')
    return face_v(0, u0, u1, zz0, zz1, "#a9764f") + inner
s.append(frame(1.35, 2.85, 2.72, 4.35))
s.append('<g class="hot" data-open="photos" tabindex="0" role="button" aria-label="Фотографии">')
s.append(frame(3.15, 4.5, 2.95, 4.2))
s.append(disc(4.31, 0, 3.6, 7, 7, "#ffd79b", ' class="dot"'))
s.append('</g>')
s.append('</g>')

# ------------------------------------------------------------------ полка
s.append('<g id="layer-shelf">')
s.append(face_v(0, 6.15, 9.15, 3.35, 3.5, "#b9855a"))
s.append(face_v(0, 6.15, 9.15, 3.1, 3.35, "#a9764f"))
s.append(box(6.35, .1, 3.5, .3, .3, .46, "#c08a5e", "#a3704a", "#8c5f3d"))
s.append(box(6.95, .1, 3.5, .28, .28, .58, "#a9c6bb", "#8fb0a5", "#7c9f94"))
s.append(box(7.75, .12, 3.5, .55, .26, .3, "#e3d3b6", "#cbb897", "#b9a789"))
s.append('</g>')

# ------------------------------------------------------------------ шкаф
s.append('<g id="layer-sideboard">')
s.append(shadow(8.4, 1.1, 90, 34, ".16"))
s.append(box(7.55, .42, 0, 1.75, .95, 3.05, "#c08a5e", "#a3704a", "#8c5f3d"))
s.append(face_v(1.37, 7.62, 9.23, .1, 2.95, "#b07f55", ' opacity=".45"'))
s.append(face_v(1.37, 8.42, 8.47, .1, 2.95, "#7d5638"))
s.append(disc(8.1, 1.37, 1.5, 3.4, 4.2, "#f0dcb8"))
s.append(disc(8.75, 1.37, 1.5, 3.4, 4.2, "#f0dcb8"))
s.append('</g>')

# ------------------------------------------------------------------- кровать
s.append('<g id="layer-chair">')
s.append(shadow(1.6, 6.6, 165, 56, ".16"))
s.append(box(0.12, 5.5, 0, 2.95, 2.1, .45, W, R, L))
s.append(box(0.18, 5.56, .45, 2.83, 1.98, .24, "#f4ece0", "#e2d6c6", "#d6c8b4"))
s.append(box(1.3, 5.56, .69, 1.71, 1.98, .17, "#bccfb4", "#a5b99e", "#97ab91"))
s.append(poly([P(1.3,7.54,.86), P(3.01,7.54,.86), P(3.01,7.54,.18), P(1.3,7.54,.18)], "#a8bda1"))
s.append(poly([P(1.3,7.54,.18), P(1.6,7.54,.02), P(1.6,7.54,.12), P(1.3,7.54,.28)], "#9fb598"))
s.append(box(0.26, 5.6, .69, .86, .9, .19, "#fbf6ec", "#ece3d4", "#e0d5c2"))
s.append(box(0.26, 6.6, .69, .8, .86, .17, "#f4ecdd", "#e4d9c8", "#d8ccb8"))
s.append(box(0.05, 5.45, 0, .14, 2.2, 1.62, "#b9855a", "#96684a", "#83593f"))
s.append(box(0.07, 5.48, 1.3, .1, 2.14, .1, "#d0a276", "#b48054", "#a06f47"))
s.append('<g class="hot" data-open="letter-chair" tabindex="0" role="button" aria-label="Плед">')
s.append(disc(1.3, 7.3, .93, 8, 8, "#ffd79b", ' class="dot"'))
s.append('</g>')
s.append('</g>')

# ------------------------------------------------------------ тумбочка, лампа
s.append('<g id="layer-table">')
s.append(shadow(3.6, 6.5, 64, 24, ".16"))
s.append(box(3.22, 6.15, 0, .82, .82, .95, W2, R2, L2))
s.append(box(3.29, 6.22, .22, .68, .68, .46, "#dcb992", "#c39d74", "#b18c66"))
s.append(disc(3.62, 6.55, .95, 30, 11, "#b9855a"))
s.append('<ellipse class="lamp-glow" id="lampGlow" cx="%d" cy="%d" rx="200" ry="150" fill="url(#lampglow)" opacity=".95"/>' % P(3.62, 6.55, 1.2))
s.append('<g class="hot" data-open="lamp" tabindex="0" role="button" aria-label="Лампа">')
s.append(box(3.55, 6.48, .95, .14, .14, .42, "#e6d3ac", "#cdb98f", "#bfab83"))
s.append(poly([P(3.41,6.34,1.62), P(3.89,6.34,1.62), P(4.01,6.95,1.5), P(3.29,6.95,1.5)], "#f7e8c6"))
s.append('<ellipse class="lamp-core" id="lampCore" cx="%d" cy="%d" rx="130" ry="100" fill="url(#lampglow)" opacity=".8"/>' % P(3.62, 6.6, 1.28))
s.append(disc(3.62, 6.6, 1.6, 8, 8, "#ffd79b", ' class="dot"'))
s.append('</g>')
s.append('</g>')

# ---------------------------------------------------------- стол, патефон, листы
s.append('<g id="layer-rug">')
rug = [P(0.9, 8.1), P(4.5, 8.1), P(5.4, 10.0), P(1.5, 10.0)]
s.append(poly(rug, "#ded8bd"))
for i in range(1, 6):
    a, b = P(0.9 + i*0.6, 8.1), P(1.5 + i*0.65, 10.0)
    s.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#c3c9a8" stroke-width="9" opacity=".75"/>')
s.append(poly([P(0.9, 8.1), P(4.5, 8.1), P(4.42, 8.28), P(0.98, 8.28)], "#cdc7a9"))
s.append('</g>')

s.append('<g id="layer-plant">')
s.append(shadow(6.3, 8.5, 105, 40, ".18"))
s.append(disc(6.2, 8.5, 0, 52, 21, "#8c5f3d"))
s.append(box(6.14, 8.44, .02, .16, .16, .8, W, R, L))
s.append(disc(6.2, 8.5, .82, 118, 46, "#d0a276"))
s.append(disc(6.2, 8.5, .80, 112, 43, "#c08a5e"))
s.append('<g class="hot" data-open="voice" tabindex="0" role="button" aria-label="Патефон с записью">')
s.append(box(5.72, 8.02, .82, .8, .7, .3, "#5f4a3a", "#4a3a2d", "#3f3227"))
s.append(box(6.62, 8.62, .82, .62, .44, .12, "#c9a878", "#b08f63", "#a08056"))
s.append(box(6.66, 8.66, .94, .54, .38, .1, "#a9c6bb", "#8fb0a5", "#7c9f94"))
s.append(disc(6.32, 8.42, 1.08, 23, 9, "#2a2320"))
s.append(disc(6.32, 8.42, 1.1, 7, 3, "#c9b48a"))
s.append(disc(6.32, 8.42, 1.2, 7, 7, "#ffd79b", ' class="dot"'))
s.append('</g>')
for (u, v, w, h) in ((6.75, 7.55, .55, .4), (7.35, 8.7, .5, .36), (5.55, 9.15, .5, .34)):
    s.append(poly([P(u,v,.02), P(u+w,v,.02), P(u+w,v+h,.02), P(u,v+h,.02)], "#efe6d2", ' opacity=".95"'))
    s.append(poly([P(u,v,.02), P(u+w,v,.02), P(u+w,v+h*.55,.02), P(u,v+h*.55,.02)], "#ddd0b8", ' opacity=".7"'))
s.append('</g>')

# ------------------------------------------------------------------ растение
s.append('<g id="layer-dust">')
s.append(shadow(9.05, 6.6, 52, 20, ".16"))
s.append(poly([P(8.6,6.1,0), P(9.42,6.1,0), P(9.28,7.05,0), P(8.74,7.05,0)], "#a9764f"))
s.append(face_u(9.42, 6.1, 7.05, 0, .56, "#c08a5e"))
s.append(face_v(7.05, 8.6, 9.42, 0, .52, "#8c5f3d"))
cx, cy = P(9.01, 6.58, .56)
for ang, ln, col in ((-58, 96, "#84a37c"), (-30, 112, "#8fae86"), (-6, 120, "#9dba92"), (20, 104, "#8fae86"), (46, 86, "#a3c09b"), (70, 68, "#8fae86")):
    rad = math.radians(ang - 90)
    ox = cx + math.cos(rad) * 8
    oy = cy + math.sin(rad) * 4
    ex = ox + math.cos(rad) * ln
    ey = oy + math.sin(rad) * ln * 0.6 + ln * 0.32
    ctrl_x = (ox + ex) / 2 + math.cos(rad + 1.2) * 14
    ctrl_y = (oy + ey) / 2 - 10
    s.append(f'<path d="M{ox:.1f} {oy:.1f} Q{ctrl_x:.1f} {ctrl_y:.1f} {ex:.1f} {ey:.1f}" stroke="{col}" stroke-width="7.5" stroke-linecap="round" fill="none"/>')
s.append('</g>')

# ------------------------------------------------------------------- гирлянда
s.append('<g id="layer-clock">')
cxc, cyc = P(0, 6.9, 3.9)
s.append(f'<circle cx="{cxc:.1f}" cy="{cyc:.1f}" r="26" fill="#f4e9d6" stroke="#a9764f" stroke-width="3"/>')
s.append(f'<line x1="{cxc:.1f}" y1="{cyc:.1f}" x2="{cxc:.1f}" y2="{cyc-14:.1f}" stroke="#8c5f3d" stroke-width="2.4"/>')
s.append(f'<line x1="{cxc:.1f}" y1="{cyc:.1f}" x2="{cxc+10:.1f}" y2="{cyc+4:.1f}" stroke="#8c5f3d" stroke-width="2.4"/>')
s.append('</g>')

s.append('<g id="layer-garland">')
def garland(points, color="#ffe4a8"):
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    out = f'<path d="{d}" stroke="#6b5442" stroke-width="1.5" fill="none" opacity=".55"/>'
    for i, (x, y) in enumerate(points):
        if i % 2 == 0 and i:
            out += (f'<circle cx="{x:.1f}" cy="{y+4:.1f}" r="10" fill="{color}" opacity=".22"/>'
                    f'<circle cx="{x:.1f}" cy="{y+4:.1f}" r="3.6" fill="{color}"/>')
    return out

def sag(a, b, drop=0.55, n=7):
    out = []
    for i in range(n):
        t = i / (n - 1)
        u = a[0] + (b[0]-a[0])*t
        v = a[1] + (b[1]-a[1])*t
        out.append(P(u, v, 5.35 - math.sin(math.pi*t) * drop))
    return out

s.append(garland(sag((0, 0.5), (0, 5.4))))
s.append(garland(sag((0, 5.4), (0, 9.9))))
s.append(garland(sag((0.5, 0), (5.2, 0))))
s.append(garland(sag((5.2, 0), (9.9, 0))))
s.append('</g>')

s.append('</svg>')
open('/tmp/iso_room.svg', 'w').write("".join(s))
print("ok", len("".join(s)))
