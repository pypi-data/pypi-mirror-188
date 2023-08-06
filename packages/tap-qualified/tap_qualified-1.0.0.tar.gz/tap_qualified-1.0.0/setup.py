# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_qualified', 'tap_qualified.tests']

package_data = \
{'': ['*'], 'tap_qualified': ['schemas/*']}

install_requires = \
['requests>=2.28.1', 'singer-sdk>=0.19.0,<1']

extras_require = \
{'s3': ['fs-s3fs>=1.1.1']}

entry_points = \
{'console_scripts': ['tap-qualified = tap_qualified.tap:TapQualified.cli']}

setup_kwargs = {
    'name': 'tap-qualified',
    'version': '1.0.0',
    'description': '`tap-qualified` is a Singer tap for Qualified, built with the Meltano Singer SDK.',
    'long_description': "# tap-qualified\n\n`tap-qualified` is a Singer tap for [Qualified](https://www.qualified.com/).\n\nQualified helps companies generate pipeline, faster. Tap into your greatest asset - your website - to identify your most valuable visitors, instantly start sales conversations, schedule  meetings, convert outbound and paid traffic, and uncover signals of buying intent.\n\nInstall from PyPi:\n\n```bash\npipx install tap-qualified\n```\n\n## Configuration\n\n### Accepted Config Options\n\n| Setting             | Required | Default | Description |\n|:--------------------|:--------:|:-------:|:------------|\n| api_key             | True     | None    | The token to authenticate against the API service |\n| user_agent          | False    | Harness.io/Tap Qualified | The user agent to use when making requests to the API service |\n| stream_maps         | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |\n| stream_map_config   | False    | None    | User-defined config values to be used within map expressions. |\n| flattening_enabled  | False    | None    | 'True' to enable schema flattening and automatically expand nested properties. |\n| flattening_max_depth| False    | None    | The max depth to flatten schemas. |\n\nA full list of supported settings and capabilities for this\ntap is available by running:\n\n```bash\ntap-qualified --about\n```\n\n### Configure using environment variables\n\nThis Singer tap will automatically import any environment variables within the working directory's\n`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching\nenvironment variable is set either in the terminal context or in the `.env` file.\n\n### Source Authentication and Authorization\n\nReach out to your account executive to inquire about API access.\n\n## Usage\n\nYou can easily run `tap-qualified` by itself or in a pipeline using [Meltano](https://meltano.com/).\n\n### Executing the Tap Directly\n\n```bash\ntap-qualified --version\ntap-qualified --help\ntap-qualified --config CONFIG --discover > ./catalog.json\n```\n\n## Developer Resources\n\nFollow these instructions to contribute to this project.\n\n### Initialize your Development Environment\n\n```bash\npipx install poetry\npoetry install\n```\n\n### Create and Run Tests\n\nCreate tests within the `tap_qualified/tests` subfolder and\n  then run:\n\n```bash\npoetry run pytest\n```\n\nYou can also test the `tap-qualified` CLI interface directly using `poetry run`:\n\n```bash\npoetry run tap-qualified --help\n```\n\n### Testing with [Meltano](https://www.meltano.com)\n\n_**Note:** This tap will work in any Singer environment and does not require Meltano.\nExamples here are for convenience and to streamline end-to-end orchestration scenarios._\n\n\nNext, install Meltano (if you haven't already) and any needed plugins:\n\n```bash\n# Install meltano\npipx install meltano\n# Initialize meltano within this directory\ncd tap-qualified\nmeltano install\n```\n\nNow you can test and orchestrate using Meltano:\n\n```bash\n# Test invocation:\nmeltano invoke tap-qualified --version\n# OR run a test `elt` pipeline:\nmeltano elt tap-qualified target-jsonl\n```\n\n### SDK Dev Guide\n\nSee the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to\ndevelop your own taps and targets.\n\nBuilt with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.\n",
    'author': 'Alex Butler',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/z3z1ma/tap-qualified',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
