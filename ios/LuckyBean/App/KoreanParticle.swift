import Foundation

/// 한국어 조사: 받침 유무로 이/가, 은/는, 을/를 선택. 한글이 아니면 뒤쪽(받침 없음) 형태.
enum KoreanParticle {
    static func hasFinalConsonant(_ word: String) -> Bool {
        guard let last = word.unicodeScalars.last?.value, (0xAC00...0xD7A3).contains(last) else { return false }
        return (last - 0xAC00) % 28 != 0
    }
    static func subject(of word: String) -> String { word + (hasFinalConsonant(word) ? "이" : "가") }
    static func topic(of word: String) -> String { word + (hasFinalConsonant(word) ? "은" : "는") }
    static func object(of word: String) -> String { word + (hasFinalConsonant(word) ? "을" : "를") }
}
