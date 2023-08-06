# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['permission_rules', 'permission_rules.migrations', 'permission_rules.services']

package_data = \
{'': ['*']}

install_requires = \
['django-json-widget>=1.1.1',
 'django-model-utils>=4.1.1',
 'django>=3.1.6',
 'djangorestframework>=3.12.2',
 'drf-access-policy>=0.8.7',
 'drf-yasg[validation]==1.20.0',
 'redis']

setup_kwargs = {
    'name': 'drf-permission-rules',
    'version': '0.4.2',
    'description': "Declarative access policies/permissions modeled after AWS' IAM policies.",
    'long_description': '# drf-permission-rules\npermission rules for DRF base on drf access policy\n\n## Usage\n\n### ViewSet permissions\n```\nclass UserViewSet(ModelViewSet, PermissionsActionMixin):\n    ...\n\n    @action(methods=["GET", "POST"], detail=False)\n    def some_action(self, request, *args, **kwargs):\n        ...\n\n\nGET /api/users/permissions\nResponse:\n{\n    "create": true,\n    "list": true,\n    "some_action": false\n}\n```\n\n### Multiple ViewSet permissions\n\n```\n# views.py\nclass UserViewSet(ModelViewSet, PermissionsActionMixin):\n    ...\n\nclass BookViewSet(ModelViewSet, PermissionsActionMixin):\n    ...\n\nclass AuthorViewSet(ModelViewSet, PermissionsActionMixin):\n    ...\n\n\n# urls.py\nurlpatterns = [\n    ...\n    path("api/", include("permission_rules.urls")),\n]\n\n\nGET /api/users/permissions\nResponse:\n{\n    "User": {\n        "create": true\n        "list": true,\n        "some_action": false\n    }\n    "Book": {\n        "create": true,\n        "list": true\n    },\n    "Author": {\n        "create": false,\n        "list": true\n    }\n}\n```\n\n\n## Speedup\n\nYou can get permissions from a file instead of a database.\n\n```\n# settings.py\n\n\nPERMISSION_RULES_SETTINGS = {\n    "use_file_instead_db": true,\n    "permission_rules_file_path": "/path/to/permissions.json"\n}\n```\n',
    'author': 'Pavel Maltsev',
    'author_email': 'pavel@speechki.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/speechki-book/drf-permission-rules',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
