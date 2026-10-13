import SwiftUI

/// 시안의 기본 버튼: 높이 56, 반경 20, 아래 4pt 단색 립. 누르면 립이 1pt로 줄며 내려앉는다.
struct LipButtonStyle: ButtonStyle {
    enum Kind { case primary, lucky, danger }

    var kind: Kind = .primary
    var height: CGFloat = LB.Size.button

    func makeBody(configuration: Configuration) -> some View {
        let pressed = configuration.isPressed
        let lip: CGFloat = pressed ? 1 : LB.Size.lip
        configuration.label
            .font(LB.Typeface.body(17, weight: .bold))
            .foregroundStyle(foreground)
            .frame(maxWidth: .infinity, minHeight: height)
            .background(
                RoundedRectangle(cornerRadius: LB.Radius.m, style: .continuous)
                    .fill(fill)
                    .shadow(color: lipColor, radius: 0, x: 0, y: lip)
            )
            .offset(y: pressed ? LB.Size.lip - 1 : 0)
            .animation(LB.Motion.press, value: pressed)
            .sensoryFeedback(.impact(weight: .light), trigger: pressed) { _, new in new }
    }

    private var fill: Color {
        switch kind {
        case .primary: LB.Palette.primary
        case .lucky: LB.Palette.lucky
        case .danger: LB.Palette.danger
        }
    }
    private var lipColor: Color {
        switch kind {
        case .primary: LB.Palette.primaryLip
        case .lucky: LB.Palette.luckyLip
        case .danger: LB.Palette.dangerLip
        }
    }
    private var foreground: Color {
        kind == .lucky ? LB.Palette.ink : .white
    }
}

extension ButtonStyle where Self == LipButtonStyle {
    static var lip: LipButtonStyle { LipButtonStyle() }
    static func lip(_ kind: LipButtonStyle.Kind, height: CGFloat = LB.Size.button) -> LipButtonStyle {
        LipButtonStyle(kind: kind, height: height)
    }
}

/// 44pt 원형 뒤로가기 버튼.
struct BackCircleButton: View {
    var label: LocalizedStringKey = "a11y.back"
    var action: () -> Void

    var body: some View {
        Button(action: action) {
            Image(systemName: "chevron.left")
                .font(.system(size: 17, weight: .bold))
                .foregroundStyle(LB.Palette.ink)
                .frame(width: LB.Size.iconButton, height: LB.Size.iconButton)
                .background(Circle().fill(LB.Palette.sheet).shadow(color: LB.Palette.ink.opacity(0.18), radius: 0, y: 2))
        }
        .accessibilityLabel(Text(label))
    }
}
