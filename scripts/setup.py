from setuptools import setup, find_packages

def get_tag():
    f = open('VERSION', 'r')
    tag = f.read().strip()
    f.close()
    return tag


def get_description():
    f = open('README', 'r')
    desc = f.read()
    f.close()
    return desc


setup(name='hailc',
      version=get_tag(),
      description='Lightly reviewed community code snippets for Hail.',
      long_description=get_description(),
      url='https://github.com/hail-is/hail-contrib',
      author='Hail Team',
      author_email='hail-team@broadinstitute.org',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7'
      ],
      keywords='bioinformatics genomics spark hail',
      packages=find_packages()
      )
