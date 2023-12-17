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
    name="server",
    version="0.0",
    description="server",
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
    include_package_data=True,
    zip_safe=False,
    extras_require={
        "testing": tests_require,
    },
    install_requires=requires,
)