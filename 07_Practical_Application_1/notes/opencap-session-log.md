# OpenCap 측정 과정과 시행착오 (2026.10.31)

## 세팅

| 항목 | 값 |
|---|---|
| 장소 | 야외 (나무 데크) |
| 카메라 | iPhone 2대, 60fps |
| 체커보드 | 4 × 5 꼭짓점, 칸 35mm, 수직 배치 (Perpendicular) |
| 포즈 모델 / 근골격 모델 | HRNet / LaiUhlrich2022 |
| 피험자 | S01 (여, 1.55m, 48kg), 오소독스 스탠스 (왼발 앞) |
| 세션 이름 | `boxing_20261031_Lee1` |

## 진행 순서

1. 피험자 생성: Subject Tags는 **Unimpaired**만 선택 (분석 결과에는 영향 없음)
2. Data sharing: 공개 공유 범위를 선택해야 Record 버튼이 활성화됨
3. 캘리브레이션 → 뉴트럴 포즈 → 트라이얼 14개 녹화
4. Download data로 zip 받기 (약 20분 걸려서 한 번 취소하고 다시 받음)

## 겪은 문제와 해결

| 문제 | 원인 / 해결 |
|---|---|
| Record 버튼이 안 눌림 | 공개 데이터 공유 범위 드롭다운을 선택하지 않음 → 선택하면 활성화 |
| `Error in processing neutral pose` 반복 | 캘리브레이션 재시도 후 **Advanced Settings → scaling setup → Any pose**로 바꾸고, 피험자가 미리 자리에 선 상태에서 Record → 통과 |
| 뉴트럴 이후 `Trial is in the queue` | 정상. 서버 처리 대기열에 들어간 상태라 기다리면 됨 |
| 다운로드가 20분 넘게 안 끝남 | Cancel → 새로고침 → 다시 Download data |
| Advanced Analysis (gait) | 보행 전용 도구라 복싱 트라이얼에는 해당 없음 |

뉴트럴 포즈 실패의 흔한 원인:
- Record를 누를 때 피험자가 아직 자리에 없음 (혼자 촬영할 때 특히)
- 화면에 다른 사람이 같이 찍힘
- 전신(특히 발)이 한쪽 카메라에서 잘림
- 역광이나 흰 옷과 흰 배경처럼 대비가 약함

## 트라이얼 목록

| 트라이얼 | 내용 |
|---|---|
| neutral | 스케일링용 정지 자세 |
| STEP1, STEP2 | 스텝 |
| JAB1, JAB2 | 잽 (왼손), 약 6~7회씩 |
| STRAIGHT1, STRAIGHT2 | 스트레이트 (오른손), 스텝과 하체 회전 사용, 6회씩 |
| STRAIGHTx1, STRAIGHTx2 | 스트레이트, **하체 고정**, 6회씩 |
| SHADOW | 섀도복싱 |
| DEFENSEx, DEFENSEo | 방어 동작 2가지 조건 |
| backattack | 백어택 |
| turn | 회전 |
