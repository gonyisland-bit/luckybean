import Foundation

/// 모든 게임이 공유하는 규칙: 럭키 라운드, 자비 가중치, 가중 추첨.
/// 순수 Swift. 난수는 주입받는다(테스트에서 SeededRNG 사용).
enum GameRules {
    static let luckyRoundChance = 0.15
    static let mercyWeight = 0.5
    static let mercyWindow: TimeInterval = 24 * 60 * 60
    static let skillMercyWidening = 1.2

    /// 럭키 라운드 여부. 직전 판이 럭키였으면 연속 금지.
    static func rollLuckyRound<R: RandomNumberGenerator>(previousWasLucky: Bool, using rng: inout R) -> Bool {
        guard !previousWasLucky else { return false }
        return Double.random(in: 0..<1, using: &rng) < luckyRoundChance
    }

    /// 자비 모드 가중치. 최근 24시간 안에 이 그룹에서 결제한 사람은 0.5.
    static func weights(for players: [PlayerID], mercyOn: Bool, recentPayers: Set<PlayerID>) -> [PlayerID: Double] {
        Dictionary(uniqueKeysWithValues: players.map { id in
            (id, (mercyOn && recentPayers.contains(id)) ? mercyWeight : 1.0)
        })
    }

    /// 최근 결제자 추출(같은 그룹, 24시간 이내, 럭키 제외).
    static func recentPayers(from history: [(date: Date, payer: PlayerID?)], now: Date) -> Set<PlayerID> {
        Set(history.compactMap { entry in
            guard let payer = entry.payer, now.timeIntervalSince(entry.date) <= mercyWindow else { return nil }
            return payer
        })
    }

    /// 가중 추첨 1명.
    static func pickWeighted<R: RandomNumberGenerator>(_ weights: [PlayerID: Double], using rng: inout R) -> PlayerID {
        precondition(!weights.isEmpty, "추첨 대상이 없음")
        // 딕셔너리 순서는 실행마다 달라질 수 있으니 정렬해서 재현성 보장
        let entries = weights.sorted { $0.key < $1.key }
        let total = entries.reduce(0) { $0 + $1.value }
        var roll = Double.random(in: 0..<total, using: &rng)
        for (id, w) in entries {
            if roll < w { return id }
            roll -= w
        }
        return entries[entries.count - 1].key
    }

    /// 빨대뽑기처럼 "뽑는 순간마다" 결정하는 게임용.
    /// 남은 사람들의 가중치 합 대비 이 사람의 가중치 = 이번 뽑기에서 걸릴 확률.
    /// 이 방식이면 전체 결제 확률이 정확히 w_i / Σw 가 된다(테스트 참고).
    static func conditionalHit<R: RandomNumberGenerator>(
        drawer: PlayerID, remaining: [PlayerID], weights: [PlayerID: Double], using rng: inout R
    ) -> Bool {
        let total = remaining.reduce(0) { $0 + (weights[$1] ?? 1) }
        guard total > 0 else { return true }
        let p = (weights[drawer] ?? 1) / total
        return Double.random(in: 0..<1, using: &rng) < p
    }
}

/// 참가자 식별자. 멤버 UUID 문자열 또는 게스트 임시 ID.
typealias PlayerID = String

/// 한 판의 결과.
enum RoundOutcome: Equatable, Sendable {
    case payer(PlayerID)
    case luckyRound
}

/// 결정 가능한 난수(테스트·리플레이용). SplitMix64.
struct SeededRNG: RandomNumberGenerator, Sendable {
    private var state: UInt64
    init(seed: UInt64) { state = seed }
    mutating func next() -> UInt64 {
        state &+= 0x9E37_79B9_7F4A_7C15
        var z = state
        z = (z ^ (z >> 30)) &* 0xBF58_476D_1CE4_E5B9
        z = (z ^ (z >> 27)) &* 0x94D0_49BB_1331_11EB
        return z ^ (z >> 31)
    }
}
