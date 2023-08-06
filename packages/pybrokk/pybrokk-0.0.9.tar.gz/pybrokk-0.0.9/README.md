[![Documentation Status](https://readthedocs.org/projects/pybrokk/badge/?version=latest)](https://pybrokk.readthedocs.io/en/latest/?badge=latest)

# pyBrokk

This package allows users to provide a list of URLs for webpages of interest and creates a dataframe with Bag of Words representation that can then later be fed into a machine learning model of their choice. Users also have the option to produce a dataframe with just the raw text of their target webpages to apply the text representation of their choice instead.

## Why `pyBrokk`

There are some libraries and packages that can facilitate this job, from scraping text from a URL to returning it to a bag of words (BOW). However, to the extent of our knowledge, there is no sufficiently handy and straightforward package for this purpose. This package is a tailored combination of `BeatifulSoup` and `CountVectorizer`. [`BeautifulSoup`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) widely used to pull different sources of data from HTML and XML pages, and [`CountVectorizer`](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html) is a well-known package to convert a collection of texts to a matrix of token counts.

### NOTE:

Some websites do not let users collect their data with web scraping tools. Make sure that your target websites do not refuse your request to collect data before applying this package.

## Features

The pyBrokk package includes the following four functions:

-   `create_id()`: Takes a list of webpage urls formatted as strings as an input and returns a list of unique string identifiers for each webpage based on their url. The identifier is composed of the main webpage name followed by a number.
-   `text_from_url()` : Takes a list of urls and using Beautiful Soup extracts the raw text from each and creates a dictionary. The keys contain the original URL and the values contain the raw text output as parsed by Beautiful Soup.
-   `duster()`: Takes a list of urls and uses the above two functions to create a dataframe with the webpage identifiers as a index, the raw url, and the raw text from the webpage with extra line breaks removed.
-   `bow()`: Takes a string text as an input and returns the list of unique words it contains.

## Installation

``` bash
$ pip install pybrokk
```

## Usage

### Imports

```{python}
import pybrokk 
import requests 
import pandas as pd 
from bs4 import BeautifulSoup 
from sklearn.feature_extraction.text import CountVectorizer
```

### Input Format

```{python}
urls = ['https://www.utoronto.ca/',
         'https://www.ubc.ca/',
         'https://www.mcgill.ca/',
         'https://www.queensu.ca/']
```

### create_id()

##### Creates unique IDs for a list of URLs

```{python}
url_ids = create_id(urls)
```

### text_from_url()

##### Creates a dictionary with original URLs as keys and parsed using `BeautifulSoup` text as values

```{python}
dictionary = text_from_url(urls)
```

### duster()

##### Create a dataframe using the outputs of `create_id()` and `text_from_url()`

```{python}
df = duster(urls)
```

### bow()

##### Create a dataframe of a bag of words appended to the input dataframe

```{python}
df_bow = bow(df)
```

## Contributing

Interested in contributing? Check out the [contributing guidelines](CONTRIBUTING.md) and the [list of contributors](CONTRIBUTORS.md) who have contributed to the development of this project thus far. Please note that this project is released with a [Code of Conduct](CONDUCT.md). By contributing to this project, you agree to abide by these terms.

## License

`pyBrokk` was created by Elena Ganacheva, Mehdi Naji, Mike Guron, Daniel Merigo. It is licensed under the terms of the MIT license.

## Credits

`pyBrokk` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter). `pyBrokk` uses [`beautiful soup`](https://www.crummy.com/software/BeautifulSoup/)
