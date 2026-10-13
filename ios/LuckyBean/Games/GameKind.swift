import Foundation

/// 1.0 게임 6종 + 웹 버전에서 가져온 기록용 legacy.
enum GameKind: String, Codable, CaseIterable, Identifiable, Sendable {
    case cardHug, roastRoulette, kiriChoice, strawDraw, pigeonJump, espresso
    case legacy

    enum Category: Sendable { case luck, skill }

    var id: String { rawValue }

    static var playable: [GameKind] { [.roastRoulette, .cardHug, .kiriChoice, .strawDraw, .pigeonJump, .espresso] }

    var category: Category {
        switch self {
        case .pigeonJump, .espresso: .skill
        default: .luck
        }
    }

    var playerRange: ClosedRange<Int> {
        switch self {
        case .pigeonJump, .espresso: 2...8
        default: 2...12
        }
    }

    /// 차례대로 입력하는 게임인지(차례 넘기기 화면 대상)
    var isTurnBased: Bool {
        switch self {
        case .cardHug, .strawDraw, .pigeonJump, .espresso: true
        case .roastRoulette, .kiriChoice, .legacy: false
        }
    }

    var titleKey: String {
        switch self {
        case .cardHug: "game.cardHug"
        case .roastRoulette: "game.roast"
        case .kiriChoice: "game.kiri"
        case .strawDraw: "game.straw"
        case .pigeonJump: "game.jump"
        case .espresso: "game.espresso"
        case .legacy: "game.legacy"
        }
    }
}

/// 한 판을 시작할 때 고정되는 규칙.
struct RoundRules: Codable, Hashable, Sendable {
    var soloHost = true
    var mercyOn = false
}
