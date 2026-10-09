# 🏃‍♂️ KSPO 스포츠영상 분석과정 (Sports Video Analysis)

> **2026년 국민체육진흥공단(KSPO) 스포츠인재아카데미 스포츠 영상분석 전문과정 아카이브**  
> 영상 기반 2D/3D 동작 분석, 데이터 수집·가공, 바이오메카닉스(생체역학) 지표 도출 및 성과물 포트폴리오 저장소입니다.

<p align="left">
  <img src="https://img.shields.io/badge/Author-Junhyeong%20Lee-0969da?style=flat-square&logo=github" alt="Author" />
  <img src="https://img.shields.io/badge/Organizer-KSPO%20국민체육진흥공단-005BAC?style=flat-square" alt="KSPO" />
  <img src="https://img.shields.io/badge/Operator-hunet-EA2839?style=flat-square" alt="Hunet" />
  <img src="https://img.shields.io/badge/Period-2026.10.10_~_11.07_(54h)-10b981?style=flat-square" alt="Period" />
  <img src="https://img.shields.io/badge/Status-In_Progress-f59e0b?style=flat-square" alt="Status" />
</p>

---

## 📌 Course Overview

- **교육명**: 2026년 스포츠영상 분석과정
- **주관/시행**: 국민체육진흥공단 (KSPO) 한국스포츠과학원 스포츠인재아카데미 / (주)휴넷
- **교육 기간**: 2026. 10. 10.(토) ~ 11. 07.(토) (매주 토·일요일 총 9회, 54시간)
- **장소**: 서울 송파구 올림픽공원 내 스포츠인재아카데미
- **목표**: 
  - 스포츠 현장 영상 기반의 2차원(2D) 및 3차원(3D) 정량적 동작 분석 역량 배양
  - 모션 트래킹, 캘리브레이션, 키포인트 추출 및 생체역학 데이터 가공
  - 분석 결과지 리포팅 및 종목별 맞춤형 실습 성과물 도출

---

## 🗓️ 9-Day Curriculum & Progress

| 회차 | 일자 | 교육 주제 | 핵심 내용 및 실습 | 상태 | 디렉토리 |
|:---:|:---:|:---|:---|:---:|:---:|
| **1회차** | `10.10 (토)` | **스포츠 영상분석 기초** | 영상 분석 개론, 비전 기반 스포츠 데이터 이해 | ⏳ 예정 | [📁 01_Basics](./01_Basics_of_Sports_Video_Analysis/) |
| **2회차** | `10.11 (일)` | **스포츠영상분석 자료수집 이론** | 카메라 파라미터, 샘플링 레이트, 캘리브레이션 원리 | ⏳ 예정 | [📁 02_Theory](./02_Data_Collection_Theory/) |
| **3회차** | `10.17 (토)` | **스포츠영상분석 자료수집 및 가공 (2차원)** | 2D 평면 모션 트래킹, 좌표 변환, 각도/속도 분석 | ⏳ 예정 | [📁 03_2D_Data](./03_2D_Collection_and_Processing/) |
| **4회차** | `10.18 (일)` | **스포츠영상분석 결과지 작성 (2차원)** | 2D 생체역학 지표 시각화 및 피드백 리포트 작성 | ⏳ 예정 | [📁 04_2D_Report](./04_2D_Analysis_Report/) |
| **5회차** | `10.24 (토)` | **스포츠영상분석 자료수집 및 가공 (3차원)** | 다중 카메라 기반 3D 재구성(Reconstruction), DLT/BA | ⏳ 예정 | [📁 05_3D_Data](./05_3D_Collection_and_Processing/) |
| **6회차** | `10.25 (일)` | **스포츠영상분석 결과지 작성 (3차원)** | 3D 관절 모멘트/각도 분석 결과지 작성 | ⏳ 예정 | [📁 06_3D_Report](./06_3D_Analysis_Report/) |
| **7회차** | `10.31 (토)` | **스포츠영상 분석 적용 실습 (Part 1)** | 실제 스포츠 종목(야구, 골프 등) 영상 분석 파이프라인 적용 | ⏳ 예정 | [📁 07_Practical_1](./07_Practical_Application_1/) |
| **8회차** | `11.01 (일)` | **스포츠영상 분석 적용 실습 (Part 2)** | 종목별 세부 데이터 튜닝 및 심화 인사이트 도출 | ⏳ 예정 | [📁 08_Practical_2](./08_Practical_Application_2/) |
| **9회차** | `11.07 (토)` | **성과물 발표** | 최종 프로젝트 분석 결과 보고 및 성과물 발표 | ⏳ 예정 | [📁 09_Final](./09_Final_Project/) |

---

## 📂 Repository Structure

```text
KSPO-Sports-Video-Analysis/
├── README.md                                  # 전체 교육 로드맵 및 진행 상황
├── .gitignore                                 # 미디어 및 바이너리 파일 제외 설정
│
├── 01_Basics_of_Sports_Video_Analysis/          # [10.10] 스포츠 영상분석 기초
│   ├── README.md
│   └── notes/
├── 02_Data_Collection_Theory/                  # [10.11] 스포츠영상분석 자료수집 이론
│   ├── README.md
│   └── notes/
├── 03_2D_Collection_and_Processing/            # [10.17] 2D 자료수집 및 가공
│   ├── README.md
│   └── src/
├── 04_2D_Analysis_Report/                      # [10.18] 2D 결과지 작성
│   ├── README.md
│   └── reports/
├── 05_3D_Collection_and_Processing/            # [10.24] 3D 자료수집 및 가공
│   ├── README.md
│   └── src/
├── 06_3D_Analysis_Report/                      # [10.25] 3D 결과지 작성
│   ├── README.md
│   └── reports/
├── 07_Practical_Application_1/                 # [10.31] 분석 적용 실습 (1)
│   ├── README.md
│   └── src/
├── 08_Practical_Application_2/                 # [11.01] 분석 적용 실습 (2)
│   ├── README.md
│   └── src/
├── 09_Final_Project/                           # [11.07] 최종 성과물 발표
│   ├── README.md
│   ├── presentation/
│   └── src/
└── docs/                                       # 참고 문서, 강의자료 템플릿
```

---

## 🛠️ Tech Stack & Domain Keywords

- **Languages & Frameworks**: `Python`, `OpenCV`, `MediaPipe`, `NumPy`, `SciPy`, `Matplotlib`
- **Analysis Domains**:
  - **2D/3D Kinematics**: Joint Angle, Angular Velocity, Center of Mass (CoM) Tracking
  - **Calibration & Reconstruction**: Direct Linear Transformation (DLT), Epipolar Geometry
  - **Sports Applications**: Baseball Pitching/Batting Mechanics, Golf Swing, Gait Analysis

---

## 👤 Author

- **이준형 (Junhyeong Lee)**
- **GitHub**: [@leejunhyeong-02](https://github.com/leejunhyeong-02)
- **Affiliation / Focus**: Computer Vision, Multimodal Deep Learning, Sports Motion Analytics
