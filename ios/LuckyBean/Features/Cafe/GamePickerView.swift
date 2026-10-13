import SwiftUI

/// C1 게임 고르기 (시안: Cafe6). 배경 그림은 M2에서 Assets의 cafe_interior 레이어로 교체.
struct GamePickerView: View {
    @Environment(AppRouter.self) private var router
    @Environment(\.dismiss) private var dismiss
    var lastGame: GameKind = .roastRoulette

    var body: some View {
        ZStack(alignment: .top) {
            LB.Palette.cafeWall.ignoresSafeArea()   // TODO: 카페 실내 그림 (art/reference/cafe_interior_bg.png)

            HStack(spacing: 10) {
                BackCircleButton { dismiss() }
                Text("place.cafe").font(LB.Typeface.section).foregroundStyle(LB.Palette.ink)
                Spacer()
            }
            .padding(.horizontal, LB.Space.m)
            .padding(.top, 8)

            VStack(alignment: .leading, spacing: 10) {
                HStack(alignment: .firstTextBaseline) {
                    Text("picker.title").font(LB.Typeface.title)
                    Spacer()
                    Text("rule.luckyRound.short")
                        .font(LB.Typeface.body(11, weight: .medium))
                        .foregroundStyle(LB.Palette.inkSub)
                        .multilineTextAlignment(.trailing)
                }
                FeaturedGameCard(game: lastGame) { router.pick(lastGame) }
                ForEach(GameKind.playable.filter { $0 != lastGame }) { game in
                    GameRow(game: game) { router.pick(game) }
                }
            }
            .padding(.horizontal, 18).padding(.top, 16).padding(.bottom, 20)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(UnevenRoundedRectangle(topLeadingRadius: LB.Radius.l, topTrailingRadius: LB.Radius.l).fill(LB.Palette.sheet).ignoresSafeArea(edges: .bottom))
            .frame(maxHeight: .infinity, alignment: .bottom)
        }
        .foregroundStyle(LB.Palette.ink)
        .toolbar(.hidden, for: .navigationBar)
    }
}

private struct FeaturedGameCard: View {
    let game: GameKind
    var action: () -> Void
    var body: some View {
        Button(action: action) {
            HStack(spacing: 14) {
                GameIcon(game: game).frame(width: 64, height: 64)
                    .background(RoundedRectangle(cornerRadius: LB.Radius.s).fill(LB.Palette.cream))
                VStack(alignment: .leading, spacing: 6) {
                    Text("picker.lastPlayed").font(LB.Typeface.body(12, weight: .medium)).opacity(0.8)
                    Text(LocalizedStringKey(game.titleKey)).font(LB.Typeface.display(21))
                    Text(LocalizedStringKey(game.taglineKey)).font(LB.Typeface.body(12)).opacity(0.9)
                }
                Spacer()
                Image(systemName: "chevron.right").font(.system(size: 17, weight: .bold))
            }
            .foregroundStyle(.white)
            .padding(12)
            .background(RoundedRectangle(cornerRadius: LB.Radius.m).fill(LB.Palette.primary).shadow(color: LB.Palette.primaryLip, radius: 0, y: LB.Size.lip))
        }
        .buttonStyle(.plain)
    }
}

private struct GameRow: View {
    let game: GameKind
    var action: () -> Void
    var body: some View {
        Button(action: action) {
            HStack(spacing: 12) {
                GameIcon(game: game).frame(width: 48, height: 48)
                    .background(RoundedRectangle(cornerRadius: LB.Radius.s).fill(Color(hex: 0xF1E8DA)))
                VStack(alignment: .leading, spacing: 3) {
                    HStack(spacing: 6) {
                        Text(LocalizedStringKey(game.titleKey)).font(LB.Typeface.game)
                        KindBadge(kind: game.category)
                    }
                    Text(LocalizedStringKey(game.taglineKey)).font(LB.Typeface.body(12)).foregroundStyle(LB.Palette.inkSub)
                }
                Spacer(minLength: 0)
            }
            .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
        .accessibilityElement(children: .combine)
    }
}

/// 게임 아이콘 자리. M2에서 art/svg/icons/*.svg를 SwiftUI Shape 또는 벡터 에셋으로 교체.
struct GameIcon: View {
    let game: GameKind
    var body: some View {
        Image("icon_\(game.rawValue)")
            .resizable().scaledToFit().padding(4)
            .accessibilityHidden(true)
    }
}

extension GameKind {
    var taglineKey: String { "tagline." + rawValue }
}

#Preview {
    NavigationStack { GamePickerView() }.environment(AppRouter())
}
