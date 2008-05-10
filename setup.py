from setuptools import setup, find_packages
import sys, os

version = '0.2'

def read(*rnames):
    text = open(os.path.join(os.path.dirname(__file__), *rnames)).read()
    text = unicode(text, 'utf-8').encode('ascii', 'xmlcharrefreplace')
    return text

description = read('README.txt') + '\n\n' + \
              'Detailed Documentation\n' + \
              '**********************\n\n' + \
              read('contentratings', 'README.txt')

setup(name='contentratings',
      version=version,
      description="A small Zope 3 package (which works best with Zope 2 and Five) that allows you to easily attach ratings to content.",
      long_description=description,
      classifiers=['Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Framework :: Zope3',
        'Framework :: Zope2',
        'Framework :: Plone',
        "Topic :: Software Development :: Libraries :: Python Modules",], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      keywords='ratings zope plone z',
      author='Alec Mitchell',
      author_email='apm13@columbia.edu',
      url='http://plone.org/products/contentratings',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
         'setuptools',
      ],
      )
