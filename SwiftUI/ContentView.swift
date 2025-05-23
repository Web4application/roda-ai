import SwiftUI

struct ContentView: View {
    @StateObject private var aiService = AIService()
    @State private var prompt: String = ""

    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                TextField("Enter your prompt...", text: $prompt)
                    .textFieldStyle(.roundedBorder)
                    .padding()

                Button("Generate Response") {
                    aiService.generate(prompt: prompt)
                }
                .buttonStyle(.borderedProminent)

                if !aiService.aiResponse.isEmpty {
                    Text("AI says:")
                        .font(.headline)
                    Text(aiService.aiResponse)
                        .padding()
                        .background(Color.gray.opacity(0.1))
                        .cornerRadius(8)
                }

                Spacer()
            }
            .navigationTitle("RODA AI Chat")
            .padding()
        }
    }
}
