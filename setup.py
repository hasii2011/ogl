import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="pyutgraphicalmodel",
    version="0.5",
    author_email='Humberto.A.Sanchez.II@gmail.com',
    description='External Pyut Graphical Data Model',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/pyutgraphicalmodel",
    packages=[
        'org', 'org.pyut', 'org.pyut.miniogl',
        'org.pyut.ogl',
        'org.pyut.ogl.events',
        'org.pyut.ogl.preferences',
        'org.pyut.ogl.resources', 'org.pyut.ogl.resources.img', 'org.pyut.ogl.resources.img.textdetails',
        'org.pyut.ogl.sd',
        'pyutgraphicalmodel',
    ],
    install_requires=['Deprecated', 'pyutmodel', 'wxPython'],
)
