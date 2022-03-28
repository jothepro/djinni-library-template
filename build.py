#!/usr/bin/env python3

from conans import tools
from djinni_build import DjinniBuild


def get_version():
    """tries to determine the library version based on the git tag, and write it to the VERSION file.
    If no tag can be found, the version is loaded from the VERSION file."""
    try:
        version = tools.Git().run("describe --tags")[1:]
        tools.save("VERSION", version)
    except:
        version = tools.load("VERSION")
    return version


djinniBuild = DjinniBuild(
    version=get_version(),
    darwin_target='MyDjinniLibrary',
    windows_target='MyDjinniLibrary',
    android_target='MyDjinniLibrary',
    android_module_name='MyDjinniLibrary',
    nupkg_net_version='net6.0',
    nupkg_name='MyDjinniLibrary',
    conan_user='jothepro',
    conan_channel='release'
)
djinniBuild.main()
