from setuptools import setup, find_packages

setup(
    name='BhauLang',
    version='0.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'bhau = bhauRunner:main'
        ]
    },
    install_requires=[
        # List your dependencies here
    ]
)
