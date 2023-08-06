# snapspam [![Docs Badge]](https://snapspam.readthedocs.io/en/stable/) [![Python Badge]](https://pypi.org/project/snapspam/)

Spam sendit, LMK, or NGL messages.

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://shell.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/MysteryBlokHed/snapspam.git)

## Installation

You can use snapspam without installing it, but installing it
will allow you to run it anywhere.

### From PyPI

To install from PyPI, [pipx](https://pypi.org/project/pipx/) is recommended.
With it installed, run:

```sh
pipx install snapspam
```

To just use pip, run:

```sh
pip install snapspam
```

### From Cloned Repository

```sh
python setup.py install
```

## Use

To get help from the CLI, run:

```sh
snapspam --help
```

or

```sh
python snapspam.py --help
```

Some information about how to use the app will be returned.

To get help for a specific target app (eg. sendit), run:

```sh
snapspam sendit --help
```

or

```sh
python snapspam.py sendit --help
```

Here's an example usage of the app to spam a sendit sticker:

```sh
snapspam sendit cd06ec9a-2879-1afa-5108-fed08b1ecaa0 'Spammed'
```

The ID can also be replaced by the full URL, like this:

```sh
snapspam sendit https://web.getsendit.com/s/cd06ec9a-2879-1afa-5108-fed08b1ecaa0 'Spammed'
```

## Documentation

Documentation of the CLI is contained in the help menu.
Library documentation is hosted on [Read the Docs].

## License

snapspam is licensed under the GNU General Public License, Version 3.0
([LICENSE](LICENSE) or <https://www.gnu.org/licenses/gpl-3.0.en.html>).

[docs badge]: https://readthedocs.org/projects/snapspam/badge/?version=latest
[python badge]: https://img.shields.io/pypi/pyversions/snapspam
[read the docs]: https://snapspam.readthedocs.io/en/stable/
