import SwiftUI

/// 비둘기 옆 이름표. 상태는 색만이 아니라 텍스트로도 드러낸다(접근성).
struct NameTag: View {
    enum State { case normal, passed, payer }
    let name: String
    var state: State = .normal

    var body: some View {
        Text(label)
            .font(LB.Typeface.tag)
            .foregroundStyle(foreground)
            .padding(.horizontal, 9)
            .padding(.vertical, 5)
            .background(
                RoundedRectangle(cornerRadius: LB.Radius.s, style: .continuous)
                    .fill(background)
                    .shadow(color: shadow, radius: 0, y: 2)
            )
            .fixedSize()
            .accessibilityLabel(Text(label))
    }

    private var label: String {
        switch state {
        case .normal: name
        case .passed: String(localized: "tag.passed \(name)")
        case .payer: String(localized: "tag.payer \(name)")
        }
    }
    private var foreground: Color { state == .normal ? LB.Palette.ink : .white }
    private var background: Color {
        switch state {
        case .normal: LB.Palette.sheet.opacity(0.94)
        case .passed: LB.Palette.ink.opacity(0.55)
        case .payer: LB.Palette.danger
        }
    }
    private var shadow: Color {
        switch state {
        case .normal: LB.Palette.ink.opacity(0.14)
        case .passed: .clear
        case .payer: LB.Palette.dangerLip
        }
    }
}

/// 운/실력 뱃지.
struct KindBadge: View {
    let kind: GameKind.Category
    var body: some View {
        Text(kind == .luck ? "badge.luck" : "badge.skill")
            .font(LB.Typeface.body(10, weight: .bold))
            .foregroundStyle(kind == .luck ? LB.Palette.badgeLuckFg : LB.Palette.badgeSkillFg)
            .padding(.horizontal, 6)
            .padding(.vertical, 3)
            .background(Capsule().fill(kind == .luck ? LB.Palette.badgeLuckBg : LB.Palette.badgeSkillBg))
    }
}

/// 게임 화면 공통 상단 바: 뒤로 · 게임 이름 · 차례 뱃지 (+ 자비 모드 칩)
struct GameTopBar: View {
    let title: LocalizedStringKey
    var turn: (index: Int, total: Int, name: String)?
    var mercyOn = false
    var onBack: () -> Void

    var body: some View {
        HStack(spacing: 10) {
            BackCircleButton(action: onBack)
            Text(title).font(LB.Typeface.section).foregroundStyle(LB.Palette.ink)
            Spacer(minLength: 0)
            if mercyOn {
                Text("rule.mercy.chip")
                    .font(LB.Typeface.body(11, weight: .bold))
                    .foregroundStyle(LB.Palette.badgeLuckFg)
                    .padding(.horizontal, 8).padding(.vertical, 5)
                    .background(Capsule().fill(LB.Palette.badgeLuckBg))
            }
            if let turn {
                Text("turn.badge \(turn.index) \(turn.total) \(turn.name)")
                    .font(LB.Typeface.body(12, weight: .bold))
                    .foregroundStyle(.white)
                    .padding(.horizontal, 10).padding(.vertical, 7)
                    .background(RoundedRectangle(cornerRadius: LB.Radius.s).fill(LB.Palette.primary))
            }
        }
        .padding(.horizontal, LB.Space.m)
    }
}

/// 게임 화면 하단 안내 패널.
struct GameHintPanel<Content: View>: View {
    @ViewBuilder var content: Content
    var body: some View {
        VStack(alignment: .leading, spacing: 10) { content }
            .padding(.horizontal, LB.Space.m)
            .padding(.vertical, 14)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(
                RoundedRectangle(cornerRadius: LB.Radius.m, style: .continuous)
                    .fill(LB.Palette.sheet)
                    .shadow(color: LB.Palette.ink.opacity(0.10), radius: 0, y: 3)
            )
            .padding(.horizontal, LB.Space.m)
    }
}
