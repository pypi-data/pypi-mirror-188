import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="notebook_utils",
    version="0.2.0",
    author="Sam Bland",
    author_email="sbland.co.uk@gmail.com",
    description="Python jupyter notebook helper utilities",
    install_requires=[
        'wheel',
        'scipy',
        'numpy',
        'pandas',
        'matplotlib',
        'deprecated',
    ],
    setup_requires=[
        'wheel',
        'pytest-cov',
        'pytest-runner',
        'snapshottest'
    ],
    tests_require=['pytest', 'numpy', 'pandas', 'matplotlib', 'pytest-benchmark'],
    extras_require={'test': ['pytest', 'numpy', 'pandas']},
    packages=setuptools.find_packages(),
    package_dir={'notebook_utils': 'notebook_utils'},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)
