![ci-cd](https://github.com/UBC-MDS/colourpycker/actions/workflows/ci-cd.yml/badge.svg)
[![codecov](https://codecov.io/gh/UBC-MDS/colourpycker/branch/main/graph/badge.svg?token=pkGKQ2l0uG)](https://codecov.io/gh/UBC-MDS/colourpycker)
[![Documentation Status](https://readthedocs.org/projects/colourpycker/badge/?version=latest)](https://colourpycker.readthedocs.io/en/latest/?badge=latest)

# colourpycker

A Python package that can be used to extract colours from images for use in data visualization projects.

## Overview

This package allows users to integrate unique colour palettes into their graphs for exploratory data analysis. The colours are retrieved from image data (via URL) and are selected based on their overall prominence in a picture. While there are existing tools that are used to process images and create figures independently, we aim to combine both of their functionalities to help programmers easily design effective and creative visualizations.

## Where Our Package Fits

As mentioned, there are packages in Python that are capable of colour extraction and data visualization, but none exist that combine the two functions to our knowledge. Some examples of such packages are as follows:

[Pillow](https://pypi.org/project/Pillow/): This package adds image processing capabilities into Python interpreters. It can perform various image transformations but does not allow for colours to be extracted directly for further use.

[extcolors](https://pypi.org/project/extcolors/): This extracts RGB colour codes from images into text along with the occurrence rate (proportion of pixels). However, we would need to use additional packages to create plots using common colours in the image. This would also not allow us to invert them, or create a palette.

[color-extraction](https://pypi.org/project/color-extraction/): This provides the most similar color for the pixels of an image from a palette of predefined colors.

[Pylette](https://github.com/qTipTip/Pylette/): This extracts colours and creates a colour palette based on an input image. This palette can be dumped into a csv file that would then need to be processed for use in data visualizations.

Therefore, we are developing `colourpycker` to bridge this gap.

## Installation

```bash
$ pip install colourpycker
```

## Functions

`get_color_palette(img_url, tolerance, limit)`: This function extracts the most common colors from an image and returns them as a data frame of hex color codes and RGB values. The user is provided with the ability to set tolerance while picking colors, along with the number of colors that should be returned.

`donut(img_url, num_clrs, tolerance, img_size, plot_show=True)`: This function creates a donut chart with information on the $n$ most common colors in the linked image. The user specifies the image, the number of colors, the tolerance for how similar the colors will be, and specifies the size of the resulting chart in pixels.

`scatterplot(img_url, dataset, x, y, fill, tolerance)`: This function creates a simple scatterplot using the colours selected from the image based on a dataset of the users choosing.

`negative(img_url, num_colours, tolerance)`: This function extracts the most common $n$ colours from an image (via URL) and inverts them to retrieve the negative version of a colour palette, returning the associated HEX codes and RGB values for each colour.

## Usage

For more examples on how to use `colourpycker`, a Jupyter Notebook can be found [here](https://github.com/UBC-MDS/colourpycker/blob/main/docs/example.ipynb) with additional use cases.

```
from colourpycker.colourpycker import scatterplot, negative, get_color_palette, donut

get_color_palette('https://i.imgur.com/s9egWBB.jpg', 20, 5)

donut('https://i.imgur.com/s9egWBB.jpg', 5, 20, 400)

scatterplot('https://i.imgur.com/s9egWBB.jpg', penguins, 'bill_length_mm', 'body_mass_g', 'species', 50)

negative("https://i.imgur.com/s9egWBB.jpg", 10, 20)
```

## Contributing

Interested in contributing? Check out the [contributing guidelines](https://github.com/UBC-MDS/colourpycker/blob/main/CONTRIBUTING.md) and [list of contributors](https://github.com/UBC-MDS/colourpycker/blob/main/CONTRIBUTORS.md) who worked on this project. Please note that this project is released with a [Code of Conduct](https://github.com/UBC-MDS/colourpycker/blob/main/CONDUCT.md). By contributing to this project, you agree to abide by its terms.

## License

`colourpycker` was created by Shaun Hutchinson, Arjun Radhakrishnan, Alex Taciuk, and Lauren Zung. It is licensed under the terms of the MIT license.

## Credits

`colourpycker` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
