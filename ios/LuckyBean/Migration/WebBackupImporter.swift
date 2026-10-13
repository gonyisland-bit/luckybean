import Foundation

/// 웹 버전(v0.8.x) 백업 JSON 파서. SwiftData에 넣기 전 단계(순수 Swift, 테스트 대상).
/// members/teams/stats 값은 JSON 문자열이 한 번 더 감싸져 있다(이중 인코딩).
struct WebBackup: Equatable, Sendable {
    struct Team: Equatable, Sendable { var name: String; var memberNames: [String] }
    struct PaidRecord: Equatable, Sendable { var name: String; var date: Date; var approximate: Bool }

    var members: [String]
    var teams: [Team]
    var records: [PaidRecord]
    /// 날짜를 복원할 수 없는 결제 횟수(이름별)
    var unknownCounts: [String: Int]
    var language: String?
}

enum WebBackupError: Error, Equatable { case notJSON, unsupported }

enum WebBackupImporter {
    private struct Raw: Decodable {
        var version: String?
        var members: String?
        var teams: String?
        var stats: String?
        var settings: Settings?
        struct Settings: Decodable { var lang: String? }
    }
    private struct RawTeam: Decodable { var count: Int?; var names: [String]? }
    private struct RawStat: Decodable { var total: Int?; var monthly: [String: Int]?; var daily: [String]? }

    static func parse(_ text: String) throws -> WebBackup {
        guard let data = text.trimmingCharacters(in: .whitespacesAndNewlines).data(using: .utf8),
              let raw = try? JSONDecoder().decode(Raw.self, from: data) else { throw WebBackupError.notJSON }
        guard raw.members != nil || raw.stats != nil || raw.teams != nil else { throw WebBackupError.unsupported }

        let members: [String] = decodeInner(raw.members) ?? []
        let rawTeams: [String: RawTeam] = decodeInner(raw.teams) ?? [:]
        let stats: [String: RawStat] = decodeInner(raw.stats) ?? [:]

        let teams = rawTeams.keys.sorted().map { WebBackup.Team(name: $0, memberNames: rawTeams[$0]?.names ?? []) }

        var records: [WebBackup.PaidRecord] = []
        var unknown: [String: Int] = [:]
        for name in stats.keys.sorted() {
            let s = stats[name]!
            let days = (s.daily ?? []).compactMap(dayFormatter.date(from:))
            records += days.map { .init(name: name, date: $0, approximate: false) }

            // 월별 합계가 daily보다 크면 그 달 1일로 보정
            var restored = days.count
            for (month, count) in (s.monthly ?? [:]).sorted(by: { $0.key < $1.key }) {
                let inMonth = (s.daily ?? []).filter { $0.hasPrefix(month) }.count
                let missing = count - inMonth
                if missing > 0, let first = dayFormatter.date(from: month + "-01") {
                    records += Array(repeating: .init(name: name, date: first, approximate: true), count: missing)
                    restored += missing
                }
            }
            let leftover = (s.total ?? 0) - restored
            if leftover > 0 { unknown[name] = leftover }
        }

        // 기록에만 있고 멤버 목록에 없는 이름도 멤버로 살린다
        var allMembers = members
        for n in stats.keys.sorted() where !allMembers.contains(n) { allMembers.append(n) }

        return WebBackup(members: allMembers, teams: teams, records: records.sorted { $0.date < $1.date },
                         unknownCounts: unknown, language: raw.settings?.lang)
    }

    private static func decodeInner<T: Decodable>(_ s: String?) -> T? {
        guard let s, let d = s.data(using: .utf8) else { return nil }
        return try? JSONDecoder().decode(T.self, from: d)
    }

    /// 웹은 toISOString().slice(0,10) → UTC 날짜. UTC 0시 = 한국·일본 오전 9시라 같은 날로 보인다.
    nonisolated(unsafe) private static let dayFormatter: DateFormatter = {
        let f = DateFormatter()
        f.calendar = Calendar(identifier: .gregorian)
        f.locale = Locale(identifier: "en_US_POSIX")
        f.timeZone = TimeZone(identifier: "UTC")
        f.dateFormat = "yyyy-MM-dd"
        f.defaultDate = nil
        return f
    }()
}
