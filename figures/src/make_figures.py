# Generates the Render Hell figures in figures/. Run: python3 figures/src/make_figures.py
import os, math
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')  # writes into figures/
# Palette matches .vscode/markdown-preview.css: strokes in the accent colour, fills as light tints
NAVY='#1d2a44'; SOFT='#3d5a80'; GREEN='#4d7a2a'; ORANGE='#b5562a'
PANEL='#f2f4f7'; RULE='#d5dae2'; TEXT='#1f2328'; MUTED='#5b6573'; WHITE='#ffffff'
LORANGE='#f6e3da'   # CPU work / mesh B / state commands
LNAVY='#dde4ef'     # fixed-function GPU hardware
LGREEN='#e3edda'    # programmable shaders / GPU work / covered pixels
GREY='#eef0f3'      # system memory
FONT="Charter, 'CMU Serif', 'Latin Modern Roman', Palatino, Georgia, serif"

class S:
    def __init__(s,w,h): s.w,s.h=w,h; s.b=[]
    def rect(s,x,y,w,h,fill=WHITE,stroke=None,rx=4,sw=1,dash=None,op=None):
        rx=0; sw=min(sw,0.9)
        a=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
        if stroke: a+=f' stroke="{stroke}" stroke-width="{sw}"'
        if dash: a+=f' stroke-dasharray="{dash}"'
        if op: a+=f' opacity="{op}"'
        s.b.append(a+'/>')
    def text(s,x,y,t,size=12,anchor='middle',weight='normal',fill=TEXT,italic=False):
        if y==28 and size==14: return
        weight='normal' if weight=='bold' and size<12 else weight
        st=' font-style="italic"' if italic else ''
        t=t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
        s.b.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}"{st}>{t}</text>')
    def lines(s,x,y,ts,size=12,lh=None,**k):
        lh=lh or size*1.25
        y0=y-(len(ts)-1)*lh/2
        for i,t in enumerate(ts): s.text(x,y0+i*lh+size*0.35,t,size,**k)
    def line(s,x1,y1,x2,y2,stroke='#1d2a44',sw=0.9,arrow=False,dash=None):
        a=f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"'
        if dash: a+=f' stroke-dasharray="{dash}"'
        if arrow: a+=' marker-end="url(#ah)"'
        s.b.append(a+'/>')
    def path(s,d,stroke='#1d2a44',sw=0.9,fill='none',arrow=False,dash=None):
        a=f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}"'
        if dash: a+=f' stroke-dasharray="{dash}"'
        if arrow: a+=' marker-end="url(#ah)"'
        s.b.append(a+'/>')
    def poly(s,pts,fill,stroke=None,sw=1,op=None):
        a=f'<polygon points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="{fill}"'
        if stroke: a+=f' stroke="{stroke}" stroke-width="{sw}"'
        if op: a+=f' opacity="{op}"'
        s.b.append(a+'/>')
    def raw(s,x): s.b.append(x)
    def save(s,name):
        svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s.w} {s.h-30}" width="{s.w}" height="{s.h-30}" font-family="{FONT}">'
             f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d2a44"/></marker>'
             f'<pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#ffffff"/><line x1="0" y1="0" x2="0" y2="6" stroke="#9aa3b2" stroke-width="0.6"/></pattern><pattern id="hatchO" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#f6e3da"/><line x1="0" y1="0" x2="0" y2="6" stroke="#b5562a" stroke-width="0.7"/></pattern></defs>'
             f'<rect x="0" y="0" width="{s.w}" height="{s.h-30}" fill="#ffffff"/>'
             + '<g transform="translate(0,-30)">'+'\n'.join(s.b)+'</g></svg>')
        open(os.path.join(OUT,name),'w').write(svg)

def legend(s,x,y,items,size=11):
    for fill,stroke,label in items:
        s.rect(x,y-9,14,12,fill,stroke,rx=2); s.text(x+20,y+1,label,size,'start',fill=MUTED)
        x+=34+len(label)*6.2

# ---------- Book I ----------
def fig_memory():
    s=S(720,360)
    s.text(360,28,'Memory hierarchy: data moves towards the cores',14,weight='bold',fill=NAVY)
    levels=[('HDD / SSD','terabytes','system',GREY,MUTED),
            ('RAM (system memory)','gigabytes','system',GREY,MUTED),
            ('VRAM (graphics card memory)','e.g. 6 GB on GTX 1660 Ti','card',LNAVY,SOFT),
            ('L2 cache','GM204: 2048 KB','chip',LGREEN,GREEN),
            ('L1 cache','GM204: 384 KB (4 × 4 × 24 KB)','chip',LGREEN,GREEN),
            ('Registers (register file)','inputs/outputs of the cores','chip',LGREEN,GREEN)]
    cx=330; top=55; h=36; gap=8
    for i,(n,sz,g,f,st) in enumerate(levels):
        w=460-i*54; y=top+i*(h+gap)
        s.rect(cx-w/2,y,w,h,f,st,rx=5)
        s.text(cx,y+h/2+4,n,12,weight='bold',fill=NAVY)
        s.text(cx+w/2+10,y+h/2+4,sz,11,'start',fill=MUTED)
        if i<len(levels)-1: s.line(cx,y+h,cx,y+h+gap,stroke=MUTED,sw=1.2,arrow=True)
    # group brackets
    def br(i0,i1,label,col):
        y0=top+i0*(h+gap); y1=top+i1*(h+gap)+h; x=78
        s.path(f'M{x+8},{y0} L{x},{y0} L{x},{y1} L{x+8},{y1}',stroke=col,sw=1.6)
        s.lines(x-8,(y0+y1)/2,label,11,anchor='end',fill=col,weight='bold')
    br(0,1,['system','(CPU side)'],MUTED); br(2,2,['graphics','card'],SOFT); br(3,5,['GPU chip','(on-chip)'],GREEN)
    # axis
    s.line(670,330,670,60,arrow=True)
    s.lines(650,345,['smaller, faster, closer to cores ↑'],10,anchor='end',fill=MUTED,italic=True)
    s.save('rh1-memory-hierarchy.svg')

def fig_cmdbuf():
    s=S(720,250)
    s.text(360,28,'Command buffer: CPU and GPU work independently',14,weight='bold',fill=NAVY)
    s.rect(30,80,120,80,LORANGE,ORANGE,rx=6); s.lines(90,120,['CPU','(+ driver)'],13,weight='bold',fill=ORANGE)
    s.rect(570,80,120,80,LGREEN,GREEN,rx=6); s.lines(630,120,['GPU'],13,weight='bold',fill=GREEN)
    cmds=[('draw',LGREEN,GREEN),('state',LORANGE,ORANGE),('draw',LGREEN,GREEN),('draw',LGREEN,GREEN),('state',LORANGE,ORANGE),('draw',LGREEN,GREEN)]
    x0=200; w=52; g=8
    s.rect(x0-10,90,len(cmds)*(w+g)+10,60,PANEL,RULE,rx=6)
    for i,(c,f,st) in enumerate(cmds):
        s.rect(x0+i*(w+g),100,w,40,f,st,rx=4); s.text(x0+i*(w+g)+w/2,124,c,11,weight='bold',fill=st)
    s.line(152,120,186,120,arrow=True); s.line(x0+len(cmds)*(w+g)+2,120,566,120,arrow=True)
    s.text(205,82,'newest',10,'start',fill=MUTED,italic=True); s.text(x0+len(cmds)*(w+g)-g,82,'oldest',10,'end',fill=MUTED,italic=True)
    s.text(90,185,'pushes commands',11,fill=MUTED); s.text(630,185,'takes the oldest (FIFO)',11,fill=MUTED)
    s.text(360,185,'queue of commands: draw calls and render-state changes',11,fill=MUTED)
    s.text(360,220,'Neither side waits for the other: the CPU keeps adding, the GPU keeps consuming.',12,fill=TEXT,italic=True)
    s.save('rh1-command-buffer.svg')

# ---------- Book II ----------
def fig_pipeline():
    s=S(720,430)
    s.text(360,28,'Logical pipeline (NVIDIA-style, simplified)',14,weight='bold',fill=NAVY)
    CPU=(LORANGE,ORANGE,None); FIX=(LNAVY,SOFT,None); PRG=(LGREEN,GREEN,None)
    OPTF=(LNAVY,SOFT,'4 3'); OPTP=(LGREEN,GREEN,'4 3')
    rows=[[('Application',CPU),('Driver','→ command buffer',CPU),('Host interface','reads commands',FIX),('Data fetch','copy engine',FIX)],
          [('Gigathread engine','threads → blocks',FIX),('Vertex fetch','Polymorph engine',FIX),('Vertex shader',PRG),('Tessellation','optional',OPTP)],
          [('Primitive assembly',FIX),('Geometry shader','optional',OPTP),('Viewport & clipping','guard band',FIX),('Triangle distribution','to rasterisers',FIX)],
          [('Rasterisation','backface cull, 2×2 quads',FIX),('Z-cull','tile depth test',FIX),('Pixel shader',PRG),('Raster output (ROP)','blend → frame buffer',FIX)]]
    bw=140; bh=56; xs=[40,210,380,550]; ys=[60,150,240,330]; n=1
    for r,row in enumerate(rows):
        for c,item in enumerate(row):
            name=item[0]; sub=item[1] if len(item)==3 else None; f,st,d=item[-1]
            x=xs[c]; y=ys[r]
            s.rect(x,y,bw,bh,f,st,rx=6,dash=d,sw=1.4)
            s.text(x+12,y+15,str(n),9,'start',weight='bold',fill=st); n+=1
            if sub: s.text(x+bw/2,y+28,name,12,weight='bold',fill=NAVY); s.text(x+bw/2,y+44,sub,10,fill=MUTED)
            else: s.text(x+bw/2,y+bh/2+5,name,12,weight='bold',fill=NAVY)
            if c<3: s.line(x+bw+2,y+bh/2,xs[c+1]-3,y+bh/2,arrow=True)
        if r<3:
            y=ys[r]+bh; s.path(f'M{xs[3]+bw/2},{y+2} L{xs[3]+bw/2},{y+17} L{xs[0]+bw/2},{y+17} L{xs[0]+bw/2},{ys[r+1]-3}',arrow=True)
    s.line(20,140,700,140,stroke=RULE,dash='3 3') if False else None
    legend(s,120,410,[(LORANGE,ORANGE,'CPU'),(LNAVY,SOFT,'fixed-function GPU hardware'),(LGREEN,GREEN,'programmable (runs on SM cores)'),(WHITE,MUTED,'dashed = optional')])
    s.save('rh2-pipeline.svg')

def fig_gpu_org():
    s=S(720,400)
    s.text(360,28,'Work distribution on the GPU',14,weight='bold',fill=NAVY)
    s.rect(230,48,260,50,LNAVY,SOFT,rx=6); s.text(360,70,'Gigathread engine',13,weight='bold',fill=NAVY); s.text(360,87,'one thread per vertex/pixel → thread blocks',10,fill=MUTED)
    xs=[40,260,480]
    for i,x in enumerate(xs):
        s.line(360,100,x+100,138,arrow=True)
        s.rect(x,140,200,170,PANEL,NAVY,rx=6,sw=1.2)
        s.text(x+100,160,f'Streaming Multiprocessor {i+1}' if i<2 else 'SM … n',12,weight='bold',fill=NAVY)
        s.rect(x+10,170,180,24,LNAVY,SOFT,rx=4); s.text(x+100,186,'Polymorph engine (vertex fetch)',10,fill=NAVY)
        s.rect(x+10,200,180,24,WHITE,RULE,rx=4); s.text(x+100,216,'warp pool: up to 64 warps × 32 threads',10,fill=TEXT)
        # 4 schedulers each 32 cores
        for k in range(4):
            sx=x+10+k*45
            s.rect(sx,230,42,16,LNAVY,SOFT,rx=2); s.text(sx+21,242,'sched',8,fill=NAVY)
            for a in range(4):
                for b in range(2):
                    s.rect(sx+3+a*9.5,250+b*10,8,8,LGREEN,GREEN,rx=1)
        s.text(x+100,282,'4 schedulers × 32 cores (Maxwell)',9,fill=MUTED)
        s.rect(x+10,288,180,16,WHITE,RULE,rx=3); s.text(x+100,300,'registers · L1',9,fill=MUTED)
        s.line(x+100,310,x+100,328,arrow=True)
    s.rect(40,330,640,24,LGREEN,GREEN,rx=4); s.text(360,346,'L2 cache (shared)',11,weight='bold',fill=GREEN)
    s.rect(40,362,640,24,LNAVY,SOFT,rx=4); s.text(360,378,'VRAM (frame buffer, vertex buffers, textures)',11,weight='bold',fill=NAVY)
    s.save('rh2-gpu-organisation.svg')

def fig_divergence():
    s=S(720,330)
    s.text(360,28,'Lock-step execution and branch divergence in one warp',14,weight='bold',fill=NAVY)
    lanes=8; x0=250; cw=46; ch=30; y0=70
    s.text(x0+lanes*cw/2,56,'threads of one warp (8 of 32 shown)',10,fill=MUTED,italic=True)
    for l in range(lanes): s.text(x0+l*cw+cw/2,y0-2,f't{l}',9,fill=MUTED)
    cond=[1,1,0,1,0,0,1,1]
    instr=[('n = texture(normalMap, uv)',None),('if (c)',None),('    a = expensiveLight(n)','then'),('    a = ambient','else'),('color = a * albedo',None)]
    for r,(t,kind) in enumerate(instr):
        y=y0+6+r*(ch+8)
        s.text(40,y+ch/2+4,t,11,'start',fill=NAVY,weight='bold' if kind is None else 'normal')
        for l in range(lanes):
            act= kind is None or (kind=='then' and cond[l]) or (kind=='else' and not cond[l])
            if act: s.rect(x0+l*cw+3,y,cw-6,ch,LGREEN,GREEN,rx=3)
            else: s.rect(x0+l*cw+3,y,cw-6,ch,'url(#hatch)',RULE,rx=3)
    s.line(x0+lanes*cw+20,y0+6,x0+lanes*cw+20,y0+6+5*(ch+8)-8,stroke=NAVY,arrow=True); s.lines(x0+lanes*cw+34,y0+100,['time'],10,anchor='start',fill=MUTED)
    legend(s,170,300,[(LGREEN,GREEN,'active lane'),('url(#hatch)',RULE,'masked (idle) lane')])
    s.text(360,318,'Both sides of the branch run one after another; masked lanes wait.',11,fill=TEXT,italic=True)
    s.save('rh2-divergence.svg')

def fig_latency():
    s=S(720,250)
    s.text(360,28,'Latency hiding: switching warps on a memory stall',14,weight='bold',fill=NAVY)
    x0=130; u=36
    rows=[('Warp A',[(0,3,'run'),(3,6,'wait'),(9,2,'run')]),('Warp B',[(3,3,'run'),(6,5,'wait'),(11,2,'run')]),('Warp C',[(6,3,'run'),(9,2,'wait')])]
    for r,(n,segs) in enumerate(rows):
        y=60+r*38
        s.text(x0-12,y+18,n,12,'end',weight='bold',fill=NAVY)
        s.rect(x0,y,13*u,26,PANEL,None,rx=3)
        for a,l,k in segs:
            if k=='run': s.rect(x0+a*u,y,l*u,26,LGREEN,GREEN,rx=3); s.text(x0+a*u+l*u/2,y+17,'executing',10,fill=GREEN)
            else: s.rect(x0+a*u,y,l*u,26,'url(#hatch)',RULE,rx=3); s.text(x0+a*u+l*u/2,y+17,'waiting for memory' if l>=4 else 'waiting',10,fill=MUTED)
    y=60+3*38+6
    s.text(x0-12,y+18,'Cores',12,'end',weight='bold',fill=NAVY)
    for a,l,c in [(0,3,'A'),(3,3,'B'),(6,3,'C'),(9,2,'A'),(11,2,'B')]:
        s.rect(x0+a*u,y,l*u-2,26,LNAVY,SOFT,rx=3); s.text(x0+a*u+l*u/2,y+17,c,11,weight='bold',fill=NAVY)
    s.line(x0,y+40,x0+13*u,y+40,stroke=NAVY,arrow=True); s.text(x0+13*u,y+55,'time',10,'end',fill=MUTED)
    s.text(360,y+70,'The SM keeps many warps resident so the cores always have a ready one.',11,fill=TEXT,italic=True)
    s.h=y+84; s.save('rh2-latency-hiding.svg')

# ---------- Book III ----------
def fig_drawcalls():
    s=S(720,300)
    s.text(360,28,'Many small draw calls make the CPU the bottleneck',14,weight='bold',fill=NAVY)
    x0=120; W=560
    def rowlab(y,t): s.text(x0-12,y+17,t,12,'end',weight='bold',fill=NAVY)
    # (a)
    s.text(40,62,'(a) many small draw calls',12,'start',weight='bold',fill=TEXT)
    rowlab(72,'CPU'); rowlab(106,'GPU')
    s.rect(x0,72,W,26,PANEL,None,rx=3); s.rect(x0,106,W,26,PANEL,None,rx=3)
    n=12; cw=W/n
    for i in range(n):
        s.rect(x0+i*cw+1,72,cw-2,26,LORANGE,ORANGE,rx=2)
        s.rect(x0+i*cw+cw*0.55+12,106,cw*0.25,26,LGREEN,GREEN,rx=2)
    s.text(x0+cw/2,90,'API',9,fill=ORANGE)
    s.text(x0+W/2,148,'CPU busy with API/driver/OS work for every call; GPU mostly idle',11,fill=MUTED,italic=True)
    # (b)
    s.text(40,182,'(b) the same work in few large submissions',12,'start',weight='bold',fill=TEXT)
    rowlab(192,'CPU'); rowlab(226,'GPU')
    s.rect(x0,192,W,26,PANEL,None,rx=3); s.rect(x0,226,W,26,PANEL,None,rx=3)
    s.rect(x0,192,70,26,LORANGE,ORANGE,rx=2); s.text(x0+35,209,'submit',10,fill=ORANGE)
    s.rect(x0+72,192,W-72,26,LNAVY,SOFT,rx=2); s.text(x0+72+(W-72)/2,209,'free for game logic, AI, physics',10,fill=NAVY)
    s.rect(x0+80,226,200,26,LGREEN,GREEN,rx=2); s.text(x0+180,243,'render',10,fill=GREEN)
    s.line(x0,270,x0+W,270,stroke=NAVY,arrow=True); s.text(x0+W,285,'time',10,'end',fill=MUTED)
    s.save('rh3-draw-calls.svg')

def fig_frames():
    s=S(720,230)
    s.text(360,28,'Queued (pre-rendered) frames: the CPU runs ahead of the GPU',14,weight='bold',fill=NAVY)
    x0=120; u=100
    s.text(x0-12,77,'CPU',12,'end',weight='bold',fill=NAVY); s.text(x0-12,121,'GPU',12,'end',weight='bold',fill=NAVY)
    for i in range(5):
        s.rect(x0+i*u+1,60,u-2,26,LORANGE,ORANGE,rx=3); s.text(x0+i*u+u/2,77,f'build frame {i+1}',10,fill=ORANGE)
    for i in range(3):
        s.rect(x0+(i+2)*u+1,104,u-2,26,LGREEN,GREEN,rx=3); s.text(x0+(i+2)*u+u/2,121,f'render frame {i+1}',10,fill=GREEN)
    s.rect(x0+1,104,2*u-2,26,'url(#hatch)',RULE,rx=3)
    s.path(f'M{x0+u/2},{88} C{x0+u/2},{170} {x0+4.5*u},{170} {x0+4.5*u},{134}',stroke=NAVY,arrow=True,dash='4 3')
    s.text(x0+2.5*u,180,'input read while building frame 1 is shown only after the GPU renders it: added latency',11,fill=NAVY)
    s.text(360,210,'Driver setting: "maximum pre-rendered frames"',11,fill=MUTED,italic=True)
    s.save('rh3-prerendered-frames.svg')

def fig_flush():
    s=S(720,300)
    s.text(360,28,'A render-state change can flush the pipeline',14,weight='bold',fill=NAVY)
    stages=['vertex','raster','pixel','ROP']; x0=130; u=34
    def panel(y0,title,flush):
        s.text(40,y0-8,title,12,'start',weight='bold',fill=TEXT)
        for k,st in enumerate(stages):
            y=y0+k*24; s.text(x0-10,y+15,st,10,'end',fill=NAVY); s.rect(x0,y,13*u,20,PANEL,None,rx=2)
        jobs=[(0,'A',LGREEN,GREEN),(1,'A',LGREEN,GREEN),(2,'A',LGREEN,GREEN)]
        bstart=3 if not flush else 6
        jobs+= [(bstart,'B',LORANGE,ORANGE),(bstart+1,'B',LORANGE,ORANGE),(bstart+2,'B',LORANGE,ORANGE)]
        for t,l,f,stc in jobs:
            for k in range(4):
                x=x0+(t+k)*u; y=y0+k*24
                s.rect(x+1,y,u-2,20,f,stc,rx=2); s.text(x+u/2,y+14,l,10,weight='bold',fill=stc)
        if flush:
            s.rect(x0+3*u,y0-2,3*u,4*24,'none',NAVY,rx=3,dash='4 3')
            s.text(x0+4.5*u,y0+4*24+12,'drain: wait for A to finish',10,fill=NAVY)
    panel(62,'(a) same render state: mesh B follows A immediately',False)
    panel(186,'(b) new render state for B: pipeline drains first',True)
    legend(s,600,90,[(LGREEN,GREEN,'mesh A')]); legend(s,600,112,[(LORANGE,ORANGE,'mesh B')])
    s.save('rh3-state-flush.svg')

def fig_quads():
    s=S(720,372)
    s.text(360,28,'Pixels are shaded in 2×2 quads: thin triangles waste work',14,weight='bold',fill=NAVY)
    def inside(p,a,b,c):
        def sg(p1,p2,p3): return (p1[0]-p3[0])*(p2[1]-p3[1])-(p2[0]-p3[0])*(p1[1]-p3[1])
        d1,d2,d3=sg(p,a,b),sg(p,b,c),sg(p,c,a)
        return not ((d1<0 or d2<0 or d3<0) and (d1>0 or d2>0 or d3>0))
    def grid(ox,oy,tri,title):
        N=12; c=20
        cov={(i,j) for i in range(N) for j in range(N) if inside((i+.5,j+.5),*tri)}
        quads={(i//2,j//2) for i,j in cov}
        for qi,qj in quads: s.rect(ox+qi*2*c,oy+qj*2*c,2*c,2*c,'url(#hatchO)',None,rx=0)
        for i,j in cov: s.rect(ox+i*c,oy+j*c,c,c,LGREEN,None,rx=0)
        for k in range(N+1):
            sw=1.2 if k%2==0 else .5; col=MUTED if k%2==0 else RULE
            s.line(ox+k*c,oy,ox+k*c,oy+N*c,stroke=col,sw=sw); s.line(ox,oy+k*c,ox+N*c,oy+k*c,stroke=col,sw=sw)
        s.poly([(ox+x*c,oy+y*c) for x,y in tri],'none',NAVY,1.6)
        lanes=len(quads)*4; eff=100*len(cov)/lanes
        s.text(ox+N*c/2,oy-10,title,12,weight='bold',fill=TEXT)
        s.text(ox+N*c/2,oy+N*c+22,f'{len(cov)} pixels covered / {lanes} lanes shaded = {eff:.0f}% useful',11,fill=NAVY)
    grid(60,70,[(1.2,1.5),(10.8,2.3),(4.6,10.6)],'(a) compact triangle')
    grid(420,70,[(0.4,1.2),(11.6,9.6),(11.2,10.9)],'(b) long thin triangle')
    legend(s,170,352,[(LGREEN,GREEN,'covered pixel (useful)'),('url(#hatchO)',ORANGE,'helper lane in a touched quad (wasted)')])
    s.save('rh3-quad-overshading.svg')

# ---------- Book IV ----------
MAT={'A':(LGREEN,GREEN),'B':(LORANGE,ORANGE),'C':(LNAVY,SOFT)}

def fig_sorting():
    s=S(720,250)
    s.text(360,28,'Sorting by render state',14,weight='bold',fill=NAVY)
    def row(y,label,seq):
        s.text(40,y-10,label,12,'start',weight='bold',fill=TEXT)
        x=40; cur=None; changes=0
        for m in seq:
            if m!=cur:
                s.rect(x,y,30,34,NAVY,NAVY); s.text(x+15,y+21,'set',10,fill=WHITE)
                x+=34; cur=m; changes+=1
            f,st=MAT[m]; s.rect(x,y,40,34,f,st); s.text(x+20,y+21,'draw '+m,10,fill=st)
            x+=44
        s.text(680,y-10,f'{len(seq)} draws, {changes} state changes',11,'end',weight='bold',fill=NAVY)
    row(66,'(a) submission order of the scene',['A','B','A','C','B','A','C','B'])
    row(150,'(b) sorted by render state',sorted(['A','B','A','C','B','A','C','B']))
    legend(s,40,222,[(NAVY,NAVY,'set render state'),(LGREEN,GREEN,'material A'),(LORANGE,ORANGE,'material B'),(LNAVY,SOFT,'material C')])
    s.save('rh4-sorting.svg')

def stone(s,cx,cy,f,st,k=1):
    s.poly([(cx-14*k,cy+8*k),(cx-10*k,cy-8*k),(cx+2*k,cy-13*k),(cx+14*k,cy-4*k),(cx+12*k,cy+10*k),(cx-2*k,cy+13*k)],f,st,0.9)
def chair(s,cx,cy,f,st,k=1):
    s.rect(cx-10*k,cy-16*k,4*k,30*k,f,st); s.rect(cx-10*k,cy,20*k,4*k,f,st); s.rect(cx+6*k,cy+4*k,4*k,10*k,f,st)
def sword(s,cx,cy,f,st,k=1):
    s.poly([(cx-2*k,cy-18*k),(cx+2*k,cy-18*k),(cx+2*k,cy+6*k),(cx-2*k,cy+6*k)],f,st,0.9)
    s.rect(cx-9*k,cy+6*k,18*k,3*k,f,st); s.rect(cx-1.5*k,cy+9*k,3*k,8*k,f,st)
def bullet(s,cx,cy,f,st,k=1):
    s.rect(cx-10*k,cy-3*k,20*k,6*k,f,st)

def draw_box(s,x,y,label='draw call'):
    s.rect(x,y,70,26,LORANGE,ORANGE); s.text(x+35,y+17,label,10,fill=ORANGE)

def fig_batch_inst():
    s=S(720,420)
    s.text(360,28,'One draw call per mesh, batching and instancing',14,weight='bold',fill=NAVY)
    G=(LGREEN,GREEN)
    # (a)
    y=70; s.text(40,y-14,'(a) one draw call per mesh (same render state)',12,'start',weight='bold',fill=TEXT)
    for i,fn in enumerate([stone,chair,sword]):
        x=60+i*170; fn(s,x+20,y+22,*G); s.line(x+42,y+22,x+66,y+22,arrow=True); draw_box(s,x+68,y+9)
    s.text(680,y+27,'3 draw calls',12,'end',weight='bold',fill=NAVY)
    # (b)
    y=180; s.text(40,y-14,'(b) batching: different meshes combined into one',12,'start',weight='bold',fill=TEXT)
    s.rect(60,y-4,150,52,PANEL,SOFT,dash='4 3'); stone(s,90,y+22,*G); chair(s,135,y+22,*G); sword(s,180,y+22,*G)
    s.text(135,y+62,'combined once in RAM',10,fill=MUTED)
    s.line(214,y+22,290,y+22,arrow=True); s.text(252,y+14,'upload',10,fill=MUTED)
    s.rect(294,y+4,90,36,LNAVY,SOFT); s.text(339,y+26,'VRAM',11,fill=NAVY)
    s.line(386,y+22,420,y+22,arrow=True); draw_box(s,424,y+9)
    s.text(680,y+27,'1 draw call',12,'end',weight='bold',fill=NAVY)
    # (c)
    y=300; s.text(40,y-14,'(c) instancing: one mesh + per-instance data',12,'start',weight='bold',fill=TEXT)
    bullet(s,85,y+8,*G); s.text(85,y+30,'one mesh',10,fill=MUTED)
    s.rect(60,y+40,170,22,PANEL,SOFT)
    for i in range(5): s.rect(64+i*33,y+43,30,16,WHITE,SOFT); s.text(79+i*33,y+55,f'M{i}',9,fill=NAVY)
    s.text(145,y+76,'per-instance data (e.g. matrices)',10,fill=MUTED)
    s.line(234,y+26,290,y+26,arrow=True); draw_box(s,294,y+13)
    s.line(366,y+26,420,y+26,arrow=True); s.text(393,y+18,'GPU',10,fill=MUTED)
    for (dx,dy,r) in [(0,0,0),(35,-12,0),(70,8,0),(25,26,0),(95,-6,0),(120,20,0),(60,40,0)]: bullet(s,440+dx,y+14+dy,*G,k=0.8)
    s.text(680,y+31,'1 draw call',12,'end',weight='bold',fill=NAVY)
    s.save('rh4-batching-instancing.svg')

def fig_batch_cull():
    s=S(720,340)
    s.text(360,28,'Batching defeats per-object culling',14,weight='bold',fill=NAVY)
    objs=[(110,-20),(160,40),(225,-55),(260,70),(195,5),(150,92),(245,-98),(80,42)]
    def inside(dx,dy): return dx>0 and abs(dy)+11<=dx*0.35
    def panel(ox,title,batched):
        oy=190
        s.text(ox+150,62,title,12,weight='bold',fill=TEXT)
        s.poly([(ox,oy),(ox+300,oy-105),(ox+300,oy+105)],PANEL,SOFT,0.9)
        s.poly([(ox-8,oy-6),(ox+6,oy),(ox-8,oy+6)],NAVY)
        if batched:
            xs=[ox+dx for dx,dy in objs]; ys=[oy+dy for dx,dy in objs]
            s.rect(min(xs)-16,min(ys)-16,max(xs)-min(xs)+32,max(ys)-min(ys)+32,'none',ORANGE,dash='4 3')
        for dx,dy in objs:
            vis=inside(dx,dy)
            if batched: f,st=(LORANGE,ORANGE)
            else: f,st=((LGREEN,GREEN) if vis else ('url(#hatch)',RULE))
            s.rect(ox+dx-11,oy+dy-11,22,22,f,st)
    panel(40,'(a) separate objects: outside ones are culled',False)
    panel(390,'(b) one batched mesh: everything is drawn',True)
    legend(s,90,330,[(LGREEN,GREEN,'drawn, visible'),('url(#hatch)',RULE,'culled'),(LORANGE,ORANGE,'drawn as part of the batch'),(PANEL,SOFT,'camera frustum')])
    s.save('rh4-batching-culling.svg')

def fig_vignette():
    s=S(720,270)
    s.text(360,28,'Reducing overdraw of a full-screen vignette',14,weight='bold',fill=NAVY)
    W,H=260,150; ix,iy=46,32
    def panel(ox,title,hollow):
        oy=78
        s.text(ox+W/2,62,title,12,weight='bold',fill=TEXT)
        s.rect(ox,oy,W,H,'url(#hatchO)',ORANGE)
        if hollow:
            s.rect(ox+ix,oy+iy,W-2*ix,H-2*iy,WHITE,ORANGE,dash='4 3')
            o=[(ox,oy),(ox+W,oy),(ox+W,oy+H),(ox,oy+H)]; i=[(ox+ix,oy+iy),(ox+W-ix,oy+iy),(ox+W-ix,oy+H-iy),(ox+ix,oy+H-iy)]
            for k in range(4):
                s.line(*o[k],*i[k],stroke=ORANGE,sw=0.7); s.line(*o[k],*i[(k+1)%4],stroke=ORANGE,sw=0.7)
            s.text(ox+W/2,oy+H/2+4,'not drawn',11,fill=MUTED,italic=True)
            share=100*(W*H-(W-2*ix)*(H-2*iy))/(W*H)
        else:
            s.line(ox,oy,ox+W,oy+H,stroke=ORANGE,sw=0.7)
            s.rect(ox+W/2-70,oy+H/2-11,140,22,WHITE,None); s.text(ox+W/2,oy+H/2+4,'100% transparent, still shaded',10,fill=MUTED,italic=True)
            share=100
        s.text(ox+W/2,oy+H+22,f'pixels shaded: {share:.0f}% of the screen',11,fill=NAVY)
    panel(60,'(a) full-screen quad with a texture',False)
    panel(400,'(b) hollow quad mesh, vertex colours',True)
    s.save('rh4-vignette-overdraw.svg')

# ---------- Book V ----------
def fig_problem_map():
    probs=['Many draw calls (III.1–2)','Many materials / state changes (III.3)','Meshes with several materials (III.4)','Many moving objects (IV.2)','Overdraw (III.7)','Thin triangles (III.6)']
    sols=['Fewer, larger meshes (V)','Sorting by render state (IV.1)','Batching (IV.2)','Instancing (IV.3)','Shared materials, texture atlas (V)','Multi-material shader (IV.4)','Skinned meshes (IV.5)','Hollow / fitted meshes (IV.6)','One big full-screen triangle (III.6)']
    edges=[(0,0),(0,2),(0,3),(1,1),(1,4),(2,5),(2,4),(3,3),(3,6),(4,7),(5,8)]
    s=S(720,30+40+len(sols)*40+20)
    s.text(360,28,'Render Hell: problems and solutions',14,weight='bold',fill=NAVY)
    s.text(150,52,'Problem (Book III)',12,weight='bold',fill=ORANGE); s.text(560,52,'Solution (Books III–V)',12,weight='bold',fill=GREEN)
    py=lambda i: 70+i*(len(sols)*40/len(probs))+ (len(sols)*40/len(probs)-30)/2
    sy=lambda j: 70+j*40
    for i,j in edges:
        y1=py(i)+15; y2=sy(j)+15
        s.path(f'M282,{y1} C360,{y1} 360,{y2} 428,{y2}',stroke=SOFT,sw=0.8,arrow=True)
    for i,t in enumerate(probs):
        s.rect(40,py(i),240,30,LORANGE,ORANGE); s.text(160,py(i)+19,t,11,fill=ORANGE)
    for j,t in enumerate(sols):
        s.rect(432,sy(j),250,30,LGREEN,GREEN); s.text(557,sy(j)+19,t,11,fill=GREEN)
    s.save('rh5-problems-solutions.svg')

# ---------- Life of a triangle ----------
def fig_lot_hierarchy():
    s=S(720,420)
    s.text(360,28,'GPU hierarchy since Fermi',14,weight='bold',fill=NAVY)
    top=[('Host interface',40),('Front end',200),('Primitive distributor',360),('Giga Thread Engine',540)]
    for t,x in top:
        s.rect(x,50,140 if x<540 else 140,32,LNAVY,SOFT); s.text(x+70,70,t,11,fill=NAVY)
    for a,b in [(180,200),(340,360)]: s.line(a+1,66,b-3,66,arrow=True)
    s.text(610,96,'manages all work',9,fill=MUTED,italic=True)
    gx=[40,205,370,535]
    for i,x in enumerate(gx):
        s.line(430,82,x+75,116,arrow=True)
        s.rect(x,118,150,150,PANEL,NAVY)
        s.text(x+75,134,f'GPC {i}',11,weight='bold',fill=NAVY)
        s.rect(x+10,142,130,22,LNAVY,SOFT); s.text(x+75,157,'Raster engine',10,fill=NAVY)
        for k in range(4):
            sx=x+10+(k%2)*67; sy=170+(k//2)*46
            s.rect(sx,sy,63,42,LGREEN,GREEN); s.text(sx+31,sy+17,'SM',10,weight='bold',fill=GREEN)
            s.rect(sx+5,sy+24,53,13,LNAVY,SOFT); s.text(sx+31,sy+34,'PolyMorph',8,fill=NAVY)
        s.line(x+75,268,x+75,284,arrow=True)
    s.rect(40,286,645,26,LNAVY,SOFT); s.text(362,303,'Work distribution crossbar (moves work between GPCs and to ROPs)',11,fill=NAVY)
    for i,x in enumerate(gx):
        s.line(x+75,312,x+75,326,arrow=True)
        s.rect(x,328,150,26,LNAVY,SOFT); s.text(x+75,345,'ROP partition · L2 slice',10,fill=NAVY)
    s.rect(40,364,645,26,GREY,MUTED); s.text(362,381,'DRAM (VRAM)',11,fill=NAVY)
    s.text(362,410,'Drawn for GM204 (4 GPCs × 4 SMs); Tegra X1 has 1 GPC × 2 SMs of the same Maxwell design.',10,fill=MUTED,italic=True)
    s.save('lot-gpu-hierarchy.svg')

def fig_lot_journey():
    cols=['CPU','Front end','GPC A','Crossbar','GPC B','ROP']
    CPU=(LORANGE,ORANGE); FIX=(LNAVY,SOFT); PRG=(LGREEN,GREEN)
    steps=[(0,['draw call','driver → pushbuffer'],CPU),
           (1,['host interface','front end'],FIX),
           (1,['primitive distrib.','→ triangle batches'],FIX),
           (2,['vertex fetch','PolyMorph engine'],FIX),
           (2,['vertex shader','warps of 32 threads'],PRG),
           (2,['viewport','+ clipping'],FIX),
           (3,['crossbar','by bounding box'],FIX),
           (4,['attribute setup','interpolants'],FIX),
           (4,['raster engine','cull, 2×2 quads'],FIX),
           (4,['pixel shader','32 threads / warp'],PRG),
           (5,['ROP','depth test, blend'],FIX)]
    cw=112; x0=24; y0=84; rh=40
    s=S(720,y0+len(steps)*rh+40)
    s.text(360,28,'Life of one triangle',14,weight='bold',fill=NAVY)
    for c,t in enumerate(cols):
        x=x0+c*cw
        s.rect(x+2,y0-26,cw-4,len(steps)*rh+28,PANEL if c%2==0 else WHITE,RULE)
        s.text(x+cw/2,y0-10,t,11,weight='bold',fill=ORANGE if c==0 else NAVY)
    prev=None
    for i,(c,t,(f,st)) in enumerate(steps):
        x=x0+c*cw+5; y=y0+i*rh+4; w=cw-10; h=rh-8
        s.rect(x,y,w,h,f,st)
        s.text(x+3,y+8,str(i+1),7,'start',fill=st)
        s.text(x+w/2,y+15,t[0],9.5,fill=NAVY); s.text(x+w/2,y+27,t[1],8.5,fill=MUTED)
        if prev:
            px,py,pw,ph=prev
            if px==x: s.line(x+w/2,py+ph,x+w/2,y-1,arrow=True)
            else: s.path(f'M{px+pw/2},{py+ph} L{px+pw/2},{y+h/2} L{x-2},{y+h/2}' if x>px else f'M{px+pw/2},{py+ph} L{px+pw/2},{y+h/2} L{x+w+2},{y+h/2}',arrow=True)
        prev=(x,y,w,h)
    s.save('lot-triangle-journey.svg')

def fig_lot_sync():
    s=S(720,300)
    s.text(360,28,'Why a CPU–GPU sync point hurts',14,weight='bold',fill=NAVY)
    x0,y0,W,H=90,60,580,150
    s.line(x0,y0+H,x0+W+10,y0+H,arrow=True); s.line(x0,y0+H,x0,y0-10,arrow=True)
    s.text(x0+W+10,y0+H+16,'time',10,'end',fill=MUTED)
    s.lines(x0-10,y0+10,['GPU units','busy'],10,anchor='end',fill=MUTED)
    top=y0+15; bot=y0+H
    s.path(f'M{x0},{bot} C{x0+30},{bot} {x0+40},{top} {x0+80},{top} L{x0+W},{top}',stroke=SOFT,sw=1,dash='4 3')
    d=(f'M{x0},{bot} C{x0+30},{bot} {x0+40},{top} {x0+80},{top} L{x0+200},{top} '
       f'C{x0+230},{top} {x0+240},{bot} {x0+270},{bot} L{x0+340},{bot} '
       f'C{x0+380},{bot} {x0+400},{top} {x0+450},{top} L{x0+W},{top}')
    s.path(d+f' L{x0+W},{bot} Z',stroke='none',fill=LGREEN)
    s.path(d,stroke=GREEN,sw=1.4)
    s.line(x0+200,y0-5,x0+200,bot,stroke=ORANGE,dash='3 3')
    s.text(x0+200,y0-10,'CPU waits for a GPU result',10,fill=ORANGE)
    for a,b,t in [(200,270,'drain'),(270,340,'idle'),(340,450,'ramp-up')]:
        s.line(x0+a,bot+22,x0+b,bot+22,stroke=NAVY,sw=0.8); s.line(x0+a,bot+18,x0+a,bot+26,stroke=NAVY,sw=0.8); s.line(x0+b,bot+18,x0+b,bot+26,stroke=NAVY,sw=0.8)
        s.text(x0+(a+b)/2,bot+38,t,10,fill=NAVY)
    legend(s,x0+20,bot+64,[(LGREEN,GREEN,'with a sync point'),(WHITE,SOFT,'dashed: no sync, GPU stays loaded')])
    s.save('lot-sync-stall.svg')

# ---------- Giesen ----------
def fig_g_stack():
    s=S(720,470)
    s.text(360,28,'The software stack',14,weight='bold',fill=NAVY)
    C=(LORANGE,ORANGE); OS=(GREY,MUTED); HW=(LNAVY,SOFT)
    # bands
    for y,h,t in [(48,160,'user mode · one set per process'),(214,110,'kernel mode / OS · one per system'),(330,120,'bus and GPU')]:
        s.rect(30,y,660,h,PANEL if t.startswith('k') else WHITE,RULE)
        s.text(40,y+14,t,9,'start',fill=MUTED,italic=True)
    for i,(x,dash) in enumerate([(60,None),(230,'4 3')]):
        for j,t in enumerate(['Application','API runtime','User-mode driver (UMD)']):
            y=68+j*46
            s.rect(x,y,150,32,*C,dash=dash); s.text(x+75,y+20,t if i==0 or j else 'Another app',11,fill=ORANGE)
            if j<2: s.line(x+75,y+32,x+75,y+44,arrow=True)
        s.path(f'M{x+75},{68+2*46+32} L{x+75},{196} L{225},{196} L{225},{232}',arrow=True)
    rows=[(234,'Graphics scheduler',OS),(280,'Kernel-mode driver (KMD)',C),(348,'PCI Express bus',OS),(396,'Command processor (GPU front end)',HW)]
    for y,t,(f,st) in rows:
        s.rect(60,y,320,32,f,st); s.text(220,y+20,t,11,fill=NAVY)
    for a,b in [(266,278),(312,346),(380,394)]: s.line(220,a,220,b,arrow=True)
    notes=[(84,['validates calls, tracks state,','manages resources']),
           (130,['(API runtime / UMD boundary is','blurrier in OpenGL)']),
           (176,['compiles shaders, translates state,','writes command (DMA) buffers']),
           (250,['time-slices the GPU between apps;','context switch = extra commands']),
           (296,['maps memory, owns the main ring','buffer, updates read/write pointers']),
           (364,['DMA transfers and pointer writes']),
           (412,['reads the commands (Part 2)'])]
    for y,t in notes:
        s.line(392,y,412,y,stroke=RULE)
        s.lines(420,y,t,10,anchor='start',fill=MUTED)
    s.save('g1-software-stack.svg')

def fig_g_ring():
    s=S(720,380)
    s.text(360,28,'Main ring buffer and DMA buffers',14,weight='bold',fill=NAVY)
    slots=['init','call DMA 1','call DMA 2','call DMA 3','','','','']
    x0=60; w=72; y=110
    s.text(x0,y-56,'main command buffer (small ring buffer, written by the KMD)',11,'start',weight='bold',fill=NAVY)
    for i,t in enumerate(slots):
        f,st=((LNAVY,SOFT) if t else (WHITE,RULE))
        s.rect(x0+i*w,y,w-4,34,f,st); s.text(x0+i*w+(w-4)/2,y+21,t,10,fill=NAVY)
    s.text(x0+8*w+4,y+21,'↺ wraps',10,'start',fill=MUTED,italic=True)
    for i,lab,col in [(1,'read pointer (GPU)',GREEN),(4,'write pointer (KMD)',ORANGE)]:
        x=x0+i*w; s.line(x,y-28,x,y-3,stroke=col,arrow=True); s.text(x,y-34,lab,10,fill=col)
    by=y+120
    s.text(x0,by+108,'command (DMA) buffers, written by the UMD in GPU-addressable memory',11,'start',weight='bold',fill=NAVY)
    for k in range(3):
        bx=x0+k*200
        s.rect(bx,by,180,90,LORANGE,ORANGE)
        s.text(bx+90,by+16,f'DMA buffer {k+1}',10,weight='bold',fill=ORANGE)
        for r,c in enumerate(['set state','draw','draw','upload texture'][:4]):
            s.rect(bx+12,by+22+r*16,156,14,WHITE,RULE); s.text(bx+90,by+33+r*16,c,9,fill=TEXT)
        sx=x0+(k+1)*w+(w-4)/2
        s.path(f'M{sx},{y+34} C{sx},{by-40} {bx+90},{by-50} {bx+90},{by-2}',stroke=SOFT,sw=0.8,arrow=True)
    s.text(360,by+130,'Both pointers are memory-mapped GPU registers; the KMD advances the write pointer when it submits new work.',10,fill=MUTED,italic=True)
    s.save('g1-ring-buffer.svg')

def fig_g_swizzle():
    s=S(720,330)
    s.text(360,28,'Linear, tiled and Morton (Z-order) layouts',14,weight='bold',fill=NAVY)
    N=8; c=24
    def morton(x,y):
        r=0
        for b in range(3): r|=((x>>b)&1)<<(2*b) | ((y>>b)&1)<<(2*b+1)
        return r
    layouts=[('(a) linear (row-major)',lambda x,y:y*N+x),
             ('(b) 4×4 tiles',lambda x,y:((y//4)*2+(x//4))*16+(y%4)*4+(x%4)),
             ('(c) Morton order',morton)]
    fills=[(LGREEN,GREEN),(LORANGE,ORANGE),(LNAVY,SOFT),(GREY,MUTED)]
    for k,(title,f) in enumerate(layouts):
        ox=40+k*228; oy=66
        s.text(ox+N*c/2,oy-12,title,12,weight='bold',fill=TEXT)
        idx={(x,y):f(x,y) for x in range(N) for y in range(N)}
        for (x,y),i in idx.items():
            fl,st=fills[i//16]
            s.rect(ox+x*c,oy+y*c,c,c,fl,RULE,sw=0.5)
            s.text(ox+x*c+c/2,oy+y*c+c/2+4,str(i),8.5,fill=st)
        # vertical access: column x=1, rows 0..3
        lines={idx[(1,y)]//16 for y in range(4)}
        s.rect(ox+1*c,oy,c,4*c,'none',NAVY,sw=0.9)
        s.text(ox+N*c/2,oy+N*c+20,f'4 pixels down a column touch {len(lines)} cache line'+('s' if len(lines)>1 else ''),10,fill=NAVY)
        if k==2:
            pts=sorted(idx,key=lambda p:idx[p])[:16]
            d='M'+' L'.join(f'{ox+x*c+c/2},{oy+y*c+c/2}' for x,y in pts)
            pass
    s.text(360,316,'Numbers are memory order; colours mark 64-byte cache lines (16 pixels of 32 bpp).',10,fill=MUTED,italic=True)
    s.save('g1-swizzling.svg')

def fig_g_ringmodels():
    s=S(720,326)
    s.text(360,28,'Two ways to index a ring buffer',14,weight='bold',fill=NAVY)
    N=8; w=48; ox=60
    def ring(oy,title,rlab,wlab,note):
        s.text(ox,oy-46,title,12,'start',weight='bold',fill=TEXT)
        for i in range(N):
            used = i>=6 or i<2
            s.rect(ox+i*w,oy,w-4,32,LGREEN if used else WHITE,GREEN if used else RULE)
            s.text(ox+i*w+(w-4)/2,oy+20,str(i),10,fill=MUTED)
        for i,lab,col in [(6,rlab,GREEN),(2,wlab,ORANGE)]:
            x=ox+i*w; s.line(x,oy-20,x,oy-3,stroke=col,arrow=True); s.text(x,oy-24,lab,10,fill=col)
        s.lines(ox+N*w+24,oy+16,note,10,anchor='start',fill=NAVY)
    ring(96,'Model 1: positions are array indices','ReadPos = 6','WritePos = 2',
         ['count = WritePos + SIZE − ReadPos = 4','(case distinction when wrapped);','full and empty both give Read = Write,','so stop at SIZE − 1 elements'])
    ring(226,'Model 2: virtual stream (distance travelled)','ReadPos = 14','WritePos = 18',
         ['count = WritePos − ReadPos = 4 (always)','slot = Pos mod SIZE (cheap for 2ⁿ);','full = (WritePos − ReadPos == SIZE),','no ambiguity'])
    s.text(360,312,'Same buffer state (SIZE = 8, 4 elements stored, wrapped around), described by two index models.',10,fill=MUTED,italic=True)
    s.save('g1-ring-models.svg')

def fig_g2_memory():
    s=S(720,300)
    s.text(360,28,'Bandwidth vs latency (2011 numbers)',14,weight='bold',fill=NAVY)
    def panel(ox,title,unit,rows,maxv,ticks,W=230):
        s.text(ox+W/2+60,58,title,12,weight='bold',fill=TEXT)
        for t in ticks:
            x=ox+120+t/maxv*W
            s.line(x,70,x,70+len(rows)*44,stroke=RULE,sw=0.5); s.text(x,84+len(rows)*44,str(t),9,fill=MUTED)
        s.text(ox+120+W,98+len(rows)*44,unit,9,'end',fill=MUTED,italic=True)
        for i,(lab,lo,hi,f,st,val) in enumerate(rows):
            y=76+i*44
            s.text(ox+112,y+19,lab,10,'end',fill=NAVY)
            s.rect(ox+120,y+6,lo/maxv*W,20,f,st)
            if hi>lo: s.rect(ox+120+lo/maxv*W,y+6,(hi-lo)/maxv*W,20,'url(#hatch)',st)
            s.text(ox+124+hi/maxv*W,y+20,val,9,'start',fill=st)
    C=(LORANGE,ORANGE); G=(LGREEN,GREEN); B=(GREY,MUTED)
    panel(20,'Peak bandwidth','GB/s',[('Core i7 2600K',19,19,*C,'≈19'),('GTX 480',180,180,*G,'≈180'),('PCIe 2.0 ×16',8,8,*B,'≈8')],200,[0,50,100,150,200])
    panel(370,'Memory latency','ns',[('Core i7 (Nehalem)',48,48,*C,'≈48'),('GTX 480',286,571,*G,'286–571')],700,[0,200,400,600],W=180)
    s.text(360,286,'GPU: ~10× the bandwidth for ~10× the latency. Latency in ns = cycles ÷ clock (2.93 GHz CPU, 1.4 GHz shader clock).',10,fill=MUTED,italic=True)
    s.save('g2-bandwidth-latency.svg')

def fig_g2_cp():
    s=S(720,360)
    s.text(360,28,'Command processor',14,weight='bold',fill=NAVY)
    F=(LNAVY,SOFT)
    s.rect(30,140,110,44,GREY,MUTED); s.lines(85,162,['memory','(VRAM / PCIe)'],10,fill=NAVY)
    s.rect(170,140,110,44,*F); s.lines(225,162,['FIFO','prefetch buffer'],10,fill=NAVY)
    s.rect(310,140,110,44,*F); s.lines(365,162,['command','decode'],10,fill=NAVY)
    s.line(142,162,168,162,arrow=True); s.line(282,162,308,162,arrow=True)
    outs=[('2D unit',F,60),('3D front end (rendering)',F,110),('shader units (compute)',(LGREEN,GREEN),160),('jump / call unit',F,210),('sync / wait unit',F,260)]
    for t,(f,st),y in outs:
        s.rect(480,y-16,200,32,f,st); s.text(580,y+4,t,10,fill=NAVY)
        s.path(f'M422,162 C450,162 450,{y} 478,{y}',arrow=True)
    s.rect(500,300,170,40,WHITE,SOFT,dash='3 3'); s.lines(585,320,['status registers','(CPU-visible)'],10,fill=NAVY)
    s.line(585,276,585,298,stroke=SOFT,arrow=True)
    s.path('M480,210 C300,210 240,230 225,186',stroke=ORANGE,arrow=True,dash='4 3')
    s.text(330,236,'changes fetch address',9,fill=ORANGE,italic=True)
    s.path('M682,110 C712,110 712,260 682,260',stroke=GREEN,arrow=True,dash='4 3')
    s.text(712,292,'completion events',9,'end',fill=GREEN,italic=True)
    s.text(225,128,'one CP, in order: hide latency by prefetching far ahead',9,fill=MUTED,italic=True)
    s.save('g2-command-processor.svg')

def fig_g2_fence():
    s=S(720,300)
    s.text(360,28,'Fences: the GPU reports progress through a status register',14,weight='bold',fill=NAVY)
    x0=60; y=80; w=150
    for i,n in enumerate([301,302,303,304]):
        x=x0+i*w
        done=i<2; cur=i==2
        f,st=((LGREEN,GREEN) if done else (LORANGE,ORANGE) if cur else (WHITE,RULE))
        s.rect(x,y,w-8,46,f,st)
        s.rect(x+4,y+4,46,38,LNAVY,SOFT); s.lines(x+27,y+23,['reg0 =',str(n)],8,fill=NAVY)
        s.text(x+(w-8+50)/2,y+28,f'buffer {n}',10,fill=st if i<3 else MUTED)
    s.text(x0,y-12,'command buffers in submission order (KMD assigns sequence ids)',11,'start',weight='bold',fill=NAVY)
    s.line(x0+2*w+27,y+70,x0+2*w+27,y+48,stroke=ORANGE,arrow=True); s.text(x0+2*w+27,y+84,'command processor is here',10,fill=ORANGE)
    s.rect(x0,y+110,200,40,LNAVY,SOFT); s.text(x0+100,y+134,'status register 0 = 303',11,fill=NAVY)
    s.path(f'M{x0+2*w+27},{y+46} C{x0+2*w+27},{y+130} {x0+260},{y+130} {x0+202},{y+130}',stroke=SOFT,arrow=True,dash='3 3')
    s.lines(x0+230,y+168,['CPU reads 303 ⇒ buffers ≤ 302 are finished:','their memory can be reclaimed'],10,anchor='start',fill=NAVY)
    s.text(360,286,'"Wait until register M = N" lets the GPU (or the CPU, by writing the register) hold back later commands.',10,fill=MUTED,italic=True)
    s.save('g2-fences.svg')

for f in [fig_memory,fig_cmdbuf,fig_pipeline,fig_gpu_org,fig_divergence,fig_latency,fig_drawcalls,fig_frames,fig_flush,fig_quads,fig_sorting,fig_batch_inst,fig_batch_cull,fig_vignette,fig_problem_map,fig_lot_hierarchy,fig_lot_journey,fig_lot_sync,fig_g_stack,fig_g_ring,fig_g_swizzle,fig_g_ringmodels,fig_g2_memory,fig_g2_cp,fig_g2_fence]: f()
print(sorted(os.listdir(OUT)))
