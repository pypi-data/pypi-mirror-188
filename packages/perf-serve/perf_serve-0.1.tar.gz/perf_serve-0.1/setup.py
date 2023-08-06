from setuptools import setup

setup(
    name='perf_serve',
    version='0.1',
    description='Easily serve linux perf profile for firefox profiler',
    url='https://github.com/forestryks/perf-serve',
    author='Andrei Odintsov',
    author_email='forestryks1@gmail.com',
    license='MIT',
    packages=['perf_serve'],
    install_requires=[
        'argparse',
        'netifaces'
    ],
    zip_safe=False
)
