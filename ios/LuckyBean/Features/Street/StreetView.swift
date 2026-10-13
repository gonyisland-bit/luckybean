import SwiftUI

/// S1 거리 첫 화면 (시안: Home6, 밤은 HomeNight6). M3에서 가로 패럴랙스 거리로 교체.
struct StreetView: View {
    @Environment(AppRouter.self) private var router

    var body: some View {
        ZStack(alignment: .bottom) {
            LinearGradient(colors: [Color(hex: 0xE9EEEA), LB.Palette.cream], startPoint: .top, endPoint: .bottom)
                .ignoresSafeArea()
            // TODO(M3): sky/far/ground/fg 레이어 + 장소 단위 스냅 페이징 (docs/04 §3)

            VStack(alignment: .leading, spacing: 4) {
                HStack(spacing: 0) {
                    Text(verbatim: "lucky").foregroundStyle(LB.Palette.ink)
                    Text(verbatim: "bean").foregroundStyle(LB.Palette.lucky)
                }
                .font(LB.Typeface.display(30))
                Text(Date.now, format: .dateTime.month().day().weekday(.wide))
                    .font(LB.Typeface.body(12)).foregroundStyle(LB.Palette.inkSub)
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
            .padding(.horizontal, LB.Space.l).padding(.top, LB.Space.s)

            HStack(spacing: 12) {
                VStack(alignment: .leading, spacing: 4) {
                    Text(verbatim: "디자인팀").font(LB.Typeface.body(14, weight: .bold))   // TODO: 마지막 그룹
                    Text("street.guestsCount \(5)").font(LB.Typeface.body(11)).foregroundStyle(LB.Palette.inkSub)
                }
                Spacer()
                Button("action.coffeeBet") { router.startCoffeeBet() }
                    .buttonStyle(.lip(.primary, height: 52))
                    .frame(width: 128)
            }
            .padding(.leading, 22).padding(.trailing, 12)
            .frame(height: 76)
            .background(RoundedRectangle(cornerRadius: LB.Radius.m).fill(LB.Palette.sheet).shadow(color: LB.Palette.ink.opacity(0.12), radius: 0, y: 3))
            .padding(.horizontal, 12).padding(.bottom, 8)
        }
        .toolbar(.hidden, for: .navigationBar)
    }
}

/// 게임 화면 자리표시: 엔진 연결 전까지 흐름 확인용.
struct PlayPlaceholderView: View {
    let game: GameKind
    let players: [PlayerID]
    let rules: RoundRules
    @Environment(AppRouter.self) private var router
    @State private var confirmExit = false

    var body: some View {
        ZStack(alignment: .top) {
            LB.Palette.cream.ignoresSafeArea()
            GameTopBar(title: LocalizedStringKey(game.titleKey), turn: (1, players.count, "—"), mercyOn: rules.mercyOn) { confirmExit = true }
            GameHintPanel {
                Text(LocalizedStringKey(game.taglineKey)).font(LB.Typeface.body(13, weight: .medium)).foregroundStyle(LB.Palette.inkSub)
                Button("debug.finish") { router.backToStreet() }.buttonStyle(.lip(.lucky))
            }
            .frame(maxHeight: .infinity, alignment: .bottom)
            .padding(.bottom, 28)
        }
        .toolbar(.hidden, for: .navigationBar)
        .alert("exit.title", isPresented: $confirmExit) {
            Button("exit.keep", role: .cancel) {}
            Button("exit.quit", role: .destructive) { router.path.removeLast() }
        } message: { Text("exit.message") }
    }
}
