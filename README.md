# LaTex Bibliography Helper
This tool helps in handling bibliography for BibTeX (a bibliography manager for LaTeX). It consists of two modules: 
- **find**: Lookup references and get their BibTeX entry by using the [dblp](https://dblp.org) API.
- **beautify**: Beautify existing references.

## Features
- Find references and retrieve their BibTeX entry automatically.
- Uniform formatting of each BibTeX entry
  - Add additional curly brackets around titles (this is how LaTeX preserves case sensitivity)
  - Ordering of attributes (tags of an entry)
  - Automatic rewriting of the booktitle attribute
  - Hiding of attributes (hiding in the sense of LaTex will ignore these fields during processing)

### Find


#### Usage

### Beautify

#### Usage

## TODOs
- DBLP (and all other scientific databases) store the wrong paper title, i.e.,  capitalization of the title does not match exactly the paper title. We may use something like [capitalizemytitle.com](https://capitalizemytitle.com/#) to propose the user an alternative title.