"""
축구 트래킹 데이터 분석: 포지션별 속도·이동거리, 포메이션 지도, 히트맵

사용법 (8주차 폴더에서):
    data/soccer_rawdata.xlsx 를 넣고
    pip install pandas numpy scipy matplotlib openpyxl
    python analysis/soccer_analysis.py
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "soccer_rawdata.xlsx"
OUT = ROOT / "results"
FIG = OUT / "figures"
FIG.mkdir(parents=True, exist_ok=True)

# ===== 1) 포지션별 요약표 =====
import pandas as pd, numpy as np
_df = pd.read_excel(DATA)
_pos = ["GK","RB","RCB","LCB","LB","DM","RCM","LCM","RW","ST","LW"]
_rows = []
for i, p in enumerate(_pos):
    x = _df.iloc[:, 2+2*i].values; y = _df.iloc[:, 3+2*i].values
    v = np.hypot(np.diff(x), np.diff(y)) / 0.1          # m/s (10Hz)
    _rows.append(dict(Position=p, AVG_V_kmh=v.mean()*3.6, MAX_V_kmh=v.max()*3.6,
                      DIST_km=v.sum()*0.1/1000, mean_x_m=x.mean(), mean_y_m=y.mean()))
pd.DataFrame(_rows).round(3).to_csv(OUT / "position_summary.csv", index=False)
print(pd.DataFrame(_rows).round(2).to_string(index=False))

# ===== 2) 포메이션 지도 =====
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc
from matplotlib import font_manager as fm

for f in fm.findSystemFonts():
    if any(k in f for k in ["NanumGothic", "NotoSansCJK", "NotoSansKR"]):
        fm.fontManager.addfont(f)
        plt.rcParams["font.family"] = fm.FontProperties(fname=f).get_name(); break
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_excel(DATA)
pos = ["GK","RB","RCB","LCB","LB","DM","RCM","LCM","RW","ST","LW"]
line = {"GK":"GK","RB":"DF","RCB":"DF","LCB":"DF","LB":"DF","DM":"MF","RCM":"MF","LCM":"MF","RW":"FW","ST":"FW","LW":"FW"}
col = {"GK":"#E8C547","DF":"#4A90C2","MF":"#5BA35B","FW":"#E07B4F"}
rows=[]
for i,p in enumerate(pos):
    x=df.iloc[:,2+2*i].values; y=df.iloc[:,3+2*i].values
    d=np.hypot(np.diff(x),np.diff(y))
    rows.append(dict(p=p,x=x.mean(),y=y.mean(),sx=x.std(),sy=y.std(),km=d.sum()/1000,v=d.mean()/0.1*3.6))
s=pd.DataFrame(rows)

W,L=68,105
fig,ax=plt.subplots(figsize=(7.2,10))
fig.patch.set_facecolor("#1f5f3a"); ax.set_facecolor("#2a7a4b")
for k in range(0,105,15):
    ax.add_patch(Rectangle((0,k),W,7.5,color="#2f8452",zorder=0))
lc=dict(color="white",lw=1.6,zorder=1,fill=False)
ax.add_patch(Rectangle((0,0),W,L,**lc))
ax.plot([0,W],[L/2,L/2],color="white",lw=1.6,zorder=1)
ax.add_patch(Circle((W/2,L/2),9.15,**lc)); ax.add_patch(Circle((W/2,L/2),0.4,color="white",zorder=1))
for y0,sgn in [(0,1),(L,-1)]:
    ax.add_patch(Rectangle((W/2-20.16,y0 if sgn>0 else y0-16.5),40.32,16.5,**lc))
    ax.add_patch(Rectangle((W/2-9.16,y0 if sgn>0 else y0-5.5),18.32,5.5,**lc))
    ax.add_patch(Circle((W/2,y0+sgn*11),0.4,color="white",zorder=1))
    ax.add_patch(Arc((W/2,y0+sgn*11),18.3,18.3,theta1=37 if sgn>0 else 217,theta2=143 if sgn>0 else 323,color="white",lw=1.6,zorder=1))

# 이동 범위(1 SD 타원)
from matplotlib.patches import Ellipse
for _,r in s.iterrows():
    ax.add_patch(Ellipse((r.x,r.y),2*r.sx,2*r.sy,color=col[line[r.p]],alpha=0.3,zorder=2,lw=0))

# 라인 연결
for grp in [["LB","LCB","RCB","RB"],["LCM","DM","RCM"],["LW","ST","RW"]]:
    g=s.set_index("p").loc[grp]; ax.plot(g.x,g.y,color="white",alpha=0.35,lw=1.2,ls="--",zorder=2)

kmin,kmax=s.km.min(),s.km.max()
for _,r in s.iterrows():
    size=900+1800*(r.km-kmin)/(kmax-kmin)
    ax.scatter(r.x,r.y,s=size,color=col[line[r.p]],edgecolor="white",lw=2,zorder=4)
    if r.p=="GK":
        ax.text(r.x,r.y,r.p,ha="center",va="center",fontsize=10.5,fontweight="bold",color="#333",zorder=5)
        ax.text(r.x,r.y-4.2,f"{r.km:.2f} km",ha="center",va="center",fontsize=8.5,color="white",zorder=5)
    else:
        ax.text(r.x,r.y+0.6,r.p,ha="center",va="center",fontsize=11,fontweight="bold",color="white",zorder=5)
        ax.text(r.x,r.y-1.9,f"{r.km:.2f} km",ha="center",va="center",fontsize=8.5,color="white",zorder=5)

ax.annotate("",xy=(W+3.2,L*0.72),xytext=(W+3.2,L*0.28),arrowprops=dict(arrowstyle="-|>",color="white",lw=1.5),annotation_clip=False)
ax.text(W+4.8,L/2,"공격 방향",rotation=90,ha="center",va="center",color="white",fontsize=10)
ax.set_xlim(-2,W+7); ax.set_ylim(-9,L+8); ax.set_aspect("equal"); ax.axis("off")
ax.text(-1,L+5.5,"평균 위치와 이동거리 (전반 45분)",fontsize=16,fontweight="bold",color="white")
ax.text(-1,L+2.2,"원 크기 = 이동거리 · 옅은 타원 = 위치 변동 범위(±1 SD)",fontsize=9.5,color="#d9eadf")
hx=0
for k,lab in [("GK","GK"),("DF","수비"),("MF","미드필더"),("FW","공격")]:
    ax.scatter(hx+1.5,-5,s=120,color=col[k],edgecolor="white",lw=1.2); ax.text(hx+3.3,-5,lab,va="center",color="white",fontsize=9.5); hx+=15
ax.text(W+6,-7.5,"이동거리: 10Hz 원본 좌표 기준(필터 미적용)",ha="right",fontsize=7.5,color="#cfe3d6")
fig.tight_layout()
fig.savefig(FIG / "formation_map.png",dpi=180,facecolor=fig.get_facecolor())

plt.close(fig)
# ===== 3) 히트맵 =====
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import font_manager as fm
from scipy.ndimage import gaussian_filter

for f in fm.findSystemFonts():
    if any(k in f for k in ["NanumGothic","NotoSansCJK","NotoSansKR"]):
        fm.fontManager.addfont(f); plt.rcParams["font.family"]=fm.FontProperties(fname=f).get_name(); break
plt.rcParams["axes.unicode_minus"]=False

df=pd.read_excel(DATA)
pos=["GK","RB","RCB","LCB","LB","DM","RCM","LCM","RW","ST","LW"]
W,L=68,105; BG="#16241c"; LINE="#cfd8d2"
cmap=LinearSegmentedColormap.from_list("h",[(0,(0,0,0,0)),(0.12,"#1d5c6b"),(0.35,"#2f9e8f"),(0.6,"#f2c14e"),(0.85,"#f07b3f"),(1,"#e8354a")])
XY={p:(df.iloc[:,2+2*i].values,df.iloc[:,3+2*i].values) for i,p in enumerate(pos)}
KM={p:np.hypot(np.diff(x),np.diff(y)).sum()/1000 for p,(x,y) in XY.items()}

def density(xs,ys,bins=1.0,sigma=2.2):
    H,xe,ye=np.histogram2d(xs,ys,bins=[np.arange(0,W+bins,bins),np.arange(0,L+bins,bins)])
    H=gaussian_filter(H,sigma); return H.T/H.max()

def pitch(ax,lw=1.2):
    ax.set_facecolor(BG)
    k=dict(color=LINE,lw=lw,fill=False,zorder=3,alpha=.8)
    ax.add_patch(Rectangle((0,0),W,L,**k)); ax.plot([0,W],[L/2,L/2],color=LINE,lw=lw,zorder=3,alpha=.8)
    ax.add_patch(Circle((W/2,L/2),9.15,**k))
    for y0,s in [(0,1),(L,-1)]:
        ax.add_patch(Rectangle((W/2-20.16,y0 if s>0 else y0-16.5),40.32,16.5,**k))
        ax.add_patch(Rectangle((W/2-9.16,y0 if s>0 else y0-5.5),18.32,5.5,**k))
        ax.add_patch(Arc((W/2,y0+s*11),18.3,18.3,theta1=37 if s>0 else 217,theta2=143 if s>0 else 323,color=LINE,lw=lw,zorder=3,alpha=.8))
    ax.set_xlim(-1,W+1); ax.set_ylim(-1,L+1); ax.set_aspect("equal"); ax.axis("off")

# 1) 팀 전체
allx=np.concatenate([XY[p][0] for p in pos if p!="GK"]); ally=np.concatenate([XY[p][1] for p in pos if p!="GK"])
D=density(allx,ally,sigma=2.0)
fig,ax=plt.subplots(figsize=(7.2,10)); fig.patch.set_facecolor(BG)
pitch(ax,1.5)
ax.imshow(D,extent=[0,W,0,L],origin="lower",cmap=cmap,interpolation="bilinear",zorder=1,vmin=0,vmax=1)
for p in pos:
    x,y=XY[p]
    ax.text(x.mean(),y.mean(),p,ha="center",va="center",fontsize=10.5,fontweight="bold",color="white",zorder=5,
            bbox=dict(boxstyle="round,pad=0.25",fc=(0,0,0,0.45),ec="none"))
ax.annotate("",xy=(W+3,L*.7),xytext=(W+3,L*.3),arrowprops=dict(arrowstyle="-|>",color=LINE,lw=1.4),annotation_clip=False)
ax.text(W+4.6,L/2,"공격 방향",rotation=90,ha="center",va="center",color=LINE,fontsize=10)
ax.set_xlim(-2,W+7); ax.set_ylim(-6,L+9)
ax.text(-1,L+6,"팀 위치 히트맵 (전반 45분)",fontsize=16,fontweight="bold",color="white")
ax.text(-1,L+2.6,"필드 플레이어 10명이 머문 시간 밀도 · 라벨 = 각 선수 평균 위치",fontsize=9.5,color="#b9c7bf")
cax=fig.add_axes([0.16,0.035,0.4,0.012]); cb=plt.colorbar(plt.cm.ScalarMappable(cmap=cmap),cax=cax,orientation="horizontal")
cb.set_ticks([0,1]); cb.set_ticklabels(["적게 머묾","오래 머묾"]); cb.ax.tick_params(colors="#b9c7bf",labelsize=8.5,length=0); cb.outline.set_visible(False)
fig.savefig(FIG / "team_heatmap.png",dpi=180,facecolor=BG,bbox_inches="tight")
plt.close(fig)

# 2) 선수별 (4-3-3 배치)
layout=[["LW","ST","RW"],["LCM","DM","RCM"],["LB","LCB","RCB","RB"],["GK"]]
fig=plt.figure(figsize=(12,15.5)); fig.patch.set_facecolor(BG)
gs=fig.add_gridspec(4,12,hspace=0.18,wspace=0.3)
for r,row in enumerate(layout):
    n=len(row); w=12//n if n>1 else 3; off=(12-w*n)//2
    for c,p in enumerate(row):
        ax=fig.add_subplot(gs[r,off+c*w:off+(c+1)*w]); pitch(ax,0.9)
        x,y=XY[p]; ax.imshow(density(x,y,sigma=2.2),extent=[0,W,0,L],origin="lower",cmap=cmap,interpolation="bilinear",zorder=1)
        ax.set_title(f"{p}  ·  {KM[p]:.2f} km",color="white",fontsize=12,fontweight="bold",pad=6)
fig.suptitle("선수별 위치 히트맵 (전반 45분, 위쪽이 공격 방향)",color="white",fontsize=18,fontweight="bold",y=0.93)
fig.savefig(FIG / "player_heatmaps.png",dpi=140,facecolor=BG,bbox_inches="tight")
