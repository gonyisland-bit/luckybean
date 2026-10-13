import CoreHaptics
import UIKit

/// docs/03 표의 햅틱을 이름으로 부른다. 기기에 햅틱이 없으면 조용히 무시.
@MainActor
final class Haptics {
    static let shared = Haptics()

    enum Pattern {
        case tick, light, medium, heavy, success, warning
        case triple          // 키리 실룩 ×3
        case drain(Double)   // 로스팅 콩 빠짐 / 영수증 출력: 길이(초)만큼 약한 연속 진동
    }

    private var engine: CHHapticEngine?

    private init() {
        guard CHHapticEngine.capabilitiesForHardware().supportsHaptics else { return }
        let made = try? CHHapticEngine()
        made?.resetHandler = { try? made?.start() }
        try? made?.start()
        engine = made
    }

    func play(_ pattern: Pattern) {
        switch pattern {
        case .tick: UISelectionFeedbackGenerator().selectionChanged()
        case .light: UIImpactFeedbackGenerator(style: .light).impactOccurred()
        case .medium: UIImpactFeedbackGenerator(style: .medium).impactOccurred()
        case .heavy: UIImpactFeedbackGenerator(style: .heavy).impactOccurred()
        case .success: UINotificationFeedbackGenerator().notificationOccurred(.success)
        case .warning: UINotificationFeedbackGenerator().notificationOccurred(.warning)
        case .triple: playEvents((0..<3).map { transient(at: Double($0) * 0.2, intensity: 0.5) })
        case .drain(let duration):
            playEvents([CHHapticEvent(
                eventType: .hapticContinuous,
                parameters: [
                    CHHapticEventParameter(parameterID: .hapticIntensity, value: 0.3),
                    CHHapticEventParameter(parameterID: .hapticSharpness, value: 0.2)
                ],
                relativeTime: 0, duration: duration)])
        }
    }

    private func transient(at time: TimeInterval, intensity: Float) -> CHHapticEvent {
        CHHapticEvent(
            eventType: .hapticTransient,
            parameters: [CHHapticEventParameter(parameterID: .hapticIntensity, value: intensity)],
            relativeTime: time)
    }

    private func playEvents(_ events: [CHHapticEvent]) {
        guard let engine, let pattern = try? CHHapticPattern(events: events, parameters: []) else { return }
        try? engine.makePlayer(with: pattern).start(atTime: CHHapticTimeImmediate)
    }
}
