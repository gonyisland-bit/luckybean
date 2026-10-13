# 07 · 로드맵과 맥 첫날 체크리스트

## 맥 첫날 (Claude Code에게 이 순서대로 시키면 된다)
1. Xcode 최신 설치, Apple Developer 계정 로그인(무료 계정도 기기 테스트 가능, CloudKit·TestFlight는 유료 계정 필요).
2. `brew install xcodegen` → 저장소 루트에서 `xcodegen generate` → `LuckyBean.xcodeproj` 열기.
3. **빌드부터 통과시키기.** 이 스타터 코드는 맥 없이 작성돼 컴파일 검증을 못 했다. 첫 작업은 "빌드 에러 전부 고치고 테스트 통과"(`⌘U`).
4. 폰트 3종(Jua, Gowun Dodum, Zen Maru Gothic — 모두 OFL)을 Google Fonts에서 받아 `LuckyBean/Resources/Fonts/`에 넣고 `project.yml`의 `UIAppFonts` 확인.
5. Signing 팀 지정, Bundle ID `studio.devgon.luckybean` 등록, iCloud(CloudKit) 컨테이너 `iCloud.studio.devgon.luckybean` 생성.
6. 시뮬레이터에서 `DesignSystemPreview`를 띄워 토큰·버튼·이름표가 시안과 맞는지 확인.

## 마일스톤
| 단계 | 내용 | 완료 기준 |
|---|---|---|
| M0 뼈대 | 프로젝트 생성, 토큰, 공통 컴포넌트, SwiftData 모델, 라우팅 | 빈 화면 흐름(거리→게임 고르기→손님→게임 자리표시→영수증)이 끝까지 이어짐 |
| M1 게임 로직 | 6개 엔진 + 공통 규칙(럭키, 자비, 동점) + 단위 테스트 | 10만 회 시뮬레이션에서 자비 가중치 오차 ±1% 이내 |
| M2 게임 화면 | 6개 게임 UI + 발표 + 영수증 + 한 판 더 | 시안 PNG와 나란히 비교해 구도 일치, 햅틱 표 적용 |
| M3 거리·장소 | 가로 거리, 밤 모드, 기록 보관소, 손님 꾸미기, 웹 가져오기 | 웹 백업 붙여넣기로 기존 기록 이관 |
| M4 부가 | 라운지(운세), 바이브(자체 음원 레이어 믹서), 주변 카페(MapKit), 위젯 | 백그라운드 재생, 위치 권한 거부 경로 |
| M5 출시 준비 | 일본어 검수, 접근성, 서포터팩 IAP, 스크린샷(한/일), TestFlight | 심사 제출 |

## 1.1 후보
사다리타기, 계절 배경, iPad, 그룹 공유(CloudKit 공유 DB), 날씨 연동 거리(비 오면 처마 밑 비둘기).

## 아직 정하지 않은 것 (개발 중 사용자에게 물을 것)
- 서포터팩 가격과 구성(소품 몇 개, 테마 몇 개)
- 운세 카드 문구 세트(웹 버전 문구 재사용 여부)
- 주변 카페 "디카페인/테라스" 필터의 데이터 출처
