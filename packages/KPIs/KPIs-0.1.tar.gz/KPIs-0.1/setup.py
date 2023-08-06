from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]



setup(
  name='KPIs',
  version='0.1',
  description='Key Performance Indicator and Backtesting',
  long_description_content_type="text/markdown",
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Rakshit Maggon',
  author_email='rakshitmaggon70@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Backtesting', 
  python_requires='>=3.6',
  packages=find_packages(),
  install_requires=[
    'yfinance',
    'numpy',
    'pandas'
    ]
)