# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygroundsegmentation']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1,<2.0.0']

setup_kwargs = {
    'name': 'pygroundsegmentation',
    'version': '0.4.2',
    'description': '',
    'long_description': '# PyGroundSegmentation\n\nThis libary includes some **ground segmentation algorithms** rewritten in python. There are no external C or C++ dependencies only pure python (numpy).\n\n# Installation\n\n```bash\npip install pygroundsegmentation\n```\n\n## Included Algorithms\n\n- [x] [GPF](https://github.com/VincentCheungM/Run_based_segmentation) (Ground Plane Fitting)\n- [ ] [Patchwork-plusplus](https://github.com/url-kaist/patchwork-plusplus)\n- [ ] [Patchwork](https://github.com/LimHyungTae/patchwork)\n- [ ] [CascadedSeg](https://github.com/n-patiphon/cascaded_ground_seg)\n\n## Example Usage\n\n```python\nfrom pygroundsegmentation import GroundPlaneFitting\n\nground_estimator = GroundPlaneFitting() #Instantiate one of the Estimators\n\nxyz_pointcloud = np.random.rand(1000,3) #Example Pointcloud\nground_idxs = ground_estimator.estimate_ground(xyz_pointcloud)\nground_pcl = xyz_pointcloud[ground_idxs]\n\n```\n',
    'author': 'JonasHablitzel',
    'author_email': 'Jonas.Hablitzel@gmx.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JonasHablitzel/PyGroundSegmentation',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
