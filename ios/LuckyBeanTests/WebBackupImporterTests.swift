import Testing
import Foundation
@testable import LuckyBean

struct WebBackupImporterTests {
    /// 웹 v0.8.1 내보내기 형식 그대로(값이 JSON 문자열로 한 번 더 감싸져 있음)
    let sample = #"""
    {"version":"v0.8.1","slot":1,"slotName":"Slot 1",
     "members":"[\"민수\",\"지은\",\"서준\"]",
     "teams":"{\"디자인팀\":{\"count\":3,\"names\":[\"민수\",\"지은\",\"서준\"]}}",
     "stats":"{\"민수\":{\"total\":5,\"monthly\":{\"2026-09\":3,\"2026-10\":1},\"daily\":[\"2026-09-03\",\"2026-10-02\"]},\"도윤\":{\"total\":1,\"monthly\":{\"2026-08\":1},\"daily\":[\"2026-08-15\"]}}",
     "settings":{"lang":"ko","dark":"false","record":"true"}}
    """#

    @Test func parsesDoubleEncodedFields() throws {
        let b = try WebBackupImporter.parse(sample)
        #expect(b.members == ["민수", "지은", "서준", "도윤"])   // 기록에만 있던 도윤도 멤버로
        #expect(b.teams == [.init(name: "디자인팀", memberNames: ["민수", "지은", "서준"])])
        #expect(b.language == "ko")
    }

    @Test func restoresMissingMonthlyRecordsAsApproximate() throws {
        let b = try WebBackupImporter.parse(sample)
        let minsu = b.records.filter { $0.name == "민수" }
        // daily 2개 + 9월 보정 2개(3-1) = 4, total 5 → 날짜 미상 1
        #expect(minsu.count == 4)
        #expect(minsu.filter(\.approximate).count == 2)
        #expect(b.unknownCounts["민수"] == 1)
        #expect(b.unknownCounts["도윤"] == nil)
    }

    @Test func rejectsGarbage() {
        #expect(throws: WebBackupError.notJSON) { try WebBackupImporter.parse("hello") }
        #expect(throws: WebBackupError.unsupported) { try WebBackupImporter.parse("{\"foo\":1}") }
    }
}
