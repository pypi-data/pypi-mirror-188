from setuptools import setup, find_packages

long_description = 'Make your code shorter with shortcuts optimised for golfing in Python - read the docs at https://www.github.com/nayakrujul/golfing-shortcuts'

setup(
  name = 'golfing-shortcuts',
  version = '1.0',
  license='Apache',
  description = 'Make your code shorter with shortcuts optimised for golfing in Python',
  author = 'Rujul Nayak',
  author_email = 'rujulnayak@outlook.com',
  url = 'https://github.com/nayakrujul/golfing-shortcuts',
  download_url = 'https://github.com/nayakrujul/golfing-shortcuts/archive/refs/tags/v_01.tar.gz',
  keywords = ['shortcuts', 'golfing', 'code-golf'],
  install_requires=[
      ],
  classifiers=[
    'Development Status :: 3 - Alpha', 
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
  long_description=long_description,
  long_description_content_type='text/x-rst',
  packages = find_packages()
)
