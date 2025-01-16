<p align="center">
<a href="https://github.com/showyourwork/showyourwork">
<img width = "450" src="https://raw.githubusercontent.com/showyourwork/.github/main/images/showyourwork.png" alt="showyourwork"/>
</a>
<br>
<br>
<a href="https://github.com/HealthyPear/reproducible-fermi-lat/actions/workflows/build.yml">
<img src="https://github.com/HealthyPear/reproducible-fermi-lat/actions/workflows/build.yml/badge.svg?branch=main" alt="Article status"/>
</a>
<a href="https://github.com/HealthyPear/reproducible-fermi-lat/raw/main-pdf/arxiv.tar.gz">
<img src="https://img.shields.io/badge/article-tarball-blue.svg?style=flat" alt="Article tarball"/>
</a>
<a href="https://github.com/HealthyPear/reproducible-fermi-lat/raw/main-pdf/ms.pdf">
<img src="https://img.shields.io/badge/article-pdf-blue.svg?style=flat" alt="Read the article"/>
</a>
</p>

An open source scientific article created using the [showyourwork](https://github.com/showyourwork/showyourwork) workflow.

# Requirements

The only requirement is the Python package [showyourwork](https://show-your.work/en/latest/) and *git*.

> [!IMPORTANT]
> The package is stable but still under development.
> Depending when your cloned this repository, if you encounter some issue
> try to install it from the latest commit on the stable branch with,
> `pip install git+https://github.com/showyourwork/showyourwork.git`

How and where to install it will depend on your preferences, e.g.:

- use only your Python3 installation and the [`venv` Standard Library module](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments)
- use [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

Please, check [showyourwork docs](https://show-your.work/en/latest/) and its repository for
documentation and help on any issue with it.

*showyourwork* uses [snakemake v7.15.2](https://snakemake.readthedocs.io/en/v7.15.2/) for defining
a workflow.

# How to start a new project

You can start a new project by using this repository as a template.

Using the web page, click on the green button "Use this template" and then
"Create a new repository".

See [GitHub Docs](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
for more details.

# How to reproduce results based on this template

After installing *showyourwork*, clone this repository with *git*,

`git clone https://github.com/YourUser/YourProjectName`

Enter in the new directory and run `showyourwork build`.

## Special requirements

*showyourwork* uses [tectonic](https://tectonic-typesetting.github.io/en-US/) as its typesetting system.

Currently *tectonic* uses a relatively old version of *biblatex*.
If you need [biber](https://ctan.org/pkg/biber) to manage your bibliography, for the moment you have to use
*biber v2.17*.

On macos you can install it with [Homebrew](https://brew.sh/)

`brew install dgfl-gh/taps/biber@2.17`