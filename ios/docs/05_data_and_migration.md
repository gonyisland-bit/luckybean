# 05 · 데이터 모델과 웹 버전 가져오기

## 1. SwiftData 모델 (CloudKit private DB 동기화)
CloudKit 규칙: 모든 속성은 optional이거나 기본값이 있어야 함, `@Attribute(.unique)` 사용 금지, 관계는 optional, 삭제 규칙은 nullify 위주.

| 모델 | 주요 속성 | 메모 |
|---|---|---|
| `Member` | id, name, feather(`Feather`), accessory(`Accessory`), legBand(`LegBand`), isGuest, createdAt, archived, legacyUnknownCount | 게스트를 저장하면 isGuest=false로 승격 |
| `Crew` | id, name, members([Member]?), sortIndex, lastUsedAt, lastGame, lastAbsentIDs | 이름 충돌 피하려고 Group 대신 Crew |
| `GameSession` | id, date, gameRaw, crew?, participants([ParticipantSnapshot] JSON), payerID?, payerName?, isLuckyRound, mercyOn, soloOn, scores JSON, receipt JSON, total, perPerson, rematchOfID?, source(`app`/`web-import`), approximateDate | 참가자는 스냅샷으로 저장(나중에 멤버 이름이 바뀌어도 과거 기록 유지) |
| `FortuneDraw` | id, date, cardID, luckyMenu | 하루 1회 |

값 타입: `ParticipantSnapshot { memberID, name, feather, accessory }`, `ReceiptItem { name, qty, price }`.

## 2. 웹 버전(v0.8.x) 백업 형식
웹 앱 `설정 > 내보내기`가 클립보드에 넣는 JSON. **members/teams/stats는 JSON 문자열을 한 번 더 감싼 값**(이중 인코딩)이라 두 번 파싱해야 한다.

```json
{
  "version": "v0.8.1",
  "slot": 1,
  "slotName": "Slot 1",
  "members": "[\"민수\",\"지은\",\"서준\"]",
  "teams": "{\"디자인팀\":{\"count\":3,\"names\":[\"민수\",\"지은\",\"서준\"]}}",
  "stats": "{\"민수\":{\"total\":3,\"monthly\":{\"2026-09\":2,\"2026-10\":1},\"daily\":[\"2026-09-03\",\"2026-09-20\",\"2026-10-02\"]}}",
  "settings": { "lang": "ko", "dark": "false", "record": "true" }
}
```
- `stats[name].daily` = 그 사람이 쏜 날짜 목록(YYYY-MM-DD, UTC 기준으로 저장됨).
- 오래된 데이터는 `total`이나 `monthly` 합이 `daily` 개수보다 클 수 있다(daily 도입 전 기록).

## 3. 가져오기 규칙 (`WebBackupImporter`)
1. members → `Member` 생성(이름 중복은 기존 멤버 재사용). 깃털·소품은 이름 순서대로 기본 조합을 돌려 배정.
2. teams → `Crew`(이름 그대로), 멤버 연결.
3. stats → 사람별 `daily` 날짜마다 `GameSession(game: .legacy, payerName: name, source: web-import)`.
4. `monthly[월] - (그 달 daily 개수)`가 양수면, 그 수만큼 그 달 1일 날짜로 세션 생성 + `approximateDate = true`.
5. `total - (daily + 보정 수)`가 양수면 날짜 미상 세션으로 만들지 않고 `Member.legacyUnknownCount`로만 더한다(통계에만 반영).
6. settings.lang → 앱 언어 제안(강제 변경 없음). dark/record는 무시.
7. 같은 백업을 두 번 가져와도 중복 생성되지 않게 `(payerName, date, source)` 조합으로 검사.

입력 경로: 설정 > "웹 버전에서 가져오기" → 붙여넣기 텍스트 필드(클립보드 감지 시 자동 채움) → 미리보기(멤버 N, 그룹 N, 기록 N) → 가져오기.
