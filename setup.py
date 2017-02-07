import setuptools
import setuptools.command.install
import os.path
import platform
import json
import subprocess

def _pre_install():
    print("Verifying that the library is accessible.")

    try:
        _check_homebrew()
        import libarchive.library
    except OSError as e:
        print("Library can not be loaded: %s" % (str(e)))
        raise

def _check_homebrew():
    if platform.system() == 'Darwin':
        #export LA_LIBRARY_FILEPATH="$(brew --prefix)/opt/libarchive/lib/libarchive.13.dylib"
        #export LIBARCHIVE_PREFIX="$(brew --prefix)/opt/libarchive"
        # let's check for homebrew
        try:
            subprocess.check_call('brew')
        except Exception as e:
            # no homebrew installed, let's bail
            return False
        try:
            # From homebrew on libarchive:
            # This formula is keg-only, which means it was not symlinked into /usr/local.
            #
            # macOS already provides this software and installing another version in
            # parallel can cause all kinds of trouble.
            # so... let's see if we can't find it ourselves and set the envvar
            # /Usr/local/opt/libarchive/lib/
            libarchive_info = json.loads(
                    subprocess.check_output(['brew', 'info', '--json=v1',
                        'libarchive']))
            libarchive_version = libarchive_info[0]['installed'][0]['version']
            # set the direct dylib envvar
            libarchive_path = path.join(subprocess.check_output([ 'brew',
                '--cellar', 'libarchive'])[:-1], libarchive_version, 'lib',
                'libarchive.dylib')
            os.environ["LA_LIBRARY_FILEPATH"] = libarchive_path
            return True
        except Exception as e:
            return False
    else:
        return False

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
    package_data={
        'libarchive': ['resources/README.rst',
                       'resources/requirements.txt'],
    },
    install_requires=install_requires,
    cmdclass={ 'install': _custom_install }
)
