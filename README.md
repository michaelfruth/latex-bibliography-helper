# LaTeX Bibliography Helper

`bibhelper` helps in handling bibliography for BibTeX (a bibliography manager for LaTeX). It consists of two modules:

- `find`: Lookup references and get their BibTeX entry.
- `beautify`: Beautify existing references.

`bibhelper` uses the REST-API of [dblp.org](https://dblp.org) to search for references and to get the respective BibTeX entry. Handling BibTeX within in Python is done by using the python library [BibtexParser](https://bibtexparser.readthedocs.io/en/master/). Due to a not so nice formatting in the original library when printing a multi-line string, a custom/forked version is used instead (https://github.com/michaelfruth/python-bibtexparser). Nevertheless, this tool works also perfectly with the original version, the modification just affects the formatting.

**Table of Contents**:
- [Features](#features)
- [Configuration](#configuration)
- [Getting Started](#getting-started)
- [Usage](#usage)
  - [Find](#find)
  - [Beautify](#beautify)
- [Development](#development)
- [TODOs](#todos)

## Features

- Find references and retrieve their BibTeX entry automatically.
- Uniform formatting of each BibTeX entry
    - Add additional curly brackets around titles (this is how LaTeX preserves case sensitivity)
    - Ordering of attributes (tags of an entry)
    - Automatic rewriting of the booktitle attribute
    - Hiding of attributes (hiding in the sense of LaTex will ignore these fields during processing)

Beautify example:
```
Original BibTeX entry:
@inproceedings{DBLP:conf/icde/FruthDS21,
  author    = {Michael Fruth and
               Kai Dauberschmidt and
               Stefanie Scherzinger},
  url       = {https://doi.org/10.1109/ICDE51399.2021.00306},
  title     = {Josch: Managing Schemas for NoSQL Document Stores},
  booktitle = {37th {IEEE} International Conference on Data Engineering, {ICDE} 2021,
               Chania, Greece, April 19-22, 2021},
  publisher = {{IEEE}},
  year      = {2021},
  pages     = {2693--2696},
  doi       = {10.1109/ICDE51399.2021.00306}
}

Beautified BibTeX entry (attributes are ordered):
@inproceedings{DBLP:conf/icde/FruthDS21,
    author     = {Michael Fruth and
                  Kai Dauberschmidt and
                  Stefanie Scherzinger},
    title      = {{Josch: Managing Schemas for NoSQL Document Stores}},     # <- Add another pair of curly brackets to keep upper/lower case
    booktitle  = {Proc.\ ICDE},             # <- Rewrite booktitle     
    _booktitle = {37th {IEEE} International Conference on Data Engineering, {ICDE} 2021,
                  Chania, Greece, April 19-22, 2021},
    pages      = {2693--2696},
    _publisher = {{IEEE}},                  # <- hide attributes by inserting a prefix
    year       = {2021},
    _url       = {https://doi.org/10.1109/ICDE51399.2021.00306},        # <- Order attributes
    _doi       = {10.1109/ICDE51399.2021.00306}
}
```

## Configuration
`bibhelper` *requires* a configuration file. If no configuration file can be found or loaded properly, the tool aborts. The following locations will be used to load the configuration file:
1. Command line argument `--config`
2. Environment variable: `LATEX_BIB_HELPER_CONFIG`
3. Home directory: `~/.latex_bib_helper_config.json`
4. Default file (shipped with the package): [bibhelper/resources/latex_bib_helper_config.json](bibhelper/resources/latex_bib_helper_config.json)

See Section [`--config`](#--config) for a detailed explanation of the configuration file.

## Getting Started
`bibhelper` can be installed via pip:

```shell
# Install most current version
pip install git+https://github.com/michaelfruth/latex-bibliography-helper.git#egg=bibhelper

# Install a specific version (version 1.0.0 in this example)
pip install git+https://github.com/michaelfruth/latex-bibliography-helper.git@1.0.0#egg=bibhelper
```

Once installed, `bibhelper` can be used (make sure that pip installed packages can be found in `$PATH`):
```shell
bibhelper --help
```

## Usage
See `bibhelper --help` for a full list of all arguments. Below are the most important arguments explained in more detail.

### `--config`

The tool is controlled by a configuration file. This configuration file contains (1) settings of the tool and (2) the
formatting rules of the BibTeX entries. See [bibhelper/resources/latex_bib_helper_config.json](bibhelper/resources/latex_bib_helper_config.json) for an
example configuration file. The configuration file **must** be valid against this schema: [bibhelper/resources/config.schema.json](bibhelper/resources/config.schema.json).

Example configuration file:

```json
{
  "settings": {
    "search": {
      "publicationUrl": "http://dblp.org/search/publ/api?q={}&format=json",
      "authorUrl": "http://dblp.org/search/author/api?q={}&format=json",
      "venueUrl": "http://dblp.org/search/venue/api?q={}&format=json"
    }
  },
  "style": {
    "rewriteBooktitle": {
      "rewrite": true,
      "nameWithPlaceholder": "Proc.\\ {}"
    },
    "hidePrefix": "_",
    "sort": true,
    "attributes": [
      "author",
      {
        "name": "editor",
        "hide": true
      }
    ]
  }
}
```

The `settings` section should be fixed because the functionality is specially adapadted for DBLP.

The `style` section can be customized:

#### `rewriteBooktitle`

Allows to rewrite the booktitle of a BibTeX entry. The shortname of the booktitle is extracted and replaced with a new
name, specified in `nameWithPlaceholder`. The python string method `.format(...)` is used to insert the extracted
shortname into the `nameWithPlaceholder` specified string, so `nameWithPlaceholder` must contain the placeholder `{}`.
The original booktitle is *not* deleted and will be created as hidden attribute (see [hidePrefix](#hideprefix)), the
newly created attribute will be used as the new booktitle. `rewrite` controls if rewriting should be performed.

Example:

```
"nameWithPlaceholder": "Proc.\\ {}" 
"hidePrefix": "_"

BibTeX entry:
@article{Test,
  booktitle  = {Performance Evaluation and Benchmarking for the Era of Cloud(s) -
               11th {TPC} Technology Conference, {TPCTC} 2019, Los Angeles, CA, USA,
               August 26, 2019, Revised Selected Papers}
}

After rewriting:
@article{Test,
  booktitle  = {Proc.\ TPCTC}
  _booktitle  = {Performance Evaluation and Benchmarking for the Era of Cloud(s) -
               11th {TPC} Technology Conference, {TPCTC} 2019, Los Angeles, CA, USA,
               August 26, 2019, Revised Selected Papers}
}
```

Rewriting the booktitle helps in getting a uniform layout of all BibTeX entries. Otherwise, there may be different text
of booktitles, e.g.:

```
1. Proceedings of the Sixteenth European Conference on Computer Systems, EuroSys 2017, nline Event, United Kingdom, April 26-28, 2021
2. EuroSys '21: Sixteenth European Conference on Computer Systems, Online Event, United Kingdom, April 26-28, 2021
3. 2021 Proceedings of the Sixteenth European Conference on Computer Systems(EuroSys)
```

#### `hidePrefix`

The prefix to use when an attribute should be "hidden". Hiding a attribute means, the attribute name is prefixed with
the string specified in `hidePrefix`. E.g. when `_` is used as hide prefix, LaTeX ignores all BibTeX attributes having
this prefix, resulting in "hidden" attributes (from LaTeX's point of view). Alternatively, unused attributes can also be
deleted, but then there is no possibility to view deleted attributes afterwards (apart from searching again for the
BibTeX entry). Therefore, using a prefix to hide attributes is the most flexible option.

Example:

```
"title" is used by LaTeX:
@article{Test,
  title     = {Hello World}
}

"title" is ignored by LaTeX.
@article{Test,
  _title     = {Hello World}
}
```

#### `sort`

This setting is used in conjunction with `attributes`. If set to true, the attributes of the resulting BibTeX entry are
ordered based on the order of `attributes` specified in the configuration file. All attributes that are not specified in
the configuration but exist in the BibTeX entry are appended at the *end* of the ordered attributes. When sorting,
attention is paid to hidden attributes, i.e., all attributes (hidden or not) are sorted as a group (but only attributes
having a multiple of `hidePrefix` are considered).

Example:

```
Configuration:
"hidePrefix": "_"
"sort": true
"attributes": ["author", "title"]

BibTeX entry:
@article{Test,
  title     = {Hello World},
  editor    = {Erika Mustermann},
  _title    = {hello world},
  author    = {Max Mustermann},
  -author   = {Franz Mustermann},
  __title   = {hElLo WoRlD}
}

After sorting:
@article{Test,
  author    = {Max Mustermann},
  title     = {Hello World},
  _title    = {hello world},
  __title   = {hElLo WoRlD},
  -author   = {Franz Mustermann},
  editor    = {Erika Mustermann}
}
```

All `title` attributes (`title`, `_title`, `__title`) are considered as a group, whereas `-author` is not considered as
a part of the `author` attribute as only a multiple of `hidePrefix` is allowed as prefix (and `-` is not
the `hidePrefix`).

Sorting has no benefit for the final output produced by LaTeX, nevertheless it uniforms all BibTeX entries, so that the
user can find his way around faster, which reduces the risk of errors introduced by the user (when, e.g., an attribute
has to be adapted/extended manually).

#### `attributes`

Contains the attributes in the exact order in which they should be sorted (when `sort` is enabled). The attribute can
either specified as simple string or as object (mixing styles is allowed):

```json
String:
... "attributes": ["author"] ...

Object: ... "attributes": [{"name": "author", "hide": true}] ...
```

The object declaration enables the setting whether the respective attribute should be hidden (
see [hidePrefix](#hideprefix)). Existing hidden attributes are *not* overwritten, `hidePrefix` is concatenated as long
until a non-existing hidden attribute name is found.

Example:

```
Configuration:
"hidePrefix": "_"
 "attributes": [ "author", {"name": "publisher", "hide": true}, {"name": "booktitle", "hide": true} ]

BibTeX entry:
@article{Test,
  author        = {Max Mustermann},
  publisher     = {Mustermann AG},
  booktitle     = {Book 1},
  _booktitle    = {Book 2},
  __booktitle   = {Book 3}
}

After processing:
@article{Test,
  author       = {Max Mustermann},
  _publisher   = {Mustermann AG},
  ___booktitle = {Book 1},
  _booktitle   = {Book 2},
  __booktitle  = {Book 3}
}
```

### `--pretty`

Apply all style specific settings of the configuration file (`--config`).

### --curly

Set another pair of curly brackets around the title to preserve capitalization. Example:

```
BibTeX entry:
@article{Test,
  title     = {Hello World}
}

This will produce the following output in LaTeX:
... Hello world ...
```

Capitalization is not preserved within BibTeX (e.g.
see https://tex.stackexchange.com/questions/10772/bibtex-loses-capitals-when-creating-bbl-file). This can be resolved by
adding another pair of curly brackets around the title.

```
BibTeX entry:
@article{Test,
  title     = {{Hello World}}
}

This will produce the following output in LaTeX:
... Hello World ...
```

When this option is enabled, another pair of curly brackets will be added to the title to preserve capitalization in
LaTeX.

#### `-ctc`, `--copy-to-clipboard`

Copies the final result (the BibTeX entry) into the clipboard (nevertheless, the final result is displayed on the
console).

### Find
The module `find` searches for publications by using the [dblp](https://dblp.org) REST-API. Once the publication is
found, the BibTeX entry is downloaded and shown. If more than one publication is found, all results will be displayed
and the user is able to choose one.

`find` accepts only one argument, the title of publication to search (`bibhelper Find --help` shows all
arguments).

#### Usage

Basic usage to search for a publication. The unmodified, original BibTeX entry is printed to console:

```shell
bibhelper Find <TITLE>
```

Extended usage to search for a publication. The result is copied into the clipboard (`-ctc`), the style of the
configuration file is applied (`--pretty`) and the title gets another pair of curly brackets (`--curly`):

```shell
bibhelper -ctc --pretty --curly Find <TITLE>
```

Example:

```shell
bibhelper -ctc --pretty --curly Find Tell-Tale Tail Latencies: Pitfalls and Perils in Database Benchmarking
```

---
**NOTE**

The title can be given in plain text (no quotation marks required). Quotation marks are interpreted by the shell, i.e.
if the title contains a quotation mark, the entire title may need to be quoted. Example:

```shell
# Wrong (quotation mark is interpreted by the shell):
bibhelper Find I'm a Hello World Application

# Correct:
bibhelper Find "I'm a Hello World Application"
```

---

### Beautify
The module `beautify` beautifies existing BibTeX entries. The source of the BibTeX entries can either be a BibTeX-file or the clipboard containing the content. When no argument is specified for the main module (either `--pretty` or `--curly`), the content will be parsed by BibtexParser and printed afterwards. BibtexParser may change the format of the content but should not modify the content (unless there are no BibTeX errors).

The following arguments are available (see `bibhelper Beautify --help` for a full list of all arguments):

#### `-f`, `--file`
The BibTeX file to use as input. The file is *not* modified, just the content is read.

#### `-cfc`, `--copy-from-clipboard`
Reads the content from the clipboard and uses this as input. A BibTeX-file may be copied to clipboard in this case.

#### Usage
Basic usage to beautify a BibTex file (content should not be modified unless there are no BibTeX errors):

```shell
bibhelper Beautify -f <PATH-TO-FILE>
```

Extended usage to beautify BibTeX content from the clipboard. The result is copied into the clipboard (`-ctc`), the style of the configuration file is applied (`--pretty`) and the title gets another pair of curly brackets (`--curly`):

```shell
bibhelper -ctc --pretty --curly Beautify -cfc
```

## Development
Development is done by using `pipenv` and `pyenv`.

1. `pipenv sync`
   - Creates a virtual environment and installs all required packages.
2. `pyenv install`
   - Install python version specified in [.python-version](.python-version)
3. `pipenv shell`
   - Spawns a shell within the virtual environment.
   - [.env](.env) is loaded automatically by pipenv. This file is needed to fix the `PYTHONPATH`, otherwise `import bibhelper...` throws an `ImportError`.   
4. `python bibhelper`
   - Execute `bibhelper` manually ([__main__.py](bibhelper/__main__.py) is executed automatically.).

## TODOs

- DBLP (and all other scientific databases) store the wrong paper title, i.e., capitalization of the title does not
  match exactly the paper title. We may use something like [capitalizemytitle.com](https://capitalizemytitle.com/#) to
  propose the user an alternative title.
- Change `rewrite_booktitle` of `util.py` such that it searches for the booktitle in all booktitle attributes (including hidden). Use case: The template of the booktitle is changed afterwards and a new one should be applied. 