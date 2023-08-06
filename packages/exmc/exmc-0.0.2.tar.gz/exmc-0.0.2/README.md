# Excel Markdown Converter

[![PyPI](https://img.shields.io/pypi/v/exmc.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/exmc.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/exmc)][pypi status]
[![License](https://img.shields.io/pypi/l/exmc)][license]

[![Read the documentation at https://exmc.readthedocs.io/](https://img.shields.io/readthedocs/exmc/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/idlewith/exmc/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/idlewith/exmc/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/exmc/
[read the docs]: https://exmc.readthedocs.io/
[tests]: https://github.com/idlewith/exmc/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/idlewith/exmc
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features

- copy excel content from clipboard, so you need paste excel content to clipboard
- type `exmc` to convert excel string to markdown table string
- type `exmc -r true` convert markdown table string to excel string

## Requirements

- `clipboard`

## Installation

You can install _Excel Markdown Converter_ via [pip] from [PyPI]:

```console
$ pip install exmc
```

## Usage

- `exmc`

copy content from excel sheet

type `exmc` in terminal/cmd,

then markdown table string will copy to clipboard automatically

so you can paste in markdown file

- `exmc -r true`

use `-r` flag convert markdown table string to excel string

so, you need copy raw markdown table string

then paste to excel file



## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Excel Markdown Converter_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/idlewith/exmc/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/idlewith/exmc/blob/main/LICENSE
[contributor guide]: https://github.com/idlewith/exmc/blob/main/CONTRIBUTING.md
[command-line reference]: https://exmc.readthedocs.io/en/latest/usage.html
