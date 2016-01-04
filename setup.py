try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Tile hash proxy server',
    'author': 'Matt Amos',
    'url': 'https://github.com/mapzen/tile-hash-proxy',
    'author_email': 'matt.amos@mapzen.com',
    'version': '0.1',
    'install_requires': ['SimpleHTTPServer', 'requests'],
    'packages': ['tile-hash-proxy'],
    'scripts': [],
    'name': 'tile-hash-proxy'
}

setup(**config)
