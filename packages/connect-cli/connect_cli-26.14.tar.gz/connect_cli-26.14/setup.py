# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['connect',
 'connect..data.connect_reports.reports',
 'connect..data.connect_reports.reports.billing_requests',
 'connect..data.connect_reports.reports.billing_requests_line_item',
 'connect..data.connect_reports.reports.contract_list',
 'connect..data.connect_reports.reports.customers_list',
 'connect..data.connect_reports.reports.executive_fullfilment_requests',
 'connect..data.connect_reports.reports.fulfillment_requests',
 'connect..data.connect_reports.reports.fulfillment_requests_failed',
 'connect..data.connect_reports.reports.fulfillment_requests_line_item',
 'connect..data.connect_reports.reports.helpdesk',
 'connect..data.connect_reports.reports.listing_list',
 'connect..data.connect_reports.reports.listing_requests',
 'connect..data.connect_reports.reports.products_catalog',
 'connect..data.connect_reports.reports.sla',
 'connect..data.connect_reports.reports.subscription_list',
 'connect..data.connect_reports.reports.tier_configuration_list',
 'connect..data.connect_reports.reports.tier_configuration_requests',
 'connect..data.connect_reports.reports.usage_in_subscription',
 'connect.cli',
 'connect.cli.core',
 'connect.cli.core.account',
 'connect.cli.plugins',
 'connect.cli.plugins.customer',
 'connect.cli.plugins.locale',
 'connect.cli.plugins.play',
 'connect.cli.plugins.product',
 'connect.cli.plugins.product.sync',
 'connect.cli.plugins.project',
 'connect.cli.plugins.project.extension',
 'connect.cli.plugins.project.report',
 'connect.cli.plugins.report',
 'connect.cli.plugins.shared',
 'connect.cli.plugins.translation']

package_data = \
{'': ['*'],
 'connect': ['.data/connect_reports/*',
             '.data/connect_reports/.github/workflows/*'],
 'connect..data.connect_reports.reports.billing_requests': ['templates/xlsx/*'],
 'connect..data.connect_reports.reports.billing_requests_line_item': ['templates/xlsx/*'],
 'connect..data.connect_reports.reports.contract_list': ['templates/xlsx/*'],
 'connect..data.connect_reports.reports.customers_list': ['templates/xlsx/*'],
 'connect..data.connect_reports.reports.executive_fullfilment_requests': ['templates/pdf/*',
                                                                          'templates/pdf/img/*'],
 'connect..data.connect_reports.reports.fulfillment_requests': ['templates/xlsx/*'],
 'connect..data.connect_reports.reports.fulfillment_requests_failed': ['templates/xlsx/*'],
 'connect..data.connect_reports.reports.fulfillment_requests_line_item': ['templates/xlsx/*'],
 'connect..data.connect_reports.reports.helpdesk': ['templates/xlsx/*'],
 'connect..data.connect_reports.reports.listing_list': ['templates/xlsx/*'],
 'connect..data.connect_reports.reports.listing_requests': ['templates/xlsx/*'],
 'connect..data.connect_reports.reports.products_catalog': ['templates/pdf/*',
                                                            'templates/pdf/assets/*',
                                                            'templates/pdf/img/*'],
 'connect..data.connect_reports.reports.sla': ['templates/xlsx/*'],
 'connect..data.connect_reports.reports.subscription_list': ['templates/xlsx/*'],
 'connect..data.connect_reports.reports.tier_configuration_list': ['templates/xlsx/*'],
 'connect..data.connect_reports.reports.tier_configuration_requests': ['templates/xlsx/*'],
 'connect..data.connect_reports.reports.usage_in_subscription': ['templates/xlsx/*'],
 'connect.cli.plugins.project.extension': ['templates/bootstrap/${project_slug}/${package_name}/*',
                                           'templates/bootstrap/${project_slug}/${package_name}/static/*',
                                           'templates/bootstrap/${project_slug}/*',
                                           'templates/bootstrap/${project_slug}/.github/workflows/*',
                                           'templates/bootstrap/${project_slug}/__mocks__/*',
                                           'templates/bootstrap/${project_slug}/tests/*',
                                           'templates/bootstrap/${project_slug}/ui/images/*',
                                           'templates/bootstrap/${project_slug}/ui/pages/*',
                                           'templates/bootstrap/${project_slug}/ui/src/*',
                                           'templates/bootstrap/${project_slug}/ui/src/pages/*',
                                           'templates/bootstrap/${project_slug}/ui/styles/*',
                                           'templates/bootstrap/${project_slug}/ui/tests/*'],
 'connect.cli.plugins.project.report': ['templates/add/${initial_report_slug}/*',
                                        'templates/add/${initial_report_slug}/templates/pdf/*',
                                        'templates/add/${initial_report_slug}/templates/xml/*',
                                        'templates/bootstrap/${project_slug}/${package_name}/${initial_report_slug}/*',
                                        'templates/bootstrap/${project_slug}/${package_name}/${initial_report_slug}/templates/pdf/*',
                                        'templates/bootstrap/${project_slug}/${package_name}/${initial_report_slug}/templates/xml/*',
                                        'templates/bootstrap/${project_slug}/*',
                                        'templates/bootstrap/${project_slug}/.github/workflows/*',
                                        'templates/bootstrap/${project_slug}/tests/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'connect-eaas-core>=26.13,<27',
 'connect-markdown-renderer>=2.0.1,<3',
 'connect-openapi-client>=25.15',
 'connect-reports-core>=26.0.0,<27.0.0',
 'fs>=2.4.12,<3.0.0',
 'interrogatio>=2.3.1,<3.0.0',
 'iso3166>=1.0.1,<2.0.0',
 'jinja2-time>=0.2.0,<0.3.0',
 'openpyxl>=3.0.7,<4.0.0',
 'phonenumbers>=8.12.19,<9.0.0',
 'poetry-core>=1.3.0,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=12.4.1,<13.0.0',
 'toml>=0.10.2,<0.11.0']

extras_require = \
{':sys_platform == "linux" or sys_platform == "darwin"': ['uvloop>=0.16.0,<0.17.0']}

entry_points = \
{'connect.cli.plugins': ['customer = '
                         'connect.cli.plugins.customer.commands:get_group',
                         'locales = '
                         'connect.cli.plugins.locale.commands:get_group',
                         'play = connect.cli.plugins.play.commands:get_group',
                         'product = '
                         'connect.cli.plugins.product.commands:get_group',
                         'project = '
                         'connect.cli.plugins.project.commands:get_group',
                         'report = '
                         'connect.cli.plugins.report.commands:get_group',
                         'translation = '
                         'connect.cli.plugins.translation.commands:get_group'],
 'console_scripts': ['ccli = connect.cli.ccli:main']}

setup_kwargs = {
    'name': 'connect-cli',
    'version': '26.14',
    'description': 'CloudBlue Connect Command Line Interface',
    'long_description': '# CloudBlue Connect Command Line Interface\n\n![pyversions](https://img.shields.io/pypi/pyversions/connect-cli.svg) [![PyPi Status](https://img.shields.io/pypi/v/connect-cli.svg)](https://pypi.org/project/connect-cli/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/connect-cli) ![Docker Pulls](https://img.shields.io/docker/pulls/cloudblueconnect/connect-cli) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/cloudblue/connect-cli/Build%20Connect%20Command%20Line%20Client) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=connect-cli&metric=coverage)](https://sonarcloud.io/summary/new_code?id=connect-cli) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=connect-cli&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=connect-cli)\n\n## Introduction\n\nThe CloudBlue Connect Command Line Interface (CLI) is an extensible unified tool to perform various automation scenarios. With just one tool, you can control multiple Connect modules from the command line and automate them through scripts.\n\nSince it is extensible, users can write their own plugins to extend its functionalities.\n\n\n## Install\n\n### Prerequisites\n\n`connect-cli` depends on [Git](https://git-scm.com/), [Cairo](https://www.cairographics.org/),\n[Pango](https://pango.gnome.org/) and [GDK-PixBuf](https://developer.gnome.org/gdk-pixbuf/stable/).\n\nPlease refers to the platform-specific instructions on how to install these dependecies:\n\n* [Linux](docs/linux_deps_install.md)\n* [Mac OS](docs/osx_deps_install.md)\n* [Windows](docs/win_deps_install.md)\n\n\n### Using PIP\n\nTo use `connect-cli` you need a system with python 3.8 or later installed.\n\n```sh\n    $ pip install --upgrade connect-cli\n```\n\n### Using Docker\n\nTo use the Docker image of `connect-cli`:\n\n```sh\n    $ docker run -it -v $HOME/.ccli:/home/connect/.ccli cloudblueconnect/connect-cli ccli\n```\n\nPlease refer to the [`connect-cli` docker image documentation](https://hub.docker.com/r/cloudblueconnect/connect-cli) for more information.\n\n\n### Using Homebrew on Mac OS\n\nTo install `connect-cli` with homebrew run:\n\n```sh\n    $ brew update\n    $ brew tap cloudblue/connect\n    $ brew install cloudblue/connect/connect-cli\n```\n\n### Using the installer on Windows\n\nAn installer package is available for Windows 10 or newer.\nYou can download its zip file from the [Github Releases](https://github.com/cloudblue/connect-cli/releases) page.\n\n\n\n## Usage\n\n* [General](docs/core_usage.md)\n* [Locales](docs/locales_usage.md)\n* [Products](docs/products_usage.md)\n* [Customers](docs/customers_usage.md)\n* [Reports](docs/reports_usage.md)\n* [Translations](docs/translations_usage.md)\n* [Projects](docs/project_usage.md)\n\n\n## Run tests\n\n`connect-cli` uses [poetry](https://python-poetry.org/) for dependencies management and packaging.\n\nTo run the `connect-cli` tests suite run:\n\n```\n$ pip install poetry\n$ poetry install\n$ poetry run pytest\n```\n\n\n## License\n\n`connect-cli` is released under the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).\n',
    'author': 'CloudBlue LLC',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://connect.cloudblue.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
