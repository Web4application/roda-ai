import PackageDescription

let package = Package(
  name: "GenerativeAICLI",
  platforms: [.macOS(.v13)],
  dependencies: [
    .package(url: "https://github.com/apple/swift-argument-parser.git", from: "1.2.0"),
    .package(name: "GoogleGenerativeAI", path: "../../"),
  ],
  targets: [
    .executableTarget(
      name: "generate-content",
      dependencies: [
        .product(name: "ArgumentParser", package: "swift-argument-parser"),
        .product(name: "GoogleGenerativeAI", package: "GoogleGenerativeAI"),
      ],
      path: "Sources"
    ),
  ]
)
