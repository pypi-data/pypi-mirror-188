# Scrapy-Custom-Delay

[![PyPI](https://img.shields.io/pypi/v/scrapy-domain-delay)](https://pypi.org/project/scrapy-domain-delay/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/scrapy-domain-delay)](https://pypi.org/project/scrapy-domain-delay/)
[![Build Status](https://app.travis-ci.com/ChiaYinChen/scrapy-domain-delay.svg?branch=master)](https://app.travis-ci.com/ChiaYinChen/scrapy-domain-delay)

`Scrapy-Domain-Delay` is a package that lets you set different delay for different website, using the [Scrapy](https://github.com/scrapy/scrapy) framework.

## Install
```
$ pip install scrapy-Custom-delay
```

## Usage

In this example, we would extract `"google"` as domain name from a full url `"https://www.google.com/"`.

### Step 1: Use the following config values in your scrapy settings:

1. Enable the AutoThrottle extension.

	```python
	AUTOTHROTTLE_ENABLED = True
	```

2. Enable the Custom Delay Throttle by adding it to `EXTENSIONS`.

	```python
	EXTENSIONS = {
	    'scrapy.extensions.throttle.AutoThrottle': None,
	    'scrapy_domain_delay.extensions.CustomDelayThrottle': 300,
	}
	```

3. Add `{'domain': 'download delay (in seconds)'}` to the `DOMAIN_DELAYS`.

	something like:

	```python
	# set up custom delays per domain
    # if two or more regexes satisfy, the first one will be used
	DOMAIN_DELAYS = {
	    r'^images.google.com*$': 1.0,
	    r'*github*': 0.5,
	}
	```
