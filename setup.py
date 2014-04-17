from setuptools import setup, find_packages
from setuptools.command.install import install

def _pre_install():
    print("Verifying that the library is accessible.")

    try:
        import libarchive.library
    except OSError:
        print("Library can not be loaded: %s" % (_LIB_FILEPATH))
        raise


class _custom_install(install):
    def run(self):
        _pre_install()
        install.run(self)

description = "Python adapter for universal, libarchive-based archive access."

setup(name='libarchive',
      version='0.1.0',
      description=description,
      long_description="""""",
      classifiers=[],
      keywords='archive libarchive 7z tar bz2 zip gz',
      author='Dustin Oprea',
      author_email='myselfasunder@gmail.com',
      url='',
      license='GPL 2',
      packages=find_packages(exclude=['dev']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      cmdclass={ 'install': _custom_install },
)

