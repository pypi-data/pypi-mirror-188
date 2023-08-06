# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['majormode']

package_data = \
{'': ['*']}

install_requires = \
['dlib',
 'exifread',
 'face-recognition',
 'numpy',
 'perseus-core-library',
 'pillow']

entry_points = \
{'console_scripts': ['photoidmagick = majormode.photoidmagick:main']}

setup_kwargs = {
    'name': 'photoidmagick',
    'version': '1.1.6',
    'description': 'Python library to automatically align and crop your photos to the correct biometric passport photo size',
    'long_description': "# Photo ID Magick\n\nPython library to automatically align and crop your photos to the correct biometric passport photo size.\n\nThis library is based on the libraries [face_detection](https://github.com/ageitgey/face_recognition) and [Pillow](https://python-pillow.org/).\n\n## Installation\n\n```bash\n$ pip install photoidmagick\n```\n\n## Usage\n\n|                         |                         |                         |                         |\n| ----------------------- | ----------------------- | ----------------------- | ----------------------- |\n| ![](doc/sample_003.jpg) | ![](doc/sample_005.jpg) | ![](doc/sample_009.jpg) | ![](doc/sample_011.jpg) |\n\n|                                |                                |                                |                                |\n| ------------------------------ | ------------------------------ | ------------------------------ | ------------------------------ |\n| ![](doc/sample_003.square.jpg) | ![](doc/sample_005.square.jpg) | ![](doc/sample_009.square.jpg) | ![](doc/sample_011.square.jpg) |\n\n```bash\n$ photoidmagick -f sample_039.jpg -s 1750x2250\nTraceback (most recent call last):\n__main__.ObliqueFacePoseException: the midsagittal facial line doesn't intersect the midhorizontal iris line in the middle\n\n\n$ photoidmagick -f sample_039.jpg -s 350x450 --allow-oblique-face\n```\n\n| Original                | Passport Photo Format            | Square Photo Format            |\n| ----------------------- | -------------------------------- | ------------------------------ |\n| ![](doc/sample_039.jpg) | ![](doc/sample_039.passport.jpg) | ![](doc/sample_039.square.jpg) |\n\n```bash\n$ photoidmagick -f sample_054.jpg -s 400x400 --allow-oblique-face\nTraceback (most recent call last):\n__main__.UnevenlyOpenEyelidException: the right eye is more opened than the left eye\n\n$ photoidmagick -f sample_054.jpg -s 1000x1000 --allow-oblique-face --allow-unevenly-open-eye\n```\n\n| Original                | Passport Photo Format            | Square Photo Format            |\n| ----------------------- | -------------------------------- | ------------------------------ |\n| ![](doc/sample_054.jpg) | ![](doc/sample_054.passport.jpg) | ![](doc/sample_054.square.jpg) |  |\n",
    'author': 'Daniel CAUNE',
    'author_email': 'daniel.caune@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/majormode/photoidmagick-python-library',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
