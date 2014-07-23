import setuptools
import setuptools.command.install

def _pre_install():
    print("Verifying that the library is accessible.")

    try:
        import libarchive.library
    except OSError as e:
        print("Library can not be loaded: %s" % (str(e)))
        raise


class _custom_install(setuptools.command.install.install):
    def run(self):
        _pre_install()
        setuptools.command.install.install.run(self)

import libarchive

app_path = os.path.dirname(libarchive.__file__)

with open(os.path.join(app_path, 'resources', 'README.rst')) as f:
      long_description = f.read()

with open(os.path.join(app_path, 'resources', 'requirements.txt')) as f:
      install_requires = list(map(lambda s: s.strip(), f))

description = "Python adapter for universal, libarchive-based archive access."

setuptools.setup(
    name='libarchive',
    version=libarchive.__version__,
    description=description,
    long_description=long_description,
    classifiers=[],
    keywords='archive libarchive 7z tar bz2 zip gz',
    author='Dustin Oprea',
    author_email='myselfasunder@gmail.com',
    url='https://github.com/dsoprea/PyEasyArchive',
    license='GPL 2',
    packages=setuptools.find_packages(exclude=['dev', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    cmdclass={ 'install': _custom_install }
)
