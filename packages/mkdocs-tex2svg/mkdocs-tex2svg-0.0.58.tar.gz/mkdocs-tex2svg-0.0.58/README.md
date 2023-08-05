# mkdocs-tex2svg

## :warning: Warning :warning:

* **THIS MKDOCS EXTENSION IS NOW OPERATIONAL (v 0.0.58).**
* **THIS MDKOCS DOCUMENTATION is in Work in Progress Mode**

State of the Art : **TKZ-TAB** SNIPPETS (for **Maths Variation Tables**) are being correctly rendered as Base64 SVGs, both for Light and Dark Modes.

## What is mkdocs-tex2svg ?

**mkdocs-tex2svg** is a configurable **Python Markdown extension for Mkdocs**, that renders **inline** LaTeX Snippets (with Single $\$...\$ $) or **block** LaTeX Formulas (with Double dollars $\$\$...\$\$ $), **with any customised extra LaTeX packages**, to base64 SVGs out of the box ! 

This package was initially and primarily developped so as to:

* **draw maths variation tables** as base64 SVGs directly in markdown files, with the **tikz** and **tkz-tab** syntax
* be compatible with Light and Dark Themes. 

But **mkdocs-tex2svg** can convert in-time **any LaTeX snippet**, using any extra LaTeX package, to base64 SVGs.

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

    * **Subgraphs / Clusters** roundings
    * **Nodes** (both borders and fonts, separately), 
    * **Edges** (both borders and fonts, separately), 
    * all-in-one colors via the `color` option
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
        light_theme: 000000      # Any HTML Color Name or any HTML Hexadecimal color code WITHOUT the `#` sign
        dark_theme: FFFFFF       # Any HTML Color Name or any HTML Hexadecimal color code WITHOUT the `#` sign
        color: 789ABC            # Any HTML Color Name or any HTML Hexadecimal color code WITHOUT the `#` sign
        bgcolor: none            # Any HTML Color Name or any HTML Hexadecimal color code WITHOUT the `#` sign
        graph_color: 789ABC      # Any HTML Color Name or any HTML Hexadecimal color code WITHOUT the `#` sign
        graph_fontcolor: 789ABC  # Any HTML Color Name or any HTML Hexadecimal color code WITHOUT the `#` sign
        node_color: 789ABC       # Any HTML Color Name or any HTML Hexadecimal color code WITHOUT the `#` sign
        node_fontcolor: 789ABC   # Any HTML Color Name or any HTML Hexadecimal color code WITHOUT the `#` sign
        edge_color: 789ABC       # Any HTML Color Name or any HTML Hexadecimal color code WITHOUT the `#` sign
        edge_fontcolor: 789ABC   # Any HTML Color Name or any HTML Hexadecimal color code WITHOUT the `#` sign
        priority: 75             # The priority for this Markdown Extension (DEFAULT : 75)
```

Where:

* `light_theme` (default `000000`) is the **default color of the graph (nodes and edges) in Light Theme** in Mkdocs
* `dark_theme` (default `FFFFFF`) is the **default color of the graph (nodes and edges) in Dark Theme** in Mkdocs
* `color` (default `789ABC`) is a color option that modifies **ALL** the following colors **IN BOTH THEMES (Light and Dark)** in just one parameter:
    * All Nodes
    * All Texts inside Nodes
    * All Edges
    * All Labels aside Edges
    FORMAT
* `bgcolor` (default `none`) sets :
    * the background color to be transparent (by default, which is equivalent to `bgcolor: none`), or
    * the background color of the graph
* `graph_color` (default `789ABC`) sets the color of all Subgraphs/Clusters Roundings
* `graph_fontcolor` (default `789ABC`) sets the color of all Subgraphs/Clusters Titles 
* `node_color` (default `789ABC`) sets the color of all Nodes
* `node_fontcolor` (default `789ABC`) sets the color of all Texts inside Nodes
* `edge_color` (default `789ABC`) sets the color of all Edges
* `edge_fontcolor` (default `789ABC`) sets the color of all Labels aside Edges
* `priority` (default `75`) sets the priority for this Markdown Extension

## Color Codes

Color Codes can be :

* a **standard HTML Color Name** as in [this W3C page](https://www.w3schools.com/tags/ref_colornames.asp) (All Caps Allowed)
* an **HTML HEXADECIMAL COLOR, WITHOUT THE # SIGN**

## Mixing & Conflicting Options

* It is possible to define a general color of the graph with the `color` option, and then overwrite some of the values with the other options (you choose)
* Colors defined with the options can always be overwritten as a **per Node basis**, or a **per Edge basis** directly inside of the tex2svg/dot syntax
* `color` option takes precedence over `light_theme` and `dark_theme` options, but not over other options

# Usage

To use it in your Markdown doc, 

with SVG output:

    ```dot
    digraph G {
        rankdir=LR
        Earth [peripheries=2]
        Mars
        Earth -> Mars
    }
    ```

or

    ```tex2svg dot attack_plan.svg
    digraph G {
        rankdir=LR
        Earth [peripheries=2]
        Mars
        Earth -> Mars
    }
    ```

or with PNG:

    ```tex2svg dot attack_plan.png
    digraph G {
        rankdir=LR
        Earth [peripheries=2]
        Mars
        Earth -> Mars
    }
    ```

**Supported tex2svg commands: dot, neato, fdp, sfdp, twopi, circo.**

# Examples

Other examples in these pages:

* Trees & Graphs : https://eskool.gitlab.io/mkhack3rs/tex2svg/examples/
* Trees : https://eskool.gitlab.io/tnsi/donnees/arbres/quelconques/
* Graphs : https://eskool.gitlab.io/tnsi/donnees/graphes/definitions

# CSS / JS Classes

* Each graph has both a `dot` and a `tex2svg` class in the `<svg>` tag, wich can be used for further customization via CSS / JS.
* Note that Javascript rod2ik's cdn `mkdocs_tex2svg.js` **MUST BE SET** in `mkdocs.yml` for `light_theme` and `dark_theme` options to be functionnal. Any other functionnality doesn't need this extra Javascript.

```yaml
extra_javascript:
  - https://cdn.jsdelivr.net/gh/rod2ik/cdn@main/mkdocs/javascripts/mkdocs-tex2svg.js
```

# Credits

* Rodrigo Schwencke for all credits : [rodrigo.schwencke/mkdocs-tex2svg](https://gitlab.com/rodrigo.schwencke/mkdocs-tex2svg)

# License

* All newer parts (Rodrigo Schwencke) are [GPLv3+](https://opensource.org/licenses/GPL-3.0)
* Older parts (Cesare Morel, Steffen Prince, Jawher Moussa) are [MIT License](http://www.opensource.org/licenses/mit-license.php)
