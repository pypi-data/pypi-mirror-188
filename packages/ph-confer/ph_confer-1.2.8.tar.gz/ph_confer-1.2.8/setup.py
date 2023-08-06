import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
  'python-etcd==0.4.3',
  'mako==1.2.3',
  'urllib3==1.23'
]

setup(
  name='ph_confer',
  version='1.2.8',
  description='A tool to automatically template configurations from a key-value store.',
  long_description='',
  # Choose your license
  license='LGPLv3',
  classifiers=[
    'Development Status :: 5 - Production/Stable',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Utilities',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
  author='ParseHub',
  author_email='serge@parsehub.com',
  url='https://www.parsehub.com',
  keywords='sysadmin development tools configuration',
  packages=find_packages(),
  zip_safe=True,
  dependency_links=[],
  install_requires=requires,
  entry_points={
    'console_scripts': [
      'phconfer=ph_confer.cli:main',
    ],
  },
)
