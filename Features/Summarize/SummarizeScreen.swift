struct SummarizeScreen: View {
    @State private var inputText = ""
    @State private var summary = ""

    var body: some View {
        VStack {
            TextEditor(text: $inputText)
                .frame(height: 200)
                .border(Color.gray)
                .padding()

            Button("Summarize") {
                summarizeText()
            }

            Text("Summary:")
                .font(.headline)
            Text(summary)
                .padding()
        }
        .padding()
    }

    func summarizeText() {
        guard let url = URL(string: "https://api.kubu-hai.com/summarize") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body = ["text": inputText]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)

        URLSession.shared.dataTask(with: request) { data, _, _ in
            guard let data = data,
                  let response = try? JSONDecoder().decode([String: String].self, from: data),
                  let result = response["summary"] else { return }

            DispatchQueue.main.async {
                summary = result
            }
        }.resume()
    }
}
