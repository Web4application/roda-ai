struct ConversationScreen: View {
    @State private var messages: [String] = []
    @State private var input = ""

    var body: some View {
        VStack {
            List(messages, id: \.self) { Text($0) }

            TextField("Say something...", text: $input, onCommit: send)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()
        }
    }

    func send() {
        guard !input.isEmpty else { return }
        messages.append("You: \(input)")

        var request = URLRequest(url: URL(string: "https://api.kubu-hai.com/chat")!)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try? JSONEncoder().encode(["message": input])

        URLSession.shared.dataTask(with: request) { data, _, _ in
            guard let data = data,
                  let response = try? JSONDecoder().decode([String: String].self, from: data),
                  let reply = response["reply"] else { return }

            DispatchQueue.main.async {
                messages.append("Bot: \(reply)")
                input = ""
            }
        }.resume()
    }
}
