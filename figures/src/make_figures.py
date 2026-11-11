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

for f in [fig_memory,fig_cmdbuf,fig_pipeline,fig_gpu_org,fig_divergence,fig_latency,fig_drawcalls,fig_frames,fig_flush,fig_quads]: f()
print(sorted(os.listdir(OUT)))
