# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['argilla_plugins',
 'argilla_plugins.active_learning',
 'argilla_plugins.datasets',
 'argilla_plugins.inference',
 'argilla_plugins.programmatic_labelling',
 'argilla_plugins.reporting',
 'argilla_plugins.utils']

package_data = \
{'': ['*']}

install_requires = \
['argilla[listeners]>=1.1.1,<2.0.0',
 'rich[jupyter]>=13.0.0,<14.0.0',
 'typer>=0.7.0,<0.8.0']

extras_require = \
{'reporting-datapane': ['datapane>=0.15.5,<0.16.0'],
 'reporting-greatexpectations': ['great-expectations>=0.15,<0.16']}

setup_kwargs = {
    'name': 'argilla-plugins',
    'version': '0.1.1',
    'description': '🔌 Open-source plugins for with practical features for Argilla using listeners.',
    'long_description': '# Argilla Plugins\n\n> 🔌 Open-source plugins for extra features and workflows\n\n**Why?**\nThe design of Argilla is intentionally programmable (i.e., developers can build complex workflows for reading and updating datasets). However, there are certain workflows and features which are shared across different use cases and could be simplified from a developer experience perspective. In order to facilitate the reuse of key workflows and empower the community, Argilla Plugins provides a collection of extensions to super power your Argilla use cases.\nSome of this pluggable method could be eventually integrated into the [core of Argilla](https://github.com/argilla-io/argilla).\n\n## Quickstart\n\n```bash\npip install argilla-plugins\n```\n\n```python\nfrom argilla_plugins.datasets import end_of_life\n\nplugin = end_of_life(\n    name="plugin-test",\n    end_of_life_in_seconds=100,\n    execution_interval_in_seconds=5,\n    discard_only=False\n)\nplugin.start()\n```\n\n## How to develop a plugin\n\n1. Pick a cool plugin from the list of topics or our issue overview.\n2. Think about an abstraction for the plugin as shown below.\n3. Refer to the solution in the issue.\n   1. fork the repo.\n   2. commit your code\n   3. open a PR.\n4. Keep it simple.\n5. Have fun.\n\n\n### Development requirements\n\n#### Function\nWe want to to keep the plugins as abstract as possible, hence they have to be able to be used within 3 lines of code.\n```python\nfrom argilla_plugins.topic import plugin\nplugin(name="dataset_name", ws="workspace" query="query", interval=1.0)\nplugin.start()\n```\n\n#### Variables\nvariables `name`, `ws`, and `query` are supposed to be re-used as much as possible throughout all plugins. Similarly, some functions might contain adaptations like `name_from` or `query_from`. Whenever possible re-use variables as much as possible.\n\nOhh, and don`t forget to have fun! 🤓\n\n## Topics\n### Reporting\n\n**What is it?**\nCreate interactive reports about dataset activity, dataset features, annotation tasks, model predictions, and more.\n\nPlugins:\n- [ ] automated reporting pluging using `datapane`. [issue](https://github.com/argilla-io/argilla-plugins/issues/1)\n- [ ] automated reporting pluging for `great-expectations`. [issue](https://github.com/argilla-io/argilla-plugins/issues/2)\n\n### Datasets\n\n**What is it?**\nEverything that involves operations on a `dataset level`, like dividing work, syncing datasets, and deduplicating records.\n\nPlugins:\n- [ ] sync data between datasets.\n  - [ ] directional A->B. [issue](https://github.com/argilla-io/argilla-plugins/issues/3)\n  - [ ] bi-directional A <-> B. [issue](https://github.com/argilla-io/argilla-plugins/issues/4)\n- [ ] remove duplicate records. [issue](https://github.com/argilla-io/argilla-plugins/issues/5)\n- [ ] create train test splits. [issue](https://github.com/argilla-io/argilla-plugins/issues/6)\n- [ ] set limits to records in datasets\n  - [X] end of life time. [issue](https://github.com/argilla-io/argilla-plugins/issues/7)\n  - [ ] max # of records. [issue](https://github.com/argilla-io/argilla-plugins/issues/8)\n\n#### End of Life\nAutomatically delete or discard records after `x` seconds.\n\n```python\nfrom argilla_plugins.datasets import end_of_life\n\nplugin = end_of_life(\n    name="plugin-test",\n    end_of_life_in_seconds=100,\n    execution_interval_in_seconds=5,\n    discard_only=False\n)\nplugin.start()\n```\n\n### Programmatic Labelling\n\n**What is it?**\nAutomatically update `annotations` and `predictions` labels and predictions of `records` based on heuristics.\n\nPlugins:\n- [X] annotated spans as gazzetteer for labelling. [issue](https://github.com/argilla-io/argilla-plugins/issues/12)\n- [ ] vector search queries and similarity threshold. [issue](https://github.com/argilla-io/argilla-plugins/issues/11)\n- [ ] use gazzetteer for labelling. [issue](https://github.com/argilla-io/argilla-plugins/issues/9)\n- [ ] materialize annotations/predictions from rules using Snorkel or a MajorityVoter [issue](https://github.com/argilla-io/argilla-plugins/issues/10)\n\n#### Token Copycat\n\nIf we annotate spans for texts like NER, we are relatively certain that these spans should be annotated the same throughout the entire dataset. We could use this assumption to already start annotating or predicting previously unseen data.\n\n```python\nfrom argilla_plugins import token_copycat\n\nplugin = token_copycat(\n    name="plugin-test",\n    query=None,\n    copy_predictions=True,\n    word_dict_kb_predictions={"key": {"label": "label", "score": 0}},\n    copy_annotations=True,\n    word_dict_kb_annotations={"key": {"label": "label", "score": 0}},\n    included_labels=["label"],\n    case_sensitive=True,\n    execution_interval_in_seconds=1,\n)\nplugin.start()\n```\n\n### Active learning\n\n**What is it?**\nA process during which a learning algorithm can interactively query a user (or some other information source) to label new data points.\n\nPlugins:\n- [ ] active learning for `TextClassification`.\n  - [X] `classy-classification`. [issue](https://github.com/argilla-io/argilla-plugins/issues/13)\n  - [ ] `small-text`. [issue](https://github.com/argilla-io/argilla-plugins/issues/15)\n- [ ] active learning for `TokenClassification`. [issue](https://github.com/argilla-io/argilla-plugins/issues/17)\n\n```python\nfrom argilla_plugins import classy_learner\n\nplugin = classy_learner(\n    name="plugin-test",\n    query=None,\n    model="all-MiniLM-L6-v2",\n    classy_config=None,\n    certainty_threshold=0,\n    overwrite_predictions=True,\n    sample_strategy="fifo",\n    min_n_samples=6,\n    max_n_samples=20,\n    batch_size=1000,\n    execution_interval_in_seconds=5,\n)\nplugin.start()\n```\n\n### Inference endpoints\n**What is it?**\nAutomatically add predictions to records as they are logged into Argilla. This can be used for making it really easy to pre-annotated a dataset with an existing model or service.\n\n- [ ] inference with un-authenticated endpoint. [issue](https://github.com/argilla-io/argilla-plugins/issues/16)\n- [ ] embed incoming records in the background. [issue](https://github.com/argilla-io/argilla-plugins/issues/18)\n\n\n### Training endpoints\n**What is it?**\nAutomatically train a model based on dataset annotations.\n\n- [ ] TBD\n\n### Suggestions\nDo you have any suggestions? Please [open an issue](https://github.com/argilla-io/argilla-plugins/issues/new/choose) 🤓\n',
    'author': 'david',
    'author_email': 'david.m.berenstein@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11.0',
}


setup(**setup_kwargs)
