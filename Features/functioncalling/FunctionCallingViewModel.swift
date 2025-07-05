class FunctionCallingViewModel: ObservableObject {
    @Published var input = ""
    @Published var response = ""

    func callFunction() {
        var request = URLRequest(url: URL(string: "https://api.kubu-hai.com/function-call")!)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try? JSONEncoder().encode(["query": input])

        URLSession.shared.dataTask(with: request) { data, _, _ in
            guard let data = data,
                  let res = try? JSONDecoder().decode([String: String].self, from: data),
                  let out = res["result"] else { return }

            DispatchQueue.main.async {
                self.response = out
            }
        }.resume()
    }
}
