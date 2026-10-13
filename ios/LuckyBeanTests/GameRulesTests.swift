import Testing
@testable import LuckyBean

/// 게임 규칙 테스트. 자비 가중치가 정확히 지켜지는지 10만 회 시뮬레이션으로 확인한다.
/// (맥 없이 작성한 코드라, 같은 수식을 Python으로 미리 검증해 둠: docs/02 참고)
struct GameRulesTests {
    let players: [PlayerID] = ["a", "b", "c", "d", "e"]
    var mercyWeights: [PlayerID: Double] { GameRules.weights(for: players, mercyOn: true, recentPayers: ["b"]) }
    let runs = 100_000

    @Test func mercyWeightIsHalfOnlyForRecentPayer() {
        let w = mercyWeights
        #expect(w["b"] == 0.5)
        #expect(w["a"] == 1.0)
        let off = GameRules.weights(for: players, mercyOn: false, recentPayers: ["b"])
        #expect(off["b"] == 1.0)
    }

    @Test func luckyRoundNeverTwiceInARow() {
        var rng = SeededRNG(seed: 1)
        for _ in 0..<10_000 { #expect(!GameRules.rollLuckyRound(previousWasLucky: true, using: &rng)) }
    }

    @Test func luckyRoundRateIsAbout15Percent() {
        var rng = SeededRNG(seed: 2)
        let hits = (0..<runs).filter { _ in GameRules.rollLuckyRound(previousWasLucky: false, using: &rng) }.count
        #expect(abs(Double(hits) / Double(runs) - 0.15) < 0.01)
    }

    @Test func weightedPickMatchesWeights() {
        var rng = SeededRNG(seed: 3)
        var count: [PlayerID: Int] = [:]
        for _ in 0..<runs { count[GameRules.pickWeighted(mercyWeights, using: &rng), default: 0] += 1 }
        let total = mercyWeights.values.reduce(0, +)
        for p in players {
            #expect(abs(Double(count[p, default: 0]) / Double(runs) - mercyWeights[p]! / total) < 0.01)
        }
    }

    /// 빨대뽑기: 뽑는 순서와 무관하게 결제 확률 = w_i / Σw
    @Test func strawConditionalDrawIsFair() {
        var rng = SeededRNG(seed: 4)
        var count: [PlayerID: Int] = [:]
        for _ in 0..<runs {
            var engine = StrawDrawEngine(players: players, weights: mercyWeights, isLuckyRound: false)
            while engine.outcome == nil { _ = engine.draw(using: &rng) }
            if case let .payer(p) = engine.outcome { count[p, default: 0] += 1 }
        }
        let total = mercyWeights.values.reduce(0, +)
        for p in players {
            #expect(abs(Double(count[p, default: 0]) / Double(runs) - mercyWeights[p]! / total) < 0.01)
        }
    }

    @Test func strawLuckyRoundEveryoneSafe() {
        var rng = SeededRNG(seed: 5)
        var engine = StrawDrawEngine(players: players, weights: mercyWeights, isLuckyRound: true)
        while engine.outcome == nil { #expect(engine.draw(using: &rng) == .safe) }
        #expect(engine.outcome == .luckyRound)
    }

    @Test func roastStopsOnWinningSegment() {
        var rng = SeededRNG(seed: 6)
        for n in 2...12 {
            let ps = (0..<n).map { "p\($0)" }
            let w = Dictionary(uniqueKeysWithValues: ps.map { ($0, 1.0) })
            for _ in 0..<200 {
                let e = RoastRouletteEngine(players: ps, weights: w, isLuckyRound: false, using: &rng)
                #expect(e.segmentUnderArrow(rotation: e.finalRotation) == e.winningIndex)
            }
        }
    }

    @Test func cardHugAlwaysEndsWithCardOwnerOrLucky() {
        var rng = SeededRNG(seed: 7)
        for lucky in [false, true] {
            for _ in 0..<2_000 {
                var e = CardHugEngine(players: players, weights: mercyWeights, isLuckyRound: lucky, using: &rng)
                var steps = 0
                while e.outcome == nil, let picker = e.currentPicker, steps < 50 {
                    let targets = e.targets(for: picker)
                    _ = e.pick(targets.randomElement(using: &rng)!)
                    steps += 1
                }
                #expect(e.outcome != nil)
                if lucky { #expect(e.outcome == .luckyRound) }
            }
        }
    }

    @Test func jumpTimeoutPaysImmediately() {
        var e = PigeonJumpEngine(players: ["a", "b", "c"])
        var rng = SeededRNG(seed: 8)
        e.jump(at: 0.91, using: &rng)
        e.timeout()
        #expect(e.resolution == .payer("b"))
    }

    @Test func espressoFurthestFromNinePays() {
        var rng = SeededRNG(seed: 9)
        var e = EspressoEngine(players: ["a", "b"], using: &rng)
        // 바늘을 직접 맞추기 어려우니 판정 함수만 검증
        let tNine = (EspressoEngine.target / EspressoEngine.maxBar) * (EspressoEngine.baseHalfPeriod / e.speedFactor)
        e.stop(at: tNine)          // a ≈ 9.0
        e.stop(at: 0.01)           // b ≈ 0.1
        #expect(e.resolution == .payer("b"))
    }

    @Test func koreanParticle() {
        #expect(KoreanParticle.subject(of: "서준") == "서준이")
        #expect(KoreanParticle.subject(of: "하린") == "하린이")
        #expect(KoreanParticle.subject(of: "도윤") == "도윤이")
        #expect(KoreanParticle.subject(of: "지우") == "지우가")
        #expect(KoreanParticle.subject(of: "Mina") == "Mina가")
    }
}
