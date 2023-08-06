# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jackdaw_ml',
 'jackdaw_ml.access_interface',
 'jackdaw_ml.detectors',
 'jackdaw_ml.search',
 'jackdaw_ml.serializers']

package_data = \
{'': ['*']}

install_requires = \
['artefactlink>=0.4.1',
 'gitpython>=3,<4',
 'giturlparse>=0,<1',
 'pyarrow>=9,<10',
 'urllib3>=1,<2']

setup_kwargs = {
    'name': 'jackdaw-ml',
    'version': '0.0.5',
    'description': 'Share and Organise Machine Learning Models',
    'long_description': '# Jackdaw ML\n\nJackdaw is a framework designed to help Data Scientists save, load, and deploy Machine Learning models in a \nsimple and robust way.\n\nUnlike other frameworks, sharing a model only requires two short lines of code.\n\n1. `@find_artefacts`\n    \n    Scan model code, finding model artefacts and variables. Jackdaw supports PyTorch, Tensorflow, XGBoost, and LightGBM\n    out of the box, but is trivial for users to expand to other frameworks.\n\n\n2. `jackdaw_ml.saves`\n    \n    Model artefacts are saved to either local or remote storage, and the user is provided with a Model ID. \n    Users can store the ID for use in deployment, or search for the model by its name, metrics, Git branch, etc. \n\nA Model can be as simple as a stored number, or as complex as a combination of frameworks. Regardless of complexity, \nJackdaw aims to make it simple to share your models with other applications, other colleagues, or other companies.\n\nDocumentation is baked into the repository, and is available [here](docs). \n\n![Example of Save & Load of a PyTorch model via Jackdaw](docs/visuals/JackdawSaveLoad.gif)\n\n\n## Setup - Working Locally\nJackdaw is available on [PyPi](https://pypi.org/project/jackdaw-ml/) and can be installed via pip;\n\n```bash\n>>> pip install jackdaw_ml\n```\n\n### Alpha - Limited Windows & Mac Support\nWhile Jackdaw is in Alpha, one of the libraries it relies upon - artefactlink - only supports Windows and Mac OS/X for Python 3.10. Linux support is available for 3.8, 3.9, and 3.10.\n\n## Setup - Sharing Models across Environments\nTo share items across multiple computers, you\'ll eventually need an account with ShareableAI. \n\nFor now, you just need your API Token. If you don\'t have a token, reach out to `lissa@shareablei.com` and they\'ll ping you one.\n\n## Roadmap - Future Features\n[View our Public Roadmap here](https://github.com/orgs/shareableai/projects/1/views/1)\n\n\n## Getting Started\n\n### Example by Framework \n* [SKLearn](examples/frameworks/test_sklearn.py)\n* [LightGBM](examples/frameworks/test_lightgbm.py)\n* [XGBoost](examples/frameworks/test_xgboost.py)\n* [PyTorch](examples/frameworks/test_pytorch.py)\n* [Tensorflow](examples/frameworks/test_tensorflow.py)\n* [DARTs](examples/frameworks/test_darts.py)\n\n### Example\n\nThe core magic of Jackdaw is within the `@artefacts` and `@find_artefacts` decorators.\n\n`@artefacts` allows you to list what should be saved on a Model. `@find_artefacts` will detect what should be saved based\non a whole host of common frameworks. Combining the two is a powerful way of ensuring complex models can be saved easily.\n\n\n```python\nfrom jackdaw_ml.artefact_decorator import find_artefacts\nfrom jackdaw_ml.trace import trace_artefacts\nfrom jackdaw_ml import saves\n\nimport lightgbm as lgb\nimport numpy as np\n\n@find_artefacts()\nclass BasicLGBWrapper:\n    model: lgb.Booster\n\n    \n# The LightGBM model isn\'t defined yet, but we can discover it via annotations.\n#   LightGBM is Pickle-safe, so it\'s serialised via the PickleSerialiser by default.\n# >>> trace_artefacts(BasicLGBWrapper())\n# <class \'__main__.BasicLGBWrapper\'>{\n#         (model) [<class \'jackdaw_ml.serializers.pickle.PickleSerializer\'>]\n# }\n\n\ndef example_data() -> lgb.Dataset:\n    data = np.random.rand(500, 10)  # 500 entities, each contains 10 features\n    label = np.random.randint(2, size=500)  # binary target\n    return lgb.Dataset(data, label=label)\n\n# Create a new Model\nmodel = BasicLGBWrapper()\n# Modify the model\nmodel.model = lgb.train({}, example_data())\n\n# Save the model\nmodel_id = saves(model)\n```\n\n\n## Saving Remotely\nSaving and loading items from ShareableAI servers, rather than locally, can be achieved by providing an API key alongside the call to \n`artefacts`. If you\'d like to test this, please follow the setup for Sharing Models Remotely.\n\n```python\n\nfrom jackdaw_ml.artefact_decorator import artefacts\nfrom jackdaw_ml.serializers.pickle import PickleSerializer\nfrom jackdaw_ml.artefact_endpoint import ArtefactEndpoint\n\n@artefacts({PickleSerializer: ["x"]}, endpoint=ArtefactEndpoint.remote(\'MyAPIKey\'))\nclass MyModel:\n    def __init__(self):\n        self.x = 3\n```\n\nWe\'ll be expanding this to allow for sharing items between other users *very* soon, so keep an eye on [Corvus](https://github.com/shareableai/jackdaw/issues/2) to know more. \n',
    'author': 'Lissa Hyacinth',
    'author_email': 'lissa@shareableai.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
