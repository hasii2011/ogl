import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="ogl",
    version="0.53.1",
    author_email='Humberto.A.Sanchez.II@gmail.com',
    description='External Pyut Graphical Shapes',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/ogl",
    package_data={
        'miniogl':        ['py.typed'],
        'ogl':             ['py.typed'],
        'ogl.events':      ['py.typed'],
        'ogl.preferences': ['py.typed'],
        'ogl.resources':   ['py.typed'],
        'ogl.sd':          ['py.typed'],
    },

    packages=[
        'miniogl',
        'ogl',
        'ogl.events',
        'ogl.preferences',
        'ogl.resources', 'ogl.resources.img', 'ogl.resources.img.textdetails',
        'ogl.sd',
    ],
    install_requires=['Deprecated', 'pyutmodel', 'wxPython'],
)
