from setuptools import setup

setup(
    name="xg",
    description="XG, our git wrapper.",
    version="0.0.1",
    packages=["xg"],
    scripts=["scripts/xg"],
    install_requires=[
        "wcwidth",
        "colorama",
    ],
)
