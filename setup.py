import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pynotifyd",
    version="0.0.2",
    author="Tudor Roman",
    author_email="tudurom@gmail.com",
    description="Simple notification server",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/ricede/pynotifyd",
    scripts=['pynotifyd/pynotifyd'],
    packages=['pynotifyd'],
    python_requires='>=3.5',
    install_requires=[
        'PyGObject',
        'dbus-python',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: POSIX",
        "Topic :: Desktop Environment",
    ),
)
