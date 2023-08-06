# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flet_mvp_utils']

package_data = \
{'': ['*']}

install_requires = \
['flet>=0.3.2,<0.4.0', 'pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'flet-mvp-utils',
    'version': '0.3.2',
    'description': 'Tools to build flet apps with the MVP architecture pattern',
    'long_description': "# flet-mvp-utils\n\nWIP, not complete!\n\nThis library provides tools that make it a bit easier\nto follow architecture patterns in your flet app\nthat leverage on immutable models and unidirectional control flow.\nThose are mostly based on the Model-View-Presenter/MVP pattern,\nhence the name of the library.\nAt this stage,\nit can be used to ease working with any model-based architecture pattern though.\n\n## Usage\n\nSay you have a form and want to validate the TextFields in it\nwhen a submit button is clicked.\n\nYour view uses [refs](https://flet.dev/docs/guides/python/control-refs/).\nThe actual UI code may be located somewhere else\nand simply receive the refs and return a component that is connected to the ref.\nWhen creating the view class, you inherit from `MvpView`\nand in your `__init__.py`, you create a dictionary that maps the attribute names\nof your model to the respective ref\nof the control that should be tied to it.\nYou then pass this dictionary to `super().__init__()`,\nalong with any variable intended for the `flet.View` constructor.\n\n```python\n```\n\n`MvpView` has a `render(model)` method that takes a model\nand updates any refs current value to the model value if they aren't the same.\nThis method is supposed to be called in the callback\nyou register with the data source,\nso that a changed model is immediately reflected in the view.\n\nYour model inherits from `MvpModel`,\nwhich is an immutable pydantic BaseModel.\nThis means you can write custom validators for each attribute\nand validate all your data whenever a new instance of the model is created.\n\n```python\nclass FormModel(MvpModel):\n    number: int = 0\n```\n\nThe business logic of your component/virtual page\nwill live in a DataSource class which inherits from `MvpDataSource`.\nSince the latter inherits from `Observable`,\nbrokers of any kind (presenter classes in MVP-based architectures)\ncan register callback functions with your DataSource class\nthat will be executed when you call `self.notify_observers()` in it.\n\nThis is meant to be used to inform the presenter that a new,\nupdated model has been created.\nSince creating and updating a model is a rather repetitive and uniform task,\n`MvpDataSource` will do it for you.\nAll you have to do is pass your model class to its constructor\nand call `self.update_model_partial(changes: dict)`\nor `self.update_model_complete(new_model: dict)` depending on your use case.\n",
    'author': 'iron3oxide',
    'author_email': 'jason.hottelet@tuta.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
