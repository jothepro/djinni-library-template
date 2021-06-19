#!/usr/bin/env python3

import os
from djinni_build.djinni_build import DjinniBuild

workdir = os.getcwd()
djinniBuild = DjinniBuild(
    working_directory=workdir,
    target='MyDjinniLibrary',
    version=open('VERSION', 'rt').read()[1:],
    android_profile=f'{workdir}/conan/profiles/android',
    macos_profile=f'{workdir}/conan/profiles/macos',
    ios_profile=f'{workdir}/conan/profiles/ios',
    windows_profile=f'{workdir}/conan/profiles/windows',
    linux_profile=f'{workdir}/conan/profiles/linux',
    android_project_dir=f'{workdir}/lib/platform/android',
    android_module_dir=f'{workdir}/lib/platform/android/MyDjinniLibrary',
    nupkg_dir=f'{workdir}/lib/platform/windows',
    swiftpackage_dir=f'{workdir}/lib/platform/darwin'
)
djinniBuild.main()
