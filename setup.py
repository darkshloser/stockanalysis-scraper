from setuptools import setup, find_packages

setup(
    name='stockanalysis_scraper',
    version='0.5.0',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'requests',
        'beautifulsoup4',
        'webdriver-manager',
    ],
    include_package_data=True,
    package_data={
        '': ['config.ini'],
    },
    entry_points={
        'console_scripts': [],
    },
    author='Dobromir Kovachev',
    author_email='dobromir.mail@gmail.com',
    description='A web scraper for different market data and news from https://stockanalysis.com/',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/darkshloser/stockanalysis-scraper',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)


