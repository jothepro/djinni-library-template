# Djinni Library

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/jothepro/djinni-library-template)](https://github.com/jothepro/djinni-library-template/releases/latest)
[![GitHub](https://img.shields.io/github/license/jothepro/djinni-library-template)](https://github.com/jothepro/djinni-library-template/blob/main/LICENSE)


A template for a Djinni library that can be used in Java/Kotlin on Android, ObjC/Swift on iOS/macOS and C# on Windows.

## Features

* 🧞‍♂️ Develop your library once in C++, use it in Code written in Java, C++/CLI (.NET 6) or Swift thanks to [Djinni](https://djinni.xlcpp.dev/).
* 👨‍👩‍👦‍👦 Can build & bundle binaries for 
  - macOS, iOS (XCFramework)
  - Android (AAR)
  - Windows .NET 6.0 (NuGet)
  - Linux
* 🎣 Dependency Management with Conan
* 🧶 Easy to use CLI to configure build output for different platforms
* 📑 Building Doxygen docs for all target languages

## How to use this template

* Create a new repository using this template. Check it out on your local machine.
* Create a `VERSION` file specifying a temporary version for local development. The build process relies on the existence
  of either a `VERSION`-file (e.g. `0.0.1`), or a Git release tag (e.g. `v0.0.1`) for determining the library version.
* Make sure you understand how to use it in your project & how to build & run for development before you change something.
* Search for all occurrences of "MyDjinniLibrary", "DjinniLibrary", "My" in the project to replace all occurrences of the
  template target and/or namespaces. You can ignore anything inside `lib/djinni-generated`, as it will be updated by 
  Djinni automatically.
  
## Installation

This template integrates into each build system by providing a package format native to each platform.

### Android (Android Library)

1. Add the repository to your project
   ```groovy
   repositories {
       maven {
           url "https://maven.pkg.github.com/jothepro/djinni-library-template"
       }
   }
   ```
2. Add the package dependencies to your applications build.gradle file:
   ```groovy
   dependencies {
       implementation 'my.djinnilibrary:mydjinnilibrary'
   }
   ```

### Visual Studio 17 2022 (NuGet Package)

*The NuGet package only works for .NET 6 (Core) Projects!*

1. [Add the Package Source](https://docs.microsoft.com/en-us/nuget/consume-packages/install-use-packages-visual-studio#package-sources).
   ```
   https://nuget.pkg.github.com/jothepro/index.json
   ```
2. In the NuGet Package Manager search for `MyDjinniLibrary` and install the package.


### XCode (Swift Package)

1. Add the repository [`jothepro/djinni-library-template-swiftpackage`](https://github.com/jothepro/djinni-library-template-swiftpackage) 
   as Package dependency to your XCode project.
   It contains the XCFramework with the Objective-C binaries.
2. Add this import to the swift code:
   ```swift
    import MyDjinniLibrary
   ```
   
### Linux (Conan Recipe)

*This template is meant to be used in a C++ project on Linux, e.g. together with `gtkmm-3.0`.
The binary for Linux consists of just the C++ interface without any wrapper.*

1. Add the conan remote.
   ```bash
   conan remote add djinni_library_template https://gitlab.com/api/v4/projects/27897297/packages/conan
   ```
2. Add the library as dependency in your conanfile.
   ```ini
   [requires]
   my_djinni_library/1.0.0@jothepro/release
   ```

<span class="next_section_button">

Read Next: [Development](docs/development.md)
</span>
