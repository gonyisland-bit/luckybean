import SwiftUI

/// 디자인 토큰. design/tokens.json 과 1:1. 값을 바꿀 땐 둘 다 바꿀 것.
enum LB {
    enum Palette {
        static let primary     = Color(hex: 0x2F6E71)
        static let primaryLip  = Color(hex: 0x234F51)
        static let lucky       = Color(hex: 0xEDB43E)
        static let luckyLip    = Color(hex: 0xB88A2A)
        static let coral       = Color(hex: 0xF2A48C)
        static let kiri        = Color(hex: 0xE8913A)
        static let kiriStripe  = Color(hex: 0xC9722A)
        static let ink         = Color(hex: 0x3B3B3D)
        static let inkSub      = Color(hex: 0x6B7174)
        static let sheet       = Color(hex: 0xFBF7F0)
        static let cream       = Color(hex: 0xF5EEE2)
        static let fill        = Color(hex: 0xECE6DA)
        static let night       = Color(hex: 0x2E3A4A)
        static let nightSky    = Color(hex: 0x3B5C93)
        static let danger      = Color(hex: 0xC2432F)
        static let dangerLip   = Color(hex: 0x8E2E20)
        static let success     = Color(hex: 0x7FB58A)
        static let badgeLuckBg  = Color(hex: 0xF8E7BD)
        static let badgeLuckFg  = Color(hex: 0x7A5A12)
        static let badgeSkillBg = Color(hex: 0xD9E8E7)
        static let badgeSkillFg = Color(hex: 0x234F51)
        static let lawn        = Color(hex: 0x6DBA86)
        static let lawnCheck   = Color(hex: 0x86C899)
        static let cafeWall    = Color(hex: 0xF6CBB8)
    }

    enum Radius {
        static let s: CGFloat = 12
        static let m: CGFloat = 20
        static let l: CGFloat = 28
    }

    enum Space {
        static let xxs: CGFloat = 4
        static let xs: CGFloat = 8
        static let s: CGFloat = 12
        static let m: CGFloat = 16
        static let l: CGFloat = 20
        static let xl: CGFloat = 24
        static let xxl: CGFloat = 32
    }

    enum Size {
        static let button: CGFloat = 56
        static let buttonCompact: CGFloat = 48
        static let iconButton: CGFloat = 44
        static let lip: CGFloat = 4
    }

    /// 비둘기 크기 토큰. 기준 단위 = 몸통 가로 30pt.
    enum PigeonScale: CGFloat {
        case s = 1.4   // 배경·주변
        case m = 1.9   // 게임 주인공
        case l = 3.0   // 발표·차례 넘기기
    }

    enum Motion {
        static let spring = Animation.spring(duration: 0.35, bounce: 0.25)
        static let press = Animation.easeOut(duration: 0.12)
        static let reveal: Double = 1.2
        static let handoff: Double = 0.8
    }
}

// MARK: - Typography

extension LB {
    enum Typeface {
        /// 제목·게임 이름·이름표. 일본어 로케일에선 Zen Maru Gothic.
        static func display(_ size: CGFloat, relativeTo style: Font.TextStyle = .title2) -> Font {
            .custom(isJapanese ? "ZenMaruGothic-Bold" : "Jua-Regular", size: size, relativeTo: style)
        }
        /// 키리 대사·운세 문장 전용.
        static func voice(_ size: CGFloat = 17) -> Font {
            .custom(isJapanese ? "ZenMaruGothic-Regular" : "GowunDodum-Regular", size: size, relativeTo: .body)
        }
        /// 본문은 시스템 폰트(Dynamic Type 그대로).
        static func body(_ size: CGFloat = 15, weight: Font.Weight = .regular) -> Font {
            .system(size: size, weight: weight)
        }

        static let hero = display(44, relativeTo: .largeTitle)
        static let title = display(24, relativeTo: .title)
        static let section = display(20, relativeTo: .title3)
        static let game = display(17, relativeTo: .headline)
        static let tag = display(14, relativeTo: .subheadline)

        private static var isJapanese: Bool {
            Locale.current.language.languageCode?.identifier == "ja"
        }
    }
}

extension Color {
    init(hex: UInt32, opacity: Double = 1) {
        self.init(
            .sRGB,
            red: Double((hex >> 16) & 0xFF) / 255,
            green: Double((hex >> 8) & 0xFF) / 255,
            blue: Double(hex & 0xFF) / 255,
            opacity: opacity
        )
    }
}
