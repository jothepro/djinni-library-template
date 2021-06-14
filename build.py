#!/usr/bin/env python3

import argparse
import os
import sys
from enum import Enum
from collections import namedtuple
from conans.client.conan_api import Conan
from string import Template
import shutil

conan = Conan()
print_prefix = '[build.py]'
workdir = os.getcwd()
target: str = 'MyDjinniLibrary'
android_profile = f'{workdir}/conan/profiles/android'
macos_profile = f'{workdir}/conan/profiles/macos'
ios_profile = f'{workdir}/conan/profiles/ios'
windows_profile = f'{workdir}/conan/profiles/windows'
android_conan_cmake_toolchain_file = f'{workdir}/cmake/toolchains/android_toolchain.cmake'
android_project_dir: str = f'{workdir}/lib/platform/android'
android_module_dir: str = f'{android_project_dir}/{target}'


def get_version():
    return open('VERSION', 'rt').read()[1:]


class NamedEnum(Enum):
    """enum that returns the name of the value on __str__"""
    def __str__(self):
        return self.name


ArchitectureDetails = namedtuple('ArchitectureName', 'conan android windows bit')


class Architecture(NamedEnum):
    """enum with all possible architectures that one can build for, and the names for them on each target platform"""
    x86_64 = ArchitectureDetails(conan='x86_64', android='x86_64', windows='win10-x64', bit='64')
    x86 = ArchitectureDetails(conan='x86', android='x86', windows='win10-x86', bit='32')
    armv8 = ArchitectureDetails(conan='armv8', android='arm64-v8a', windows='win10-arm64', bit='64')
    armv7 = ArchitectureDetails(conan='armv7', android='armeabi-v7a', windows='win10-arm', bit='32')

    @staticmethod
    def from_string(s):
        """this is required for the enum to work with argparse"""
        try:
            return Architecture[s]
        except KeyError:
            raise ValueError()


class BuildConfiguration(NamedEnum):
    """enum of all possible build configurations."""
    release = 'Release'
    debug = 'Debug'

    @staticmethod
    def from_string(s):
        """this is required for the enum to work with argparse"""
        try:
            return BuildConfiguration[s]
        except KeyError:
            raise ValueError()


class BuildContext:
    """Base class for all build contexts. Contains common code that is shared between builds for different
    languages/platforms """

    def __init__(self, build_directory: str, profile: str, architectures: [Architecture],
                 configuration: BuildConfiguration):
        self.profile = profile
        self.build_directory = build_directory
        self.architectures = architectures
        self.configuration = configuration

    def build(self):
        """builds all selected architectures"""
        for architecture in self.architectures:
            print(f'{print_prefix} building for architecture {architecture.name}:')
            conan.build(conanfile_path=workdir, build_folder=f"{self.build_directory}/{architecture.value.conan}")

    def conan_install(self, architecture: Architecture, settings: list[str] = [],
                      env: list[str] = []):
        """installs all conan dependencies defined in conanfile.py"""
        print(f'{print_prefix} installing dependencies for architecture {architecture.name}:')
        all_settings = settings + [f"arch={architecture.value.conan}",
                                   f'build_type={self.configuration.value}']
        all_env = env + ['CONAN_RUN_TESTS=False']
        conan.install(install_folder=f"{self.build_directory}/{architecture.value.conan}",
                      profile_names=[self.profile], build=["missing"],
                      settings=all_settings,
                      env=all_env)

    @staticmethod
    def render_doxygen_docs(doxyfile: str):
        """calls doxygen with the given Doxyfile."""
        print(f'{print_prefix} generating documentation from {doxyfile}:')
        os.system(f'doxygen {doxyfile}')


class AndroidBuildContext(BuildContext):
    """Build context for Android. This defines the logic for packaging all binaries into one AAR"""

    def install(self, android_ndk: str, conan_cmake_toolchain_file: str, java_home: str):
        for architecture in self.architectures:
            self.conan_install(architecture=architecture,
                               env=[f"CONAN_CMAKE_TOOLCHAIN_FILE={conan_cmake_toolchain_file}",
                                    f"ANDROID_ABI={architecture.value.android}",
                                    f"ANDROID_NDK={android_ndk}",
                                    f"JAVA_HOME=\"{java_home}\""])

    def package(self, java_home: str):
        """copies all resources into the Android Studio project and builds it"""
        print(f'{print_prefix} packaging to AAR:')
        for architecture in self.architectures:
            print(f'{print_prefix} copy `lib{target}.so` for architecture {architecture.value.conan} to Android Studio Project')
            shutil.copy(src=f'{self.build_directory}/{architecture.value.conan}/lib/lib{target}.so',
                        dst=f'{android_module_dir}/src/main/jniLibs/{architecture.value.android}')
        print(f'{print_prefix} copy `{target}.jar` to Android Studio Project')
        shutil.copy(src=f'{self.build_directory}/{self.architectures[0].value.conan}/lib/{target}.jar',
                    dst=f'{android_module_dir}/libs')
        print(f'{print_prefix} build Android Studio Project')
        os.chdir(android_project_dir)
        os.putenv('JAVA_HOME', java_home)
        ret = os.system(f'./gradlew assemble{self.configuration.value}')
        os.chdir(workdir)
        if ret != 0:
            print(f'{print_prefix} building Android Studio Project has failed', file=sys.stderr)
            exit(2)
        shutil.copy(src=f'{android_module_dir}/build/outputs/aar/{target}-{self.configuration.name}.aar',
                    dst=f'{self.build_directory}')

    @staticmethod
    def render_doxygen_docs():
        """renders the doxygen documentation for Java"""
        BuildContext.render_doxygen_docs('Doxyfile-Java')


class DarwinBuildContext(BuildContext):
    """Build Context for iOS,macOS. This defines the logic for packaging all binaries into a single XCFramework"""

    def __init__(self, build_directory: str, profile: str, architectures: list[Architecture],
                 configuration: BuildConfiguration, sdk: str):
        super().__init__(build_directory, profile, architectures, configuration)
        self.sdk = sdk

    def install(self):
        for architecture in self.architectures:
            self.conan_install(architecture=architecture,
                               settings=[f'os.sdk={self.sdk}'])

    @property
    def target_folder(self):
        """determines the name of the folder in which the XCode build will output the binaries. The folder name
        differs depending on the target platform."""
        folder_name = self.configuration.value
        if self.sdk in ['iphoneos', 'iphonesimulator']:
            folder_name = f'{self.configuration.value}-{self.sdk}'
        return folder_name

    @property
    def combined_architecture(self):
        """determines the name of a target folder that contains a universal binary targeting multiple architectures.
        This is not the name used inside the XCFramework, it's just used for temporarily storing the generated
        universal binary."""
        return '_'.join(map(str, self.architectures))

    def build(self):
        """builds the binaries for each architecture and combines the resulting frameworks with lipo into a universal
        binary framework"""
        super().build()
        if len(self.architectures) > 1:
            lipo_dir = f"{self.build_directory}/{self.combined_architecture}"
            if os.path.exists(lipo_dir):
                shutil.rmtree(lipo_dir)
            os.mkdir(lipo_dir)
            shutil.copytree(
                src=f'{self.build_directory}/{self.architectures[0]}/lib/{self.target_folder}/{target}.framework',
                dst=f'{lipo_dir}/lib/{self.target_folder}/{target}.framework', symlinks=True)
            lipo_input: str = ''
            lipo_output: str = f'{lipo_dir}/lib/{self.target_folder}/{target}.framework/{target}'
            if self.sdk == 'macosx':
                lipo_output: str = f'{lipo_dir}/lib/{self.target_folder}/{target}.framework/Versions/A/{target}'
            for architecture in self.architectures:
                if self.sdk == 'macosx':
                    lipo_input += f'{self.build_directory}/{architecture}/lib/{self.target_folder}/{target}.framework/Versions/A/{target} '
                else:
                    lipo_input += f'{self.build_directory}/{architecture}/lib/{self.target_folder}/{target}.framework/{target} '
            os.system(
                f'lipo {lipo_input} -create -output {lipo_output}')

    @staticmethod
    def package(build_context_list: [BuildContext], configuration: BuildConfiguration, build_directory: str):
        """combines the frameworks targeting different architectures into one big XCFramework for distribution."""
        print(f'{print_prefix} packaging to xcframework:')
        output_file = f'{build_directory}/{target}-{configuration.name}.xcframework'
        arguments = f'-output {output_file} '
        for build_context in build_context_list:
            if build_context.architectures is not None:
                arguments += f"-framework {build_context.build_directory}/{build_context.combined_architecture}/lib/{build_context.target_folder}/{target}.framework "
        if os.path.exists(output_file):
            shutil.rmtree(output_file)
        os.system(f'xcodebuild -create-xcframework {arguments}')

    @staticmethod
    def render_doxygen_docs():
        """renders the doxygen documentation for Objective-C"""
        BuildContext.render_doxygen_docs('Doxyfile-ObjC')


class WindowsBuildContext(BuildContext):
    """Build context for Windows (.NET 5.0). This defines the logic for packaging the dlls for multiple architectures
    into one NuGet package for distribution."""

    def install(self):
        for architecture in self.architectures:
            self.conan_install(architecture=architecture)

    def package(self):
        """Copies all dlls into the NuGet template in `lib/platform/windows` and runs `nuget pack`. The resulting
        nupkg will be copied to the build output folder """
        print(f'{print_prefix} packaging to NuGet package:')
        nupkg_root_dir = f'{workdir}/lib/platform/windows'
        nuspec = f'{target}.nuspec'
        shutil.copy(src=f'{self.build_directory}/{self.architectures[0].name}/lib/{self.configuration.value}/{target}.dll',
                    dst=f'{nupkg_root_dir}/lib/net5.0/')
        for architecture in self.architectures:
            destination = f'{nupkg_root_dir}/runtimes/{architecture.value.windows}/lib/net5.0/'
            shutil.copy(src=f'{self.build_directory}/{architecture.name}/lib/{self.configuration.value}/{target}.dll',
                        dst=destination)
            shutil.copy(src=f'{self.build_directory}/{architecture.name}/lib/{self.configuration.value}/Ijwhost.dll',
                        dst=destination)
        WindowsBuildContext.configure_nuspec(f'{nupkg_root_dir}/{nuspec}')
        os.chdir(nupkg_root_dir)
        os.system(f'nuget pack {nuspec}')
        os.chdir(workdir)
        shutil.copy(src=f'{nupkg_root_dir}/{target}.{get_version()}.nupkg',
                    dst=f'{self.build_directory}/')

    @staticmethod
    def configure_nuspec(nuspec: str):
        """Writes the current version defined in the VERSION file into the nuspec template"""
        with open(f'{nuspec}.template', 'rt') as fin:
            with open(f'{nuspec}', "wt") as fout:
                for line in fin:
                    fout.write(line.replace('{version}', get_version()))

    @staticmethod
    def render_doxygen_docs():
        """renders the doxygen documentation for C++/CLI"""
        BuildContext.render_doxygen_docs('Doxyfile-CppCli')


def main():
    """Main entrypoint of build.py. Parses the given CLI parameters & initializes the build contexts for the selected
    target platforms accordingly"""
    parser = argparse.ArgumentParser(description='Build & package library for different platforms')
    parser.add_argument('--configuration', dest='configuration', type=BuildConfiguration.from_string,
                        choices=list(BuildConfiguration), default=BuildConfiguration.release)
    parser.add_argument('--android', nargs='*', dest='android_architectures', type=Architecture.from_string,
                        choices=list(Architecture),
                        help="list of architectures that the library should be built for android")
    parser.add_argument('--aar', action='store_const', const=True, dest='package_aar',
                        help='wether to package the resulting binaries as AAR for Android')
    parser.add_argument('--macos', nargs='*', dest='macos_architectures', type=Architecture.from_string,
                        choices=list([Architecture.armv8, Architecture.x86_64]))
    parser.add_argument('--iphonesimulator', nargs='*', dest='iphonesimulator_architectures',
                        type=Architecture.from_string,
                        choices=list([Architecture.armv8, Architecture.x86_64]))
    parser.add_argument('--iphoneos', nargs='*', dest='iphoneos_architectures', type=Architecture.from_string,
                        choices=list([Architecture.armv8, Architecture.armv7]))
    parser.add_argument('--xcframework', action='store_const', const=True, dest='xcframework',
                        help='wether to package all macOS/iOS related binaries into an xcframework')
    parser.add_argument('--windows', nargs='*', dest='windows_architectures', type=Architecture.from_string,
                        choices=list(Architecture),
                        help='list of architectures to build for windows')
    parser.add_argument('--nuget', action='store_const', const=True, dest='nuget',
                        help='wether to package the resulting dlls as nuget for windows')
    parser.add_argument('--build-directory', dest='build_directory', type=str, default="build")
    parser.add_argument('--android-ndk', dest='android_ndk', type=str, help='directory of the NDK installation')
    parser.add_argument('--java-8-home', dest='java_8_home', type=str,
                        help='JAVA_HOME for a Java 1.8 installation. Required if building for Android')
    parser.add_argument('--java-11-home', dest='java_11_home', type=str,
                        help='JAVA_HOME for a Java Version > 11. Required if building for Android')
    parser.add_argument('--render-docs', action='store_const', const=True, dest='render_docs',
                        help='render doxygen documentation for the languages of the selected target platforms')

    arguments = parser.parse_args()
    arguments.build_directory = os.path.abspath(arguments.build_directory)

    if arguments.android_architectures:
        message_template = Template('Missing parameter: `$parameter` is required if building for Android!')
        missing_parameter: bool = False
        if not arguments.android_ndk:
            missing_parameter = True
            print(message_template.substitute(parameter='--android-ndk'), file=sys.stderr)
        if not arguments.java_8_home:
            missing_parameter = True
            print(message_template.substitute(parameter='--java-8-home'), file=sys.stderr)
        if not arguments.java_11_home and arguments.package_aar:
            missing_parameter = True
            print(message_template.substitute(parameter='--java-11-home'), file=sys.stderr)
        if missing_parameter:
            print()
            parser.print_help()
            exit(1)

        android = AndroidBuildContext(build_directory=f'{arguments.build_directory}/android',
                                      profile=android_profile,
                                      architectures=arguments.android_architectures,
                                      configuration=arguments.configuration)
        android.install(android_ndk=arguments.android_ndk,
                        conan_cmake_toolchain_file=android_conan_cmake_toolchain_file,
                        java_home=arguments.java_8_home)
        android.build()
        if arguments.package_aar:
            android.package(java_home=arguments.java_11_home)
        if arguments.render_docs:
            AndroidBuildContext.render_doxygen_docs()

    macos = DarwinBuildContext(build_directory=f'{arguments.build_directory}/macos',
                               profile=macos_profile,
                               architectures=arguments.macos_architectures,
                               configuration=arguments.configuration,
                               sdk='macosx')
    iphone = DarwinBuildContext(build_directory=f'{arguments.build_directory}/iphone',
                                profile=ios_profile,
                                architectures=arguments.iphoneos_architectures,
                                configuration=arguments.configuration,
                                sdk='iphoneos')
    iphonesimulator = DarwinBuildContext(build_directory=f'{arguments.build_directory}/iphonesimulator',
                                         profile=ios_profile,
                                         architectures=arguments.iphonesimulator_architectures,
                                         configuration=arguments.configuration,
                                         sdk='iphonesimulator')
    if arguments.macos_architectures is not None:
        macos.install()
        macos.build()
    if arguments.iphonesimulator_architectures is not None:
        iphonesimulator.install()
        iphonesimulator.build()
    if arguments.iphoneos_architectures is not None:
        iphone.install()
        iphone.build()

    if arguments.render_docs and ((arguments.macos_architectures is not None) or (arguments.iphonesimulator_architectures is not None) or (
            arguments.iphoneos_architectures is not None)):
        DarwinBuildContext.render_doxygen_docs()

    if arguments.xcframework:
        DarwinBuildContext.package(build_context_list=[iphonesimulator, iphone, macos],
                                   build_directory=arguments.build_directory,
                                   configuration=arguments.configuration)

    if arguments.windows_architectures:
        windows = WindowsBuildContext(build_directory=f'{arguments.build_directory}/windows',
                                      profile=windows_profile,
                                      architectures=arguments.windows_architectures,
                                      configuration=arguments.configuration)
        windows.install()
        windows.build()
        if arguments.nuget:
            windows.package()
        if arguments.render_docs:
            WindowsBuildContext.render_doxygen_docs()

    if arguments.render_docs:
        BuildContext.render_doxygen_docs('Doxyfile-Cpp')


if __name__ == "__main__":
    main()
