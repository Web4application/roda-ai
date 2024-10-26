// swift-tools-version:5.2
import PackageDescription

let package = Package(
name: "MyVaporApp",
dependencies: [
.package(url: "https://github.com/vapor/vapor.git", from: "4.0.0"),
.package(url: "https://github.com/vapor/queues.git", from: "1.0.0")
],
targets: [
.target(name: "App", dependencies: [
.product(name: "Vapor", package: "vapor"),
.product(name: "Queues", package: "queues")
]),
.target(name: "Run", dependencies: ["App"])
]
)
