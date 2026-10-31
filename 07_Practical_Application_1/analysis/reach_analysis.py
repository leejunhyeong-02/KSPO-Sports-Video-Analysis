"""
OpenCap 복싱 데이터 분석: 스트레이트 리치와 골반 회전

사용법 (저장소 최상위 폴더에서):
    pip install -r analysis/requirements.txt
    python analysis/reach_analysis.py

출력:
    results/punches.csv            펀치별 측정값
    results/summary.csv            동작별 평균
    results/figures/*.png          그래프
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "opencap"
OUT = ROOT / "results"
FIG = OUT / "figures"
HEIGHT_M = 1.55  # 대상자 키 (sessionMetadata.yaml)

TRIALS = ["STRAIGHT1", "STRAIGHT2", "STRAIGHTx1", "STRAIGHTx2", "JAB1", "JAB2"]


# ---------------------------------------------------------------- 파일 읽기
def load_trc(path):
    """OpenCap .trc → (time[s], {마커이름: (N,3) 좌표[m]}). Y축이 위쪽."""
    lines = Path(path).read_text().splitlines()
    names = [n for n in lines[3].split("\t")[2:] if n]
    body = [l for l in lines[5:] if l.strip()]
    d = np.loadtxt(body)
    xyz = d[:, 2:2 + 3 * len(names)].reshape(len(d), len(names), 3)
    return d[:, 1], {n: xyz[:, i, :] for i, n in enumerate(names)}


def load_mot(path):
    """OpenSim .mot → DataFrame (각도 단위: 도)."""
    lines = Path(path).read_text().splitlines()
    start = next(i for i, l in enumerate(lines) if l.strip() == "endheader") + 1
    return pd.read_csv(path, sep=r"\s+", skiprows=start)


def horiz(a):
    """수평면 성분(x, z)만 사용."""
    return a[..., [0, 2]]


# ---------------------------------------------------------------- 펀치 단위 분석
def analyze_trial(trial):
    t, M = load_trc(DATA / "MarkerData" / f"{trial}.trc")
    mot = load_mot(DATA / "OpenSimData" / "Kinematics" / f"{trial}.mot")

    jab = trial.startswith("JAB")
    wrist, shoulder = ("LWrist", "LShoulder") if jab else ("RWrist", "RShoulder")
    elbow = "elbow_flex_l" if jab else "elbow_flex_r"
    cond = "JAB" if jab else ("STRAIGHTx" if "x" in trial else "STRAIGHT")

    feet = (M["LAnkle"] + M["RAnkle"]) / 2  # 매 프레임 양 발목 중간점

    # 1) 펀치 검출: 발 중심→손목 수평거리의 봉우리
    dist = np.linalg.norm(horiz(M[wrist] - feet), axis=1)
    peaks, _ = find_peaks(dist, prominence=0.15, distance=20)

    # 2) 펀치 방향: 봉우리 시점들의 발→손목 방향 평균
    v = horiz(M[wrist] - feet)[peaks]
    u = (v / np.linalg.norm(v, axis=1, keepdims=True)).mean(0)
    u /= np.linalg.norm(u)
    proj = lambda a: horiz(a) @ u

    reach = proj(M[wrist] - feet)          # 리치 = 발→어깨 + 어깨→손목
    shoulder_fwd = proj(M[shoulder] - feet)
    arm = proj(M[wrist] - M[shoulder])

    pelvis = mot["pelvis_rotation"].to_numpy()
    trunk = pelvis + mot["lumbar_rotation"].to_numpy()

    rows, prev = [], 0
    for i, p in enumerate(peaks):
        g = prev + int(np.argmin(reach[prev:p + 1]))  # 직전 가드(리치 최소) 시점
        prev = p
        rows.append(dict(
            id=f"{trial}-{i + 1}", trial=trial, cond=cond, punch=i + 1, t=t[p],
            reach_cm=reach[p] * 100,
            reach_pctH=reach[p] / HEIGHT_M * 100,
            shoulder_fwd_cm=shoulder_fwd[p] * 100,
            arm_cm=arm[p] * 100,
            ground_reach_cm=proj(M[wrist][p] - feet[g]) * 100,
            step_cm=proj(feet[p] - feet[g]) * 100,
            pelvis_rot_deg=abs(pelvis[p] - pelvis[g]),
            trunk_rot_deg=abs(trunk[p] - trunk[g]),
            elbow_flex_peak=mot[elbow].iloc[p],
        ))
    series = dict(t=t, reach=reach * 100, pelvis=pelvis, peaks=peaks, cond=cond)
    return rows, series


# ---------------------------------------------------------------- 그래프
COLORS = {"STRAIGHT": "#2f6db5", "STRAIGHTx": "#d9822b", "JAB": "#8a8f98"}


def fig_decomposition(summary):
    order = ["STRAIGHT", "STRAIGHTx", "JAB"]
    s = summary.set_index("cond").loc[order]
    fig, ax = plt.subplots(figsize=(7, 3.4))
    y = np.arange(len(order))
    ax.barh(y, s["shoulder_fwd_cm"], color=[COLORS[c] for c in order], label="Shoulder forward (pelvis/trunk rotation)")
    ax.barh(y, s["arm_cm"], left=s["shoulder_fwd_cm"], color="#c9ccd1", label="Arm extension (shoulder→wrist)")
    for yi, c in zip(y, order):
        ax.text(s.loc[c, "reach_cm"] + 1, yi, f"{s.loc[c, 'reach_cm']:.1f} cm", va="center")
    ax.set_yticks(y, order)
    ax.invert_yaxis()
    ax.set_xlabel("Reach from feet center (cm)")
    ax.set_xlim(0, s["reach_cm"].max() * 1.15)
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, fontsize=8, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG / "reach_decomposition.png", dpi=150)
    plt.close(fig)


def fig_scatter(df):
    s = df[df.cond != "JAB"]
    res = stats.linregress(s.pelvis_rot_deg, s.reach_cm)
    fig, ax = plt.subplots(figsize=(6, 4))
    for c in ["STRAIGHT", "STRAIGHTx"]:
        d = s[s.cond == c]
        ax.scatter(d.pelvis_rot_deg, d.reach_cm, color=COLORS[c], label=c, s=36)
    xs = np.linspace(s.pelvis_rot_deg.min(), s.pelvis_rot_deg.max(), 50)
    ax.plot(xs, res.intercept + res.slope * xs, "--", color="#555")
    ax.set_xlabel("Pelvis rotation, guard → impact (deg)")
    ax.set_ylabel("Reach (cm)")
    ax.set_title(f"r = {res.rvalue:.2f}, slope = {res.slope * 10:.1f} cm / 10°", fontsize=10)
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG / "pelvis_vs_reach.png", dpi=150)
    plt.close(fig)
    return res


def fig_timeline(series):
    fig, ax = plt.subplots(figsize=(8, 3.5))
    for tr in ["STRAIGHT1", "STRAIGHT2", "STRAIGHTx1", "STRAIGHTx2"]:
        s = series[tr]
        ax.plot(s["t"], s["reach"], color=COLORS[s["cond"]], alpha=1 if tr.endswith("1") else 0.5, lw=1.6, label=tr)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Reach (cm)")
    ax.legend(ncol=4, fontsize=8, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG / "reach_timeline.png", dpi=150)
    plt.close(fig)


def fig_straight1_angles():
    """STRAIGHT1 관절 각도: 골반 → 몸통 → 팔 순서 확인용."""
    mot = load_mot(DATA / "OpenSimData" / "Kinematics" / "STRAIGHT1.mot")
    fig, axes = plt.subplots(3, 1, figsize=(9.5, 6), sharex=True)
    axes[0].plot(mot.time, mot.pelvis_rotation, color="#2f6db5", label="pelvis_rotation")
    axes[0].plot(mot.time, mot.lumbar_rotation, color="#d9822b", label="lumbar_rotation")
    axes[1].plot(mot.time, mot.elbow_flex_r, color="#3a9a5b", label="elbow_flex_r")
    axes[1].plot(mot.time, mot.arm_flex_r, color="#8e5bb5", label="arm_flex_r")
    axes[2].plot(mot.time, mot.knee_angle_r, color="#555", label="knee_angle_r")
    axes[2].plot(mot.time, mot.knee_angle_l, color="#aaa", label="knee_angle_l")
    for ax in axes:
        ax.set_ylabel("deg")
        ax.legend(fontsize=8, frameon=False, loc="upper left", bbox_to_anchor=(1.0, 1.0))
        ax.spines[["top", "right"]].set_visible(False)
    axes[-1].set_xlabel("Time (s)")
    axes[0].set_title("STRAIGHT1 joint angles", fontsize=10)
    fig.tight_layout()
    fig.savefig(FIG / "straight1_joint_angles.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------- 실행
def main():
    FIG.mkdir(parents=True, exist_ok=True)
    rows, series = [], {}
    for tr in TRIALS:
        r, s = analyze_trial(tr)
        rows += r
        series[tr] = s
    df = pd.DataFrame(rows)
    df.round(2).to_csv(OUT / "punches.csv", index=False)

    cols = ["reach_cm", "reach_pctH", "shoulder_fwd_cm", "arm_cm", "ground_reach_cm",
            "step_cm", "pelvis_rot_deg", "trunk_rot_deg", "elbow_flex_peak"]
    summary = df.groupby("cond")[cols].mean().reset_index()
    summary.insert(1, "n", df.groupby("cond").size().values)
    summary.round(2).to_csv(OUT / "summary.csv", index=False)

    fig_decomposition(summary)
    res = fig_scatter(df)
    fig_timeline(series)
    fig_straight1_angles()

    a = df[df.cond == "STRAIGHT"].reach_cm
    b = df[df.cond == "STRAIGHTx"].reach_cm
    tt = stats.ttest_ind(a, b)
    print(summary.round(1).to_string(index=False))
    print(f"\nSTRAIGHT - STRAIGHTx reach: {a.mean() - b.mean():.1f} cm (t = {tt.statistic:.2f}, p = {tt.pvalue:.1e})")
    print(f"pelvis rotation vs reach: r = {res.rvalue:.2f}, {res.slope * 10:.1f} cm per 10 deg")


if __name__ == "__main__":
    main()
