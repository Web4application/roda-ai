import Foundation
import Combine

class AIService: ObservableObject {
    @Published var aiResponse: String = ""
    private var cancellables = Set<AnyCancellable>()

    func generate(prompt: String) {
        guard let url = URL(string: "http://localhost:8080/generate") else {
            print("Invalid URL")
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")

        let body = ["prompt": prompt]

        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: body)
        } catch {
            print("Failed to serialize JSON: \(error)")
            return
        }

        URLSession.shared.dataTaskPublisher(for: request)
            .tryMap { data, response -> Data in
                guard let httpResponse = response as? HTTPURLResponse,
                      httpResponse.statusCode == 200 else {
                    throw URLError(.badServerResponse)
                }
                return data
            }
            .decode(type: AIResponse.self, decoder: JSONDecoder())
            .receive(on: DispatchQueue.main)
            .sink(receiveCompletion: { completion in
                if case let .failure(error) = completion {
                    print("Error fetching AI response: \(error)")
                }
            }, receiveValue: { [weak self] response in
                self?.aiResponse = response.response
            })
            .store(in: &cancellables)
    }
}

struct AIResponse: Codable {
    let response: String
}
