import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name="ogl",
    version="0.70.20",
    author='Humberto A. Sanchez II',
    author_email='Humberto.A.Sanchez.II@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='External Pyut Graphical Shapes',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/ogl",
    package_data={
        'miniogl':              ['py.typed'],
        'ogl':                  ['py.typed'],
        'ogl.events':           ['py.typed'],
        'ogl.preferences':      ['py.typed'],
        'ogl.resources':        ['py.typed'],
        'ogl.resources.img':             ['py.typed'],
        'ogl.resources.img.textdetails': ['py.typed'],
        'ogl.sd':               ['py.typed'],
        'ogl.ui':               ['py.typed'],
        'ogl.ui.valuecontrols': ['py.typed'],
    },

    packages=[
        'miniogl',
        'ogl',
        'ogl.events',
        'ogl.preferences',
        'ogl.resources', 'ogl.resources.img', 'ogl.resources.img.textdetails',
        'ogl.sd',
        'ogl.ui', 'ogl.ui.valuecontrols',
    ],
    install_requires=['Deprecated~=1.2.13', 'pyutmodel~=1.4.0', 'hasiicommon==0.0.7', 'wxPython~=4.2.0'],
)
