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