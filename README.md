# Djinni Library

A template for a Djinni library that can be used in Java/Kotlin on Android, ObjC/Swift on iOS/macOS and C# on Windows.

## Features

* 🧞‍♂️ Develop your library once in C++, use it in Code written in Java, C++/CLI (.NET 5) or Swift thanks to [Djinni](https://djinni.xlcpp.dev/).
* 👨‍👩‍👦‍👦 Can build & bundle binaries for 
  - macOS, iOS (XCFramework)
  - Android (AAR)
  - Windows .NET 5.0 (NuGet)
  - Linux
* 🎣 Dependency Management with Conan
* 🧶 Easy to use CLI to configure build output for different platforms
* 📑 Building Doxygen docs for all target languages

## How to use this template

* Create a new repository using this template.
* Make sure you understand how to use it in your project & how to build & run for development before you change something.
* Search for all occurrences of "MyDjinniLibrary", "DjinniLibrary", "My" in the project to replace all ocurrences of the
  template target and/or namespaces. You can ignore anything inside `lib/djinni-generated`, as it will be updated by Djinni automatically.

## Installation

- Android: [my.djinnilibrary.mydjinnilibrary (Maven)](https://github.com/jothepro/djinni-library-template/packages/881665)
- Windows: [MyDjinniLibrary (NuGet)](https://github.com/jothepro/djinni-library-template/packages/881693)
- Darwin: [djinni-library-template-swiftpackage (Swift Package)](https://github.com/jothepro/djinni-library-template-swiftpackage)

## Development

### Build Requirements

- [Conan](https://conan.io/) >= 1.36
- [CMake](https://cmake.org/) >= 3.15
- [Python](https://www.python.org/) >= 3.5
- [Doxygen](https://www.doxygen.nl/index.html) >= 1.9.1 (optional)
  
#### Android (Java)

- Android NDK
- Separate installations of:
  - Java 8
  - Java 11

#### Windows (C++/CLI)

- [Nuget CLI](https://docs.microsoft.com/en-us/nuget/install-nuget-client-tools#nugetexe-cli) >= 5.9
- [Visual Studio 16 2019](https://docs.microsoft.com/en-us/visualstudio/windows/?view=vs-2019)
  * .NET 5.0 Runtime
  * .NET SDK

### Build

#### Pure C++ build

During development, building the C++-Code and running tests can be done as usual in a C++ project with Conan:

* **Commandline:**
  ```bash 
   # Create build folder for out-of-source build
  mkdir build && cd build
  # Install Dependencies with Conan
  conan install ..
  # Configure, Build & Test
  conan build ..
   ```
* **Clion:** Install the [Conan Plugin](https://plugins.jetbrains.com/plugin/11956-conan) before configuring & building the project as usual.

#### Building for use in another Language

The `build.py` CLI helps you to easily build & package the library for usage in another language, without having to know
what is going on under the hood.

For details on what the various parameters of the CLI do, please consult `./build.py --help`.

All build outputs generated by `build.py` will be written to `./build/` by default. 
You can overwrite the build directory with the `--build-directory` parameter.

Before running `build.py` for the first time, install the Python dependencies:
```bash
pip3 install -r requirements.txt
```

##### Building an Android AAR

When building for Android, Java 11 is required.
In addition to that you need to provide the NDK that you want to build with as environment variable `ANDROID_NDK_HOME`.
```bash
export ANDROID_NDK_HOME=/path/to/your/ndk/22.0.6917172
./build.py --android x86_64 armv8 --package aar
```

This results in an Android Library (AAR) that contains both the Java-Gluecode required to call the native Library
and the binaries for both `x86_64` (for the emulator) & `arm64-v8a` (for the real hardware) architectures.

##### Building an XCFramework for iOS/macOS

All binaries for iOS/macOS will be combined into one big XCFramework, for easy referencing in
any Swift/Objective-C project. Note that for iOS two different platforms need to be targeted: The simulator
and the real iPhone hardware:

```bash
./build.py --iphoneos armv8 --iphonesimulator x86_64 armv8 --macos x86_64 armv8 --package xcframework
```

This results in an XCFramework that contains binaries for

* real iPhones (iOS)
* the iPhone Simulator (iOS) for both Intel & Apple silicon (ARM) architectures.
* macOS for both Intel & Apple silicon (ARM) architectures.

##### Building a .NET 5 NuGet package

```bash
./build.py --windows x86_64 x86 armv8 --package nuget
```

This results in a NuGet package that contains binaries for 3 different architectures (`x86_64`, `x86` and `arm64`).
The NuGet package makes it easy for you to include the library in a .NET 5 project without having to worry about
what `dll` to include for which architecture in the build process.

**Attention**: If you encounter the following error message when building a project that references the NuGet package, don't panic!
> Error MSB3270 There was a mismatch between the processor architecture of the project being built "x86" and the processor architecture of the reference "MyDjinniLibrary", "AMD64". This mismatch may cause runtime failures. Please consider changing the targeted processor architecture of your project through the Configuration Manager so as to align the processor architectures between your project and references, or take a dependency on references with a processor architecture that matches the targeted processor architecture of your project.

You can just ignore it, it's a false positive! The NuGet package comes with logic that will indeed package the right `dll` 
during build time. Disable the warning in the projects `.csproj` file by adding:
```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <ResolveAssemblyWarnOrErrorOnTargetArchitectureMismatch>
       None
    </ResolveAssemblyWarnOrErrorOnTargetArchitectureMismatch>
  </PropertyGroup>
</Project>
```

### Test

The library comes preconfigured for Unit-Testing with Catch2:

* **Commandline:** To run just the unit-tests, you can run `conan build .. --test`.
* **CLion:** Execute the `MyDjinniLibraryTest` target

Building & executing tests is **not supported on Windows**!

### Documentation

The repository comes with 4 different doxygen configurations, each is for a different target language:
- `Doxyfile-Cpp`: Documents the C++ interfaces that will be exposed for all the languages. They can also be used 
  directly in a C++ project, e.g. for targeting Linux with `gtkmm`.
- `Doxyfile-CppCli`: Documents the C++/CLI gluecode for targeting Windows .NET 5
- `Doxyfile-Java`: Documents the Java gluecode for targeting Android
- `Doxyfile-ObjC`: Documents the Objective-C gluecode for targeting iOS/macOS

All Doxyfiles depend on code generated by Djinni, located in `lib/djinni-generated`.
To ensure that the required files are present, the best way to generate the docs is with the 
`build.py` CLI when building for a specific platform anyways with the `--render-docs` parameter:
```bash
# This will generate the docs for C++, Java & Objective-C
./build.py --render-docs --android x86_64 --macos x86_64 
```

The resulting documentation can be found under `docs/generated/html`.

### Project Structure

```
.
├── CMakeLists.txt               : Root `CMakeLists.txt`. Includes Library sources and unit tests.
├── Doxyfile-Cpp                 : Doxyfile for the C++ interface that is generated with Djinni from `my_djinni_library.djinni`.
├── Doxyfile-CppCli              : Doxyfile for the generated C++/CLI interface.
├── Doxyfile-Java                : Doxyfile for the generated Java interface.
├── Doxyfile-ObjC                : Doxyfile for the generated Objective-C interface.
├── LICENSE                      : License file.
├── README.md                    : The document that you read right now.
├── build.py                     : Build script that automates building & packaging the binaries for all the supported platforms.
├── cmake
│   ├── modules
│   │   ├── GetVersion.cmake     : CMake module that reads the current project version from a temporary `VERSION` file that 
│   │   │                          is created by Conan during the install phase or from the git repository if no `VERSION` file can be found.
│   │   └── djinni-cmake         : CMake module that introduces the `add_djinni_library` function to configure the Djinni library.
│   │       └── ...
│   └── toolchains 
│       └── android_toolchain.cmake : CMake toolchain that is required if building for Android. 
│                                     This toolchain is passed to Conan in `build.py` when building for Android.
├── conan
│   └── profiles                 : Folder containing Conan profiles for all supported target platforms (`android`, `ios`, `macos`, `windows`).
│       └── ...                    These profiles are used by `build.py` () to configure the CMake targets accordingly.
├── conanfile.py                 : Conanfile for installing dependencies & defining the library itself as Conan package.
├── docs
│   ├── doxygen-awesome-css      : Submodule of the `doxygen-awesome-css` doxygen theme.
│   │   └── ...
│   ├── doxygen-custom           : Doxygen customization (CSS & html)
│   │   └── ...
│   ├── generated
│   │   └── html                 : Folder that Doxygen will write the generated html documentation to.
│   │       ├── index.html       : Entrypoint for the Doxygen documentation.
│   │       └── ...                Each target language is documented in a sub-folder in an entirely separate doxygen Website.
│   ├── idl.dox                  : Doxygen page that includes the Djinni IDL file used to generate the documented interfaces.
│   └── img                      : Image resources for Doxygen
│       └── ...
├── lib                          : Folder containing library sources.
│   ├── CMakeLists.txt           : `CMakeLists.txt` that defines the library target and links it to the djinni-support-lib
│   ├── djinni-generated         : The djinni generator will write the generated interfaces for each language into this folder.
│   │   └── ...
│   ├── my_djinni_library.djinni : Djinni interface definition language file that defines the libraries interface.
│   ├── platform
│   │   ├── android              : Android Studio project that is used to build the Android Library (AAR).
│   │   │   └── ...                `build.py` copies the binaries & jar built for Java into certain locations in this project, 
│   │   │                          builds the AAR with gradle and copies the result back to the build folder.
│   │   └── windows              : NuGet package structure that is used by `build.py` to package the .NET 5 NuGet package.
│   │       ├── MyDjinniLibrary.nuspec.template : Nuspec template that is populated with the project version from the `VERSION` file by `build.py`.
│   │       └── ...
│   └── src                      : Finally! The source files of the library.
│       └── ...
├── requirements.txt             : Python requirements for executing `build.py`
└── test                         : Folder containing the library unit tests.
    ├── CMakeLists.txt           : `CMakeLists.txt` that configures the Unit tests with Catch2.
    └── ...
```