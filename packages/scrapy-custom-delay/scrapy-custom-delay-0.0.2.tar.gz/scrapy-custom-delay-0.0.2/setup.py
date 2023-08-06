"""Package this project."""
from setuptools import find_packages, setup

from scrapy_domain_delay import __version__


setup(
    name='scrapy-custom-delay',
    version=__version__,
    project_urls={
        'Source': 'https://github.com/653603927/scrapy-custom-delay',
    },
    description=(
        'This package provides a way to let '
        'you set different delay for different '
        'website, using the Scrapy framework.'
    ),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    author='LiuXiaotong',
    author_email='lxtxiaotong@foxmail.com',
    classifiers=[
        'Framework :: Scrapy',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
    install_requires=[
        'scrapy>=1.6.0',
    ],
)
