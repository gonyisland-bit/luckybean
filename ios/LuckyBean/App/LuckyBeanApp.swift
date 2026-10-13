import SwiftUI
import SwiftData

@main
struct LuckyBeanApp: App {
    @State private var router = AppRouter()
    private let container: ModelContainer = {
        do { return try LuckyBeanSchema.makeContainer() }
        catch { fatalError("ModelContainer 생성 실패: \(error)") }
    }()

    var body: some Scene {
        WindowGroup {
            RootView()
                .environment(router)
                .tint(LB.Palette.primary)
        }
        .modelContainer(container)
    }
}

/// 화면 이동. 커피내기 흐름은 하나의 NavigationStack 경로로 관리한다.
@MainActor @Observable
final class AppRouter {
    enum Route: Hashable {
        case gamePicker
        case play(GameKind, players: [PlayerID], rules: RoundRules)
        case reveal(sessionID: UUID)
        case receipt(sessionID: UUID)
        case nearby
        case records
        case lounge
        case vibe
        case members
        case settings
    }

    var path: [Route] = []
    var guestSheetFor: GameKind?

    func startCoffeeBet() { path = [.gamePicker] }
    func pick(_ game: GameKind) { guestSheetFor = game }
    func play(_ game: GameKind, players: [PlayerID], rules: RoundRules) {
        guestSheetFor = nil
        path.append(.play(game, players: players, rules: rules))
    }
    func backToStreet() { path = [] }
}

struct RootView: View {
    @Environment(AppRouter.self) private var router

    var body: some View {
        @Bindable var router = router
        NavigationStack(path: $router.path) {
            StreetView()
                .navigationDestination(for: AppRouter.Route.self) { route in
                    switch route {
                    case .gamePicker: GamePickerView()
                    case let .play(game, players, rules): PlayPlaceholderView(game: game, players: players, rules: rules)
                    default: ComingSoonView(route: route)
                    }
                }
        }
        .sheet(item: $router.guestSheetFor) { game in
            GuestSheet(game: game)
                .presentationDetents([.large])
                .presentationCornerRadius(LB.Radius.l)
        }
    }
}

/// 아직 안 만든 화면 자리표시(M0에서 하나씩 교체).
struct ComingSoonView: View {
    let route: AppRouter.Route
    var body: some View {
        ZStack {
            LB.Palette.cream.ignoresSafeArea()
            Text(String(describing: route)).font(LB.Typeface.body(13)).foregroundStyle(LB.Palette.inkSub).padding()
        }
        .toolbar(.hidden, for: .navigationBar)
    }
}
