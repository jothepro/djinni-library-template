#!/usr/bin/env python3

from djinni_build import DjinniBuild

djinniBuild = DjinniBuild(
    darwin_target='MyDjinniLibrary',
    windows_target='MyDjinniLibrary',
    android_target='MyDjinniLibrary',
    android_module_name='MyDjinniLibrary',
    nupkg_name='MyDjinniLibrary',
    conan_user='jothepro',
    conan_channel='release'
)
djinniBuild.main()
