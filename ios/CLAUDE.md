# CLAUDE.md — 럭키빈 (Lucky Bean) iOS

Claude Code가 이 저장소에서 일할 때 가장 먼저 읽는 파일이다. 아래 규칙은 시안 6차까지 사용자(고니)와 합의된 결정이다. 바꾸려면 먼저 사용자에게 물어볼 것.

## 1. 제품 한 줄
커피내기 미니게임 + 기록 앱. 게임 6종(1.0), 커피 운세, 주변 카페(실제 지도), 카페 노이즈/음악(바이브). 서버 없음. 한국·일본 앱스토어의 감성 그림책 스타일 앱이 목표.

- 앱 이름: 럭키빈 / ラッキービーン / Lucky Bean
- Bundle ID: `studio.devgon.luckybean`
- 최소 iOS 18, iPhone 우선(세로 고정). iPad는 1.1 이후.
- 수익: 무료 + 서포터팩(일회성 IAP, 꾸미기 소품·테마. 게임 기능은 절대 잠그지 않음)

## 2. 기술 스택 (고정)
| 영역 | 선택 | 메모 |
|---|---|---|
| UI | SwiftUI + `@Observable` | UIKit 브리지는 지도 커스텀 마커 등 꼭 필요할 때만 |
| 저장 | SwiftData + CloudKit private DB | 모든 속성 optional 또는 기본값, `@Attribute(.unique)` 금지(CloudKit 제약) |
| 지도 | MapKit for SwiftUI (`Map`, `MKLocalSearch`) | 주변 카페 = 실제 지도 + 내 위치 |
| 소리 | AVAudioEngine | 앰비언트는 레이어 믹싱, 효과음은 짧은 버퍼. 음원은 전부 자체 제작 |
| 햅틱 | Core Haptics (`CHHapticEngine`) + `sensoryFeedback` | 게임 손맛 핵심, docs/03 표를 따른다 |
| 위젯 | WidgetKit | 오늘의 운세, 이번 달 커피왕 |
| 다국어 | String Catalog (`Localizable.xcstrings`) | ko(기본) / ja / en |
| 결제 | StoreKit 2 | 서포터팩 1종부터 |
| 프로젝트 | XcodeGen (`project.yml`) | `.xcodeproj`는 커밋하지 않는다 |
| 서드파티 | 없음 | 패키지 추가 전 사용자에게 확인 |

## 3. 폴더 구조
```
LuckyBean/
  App/            앱 진입점, 라우팅, 환경 객체
  DesignSystem/   토큰(색·타입·간격·반경), 공통 컴포넌트
  Models/         SwiftData 모델
  Games/          게임 공통 규칙(GameRules) + 게임별 엔진(순수 Swift, UI 없음)
  Features/       화면 단위 폴더 (Street, Cafe, Guests, Play, Result, Records, Lounge, Vibe, Nearby, Settings)
  Migration/      웹 버전 백업(JSON) 가져오기
  Audio/          AudioEngine, 앰비언트 레이어, 효과음
  Resources/      Assets.xcassets, Localizable.xcstrings, 폰트
LuckyBeanTests/   게임 규칙·마이그레이션 단위 테스트
docs/             기획 명세 (먼저 읽을 것)
art/              시안 레퍼런스 PNG, SVG 원본, 그림 생성 스크립트
```

## 4. 작업 원칙
1. **게임 로직은 `Games/`에 순수 Swift로**, 뷰는 엔진 상태만 그린다. 엔진은 `Date`/난수를 주입받아 테스트 가능해야 한다(`RandomNumberGenerator` 주입).
2. **당첨자를 정하는 시점은 게임마다 다르다.** docs/02의 "결정 시점" 열을 그대로 따를 것. 자비 모드 가중치가 정확히 지켜지도록 설계된 방식이라 임의로 바꾸면 확률이 틀어진다.
3. 화면 하나 만들 때마다 SwiftUI `#Preview`를 붙이고, 시안 PNG(`art/reference/`)와 나란히 비교한다.
4. 문자열 하드코딩 금지. 전부 String Catalog 키. 일본어가 가장 길다고 가정하고 레이아웃을 잡는다.
5. 접근성: Dynamic Type(최대 AX1까지 깨지지 않게), VoiceOver 라벨(비둘기는 "민수의 비둘기, 회색, 베레모"), 색만으로 당첨 표시 금지(항상 텍스트 동반), 모션 줄이기 설정 시 흔들림·화면 셰이크 끄기.
6. 커밋은 작은 단위. 빌드 깨진 상태로 커밋 금지. 테스트 통과 확인 후 커밋.

## 5. 디자인 규칙 (시안 6차 확정)
- 토큰: `design/tokens.json` = `DesignSystem/Tokens.swift`. 둘이 어긋나면 tokens.json이 정답.
- 주색 `#2F6E71`(흰 글자 5.85:1), 버튼 립 `#234F51`, Lucky `#EDB43E`, Coral `#F2A48C`, 키리 `#E8913A`, 잉크 `#3B3B3D`, 시트 `#FBF7F0`.
- 버튼: 높이 56, 반경 20, 아래 4pt 단색 그림자(립). 그라데이션·블러 그림자 금지.
- 폰트: 제목 Jua, 키리/운세 대사만 Gowun Dodum, 일본어 Zen Maru Gothic, 본문은 시스템 폰트.
- **빛 번짐(블러 글로우) 금지.** 밤·저녁 장면의 빛은 또렷한 반투명 도형으로.
- 손으로 그린 떨림 + 종이 결: 떨림은 패스에 미리 구워 넣고, 결은 Metal `layerEffect` 셰이더 하나로 전 화면에 얹는다(이미지 필터 남발 금지).

### 캐릭터 규칙
- **키리**: 주황 줄무늬 고양이. 작은 점눈, 목띠·목걸이 없음, 크기는 화면 간 일정하게. 모든 장면에 등장시키지 않는다. 키리의 선택 게임에서는 **뒷모습만**(네 발로 걷기 → 웅크려 덥석).
- **비둘기 손님**: nestrip 스타일 **옆모습이 기본**(주황 눈, 흰 콧등, 청록 목깃+분홍 띠, 날개 줄무늬 2개, 검은 꼬리끝, 빨간 다리). 손님 구분 = 깃털색 + 소품 + **발목 링 색**. 정면은 꾸미기 화면 정도에만.
- 비둘기 크기 토큰: S 1.4(배경·주변) / M 1.9(게임 주인공) / L 3.0(발표·차례 넘기기). 기준 단위는 docs/04.
- 모든 게임은 같은 동네(럭키빈 카페 거리, 길 건너 공원, 지붕)에서 일어난다. 배경에 카페가 보이면 같은 외관(분홍 벽, 스캘럽 지붕, 노란 간판, 줄무늬 차양)을 유지.

## 6. 하지 말 것
- 서버, 계정, 광고, 추적 SDK 추가
- 게임 결과를 몰래 조작하는 기능(자비 모드는 **모두에게 보이는** 공개 옵션으로만)
- 게임 기능을 유료로 잠그기
- 실제 브랜드/캐릭터를 닮은 그림, 특정 작가 그림 따라 그리기
- 시안에 없는 화면을 임의로 추가(필요하면 먼저 제안)

## 7. 문서 지도
- `docs/01_product_spec.md` 화면 목록·흐름·시안 보드 매핑
- `docs/02_game_rules.md` 6종 규칙, 럭키 라운드, 자비 모드, 한 명 진행, 한 판 더
- `docs/03_motion_haptics_sound.md` 장면별 모션·햅틱·소리 표
- `docs/04_art_pipeline.md` 그림 파츠 목록, 레이어, 내보내기 규칙
- `docs/05_data_and_migration.md` SwiftData 모델, CloudKit 주의, 웹 백업 가져오기
- `docs/06_localization.md` 용어집(ko/ja/en)
- `docs/07_roadmap.md` 마일스톤과 맥 첫날 체크리스트
