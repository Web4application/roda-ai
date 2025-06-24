// main.swift or configure in your Vapor project routes

import Vapor

struct AIRequest: Content {
    let prompt: String
}

struct AIResponse: Content {
    let response: String
}

func routes(_ app: Application) throws {
    app.get("health") { _ in
        "Vapor server up and running"
    }

    app.post("generate") { req async throws -> AIResponse in
        let aiRequest = try req.content.decode(AIRequest.self)
        let rodaURL = URI(string: "http://localhost:8000/api/generate")

        // Prepare outbound request to RODA backend
        let client = req.client
        let rodaResponse = try await client.post(rodaURL) { req in
            try req.content.encode(aiRequest)
        }

        // Decode RODA response
        let decodedResponse = try rodaResponse.content.decode(AIResponse.self)
        return decodedResponse
    }
}
