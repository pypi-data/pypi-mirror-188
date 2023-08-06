# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tail_jsonl', 'tail_jsonl._private']

package_data = \
{'': ['*']}

install_requires = \
['calcipy>=0.21.3', 'rich>=13.3.1']

entry_points = \
{'console_scripts': ['tail-jsonl = tail_jsonl:main']}

setup_kwargs = {
    'name': 'tail-jsonl',
    'version': '0.0.1',
    'description': 'Tail JSONL Logs',
    'long_description': '# tail-jsonl\n\nTail JSONL Logs\n\n## Background\n\nI wanted to find a tool that could:\n\n1. Convert a stream of JSONL logs into a readable `logfmt`-like output with minimal configuration\n1. Show exceptions on their own line\n\nI investigated a lot of alternatives such as: [humanlog](https://github.com/humanlogio/humanlog), [lnav](https://docs.lnav.org/en/latest/formats.html#), [goaccess](https://goaccess.io/get-started), [angle-grinder](https://github.com/rcoh/angle-grinder#rendering), [jq](https://github.com/stedolan/jq), [textualog](https://github.com/rhuygen/textualog), etc. but None had the exception formatting I wanted.\n\n## Installation\n\n```sh\npipx install tail-jsonl\n```\n\n## Usage\n\n```sh\necho \'{"message": "message", "timestamp": "2023-01-01T01:01:01.0123456Z", "level": "debug", "data": true, "more-data": [null, true, -123.123]}\' | tail-jsonl\n```\n\n## Project Status\n\nSee the `Open Issues` and/or the [CODE_TAG_SUMMARY]. For release history, see the [CHANGELOG].\n\n## Contributing\n\nWe welcome pull requests! For your pull request to be accepted smoothly, we suggest that you first open a GitHub issue to discuss your idea. For resources on getting started with the code base, see the below documentation:\n\n- [DEVELOPER_GUIDE]\n- [STYLE_GUIDE]\n\n## Code of Conduct\n\nWe follow the [Contributor Covenant Code of Conduct][contributor-covenant].\n\n### Open Source Status\n\nWe try to reasonably meet most aspects of the "OpenSSF scorecard" from [Open Source Insights](https://deps.dev/pypi/tail_jsonl)\n\n## Responsible Disclosure\n\nIf you have any security issue to report, please contact the project maintainers privately. You can reach us at [dev.act.kyle@gmail.com](mailto:dev.act.kyle@gmail.com).\n\n## License\n\n[LICENSE]\n\n[changelog]: ./docs/CHANGELOG.md\n[code_tag_summary]: ./docs/CODE_TAG_SUMMARY.md\n[contributor-covenant]: https://www.contributor-covenant.org\n[developer_guide]: ./docs/DEVELOPER_GUIDE.md\n[license]: https://github.com/kyleking/tail-jsonl/LICENSE\n[style_guide]: ./docs/STYLE_GUIDE.md\n',
    'author': 'Kyle King',
    'author_email': 'dev.act.kyle@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyleking/tail-jsonl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.12,<4.0.0',
}


setup(**setup_kwargs)
