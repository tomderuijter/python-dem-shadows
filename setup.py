from distutils.core import setup


def setup_config():
    config = {
        'name': 'python-dem-raycast',
        'version': '0.1',
        'description': 'Python library for casting solar shadows on digital elevation models.',
        'author': 'Tom de Ruijter',
        'author_email': 'deruijter.tom@gmail.com',
        'url': 'https://github.com/tomderuijter/python-dem-raycast',
        'download_url': 'https://github.com/tomderuijter/python-dem-raycast/tarball/v0.1',
        'packages': ['python-dem'],
        'keywords': ['dem', 'elevation', 'raycast', 'insolation', 'sun position', 'gis'],
        'classifiers': [
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
        ],
        'install_requires': ['numpy'],
    }
    return config


if __name__ == "__main__":
    setup(**setup_config())
