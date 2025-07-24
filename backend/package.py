// swift-tools-version:5.5
import PackageDescription

let package = Package(
    name: "rodaai",
    platforms: [.macOS(.v13)],
    dependencies: [
        .package(url: "https://github.com/vapor/vapor.git", from: "4.0.0")
    ],
    targets: [
        .executableTarget(
            name: "App",
            dependencies: [.product(name: "Vapor", package: "vapor")]
        )
    ]
)
