import os

from setuptools import setup, find_packages

# here = os.path.abspath(os.path.dirname(__file__))
# with open(os.path.join(here, "README.txt")) as f:
#     README = f.read()
# with open(os.path.join(here, "CHANGES.txt")) as f:
#     CHANGES = f.read()

requires = [
    "grpcio",
    "pyramid",
    "waitress",
    "grpcio-tools",
    "pyramid_jinja2",
    "plaster_pastedeploy",
    "pyramid_debugtoolbar",
]

tests_require = [
    "pytest",
    "WebTest",
    "pytest-cov",
]

setup(
    name="rest",
    version="0.0",
    description="rest",
    # long_description=README + "\n\n" + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    url="",
    author="",
    author_email="",
    keywords="web pyramid pylons",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        "testing": tests_require,
    },
    install_requires=requires,
    entry_points={
        "paste.app_factory": [
            "main = rest:main",
        ],
    },
)
