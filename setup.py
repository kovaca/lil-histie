import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='lil_histie',
    version='0.0.1',
    packages=find_packages(),
    author="Alex Kovac",
    author_email="akovac@wri.org",
    description="Simple CLI to display histograms from piped gdalinfo output.",
    long_description=long_description,
    url="https://github.com/kovaca/lil-histie",
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points='''
        [console_scripts]
        lil_histie=lil_histie.histogram:cli
    ''',
)