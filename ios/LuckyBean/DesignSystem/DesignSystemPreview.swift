import SwiftUI

/// 맥 첫날 확인용: 토큰·버튼·이름표·뱃지를 시안과 나란히 비교한다.
struct DesignSystemPreview: View {
    private let swatches: [(String, Color)] = [
        ("primary", LB.Palette.primary), ("lucky", LB.Palette.lucky), ("coral", LB.Palette.coral),
        ("kiri", LB.Palette.kiri), ("ink", LB.Palette.ink), ("sheet", LB.Palette.sheet),
        ("night", LB.Palette.night), ("danger", LB.Palette.danger)
    ]

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text(verbatim: "럭키빈 디자인 시스템").font(LB.Typeface.hero)
                LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 4), spacing: 12) {
                    ForEach(swatches, id: \.0) { name, color in
                        VStack(spacing: 4) {
                            RoundedRectangle(cornerRadius: LB.Radius.s).fill(color).frame(height: 48)
                                .overlay(RoundedRectangle(cornerRadius: LB.Radius.s).stroke(LB.Palette.fill))
                            Text(verbatim: name).font(LB.Typeface.body(11))
                        }
                    }
                }
                Button(String(localized: "receipt.rematch")) {}.buttonStyle(.lip(.lucky))
                Button(String(localized: "handoff.ready")) {}.buttonStyle(.lip)
                Button(String(localized: "exit.quit")) {}.buttonStyle(.lip(.danger, height: LB.Size.buttonCompact))
                HStack(spacing: 8) {
                    NameTag(name: "민수")
                    NameTag(name: "지은", state: .passed)
                    NameTag(name: "하린", state: .payer)
                    KindBadge(kind: .luck)
                    KindBadge(kind: .skill)
                }
                Text(verbatim: "“살금살금… 누구를 덮칠까”").font(LB.Typeface.voice())
            }
            .padding(LB.Space.l)
        }
        .background(LB.Palette.cream)
        .foregroundStyle(LB.Palette.ink)
    }
}

#Preview { DesignSystemPreview() }
