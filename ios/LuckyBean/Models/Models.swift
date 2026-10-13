import Foundation
import SwiftData

// CloudKit 동기화 규칙: 모든 속성 기본값/optional, unique 제약 금지, 관계 optional.

enum Feather: String, Codable, CaseIterable, Sendable { case gray, white, brown, charcoal, sand, rose, slate, cocoa }
enum Accessory: String, Codable, CaseIterable, Sendable { case none, beret, ribbon, scarf, glasses, cap, flower, bowtie, bandana, crown, headphones }
enum LegBand: String, Codable, CaseIterable, Sendable { case coral, sky, mustard, mint, peach, lilac, leaf, berry }

@Model
final class Member {
    var id: UUID = UUID()
    var name: String = ""
    var featherRaw: String = Feather.gray.rawValue
    var accessoryRaw: String = Accessory.none.rawValue
    var legBandRaw: String = LegBand.coral.rawValue
    var isGuest: Bool = false
    var archived: Bool = false
    var createdAt: Date = Date()
    /// 웹 버전에서 날짜 없이 넘어온 결제 횟수(통계에만 더함)
    var legacyUnknownCount: Int = 0
    @Relationship(inverse: \Crew.members) var crews: [Crew]? = []

    init(name: String, feather: Feather = .gray, accessory: Accessory = .none, legBand: LegBand = .coral, isGuest: Bool = false) {
        self.name = name
        self.featherRaw = feather.rawValue
        self.accessoryRaw = accessory.rawValue
        self.legBandRaw = legBand.rawValue
        self.isGuest = isGuest
    }

    var feather: Feather { Feather(rawValue: featherRaw) ?? .gray }
    var accessory: Accessory { Accessory(rawValue: accessoryRaw) ?? .none }
    var legBand: LegBand { LegBand(rawValue: legBandRaw) ?? .coral }
    var playerID: PlayerID { id.uuidString }
}

/// 그룹. SwiftUI의 Group과 이름이 겹치지 않게 Crew.
@Model
final class Crew {
    var id: UUID = UUID()
    var name: String = ""
    var members: [Member]? = []
    var sortIndex: Int = 0
    var lastUsedAt: Date = Date()
    var lastGameRaw: String?
    /// 마지막 판에서 빠졌던 멤버(다음 손님 시트의 기본값)
    var lastAbsentIDs: [UUID] = []

    init(name: String, members: [Member] = []) {
        self.name = name
        self.members = members
    }
}

struct ParticipantSnapshot: Codable, Hashable, Sendable {
    var memberID: UUID?
    var name: String
    var featherRaw: String
    var accessoryRaw: String
}

struct ReceiptItem: Codable, Hashable, Sendable {
    var name: String
    var qty: Int
    var price: Int
}

enum SessionSource: String, Codable, Sendable { case app, webImport }

@Model
final class GameSession {
    var id: UUID = UUID()
    var date: Date = Date()
    var gameRaw: String = GameKind.legacy.rawValue
    var crew: Crew?
    var participantsData: Data = Data()   // [ParticipantSnapshot] JSON
    var payerID: UUID?
    var payerName: String?
    var isLuckyRound: Bool = false
    var mercyOn: Bool = false
    var soloHost: Bool = true
    var scoresData: Data?                 // [이름: 점수] JSON (실력 게임)
    var receiptData: Data?                // [ReceiptItem] JSON
    var total: Int = 0
    var rematchOfID: UUID?
    var sourceRaw: String = SessionSource.app.rawValue
    var approximateDate: Bool = false

    init(date: Date = Date(), game: GameKind, payerName: String?, source: SessionSource = .app) {
        self.date = date
        self.gameRaw = game.rawValue
        self.payerName = payerName
        self.sourceRaw = source.rawValue
    }

    var game: GameKind { GameKind(rawValue: gameRaw) ?? .legacy }

    var participants: [ParticipantSnapshot] {
        get { (try? JSONDecoder().decode([ParticipantSnapshot].self, from: participantsData)) ?? [] }
        set { participantsData = (try? JSONEncoder().encode(newValue)) ?? Data() }
    }

    var receipt: [ReceiptItem] {
        get { receiptData.flatMap { try? JSONDecoder().decode([ReceiptItem].self, from: $0) } ?? [] }
        set { receiptData = try? JSONEncoder().encode(newValue); total = newValue.reduce(0) { $0 + $1.qty * $1.price } }
    }

    /// 1인당 금액(원 단위 올림)
    var perPerson: Int {
        let n = max(participants.count, 1)
        return (total + n - 1) / n
    }
}

@Model
final class FortuneDraw {
    var id: UUID = UUID()
    var date: Date = Date()
    var cardID: String = ""
    var luckyMenu: String?

    init(date: Date = Date(), cardID: String, luckyMenu: String? = nil) {
        self.date = date
        self.cardID = cardID
        self.luckyMenu = luckyMenu
    }
}

enum LuckyBeanSchema {
    static let models: [any PersistentModel.Type] = [Member.self, Crew.self, GameSession.self, FortuneDraw.self]

    @MainActor
    static func makeContainer(inMemory: Bool = false) throws -> ModelContainer {
        let config = ModelConfiguration(
            schema: Schema(models),
            isStoredInMemoryOnly: inMemory,
            cloudKitDatabase: inMemory ? .none : .private("iCloud.studio.devgon.luckybean")
        )
        return try ModelContainer(for: Schema(models), configurations: config)
    }
}
