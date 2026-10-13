import Foundation

// 실력 게임 2종. 화면은 시간 t(초)를 넘겨 바/바늘 위치를 받아 그리고, 탭 시점의 t로 판정한다.

/// 실력 게임 공통: 가장 나쁜 점수를 찾고, 동점이면 재대결 명단을 돌려준다.
enum SkillResolution: Equatable, Sendable {
    case payer(PlayerID)
    case tieBreak([PlayerID])
}

// MARK: - 비둘기 점프

struct PigeonJumpEngine: Sendable {
    static let barPeriod = 1.4          // 타이밍 바 왕복 주기(초)
    static let timeLimit = 10.0
    static let greenCenter = 0.65
    static let greenHalfWidth = 0.10

    let players: [PlayerID]
    let mercyTargets: Set<PlayerID>
    private(set) var distances: [PlayerID: Double] = [:]
    private(set) var timedOut: PlayerID?

    init(players: [PlayerID], mercyTargets: Set<PlayerID> = []) {
        precondition(GameKind.pigeonJump.playerRange.contains(players.count))
        self.players = players
        self.mercyTargets = mercyTargets
    }

    var currentJumper: PlayerID? {
        guard timedOut == nil else { return nil }
        return players.first { distances[$0] == nil }
    }

    /// 0...1 삼각파. 0.5초에 끝까지 갔다 돌아오는 바.
    static func barPosition(at t: Double) -> Double {
        let phase = (t / barPeriod).truncatingRemainder(dividingBy: 1)
        return phase < 0.5 ? phase * 2 : (1 - phase) * 2
    }

    func greenHalfWidth(for player: PlayerID) -> Double {
        Self.greenHalfWidth * (mercyTargets.contains(player) ? GameRules.skillMercyWidening : 1)
    }

    /// 탭 시점의 t(현재 차례 시작부터 경과 초)로 거리(m) 확정.
    @discardableResult
    mutating func jump<R: RandomNumberGenerator>(at t: Double, using rng: inout R) -> Double? {
        guard let p = currentJumper, t <= Self.timeLimit else { return nil }
        let widen = mercyTargets.contains(p) ? GameRules.skillMercyWidening : 1
        let error = abs(Self.barPosition(at: t) - Self.greenCenter) / widen
        let base = max(0.5, 9.0 - error * 12.0)
        let d = ((base + Double.random(in: -0.3...0.3, using: &rng)) * 10).rounded() / 10
        distances[p] = max(0.5, d)
        return distances[p]
    }

    /// 10초 안에 탭하지 않으면 즉시 결제자 확정.
    mutating func timeout() {
        guard let p = currentJumper else { return }
        timedOut = p
    }

    var resolution: SkillResolution? {
        if let timedOut { return .payer(timedOut) }
        guard distances.count == players.count else { return nil }
        let minD = distances.values.min()!
        let losers = players.filter { distances[$0] == minD }
        return losers.count == 1 ? .payer(losers[0]) : .tieBreak(losers)
    }
}

// MARK: - 에스프레소 마스터

struct EspressoEngine: Sendable {
    static let target = 9.0
    static let maxBar = 12.0
    static let baseHalfPeriod = 1.1   // 0→12 BAR 걸리는 시간(초)

    let players: [PlayerID]
    let mercyTargets: Set<PlayerID>
    let speedFactor: Double           // 판마다 ±15%
    private(set) var readings: [PlayerID: Double] = [:]

    init<R: RandomNumberGenerator>(players: [PlayerID], mercyTargets: Set<PlayerID> = [], using rng: inout R) {
        precondition(GameKind.espresso.playerRange.contains(players.count))
        self.players = players
        self.mercyTargets = mercyTargets
        speedFactor = Double.random(in: 0.85...1.15, using: &rng)
    }

    var currentBarista: PlayerID? { players.first { readings[$0] == nil } }

    /// 바늘 위치(BAR). 0→12→0 왕복.
    func needle(at t: Double) -> Double {
        let half = Self.baseHalfPeriod / speedFactor
        let phase = (t / (half * 2)).truncatingRemainder(dividingBy: 1)
        let tri = phase < 0.5 ? phase * 2 : (1 - phase) * 2
        return tri * Self.maxBar
    }

    @discardableResult
    mutating func stop(at t: Double) -> Double? {
        guard let p = currentBarista else { return nil }
        let v = (needle(at: t) * 10).rounded() / 10
        readings[p] = v
        return v
    }

    /// 판정용 차이(자비 대상은 1.2로 나눔). 화면에는 원래 차이를 보여준다.
    func judgedDiff(for p: PlayerID) -> Double? {
        guard let v = readings[p] else { return nil }
        let raw = abs(v - Self.target)
        return mercyTargets.contains(p) ? raw / GameRules.skillMercyWidening : raw
    }

    var resolution: SkillResolution? {
        guard readings.count == players.count else { return nil }
        let diffs = players.map { ($0, judgedDiff(for: $0)!) }
        let maxD = diffs.map(\.1).max()!
        let losers = diffs.filter { abs($0.1 - maxD) < 0.0001 }.map(\.0)
        return losers.count == 1 ? .payer(losers[0]) : .tieBreak(losers)
    }
}
