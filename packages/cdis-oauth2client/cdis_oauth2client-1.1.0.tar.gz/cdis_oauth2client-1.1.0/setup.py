from setuptools import setup
from subprocess import check_output


def get_version():
    # https://github.com/uc-cdis/dictionaryutils/pull/37#discussion_r257898408
    try:
        tag = check_output(
            ["git", "describe", "--tags", "--abbrev=0", "--match=[0-9]*"]
        )
        return tag.decode("utf-8").strip("\n")
    except Exception:
        raise RuntimeError(
            "The version number cannot be extracted from git tag in this source "
            "distribution; please either download the source from PyPI, or check out "
            "from GitHub and make sure that the git CLI is available."
        )


setup(
    name="cdis_oauth2client",
    version='1.1.0',
    description="Flask blueprint and utilities for oauth2 client",
    url="https://github.com/uc-cdis/cdis_oauth2client",
    license="Apache",
    packages=[
        "cdis_oauth2client",
    ],
    install_requires=[
        "Flask>=1.1.1",
        "requests>=2.5",
        "cdispyutils>=1.0.4",
    ],
)
