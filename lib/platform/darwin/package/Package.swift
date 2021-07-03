// swift-tools-version:5.3
import PackageDescription

let package = Package(
        name: "MyDjinniLibrary",
        platforms: [
            .macOS(.v11), .iOS(.v13)
        ],
        products: [
            // Products define the executables and libraries a package produces, and make them visible to other packages.
            .library(
                    name: "MyDjinniLibrary",
                    targets: ["MyDjinniLibraryBinaryPackage"])
        ],
        dependencies: [
            // Dependencies declare other packages that this package depends on.
        ],
        targets: [
            .binaryTarget(
                    name: "MyDjinniLibraryBinaryPackage",
                    path: "bin/MyDjinniLibrary.xcframework"
            )
        ]
)