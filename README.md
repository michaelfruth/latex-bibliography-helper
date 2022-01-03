# LaTex Bibliography Helper
This tool helps in handling bibliography for BibTeX (a bibliography manager for LaTeX). It consists of two modules: 
- `find`: Lookup references and get their BibTeX entry by using the [dblp](https://dblp.org) REST-API.
- `beautify`: Beautify existing references.

## Features
- Find references and retrieve their BibTeX entry automatically.
- Uniform formatting of each BibTeX entry
  - Add additional curly brackets around titles (this is how LaTeX preserves case sensitivity)
  - Ordering of attributes (tags of an entry)
  - Automatic rewriting of the booktitle attribute
  - Hiding of attributes (hiding in the sense of LaTex will ignore these fields during processing)

## Usage
The entrypoint of this tool is the python module `latex_bib_helper.py`, from which the `find` and `beautify` module can be executed. `latex_bib_helper.py` supports several options, which will influence the behaviour to the respective module.

See `latex_bib_helper.py --help` for a full list of all arguments. Below are the most important arguments explained in more detail.

### `--config`
The tool is controlled by a configuration file. This configuration file contains (1) settings of the tool and (2) the formatting rules of the BibTeX entries. See [example-config.json](latex_bibliography_helper/example-config.json) for an example configuration file.

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
Allows to rewrite the booktitle of a BibTeX entry. The shortname of the booktitle is extracted and replaced with a new name, specified in `nameWithPlaceholder`. The python string method `.format(...)` is used to insert the extracted shortname into the `nameWithPlaceholder` specified string, so `nameWithPlaceholder` must contain the placeholder `{}`. The original booktitle is *not* deleted and will be created as hidden attribute (see [hidePrefix](#hideprefix)), the newly created attribute will be used as the new booktitle. `rewrite` controls if rewriting should be performed. 

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

Rewriting the booktitle helps in getting a uniform layout of all BibTeX entries. Otherwise, there may be different text of booktitles, e.g.:
```
1. Proceedings of the Sixteenth European Conference on Computer Systems, EuroSys 2017, nline Event, United Kingdom, April 26-28, 2021
2. EuroSys '21: Sixteenth European Conference on Computer Systems, Online Event, United Kingdom, April 26-28, 2021
3. 2021 Proceedings of the Sixteenth European Conference on Computer Systems(EuroSys)
```

#### `hidePrefix`
The prefix to use when an attribute should be "hidden". Hiding a attribute means, the attribute name is prefixed with the string specified in `hidePrefix`. E.g. when `_` is used as hide prefix, LaTeX ignores all BibTeX attributes having this prefix, resulting in "hidden" attributes (from LaTeX's point of view). Alternatively, unused attributes can also be deleted, but then there is no possibility to view deleted attributes afterwards (apart from searching again for the BibTeX entry). Therefore, using a prefix to hide attributes is the most flexible option.

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
This setting is used in conjunction with `attributes`. If set to true, the attributes of the resulting BibTeX entry are ordered based on the order of `attributes` specified in the configuration file. All attributes that are not specified in the configuration but exist in the BibTeX entry are appended at the *end* of the ordered attributes. When sorting, attention is paid to hidden attributes, i.e., all attributes (hidden or not) are sorted as a group (but only attributes having a multiple of `hidePrefix` are considered).

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
All `title` attributes (`title`, `_title`, `__title`) are considered as a group, whereas `-author` is not considered as a part of the `author` attribute as only a multiple of `hidePrefix` is allowed as prefix (and `-` is not the `hidePrefix`).  

Sorting has no benefit for the final output produced by LaTeX, nevertheless it uniforms all BibTeX entries, so that the user can find his way around faster, which reduces the risk of errors introduced by the user (when, e.g., an attribute has to be adapted/extended manually).

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
Capitalization is not preserved within BibTeX (e.g. see https://tex.stackexchange.com/questions/10772/bibtex-loses-capitals-when-creating-bbl-file). This can be resolved by adding another pair of curly brackets around the title.

```
BibTeX entry:
@article{Test,
  title     = {{Hello World}}
}

This will produce the following output in LaTeX:
... Hello World ...
```

When this option is enabled, another pair of curly brackets will be added to the title to preserve capitalization in LaTeX.


### Find
The module `find` searches for publications by using the [dblp](https://dblp.org) REST-API. Once the publication is found, the BibTeX entry is downloaded and shown. If more than one publication is found, all results will be displayed and the user is able to choose one.

#### Usage

### Beautify

#### Usage

## TODOs
- DBLP (and all other scientific databases) store the wrong paper title, i.e.,  capitalization of the title does not match exactly the paper title. We may use something like [capitalizemytitle.com](https://capitalizemytitle.com/#) to propose the user an alternative title.