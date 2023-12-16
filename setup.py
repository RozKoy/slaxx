from setuptools import setup, find_packages

requires = [
    "grpcio",
    "alembic",
    "PyMySQL",
    "SQLAlchemy",
    "grpcio-tools",
    "mysql-connector-python",
]

tests_require = [
    "pytest",
    "pytest-cov",
]

setup(
    name="slaxx",
    version="1.0",
    description="slaxx",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: GRPC",
    ],
    url="",
    author="",
    author_email="",
    keywords="grpc pyramid",
    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
    include_package_data=True,
    extras_require={
        "testing": tests_require,
    },
    install_requires=requires,
    )