#!/usr/bin/env python3

import os
from conans import tools
from djinni_build.djinni_build import DjinniBuild
from build_tools.get_version import get_version

workdir = os.getcwd()
djinniBuild = DjinniBuild(
    working_directory=workdir,
    darwin_target='MyDjinniLibrary',
    darwin_target_dir=f'lib/platform/darwin',
    windows_target='MyDjinniLibrary',
    windows_target_dir=f'lib/platform/windows',
    android_target='MyDjinniLibrary',
    android_target_dir=f'lib/platform/android',
    version=get_version(),
    android_profile=f'{workdir}/conan/profiles/android',
    macos_profile=f'{workdir}/conan/profiles/macos',
    ios_profile=f'{workdir}/conan/profiles/ios',
    windows_profile=f'{workdir}/conan/profiles/windows',
    linux_profile=f'{workdir}/conan/profiles/linux',
    android_project_dir=f'{workdir}/lib/platform/android/package',
    android_module_name='MyDjinniLibrary',
    nupkg_dir=f'{workdir}/lib/platform/windows/package',
    nupkg_name='MyDjinniLibrary',
    swiftpackage_dir=f'{workdir}/lib/platform/darwin/package'
)
djinniBuild.main()
