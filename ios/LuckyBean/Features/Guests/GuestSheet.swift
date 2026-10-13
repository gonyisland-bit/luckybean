import SwiftUI
import SwiftData

/// C2 오늘의 손님 + 오늘 규칙 (시안: Guest6).
struct GuestSheet: View {
    let game: GameKind
    @Environment(AppRouter.self) private var router
    @Query(sort: \Crew.lastUsedAt, order: .reverse) private var crews: [Crew]
    @State private var selectedCrew: Crew?
    @State private var absent: Set<UUID> = []
    @State private var rules = RoundRules()

    private var members: [Member] { (selectedCrew?.members ?? []).filter { !$0.archived } }
    private var present: [Member] { members.filter { !absent.contains($0.id) } }
    private var canStart: Bool { game.playerRange.contains(present.count) }

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Capsule().fill(Color(hex: 0xD7D2C8)).frame(width: 40, height: 5).frame(maxWidth: .infinity)
            Text(LocalizedStringKey(game.titleKey)).font(LB.Typeface.body(12, weight: .medium)).foregroundStyle(LB.Palette.primary)
            Text("guests.title").font(LB.Typeface.title)
            Text("guests.hint").font(LB.Typeface.body(13)).foregroundStyle(LB.Palette.inkSub)

            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 8) {
                    ForEach(crews) { crew in
                        Button(crew.name) { selectedCrew = crew; absent = Set(crew.lastAbsentIDs) }
                            .font(LB.Typeface.body(13, weight: .bold))
                            .padding(.horizontal, 12).padding(.vertical, 9)
                            .background(RoundedRectangle(cornerRadius: LB.Radius.s).fill(crew.id == selectedCrew?.id ? LB.Palette.primary : LB.Palette.fill))
                            .foregroundStyle(crew.id == selectedCrew?.id ? .white : LB.Palette.ink)
                    }
                }
            }

            LazyVGrid(columns: Array(repeating: GridItem(.flexible(), spacing: 8), count: 3), spacing: 10) {
                ForEach(members) { m in
                    let on = !absent.contains(m.id)
                    Button {
                        if on { absent.insert(m.id) } else { absent.remove(m.id) }
                    } label: {
                        VStack(spacing: 6) {
                            PigeonAvatar(member: m).frame(width: 68, height: 68)
                                .overlay(RoundedRectangle(cornerRadius: LB.Radius.m).stroke(LB.Palette.primary, lineWidth: on ? 3 : 0))
                            Text(m.name).font(LB.Typeface.game)
                            Text(on ? "guests.in" : "guests.out").font(LB.Typeface.body(11)).foregroundStyle(LB.Palette.inkSub)
                        }
                        .opacity(on ? 1 : 0.4)
                    }
                    .buttonStyle(.plain)
                    .sensoryFeedback(.selection, trigger: on)
                    .accessibilityAddTraits(on ? .isSelected : [])
                }
            }

            VStack(alignment: .leading, spacing: 0) {
                Text("rules.today").font(LB.Typeface.game).padding(.bottom, 4)
                RuleToggle(title: "rule.solo", detail: "rule.solo.detail", isOn: $rules.soloHost)
                RuleToggle(title: "rule.mercy", detail: "rule.mercy.detail", isOn: $rules.mercyOn)
                HStack {
                    VStack(alignment: .leading, spacing: 2) {
                        Text("rule.luckyRound").font(LB.Typeface.body(13, weight: .bold))
                        Text("rule.luckyRound.detail").font(LB.Typeface.body(11)).foregroundStyle(LB.Palette.inkSub)
                    }
                    Spacer()
                    Text("rule.alwaysOn").font(LB.Typeface.body(12, weight: .bold)).foregroundStyle(LB.Palette.luckyLip)
                }
                .padding(.vertical, 9)
                .overlay(alignment: .top) { Divider() }
            }

            Spacer(minLength: 0)
            Button("guests.start \(present.count)") {
                router.play(game, players: present.map(\.playerID), rules: rules)
            }
            .buttonStyle(.lip)
            .disabled(!canStart)
            if !canStart {
                Text("guests.range \(game.playerRange.lowerBound) \(game.playerRange.upperBound)")
                    .font(LB.Typeface.body(12)).foregroundStyle(LB.Palette.danger).frame(maxWidth: .infinity)
            }
        }
        .padding(.horizontal, LB.Space.l).padding(.top, LB.Space.s).padding(.bottom, LB.Space.xl)
        .background(LB.Palette.sheet)
        .foregroundStyle(LB.Palette.ink)
        .onAppear { if selectedCrew == nil { selectedCrew = crews.first; absent = Set(crews.first?.lastAbsentIDs ?? []) } }
    }
}

private struct RuleToggle: View {
    let title: LocalizedStringKey
    let detail: LocalizedStringKey
    @Binding var isOn: Bool
    var body: some View {
        Toggle(isOn: $isOn) {
            VStack(alignment: .leading, spacing: 2) {
                Text(title).font(LB.Typeface.body(13, weight: .bold))
                Text(detail).font(LB.Typeface.body(11)).foregroundStyle(LB.Palette.inkSub)
            }
        }
        .tint(LB.Palette.primary)
        .padding(.vertical, 9)
        .overlay(alignment: .top) { Divider() }
    }
}

/// 비둘기 아바타 자리. M2에서 파츠 합성 뷰(PigeonView)로 교체.
struct PigeonAvatar: View {
    let member: Member
    var body: some View {
        RoundedRectangle(cornerRadius: LB.Radius.m)
            .fill(LB.Palette.cream)
            .overlay(Image("avatar_\(member.feather.rawValue)").resizable().scaledToFit())
            .clipShape(RoundedRectangle(cornerRadius: LB.Radius.m))
            .accessibilityLabel(Text("a11y.pigeon \(member.name)"))
    }
}
