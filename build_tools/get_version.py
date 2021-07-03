from conans import tools


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
