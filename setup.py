from setuptools import setup, find_packages

setup(
    name='nnc',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4==4.12.3',
        'requests==2.31.0',
        'urllib3==2.2.1',
    ],
    python_requires='>=3.9',
    author='seoly0',
    author_email='seoly0.dev@gmail.com',
    description='naver news crawler',
    url='https://github.com/seoly0/naver-news-crawler',
)