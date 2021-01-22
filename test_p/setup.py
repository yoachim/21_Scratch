from setuptools import setup, find_packages

setup(name='test_sim',
      version='1.0',
      package_dir={'': 'test_sim'},
       packages=find_packages(where='test_sim'),
      )
