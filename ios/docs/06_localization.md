# 06 · 다국어 용어집 (ko / ja / en)

- 기본 언어 ko. 일본어는 존댓말 대신 다정한 반말 톤(です・ます는 버튼 문구에만 짧게).
- 일본어 폰트: Zen Maru Gothic(제목·본문 모두). 한국어 제목 Jua, 본문 시스템.
- 일본어가 가장 길다고 가정: 버튼 라벨은 일본어 기준 10자 이내로 맞춘다.

| 키 | ko | ja | en |
|---|---|---|---|
| app.name | 럭키빈 | ラッキービーン | Lucky Bean |
| action.coffeeBet | 커피내기 | コーヒー賭け | Coffee Bet |
| picker.title | 무슨 게임으로 정할까요? | どのゲームで決める？ | Which game today? |
| badge.luck | 운 | 運 | Luck |
| badge.skill | 실력 | 実力 | Skill |
| rule.luckyRound | 럭키 라운드 15% · 전원 통과 | ラッキーラウンド15%・全員セーフ | Lucky round 15% · everyone's safe |
| rule.solo | 한 명이 진행 | ひとりで進行 | One phone, one host |
| rule.mercy | 자비 모드 | おなさけモード | Mercy mode |
| guests.title | 오늘의 손님 | 今日のお客さん | Today's guests |
| guests.start | %lld명으로 시작 | %lld人ではじめる | Start with %lld |
| game.cardHug | 카드품기 | カードかくし | Card Hug |
| game.roast | 로스팅 룰렛 | ロースト・ルーレット | Roast Roulette |
| game.kiri | 키리의 선택 | キリのえらび | Kiri's Pick |
| game.straw | 빨대뽑기 | ストローくじ | Straw Draw |
| game.jump | 비둘기 점프 | ハトジャンプ | Pigeon Jump |
| game.espresso | 에스프레소 마스터 | エスプレッソマスター | Espresso Master |
| turn.badge | %1$lld/%2$lld · %3$@ | %1$lld/%2$lld・%3$@ | %1$lld/%2$lld · %3$@ |
| handoff.title | %@ 차례 | %@の番 | %@'s turn |
| handoff.ready | 준비됐어요 | じゅんびOK | Ready |
| exit.title | 이 판을 접을까요? | このゲームをやめる？ | Quit this round? |
| reveal.payer | %@이(가) 쏩니다! | %@のおごり！ | %@ treats everyone! |
| reveal.lucky | 오늘은 사장님이 쏩니다! | 今日はマスターのおごり！ | The house is buying today! |
| receipt.saved | 기록에 저장했어요 | 記録に保存したよ | Saved to records |
| receipt.undo | 되돌리기 %lld | 取り消し %lld | Undo %lld |
| receipt.perPerson | 1인당 (%lld명) | ひとりあたり（%lld人） | Per person (%lld) |
| receipt.rematch | 복수전! 한 판 더 | リベンジ！もう一回 | Rematch! |
| receipt.share | 이미지로 공유 | 画像でシェア | Share image |
| nearby.title | 게임 끝! 가까운 카페 | ゲーム終了！近くのカフェ | Game over! Cafés nearby |
| nearby.directions | 길찾기 | ルート | Directions |
| kiri.stalk | 살금살금… 누구를 덮칠까 | そろり…だれにしようかな | Sneaking… who's it gonna be? |
| kiri.catch | 덥석! | ガブッ！ | Pounce! |

한국어 조사 처리: `reveal.payer`는 받침 유무로 이/가를 고르는 헬퍼(`KoreanParticle.subject(of:)`)를 쓴다. 문자열에 `이(가)`를 그대로 노출하지 않는다.
