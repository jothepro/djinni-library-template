from conans import ConanFile, CMake, tools

required_conan_version = ">=1.36"


def get_version():
    """tries to determine the library version based on the git tag, and write it to the VERSION file.
    If no tag can be found, the version is loaded from the VERSION file."""
    version = ""
    try:
        version = tools.Git().run("describe --tags")[1:]
        tools.save("VERSION", version)
    except:
        version = tools.load("VERSION")
    return version


class MyLibraryConan(ConanFile):
    name = "my_djinni_library"
    version = get_version()
    description = """A basic Djinni C++ library project template using CMake and Conan."""
    settings = "os", "compiler", "build_type", "arch"
    license = "AGPL-3.0-or-later"
    generators = "cmake_find_package", "cmake_paths"
    exports = "VERSION"
    exports_sources = "lib/src/*", "lib/include/*", "lib/CMakeLists.txt", "lib/*.djinni", \
                      "lib/platform/*/CMakeLists.txt", "lib/platform/*/src/*", "lib/platform/*/include/*", "test/*", \
                      "cmake/*", "VERSION", "LICENSE", "CMakeLists.txt"
    author = "jothepro"
    options = {
        "fPIC": [True, False]
    }
    default_options = {
        "fPIC": True
    }
    requires = (
    )
    build_requires = (
        "catch2/2.13.4",
        "djinni-generator/1.1.0"
    )

    def build(self):
        generator = None
        if tools.is_apple_os(self.settings.os):
            generator = "Xcode"
        elif self.settings.os == "Windows":
            generator = "Visual Studio 16 2019"
        cmake = CMake(self, generator=generator)
        if self.settings.os == "Android":
            cmake.definitions["ANDROID_PLATFORM"] = self.settings.os.api_level
        if not tools.get_env("CONAN_RUN_TESTS", True):
            cmake.definitions["BUILD_TESTING"] = "OFF"
        cmake.configure()
        cmake.build()
        if tools.get_env("CONAN_RUN_TESTS", True):
            cmake.test()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
