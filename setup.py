from setuptools import setup, find_packages
from setuptools.command.install import install

def _pre_install():
    print("Verifying that the library is accessible.")

    try:
        import libarchive.library
    except OSError as e:
        print("Library can not be loaded: %s" % (str(e)))
        raise


class _custom_install(install):
    def run(self):
        _pre_install()
        install.run(self)

description = "Python adapter for universal, libarchive-based archive access."

setup(name='libarchive',
      version='0.3.10',
      description=description,
      long_description="""""",
      classifiers=[],
      keywords='archive libarchive 7z tar bz2 zip gz',
      author='Dustin Oprea',
      author_email='myselfasunder@gmail.com',
      url='https://github.com/dsoprea/PyEasyArchive',
      license='GPL 2',
      packages=find_packages(exclude=['dev', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      cmdclass={ 'install': _custom_install },
)
