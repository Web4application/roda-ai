import SwiftUI

@MainActor
class FunctionCallingViewModel: ObservableObject {
    // Existing properties and initializers

    @Published var recognizedText = ""
    private let speechRecognitionManager = SpeechRecognitionManager()
    private let textToSpeechManager = TextToSpeechManager()

    override init() {
        // Initialization code
        speechRecognitionManager.$recognizedText
            .receive(on: DispatchQueue.main)
            .assign(to: &$recognizedText)
    }

    func startRecognition() {
        speechRecognitionManager.startRecognition()
    }

    func sendMessage(_ text: String, streaming: Bool = true) async {
        // Existing code
        textToSpeechManager.speak(text: messages.last?.message ?? "")
    }
}
