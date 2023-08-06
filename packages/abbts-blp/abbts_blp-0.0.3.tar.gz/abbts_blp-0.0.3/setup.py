from setuptools import setup
import abbts_blp

setup(
    name='abbts_blp',
    version=abbts_blp.__VERSION__,
    author='Pascal Helfenstein',
    author_email='pascal.helfenstien@xemax.ch',
    packages=['abbts_blp'],
    # scripts=['bin/script1','bin/script2'],
    url='http://pypi.python.org/pypi/abbts-blp/',
    license='LICENSE.txt',
    description='abbts_blp',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Optional (see note above)
    install_requires=[
        'pyserial >= 3.5',
        'Pillow >= 9.3',
    ],
)
