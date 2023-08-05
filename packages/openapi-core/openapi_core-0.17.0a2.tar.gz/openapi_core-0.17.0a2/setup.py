# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openapi_core',
 'openapi_core.casting',
 'openapi_core.casting.schemas',
 'openapi_core.contrib',
 'openapi_core.contrib.django',
 'openapi_core.contrib.falcon',
 'openapi_core.contrib.flask',
 'openapi_core.contrib.requests',
 'openapi_core.contrib.starlette',
 'openapi_core.contrib.werkzeug',
 'openapi_core.deserializing',
 'openapi_core.deserializing.media_types',
 'openapi_core.deserializing.parameters',
 'openapi_core.extensions',
 'openapi_core.extensions.models',
 'openapi_core.schema',
 'openapi_core.security',
 'openapi_core.spec',
 'openapi_core.templating',
 'openapi_core.templating.media_types',
 'openapi_core.templating.paths',
 'openapi_core.templating.responses',
 'openapi_core.templating.security',
 'openapi_core.testing',
 'openapi_core.unmarshalling',
 'openapi_core.unmarshalling.schemas',
 'openapi_core.validation',
 'openapi_core.validation.request',
 'openapi_core.validation.response']

package_data = \
{'': ['*']}

install_requires = \
['isodate',
 'jsonschema-spec>=0.1.1,<0.2.0',
 'more-itertools',
 'openapi-schema-validator>=0.3.0,<0.5',
 'openapi-spec-validator>=0.5.0,<0.6.0',
 'parse',
 'pathable>=0.4.0,<0.5.0',
 'typing-extensions>=4.3.0,<5.0.0',
 'werkzeug']

extras_require = \
{':python_version < "3.8"': ['backports-cached-property>=1.0.2,<2.0.0'],
 'django': ['django>=3.0'],
 'falcon': ['falcon>=3.0'],
 'flask': ['flask'],
 'requests': ['requests']}

setup_kwargs = {
    'name': 'openapi-core',
    'version': '0.17.0a2',
    'description': 'client-side and server-side support for the OpenAPI Specification v3',
    'long_description': '************\nopenapi-core\n************\n\n.. image:: https://img.shields.io/pypi/v/openapi-core.svg\n     :target: https://pypi.python.org/pypi/openapi-core\n.. image:: https://travis-ci.org/p1c2u/openapi-core.svg?branch=master\n     :target: https://travis-ci.org/p1c2u/openapi-core\n.. image:: https://img.shields.io/codecov/c/github/p1c2u/openapi-core/master.svg?style=flat\n     :target: https://codecov.io/github/p1c2u/openapi-core?branch=master\n.. image:: https://img.shields.io/pypi/pyversions/openapi-core.svg\n     :target: https://pypi.python.org/pypi/openapi-core\n.. image:: https://img.shields.io/pypi/format/openapi-core.svg\n     :target: https://pypi.python.org/pypi/openapi-core\n.. image:: https://img.shields.io/pypi/status/openapi-core.svg\n     :target: https://pypi.python.org/pypi/openapi-core\n\nAbout\n#####\n\nOpenapi-core is a Python library that adds client-side and server-side support\nfor the `OpenAPI v3.0 <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md>`__\nand `OpenAPI v3.1 <https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md>`__ specification.\n\nKey features\n************\n\n* **Validation** of requests and responses\n* Schema **casting** and **unmarshalling**\n* Media type and parameters **deserialization**\n* **Security** providers (API keys, Cookie, Basic and Bearer HTTP authentications)\n* Custom **deserializers** and **formats**\n* **Integration** with libraries and frameworks\n\n\nDocumentation\n#############\n\nCheck documentation to see more details about the features. All documentation is in the "docs" directory and online at `openapi-core.readthedocs.io <https://openapi-core.readthedocs.io>`__\n\n\nInstallation\n############\n\nRecommended way (via pip):\n\n::\n\n    $ pip install openapi-core\n\nAlternatively you can download the code and install from the repository:\n\n.. code-block:: bash\n\n   $ pip install -e git+https://github.com/p1c2u/openapi-core.git#egg=openapi_core\n\n\nUsage\n#####\n\nFirstly create your specification object.\n\n.. code-block:: python\n\n   from openapi_core import Spec\n\n   spec = Spec.from_file_path(\'openapi.json\')\n\nNow you can use it to validate against requests and/or responses. \n\nRequest\n*******\n\nUse ``validate_request`` function to validate request against a given spec.\n\n.. code-block:: python\n\n   from openapi_core import validate_request\n\n   # raise error if request is invalid\n   result = validate_request(request, spec=spec)\n\nRequest object should implement OpenAPI Request protocol (See `Integrations <https://openapi-core.readthedocs.io/en/latest/integrations.html>`__).\n\n(For OpenAPI v3.1) Use the same function to validate webhook request against a given spec.\n\n.. code-block:: python\n\n   # raise error if request is invalid\n   result = validate_request(webhook_request, spec=spec)\n\nWebhook request object should implement OpenAPI WebhookRequest protocol (See `Integrations <https://openapi-core.readthedocs.io/en/latest/integrations.html>`__).\n\nRetrieve request data from validation result\n\n.. code-block:: python\n\n   # get parameters object with path, query, cookies and headers parameters\n   validated_params = result.parameters\n   # or specific parameters\n   validated_path_params = result.parameters.path\n\n   # get body\n   validated_body = result.body\n\n   # get security data\n   validated_security = result.security\n\nResponse\n********\n\nUse ``validate_response`` function to validate response against a given spec.\n\n.. code-block:: python\n\n   from openapi_core import validate_response\n\n   # raise error if response is invalid\n   result = validate_response(request, response, spec=spec)\n\nResponse object should implement OpenAPI Response protocol (See `Integrations <https://openapi-core.readthedocs.io/en/latest/integrations.html>`__).\n\n(For OpenAPI v3.1) Use the same function to validate response from webhook request against a given spec.\n\n.. code-block:: python\n\n   # raise error if request is invalid\n   result = validate_response(webhook_request, response, spec=spec)\n\nRetrieve response data from validation result\n\n.. code-block:: python\n\n   # get headers\n   validated_headers = result.headers\n\n   # get data\n   validated_data = result.data\n\nIn order to explicitly validate a:\n\n* OpenAPI 3.0 spec, import ``V30RequestValidator`` or ``V30ResponseValidator`` \n* OpenAPI 3.1 spec, import ``V31RequestValidator`` or ``V31ResponseValidator`` or ``V31WebhookRequestValidator`` or ``V31WebhookResponseValidator`` \n\n.. code:: python\n\n   from openapi_core import V31ResponseValidator\n\n   result = validate_response(request, response, spec=spec, cls=V31ResponseValidator)\n\nYou can also explicitly import ``V3RequestValidator`` or ``V3ResponseValidator``  which is a shortcut to the latest v3 release.\n\nRelated projects\n################\n* `bottle-openapi-3 <https://github.com/cope-systems/bottle-openapi-3>`__\n   OpenAPI 3.0 Support for the Bottle Web Framework\n* `openapi-spec-validator <https://github.com/p1c2u/openapi-spec-validator>`__\n   Python library that validates OpenAPI Specs against the OpenAPI 2.0 (aka Swagger) and OpenAPI 3.0 specification\n* `openapi-schema-validator <https://github.com/p1c2u/openapi-schema-validator>`__\n   Python library that validates schema against the OpenAPI Schema Specification v3.0.\n* `pyramid_openapi3 <https://github.com/niteoweb/pyramid_openapi3>`__\n   Pyramid addon for OpenAPI3 validation of requests and responses.\n* `tornado-openapi3 <https://github.com/correl/tornado-openapi3>`__\n   Tornado OpenAPI 3 request and response validation library.\n',
    'author': 'Artur Maciag',
    'author_email': 'maciag.artur@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/p1c2u/openapi-core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
