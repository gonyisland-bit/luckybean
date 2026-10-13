# 럭키빈 iOS · 개발 시작 패키지

맥 없이 준비할 수 있는 단계까지 끝낸 상태다. 맥에서 이 폴더를 열고 Claude Code를 실행하면 바로 SwiftUI 개발로 들어갈 수 있다.

## 들어 있는 것
| 경로 | 내용 |
|---|---|
| `CLAUDE.md` | Claude Code가 가장 먼저 읽는 규칙(기술 스택, 디자인·캐릭터 규칙, 하지 말 것) |
| `docs/01~07` | 화면 명세, 게임 규칙, 모션·햅틱·소리 표, 그림 파이프라인, 데이터·웹 이관, 다국어 용어집, 로드맵 |
| `design/tokens.json` | 디자인 토큰 원본(색 대비 검증 완료) |
| `project.yml` | XcodeGen 프로젝트 정의(iOS 18, Swift 6, CloudKit, 3개 언어) |
| `LuckyBean/` | 시작 코드: 토큰·버튼·이름표·HUD, SwiftData 모델, 게임 엔진 6종, 웹 백업 가져오기, 화면 뼈대(거리→게임 고르기→손님 시트→게임 자리표시) |
| `LuckyBean/Resources/` | String Catalog(62키, ko/ja/en), 에셋(게임 아이콘·아바타 벡터) |
| `LuckyBeanTests/` | 게임 규칙 10만 회 시뮬레이션 테스트, 웹 백업 파싱 테스트 |
| `art/reference/` | 6차 확정 시안 PNG 16장 + 파츠 |
| `art/svg/` | 비둘기 5명 × 9포즈, 키리 12포즈, 게임 아이콘 6종 (벡터 원본) |
| `art/generator/` | 시안 그림 생성 스크립트 |

시안 캔버스: https://claude.ai/artifact/4v4m25RLLZUkhQxu4psq1M (6차 줄이 최신)

## 맥에서 첫 실행
```bash
brew install xcodegen
git clone -b ios-starter https://github.com/gonyisland-bit/luckybean.git
cd luckybean/ios
xcodegen generate
claude            # Claude Code 실행
```
Claude Code에 처음 보낼 메시지 예시:
> CLAUDE.md와 docs/07_roadmap.md를 읽고 "맥 첫날" 체크리스트대로 진행해줘. 이 코드는 맥 없이 작성돼서 컴파일 검증이 안 됐어. 먼저 빌드 에러를 전부 고치고 테스트를 통과시킨 다음, DesignSystemPreview를 시뮬레이터에서 띄워서 art/reference 시안과 비교해줘.

## 주의
- 이 코드는 **컴파일을 돌려보지 못했다**(리눅스 환경, Swift 툴체인 없음). 게임 확률 수식은 Python 시뮬레이션으로 따로 검증했다(docs/02 §3). 첫 빌드에서 자잘한 문법·동시성 오류가 나올 수 있다.
- 폰트 파일은 라이선스상 포함 가능하지만 용량 때문에 빼 두었다. `LuckyBean/Resources/Fonts/README.md` 참고.
- 웹 버전 `sounds/*.mp3`는 넣지 않았다. 자체 제작 음원으로 교체 예정(docs/03).
