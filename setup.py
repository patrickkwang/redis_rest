"""Setup file for redis_rest package."""
from setuptools import setup

setup(
    name='redis_rest',
    version='1.0.0',
    author='Patrick Wang',
    author_email='patrick@covar.com',
    url='https://github.com/patrickkwang/redis_rest',
    description='REST interface for Redis',
    packages=['redis_rest'],
    include_package_data=True,
    zip_safe=False,
    license='MIT',
    python_requires='>=3.8',
)
