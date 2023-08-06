# mkdocs-tex2svg

## :warning: Warning :warning:

* **THIS MKDOCS EXTENSION IS NOW OPERATIONAL (!!)**
* <img src="./workInProgress.gif" style="width:5%;"> **NEVERTHELESS, THIS MDKOCS DOCUMENTATION is a Work in Progress Mode** <img src="./workInProgress.gif" style="width:5%;">

State of the Art : **[TKZ-TAB](https://ctan.org/pkg/tkz-tab)** SNIPPETS (for **Maths Variation Tables**) are being correctly rendered as Base64 SVGs, both for Light and Dark Modes.

## What is mkdocs-tex2svg ?

**mkdocs-tex2svg** is a configurable **Python Markdown extension for Mkdocs**, that renders **inline** LaTeX Snippets (within Single $\$...\$ $) or **block** LaTeX Formulas (within Double dollars $\$\$...\$\$ $), **customised with any extra LaTeX packages**, to base64 SVGs out of the box ! 

In particular, **mkdocs-tex2svg** renders Mathematic Variation Tables to Base64 SVGs, via the [tkz-tab](https://ctan.org/pkg/tkz-tab) syntax, natively compatible with mkdocs-material Light and Dark Themes.

But **mkdocs-tex2svg** can more generally convert in real time **any LaTeX snippet**, using any extra LaTeX package, to base64 SVGs (work in progress)

## LaTeX Prerequisites

Note that **a comprehensive LaTeX distribution must be installed on the server** (or locally for debugging) for this extension to work with **mkdocs**, and hence draw maths variation tables.  
More precisely, for this extension to work on GitLab/Github Pages, the `texlive-most` pasckage **MUST** be installed :

Install `texlive-most`, on Manjaro/Archlinux with :

`$ sudo pacman -S texlive-most`

FYI, This package texlive-most provides:

* the `pdflatex` command
* the `pdfcrop` command
* all additional but nonetheless required latex packages, as **tkiz** and **tikz-tab**


## Other Dependencies

The **pdf2svg** package **MUST** also be installed (to be able to use the `pdf2svg` command)

For Example for Manjaro/Archlinux :

`$ sudo pacman -S pdf2svg`

LaTeX Snippets are made in a LaTeX block called **mathtable** (directly in your markdown file) :

* **mkdocs-tex2svg** adapts natively to Mkdocs's **Light and Dark themes**
* **mkdocs-tex2svg** supports native **HTML color Names** AND **HTML Hexa Color codes**
* **mkdocs-tex2svg** colors are **configurable via options** in the `mkdocs.yml` config file.  

Different colors can be easily set for :

* **Borders and Texts** of Variation Tables
* **Backgrounds for Labels** inside Variation Tables, 
* Different colors for Mkdocs's **Light** & **Dark Themes** can be set

# mkdocs-tex2svg is part of mkhack3rs

**mkdocs-tex2svg** is one of several other one-line-install additional functionnalities for mkdocs.  
Please have a look at *mkhack3rs* site if interested :

*  **[mkhack3rs](https://eskool.gitlab.io/mkhack3rs/)**: https://eskool.gitlab.io/mkhack3rs/   

# Installation

## Via PIP

**mkdocs-tex2svg** is a Python package, installable with pip :

`$ pip install mkdocs-tex2svg`

or upgrade via pip (if already installed)

`$ pip install --upgrade mkdocs-tex2svg`

Project's page in PyPI is: https://pypi.org/project/mkdocs-tex2svg/

## Via Conda or Mamba

Please have a look at [this github page](https://github.com/conda-forge/mkdocs-tex2svg-feedstock) if you want get more precise instructions to install `mkdocs-tex2svg` with **conda** or **mamba**, via the **conda-forge** github channel :

[https://github.com/conda-forge/mkdocs-tex2svg-feedstock](https://github.com/conda-forge/mkdocs-tex2svg-feedstock)

# Configuration

## Activation

Activate the `mkdocs_tex2svg` extension. For example, with **Mkdocs**, you add a
stanza to `mkdocs.yml`:

```yaml
markdown_extensions:
    - mkdocs_tex2svg
```

## Options

**Optionnally**, use any (or a combination) of the following options with all colors being written as:

* a **standard HTML Color Name** as in [this W3C page](https://www.w3schools.com/tags/ref_colornames.asp) (All Caps Allowed)
* an **HTML HEXADECIMAL COLOR, but WITHOUT THE # SIGN**
```yaml
markdown_extensions:
  - mkdocs_tex2svg:
      vartable:                     # Specific Configs for Variations Tables
        light:                      # Light Theme Configs
          color: chartreuse             # Any HTML Color Name, or, any HTML Hexadecimal color code WITHOUT the `#` sign
          bglabel: darksalmon           # Any HTML Color Name, or, any HTML Hexadecimal color code WITHOUT the `#` sign
          bgvi: FFFFFF                  # Any HTML Color Name, or, any HTML Hexadecimal color code WITHOUT the `#` sign
        dark:                       # Dark Theme Configs
          color: lavenderblush          # Any HTML Color Name, or, any HTML Hexadecimal color code WITHOUT the `#` sign
          bglabel: darkblue             # Any HTML Color Name, or, any HTML Hexadecimal color code WITHOUT the `#` sign
          bgvi: red                     # Any HTML Color Name, or, any HTML Hexadecimal color code WITHOUT the `#` sign
        priority: 75                 # The priority for this Markdown Extension (DEFAULT : 75)
```

Where:

* `vartable` refers to configs which are specific to Maths Variation Tables
* `light` is the keyword for configs relative to **Light Theme** in Mkdocs
* `dark` is the keyword for configs relative to **Dark Theme** in Mkdocs
* `color` is a color option that modifies **The Color** of Variation Tables :
    * Borders and Arrows
    * All Texts (Labels, annd non Labels)
    * **Defaults** for **colors** are :
        * `black` for Light Theme, and 
        * `white` for Dark Theme
* `bglabel` sets the Bakcground Color the the **Labels** (texts upon arrows mainly). 
    * **Defaults** for **bgLabels** are:
        * `white` for Light Theme, and 
        * `2E303E` for Dark Theme = Default Mkdocs Material Dark Background for Slate
* `bgvi` sets the Background Color for **Valeurs Interdites (VI)** / **Forbidden Values (FV)** (the background inside the double vertical bars)
    * **Defaults** for **bgvi** are :
        * `white` for Light Theme, and 
        * `2E303E` for Dark Theme = Default Mkdocs Material Dark Background for Slate
* `priority` (default `75`) sets the priority for this Markdown Extension

## Color Codes

Color Codes can be :

* a **standard HTML Color Name** as in [this W3C page](https://www.w3schools.com/tags/ref_colornames.asp) (All Caps Allowed)
* an **HTML HEXADECIMAL COLOR, WITHOUT THE # SIGN**

## Mixing & Conflicting Options

* No known conflicts with the **tkz-tab** syntax (may be the bglabels? feel free feedback any issue)

# Usage

To use it in your Markdown doc, 

with SVG output:

    ```vartable
    \begin{tikzpicture}
    \tikzset{h style/.style = {fill=red!50}}
    \tkzTabInit[lgt=1,espcl=2]{$x$ /1, $f$ /2}{$0$,$1$,$2$,$3$}%
    \tkzTabVar{+/ $1$ / , -CH/ $-2$ / , +C/ $5$, -/ $0$ / }
    \end{tikzpicture}
    ```

# Examples

Other examples in these pages:

* Installation & Configs : [https://eskool.gitlab.io/mkhack3rs/maths/tables/](https://eskool.gitlab.io/mkhack3rs/maths/tables/)
* Examples : [https://eskool.gitlab.io/mkhack3rs/maths/tables/examples/](https://eskool.gitlab.io/mkhack3rs/maths/tables/examples/)

# CSS / JS Classes

* Each `vartable` svg img is preceded by a span tag with the two classes : `tex2svg` and `vartable.

# Credits

* Rodrigo Schwencke for all credits : [rod2ik/mkdocs-tex2svg](https://gitlab.com/rod2ik/mkdocs-tex2svg)

# License

* All parts are from [Rodrigo Schwencke / rod2ik](https://gitlab.com/rod2ik) are [GPLv3+](https://opensource.org/licenses/GPL-3.0)
