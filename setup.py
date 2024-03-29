from pathlib import Path
from setuptools import setup, find_packages
import re

HERE = Path(__file__).parent
META_PATH = Path().joinpath("snapsnare", "__init__.py")


def read(*parts) -> str:
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with HERE.joinpath(*parts).open(mode='r', encoding='utf-8') as f:
        return f.read()


def find_meta(meta: str) -> str:
    """
    Extract __*meta*__ from the project META_FILE.
    """
    meta_match = re.search(
        f"^__{meta}__ = ['\"]([^'\"]*)['\"]",
        read(META_PATH), re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError(f"Unable to find __{meta}__ string.")


setup(
    name=find_meta('title'),
    version=find_meta('version'),
    description=find_meta('description'),
    long_description=read('README.md'),
    license=find_meta('license'),
    author=find_meta('author'),
    author_email=find_meta('email'),
    maintainer=find_meta('author'),
    maintainer_email=find_meta('email'),
    url=find_meta('uri'),
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Other Audience',
        'Topic :: Multimedia :: Sound/Audio'
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='snapsnare wiki musicians',
    packages=find_packages(exclude=['db', 'docs', 'snippets', 'tests', 'venv']),
    include_package_data=True,
    install_requires=[
        'flask_restful',
        'flask-jwt-extended',
        'flask-login',
        'flask==2.0.2',
        'click',
        'psycopg2-binary',
        'requests',
        'paprika-connector==0.0.6',
        'pydub'
    ],
    package_data={
        'snapsnare': [
            '*.json', 'static/*', 'repositories/*/*.sql', 'templates/*/*.html', 'templates/*/*/*.html'
        ]
    },
    entry_points={
        'console_scripts': [
            'snapsnare=snapsnare.app:main'
        ],
    },
)
