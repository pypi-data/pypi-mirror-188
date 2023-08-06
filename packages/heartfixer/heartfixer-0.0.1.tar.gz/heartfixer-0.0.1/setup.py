from setuptools import setup

setup(
    name="heartfixer",
    py_modules=["heartfixer"],
    packages=["heartfixer"],
    version="0.0.1",
    url="https://github.com/smallcloudai/heartfixer",
    summary="Command line tool to fix things using AI",
    description="Fix things using AI / Python library",
    license='GNU GPLv3',
    install_requires=[
        "termcolor",
        "pandas",
    ],
    author="Small Magellanic Cloud AI Ltd.",
    author_email="cli-tool@smallcloud.tech",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: Console",
        "Operating System :: OS Independent",
    ]
)
