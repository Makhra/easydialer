from setuptools import setup

setup(
    name = 'ezdialer',
    version = '0.1.0',
    packages = ['easydialer'],
    entry_points = {
        'console_scripts': [
            'ezdialer = easydialer.__main__:main'
        ]
    })