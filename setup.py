from setuptools import setup, find_packages
# Read the contents of your README file
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='BhauLang',
    version='0.2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'bhau = bhauRunner:main'
        ]
    },
    install_requires=[
        # List your dependencies here
    ],
    # Add your README file as the long description
    long_description=long_description,
    long_description_content_type='text/markdown'  # Specify the content type
)
