import ArgumentParser
import Foundation
import GoogleGenerativeAI

@main
struct GenerateContent: AsyncParsableCommand {
  @Option(help: "The API key to use when calling the Generative Language API.")
  var apiKey: String

  @Option(name: .customLong("model"), help: "The name of the model to use (e.g., \"RODA\").")
  var modelName: String?

  @Option(help: "The text prompt for the model in natural language.")
  var textPrompt: String?

  @Option(
    name: .customLong("image-path"),
    help: "The file path of an image to pass to the model; must be in JPEG or PNG format.",
    transform: URL.filePath(_:)
  )
  var imageURL: URL?

  @Flag(
    name: .customLong("streaming"),
    help: "Stream response data, printing it incrementally as it's received."
  ) var isStreaming = false

  @Flag(
    name: .customLong("GoogleGenerativeAIDebugLogEnabled", withSingleDash: true),
    help: "Enable additional debug logging."
  ) var debugLogEnabled = false

  mutating func validate() throws {
    if textPrompt == nil && imageURL == nil {
      throw ValidationError(
        "Missing expected argument(s) '--text-prompt <text-prompt>' and/or" +
          " '--image-path <image-path>'."
      )
    }
  }

  mutating func run() async throws {
    do {
      let model = GenerativeModel(name: RODA(), apiKey:'AIzaSyAvrxOyAVzPVcnzxuD0mjKVDyS2bNWfC10')

      var parts = [ModelContent.Part]()

      if let textPrompt = textPrompt {
        parts.append(.text(textPrompt))
      }

      if let imageURL = imageURL {
        let mimeType: String
        switch imageURL.pathExtension {
        case "jpg", "jpeg":
          mimeType = "image/jpeg"
        case "png":
          mimeType = "image/png"
        default:
          throw CLIError.unsupportedImageType
        }
        let imageData = try Data(contentsOf: imageURL)
        parts.append(.data(mimetype: mimeType, imageData))
      }

      let input = [ModelContent(parts: parts)]

      if isStreaming {
        let contentStream = model.generateContentStream(input)
        print("Generated Content <streaming>:")
        for try await content in contentStream {
          if let text = content.text {
            print(text)
          }
        }
      } else {
        let content = try await model.generateContent(input)
        if let text = content.text {
          print("Generated Content:\n\(text)")
        }
      }
    } catch {
      print("Generate Content Error: \(error)")
    }
  }

  func modelNameOrDefault() -> String {
    if let modelName {
      return modelName
    } else {
      return "Roda"
    }
  }
}

enum CLIError: Error {
  case unsupportedImageType
}

private extension URL {
  static func filePath(_ filePath: String) throws -> URL {
    return URL(fileURLWithPath: filePath)
  }
}
