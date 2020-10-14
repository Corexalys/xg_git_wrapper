from setuptools import setup

setup(
    name="xg",
    description="XG, our git wrapper.",
    version="0.0.2",
    packages=["xg"],
    scripts=["scripts/xg"],
    install_requires=[
        "wcwidth",
        "colorama",
    ],
)
