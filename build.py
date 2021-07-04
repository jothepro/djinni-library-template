#!/usr/bin/env python3

import os
from conans import tools
from build_tools.djinni_build.djinni_build import DjinniBuild
from build_tools.get_version import get_version

djinniBuild = DjinniBuild(
    working_directory=os.getcwd(),
    darwin_target='MyDjinniLibrary',
    darwin_target_dir='lib/platform/darwin',
    windows_target='MyDjinniLibrary',
    windows_target_dir='lib/platform/windows',
    android_target='MyDjinniLibrary',
    android_target_dir='lib/platform/android',
    version=get_version(),
    android_profile='conan/profiles/android',
    macos_profile='conan/profiles/macos',
    ios_profile='conan/profiles/ios',
    windows_profile='conan/profiles/windows',
    linux_profile='conan/profiles/linux',
    android_project_dir='lib/platform/android/package',
    android_module_name='MyDjinniLibrary',
    nupkg_dir='lib/platform/windows/package',
    nupkg_name='MyDjinniLibrary',
    swiftpackage_dir='lib/platform/darwin/package'
)
djinniBuild.main()
