import Foundation

// 운 게임 4종 엔진. UI 없음, 시간 없음. 뷰는 엔진 상태를 그리고 사용자 입력을 그대로 넘긴다.
// 각 엔진의 "결정 시점"은 docs/02 표를 따른다.

// MARK: - 카드품기

/// 차례인 사람이 남의 비둘기를 지목한다. 카드는 시작 시 가중치로 한 비둘기에 숨겨 둔다.
struct CardHugEngine: Sendable {
    enum PickResult: Equatable, Sendable { case flewAway(owner: PlayerID), cardFound(owner: PlayerID) }

    let players: [PlayerID]          // 차례 순서
    let isLuckyRound: Bool
    private let cardOwner: PlayerID?  // 럭키 라운드면 nil (카드 없음)
    private(set) var flown: Set<PlayerID> = []
    private(set) var turnIndex = 0
    private(set) var outcome: RoundOutcome?

    init<R: RandomNumberGenerator>(players: [PlayerID], weights: [PlayerID: Double], isLuckyRound: Bool, using rng: inout R) {
        precondition(GameKind.cardHug.playerRange.contains(players.count))
        self.players = players
        self.isLuckyRound = isLuckyRound
        self.cardOwner = isLuckyRound ? nil : GameRules.pickWeighted(weights, using: &rng)
        skipTurnsWithoutTargets()
    }

    var remaining: [PlayerID] { players.filter { !flown.contains($0) } }
    var currentPicker: PlayerID? { outcome == nil ? players[turnIndex % players.count] : nil }

    /// 지목 가능한 비둘기: 아직 앉아 있고 내 것이 아닌 것.
    func targets(for picker: PlayerID) -> [PlayerID] { remaining.filter { $0 != picker } }

    mutating func pick(_ target: PlayerID) -> PickResult? {
        guard outcome == nil, let picker = currentPicker, targets(for: picker).contains(target) else { return nil }
        if target == cardOwner {
            outcome = .payer(target)
            return .cardFound(owner: target)
        }
        flown.insert(target)
        if remaining.count == 1 { // 마지막 1마리는 자동 공개
            let last = remaining[0]
            outcome = (last == cardOwner) ? .payer(last) : .luckyRound
        } else {
            turnIndex += 1
            skipTurnsWithoutTargets()
        }
        return .flewAway(owner: target)
    }

    private mutating func skipTurnsWithoutTargets() {
        var guardCount = 0
        while outcome == nil, let p = currentPicker, targets(for: p).isEmpty, guardCount < players.count {
            turnIndex += 1; guardCount += 1
        }
    }
}

// MARK: - 로스팅 룰렛

/// 칸 크기는 모두 같다. 결과는 시작 시 가중치로 정하고, 회전 각도를 그 칸에 멈추도록 역산한다.
struct RoastRouletteEngine: Sendable {
    let segments: [PlayerID]      // 시계 방향, 0번 칸이 12시에서 시작
    let winningIndex: Int
    let isLuckyRound: Bool
    /// 최종 회전 각도(도). 화살표는 12시 고정, 통이 시계 방향으로 돈다.
    let finalRotation: Double
    let spinDuration: Double

    init<R: RandomNumberGenerator>(players: [PlayerID], weights: [PlayerID: Double], isLuckyRound: Bool, using rng: inout R) {
        precondition(GameKind.roastRoulette.playerRange.contains(players.count))
        let shuffled = players.shuffled(using: &rng)
        segments = shuffled
        self.isLuckyRound = isLuckyRound
        if isLuckyRound {
            winningIndex = Int.random(in: 0..<shuffled.count, using: &rng) // 이 칸 바닥에 LUCKY PASS
        } else {
            let payer = GameRules.pickWeighted(weights, using: &rng)
            winningIndex = shuffled.firstIndex(of: payer)!
        }
        let seg = 360.0 / Double(shuffled.count)
        let jitter = Double.random(in: -0.35...0.35, using: &rng) * seg / 2
        let centerOfWinner = (Double(winningIndex) + 0.5) * seg
        let turns = Double(Int.random(in: 4...6, using: &rng))
        // 회전 R 후 12시에 오는 칸 = (360 - R) mod 360 위치
        finalRotation = turns * 360 + (360 - centerOfWinner) + jitter
        spinDuration = Double.random(in: 3.5...5.0, using: &rng)
    }

    var outcome: RoundOutcome { isLuckyRound ? .luckyRound : .payer(segments[winningIndex]) }

    /// 회전 각도 → 12시에 걸린 칸 번호 (틱 햅틱·검증용)
    func segmentUnderArrow(rotation: Double) -> Int {
        let seg = 360.0 / Double(segments.count)
        let pos = (360 - rotation.truncatingRemainder(dividingBy: 360)).truncatingRemainder(dividingBy: 360)
        return Int(((pos + 360).truncatingRemainder(dividingBy: 360)) / seg) % segments.count
    }
}

// MARK: - 키리의 선택

/// 결과는 시작 시 결정. 배회 경로(가짜 접근 포함)는 연출용 계획.
struct KiriChoiceEngine: Sendable {
    let target: PlayerID?      // 럭키면 nil: 키리가 덮쳤는데 빈 풀밭(비둘기가 다 피함)
    let isLuckyRound: Bool
    let waypoints: [PlayerID]  // 가짜 접근 대상들 → 마지막이 실제 대상
    let plannedDuration: Double
    static let minimumDuration = 1.5

    init<R: RandomNumberGenerator>(players: [PlayerID], weights: [PlayerID: Double], isLuckyRound: Bool, using rng: inout R) {
        precondition(GameKind.kiriChoice.playerRange.contains(players.count))
        self.isLuckyRound = isLuckyRound
        let chosen: PlayerID
        if isLuckyRound { chosen = players.randomElement(using: &rng)! } else { chosen = GameRules.pickWeighted(weights, using: &rng) }
        target = isLuckyRound ? nil : chosen
        let decoyCount = Int.random(in: 1...2, using: &rng)
        let others = players.filter { $0 != chosen }.shuffled(using: &rng)
        waypoints = Array(others.prefix(decoyCount)) + [chosen]
        plannedDuration = Double.random(in: 3.0...6.0, using: &rng)
    }

    var outcome: RoundOutcome { target.map { .payer($0) } ?? .luckyRound }

    /// 화면을 탭했을 때 남은 시간을 줄인다. 결과는 바뀌지 않는다.
    func hurriedDuration(elapsed: Double) -> Double {
        max(Self.minimumDuration, min(plannedDuration, elapsed + 0.8))
    }
}

// MARK: - 빨대뽑기

/// 내 빨대를 내가 뽑는다. 뽑는 순간마다 조건부 확률로 꼬불 여부를 정한다.
struct StrawDrawEngine: Sendable {
    enum DrawResult: Equatable, Sendable { case safe, curly }

    let players: [PlayerID]
    let weights: [PlayerID: Double]
    let isLuckyRound: Bool
    private(set) var drawn: [PlayerID] = []
    private(set) var outcome: RoundOutcome?

    init(players: [PlayerID], weights: [PlayerID: Double], isLuckyRound: Bool) {
        precondition(GameKind.strawDraw.playerRange.contains(players.count))
        self.players = players
        self.weights = weights
        self.isLuckyRound = isLuckyRound
    }

    var remaining: [PlayerID] { players.filter { !drawn.contains($0) } }
    var currentDrawer: PlayerID? { outcome == nil ? remaining.first : nil }

    mutating func draw<R: RandomNumberGenerator>(using rng: inout R) -> DrawResult? {
        guard let drawer = currentDrawer else { return nil }
        let pool = remaining
        drawn.append(drawer)
        if isLuckyRound {
            if remaining.isEmpty { outcome = .luckyRound }
            return .safe
        }
        if GameRules.conditionalHit(drawer: drawer, remaining: pool, weights: weights, using: &rng) {
            outcome = .payer(drawer)
            return .curly
        }
        return .safe
    }
}
