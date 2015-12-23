import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    print("setuptools is required for tt installation.\n"
          "You can install it using pip.")
    sys.exit(1)


from tt.core import program_author, program_build_date, program_license
from tt.core import program_license, program_url, program_version
from tt.core import program_desc

setup(
    name="tt",
    version=program_version,
    description=program_desc,
    author=program_author,
    url=program_url,
    license=program_license,
    install_requires=["setuptools"],
    packages=find_packages(),
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    ]
)
