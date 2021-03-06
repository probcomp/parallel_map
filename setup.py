# -*- coding: utf-8 -*-
# See LICENSE.txt

import os

# If some modules are not found, we use others, so no need to warn:
try:
    from setuptools import setup
    from setuptools.command.build_py import build_py
    from setuptools.command.sdist import sdist
    from setuptools.command.test import test
except ImportError:
    from distutils.core import setup
    from distutils.cmd import Command
    from distutils.command.build_py import build_py
    from distutils.command.sdist import sdist

    class test(Command):
        def __init__(self, *args, **kwargs):
            Command.__init__(self, *args, **kwargs)
        def initialize_options(self): pass
        def finalize_options(self): pass
        def run(self): self.run_tests()
        def run_tests(self): Command.run_tests(self)
        def set_undefined_options(self, opt, val):
            Command.set_undefined_options(self, opt, val)

def get_version():
    # The .git directory does not exist in the sdist, so read VERSION.
    if not os.path.exists('.git'):
        with open('VERSION', 'r') as f:
            version = f.read().strip()
            return version, version

    import re
    import subprocess
    # git describe a commit using the most recent tag reachable from it.
    # Release tags start with v* (XXX what about other tags starting with v?)
    # and are of the form `v1.1.2`.
    #
    # The output `desc` will be of the form v1.1.2-2-gb92bef6[-dirty]:
    # - verpart     v1.1.2
    # - revpart     2
    # - localpart   gb92bef6[-dirty]
    desc = subprocess.check_output([
        'git', 'describe', '--dirty', '--long', '--match', 'v*',
    ])
    match = re.match(r'^v([^-]*)-([0-9]+)-(.*)$', desc.decode('ASCII'))
    assert match is not None
    verpart, revpart, localpart = match.groups()
    # Create a post version.
    if revpart > '0' or 'dirty' in localpart:
        # Local part may be g0123abcd or g0123abcd-dirty.
        # Hyphens not kosher here, so replace by dots.
        localpart = localpart.replace('-', '.')
        full_version = '%s.post%s+%s' % (verpart, revpart, localpart)
    # Create a release version.
    else:
        full_version = verpart

    # Strip the local part if there is one, to appease pkg_resources,
    # which handles only PEP 386, not PEP 440.
    if '+' in full_version:
        pkg_version = full_version[:full_version.find('+')]
    else:
        pkg_version = full_version

    # Sanity-check the result.  XXX Consider checking the full PEP 386
    # and PEP 440 regular expressions here?
    assert '-' not in full_version, '%r' % (full_version,)
    assert '-' not in pkg_version, '%r' % (pkg_version,)
    assert '+' not in pkg_version, '%r' % (pkg_version,)

    return pkg_version, full_version

pkg_version, full_version = get_version()

def write_version_py(path):
    try:
        with open(path, 'rb') as f:
            version_old = f.read()
    except IOError:
        version_old = None
    version_new = '__version__ = %r\n' % (full_version,)
    if version_old != version_new:
        print('writing %s' % (path,))
        with open(path, 'w') as f:
            f.write(version_new)

def readme_contents():
    import os.path
    root_path = os.path.abspath(os.path.dirname(__file__))
    readme_path = os.path.join(root_path, 'README.md')
    with open(readme_path) as readme_file:
        return readme_file.read()

class local_build_py(build_py):
    def run(self):
        write_version_py(version_py)
        build_py.run(self)

# Make sure the VERSION file in the sdist is exactly specified, even
# if it is a development version, so that we do not need to run git to
# discover it -- which won't work because there's no .git directory in
# the sdist.
class local_sdist(sdist):
    def make_release_tree(self, base_dir, files):
        import os
        sdist.make_release_tree(self, base_dir, files)
        version_file = os.path.join(base_dir, 'VERSION')
        print('updating %s' % (version_file,))
        # Write to temporary file first and rename over permanent not
        # just to avoid atomicity issues (not likely an issue since if
        # interrupted the whole sdist directory is only partially
        # written) but because the upstream sdist may have made a hard
        # link, so overwriting in place will edit the source tree.
        with open(version_file + '.tmp', 'w') as f:
            f.write('%s\n' % (pkg_version,))
        os.rename(version_file + '.tmp', version_file)

# XXX These should be attributes of `setup', but helpful distutils
# doesn't pass them through when it doesn't know about them a priori.
version_py = 'src/version.py'

setup(
    name='parallel_map',
    version=pkg_version,
    description='Simple utility for parallel mapping.',
    long_description=readme_contents(),
    url='https://github.com/probcomp/parallel_map',
    license='Apache-2.0',
    maintainer='Feras Saad',
    maintainer_email='fsaad@mit.edu',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
    ],
    packages=[
        'parallel_map',
        'parallel_map.tests',
    ],
    package_dir={
        'parallel_map': 'src',
        'parallel_map.tests': 'tests',
    },
    cmdclass={
        'build_py': local_build_py,
        'sdist': local_sdist,
    },
)
