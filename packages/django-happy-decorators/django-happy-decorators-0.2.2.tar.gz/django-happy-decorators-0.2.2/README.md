# Django Happy Decorators

[![Build Status](https://travis-ci.org/rodrigobdz/django-happy-decorators.svg?branch=master)](https://travis-ci.org/rodrigobdz/django-happy-decorators)
[![Coverage Status](https://coveralls.io/repos/github/rodrigobdz/django-happy-decorators/badge.svg?branch=master)](https://coveralls.io/github/rodrigobdz/django-happy-decorators?branch=master)
[![PyPI version](https://badge.fury.io/py/django-happy-decorators.svg)](https://badge.fury.io/py/django-happy-decorators)
[![Documentation Status](https://readthedocs.org/projects/django-happy-decorators/badge/?version=latest)](https://django-happy-decorators.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# Overview

Django Happy Decorators is a collection of useful decorators for Django.

# Decorators

- `rate_limit`: Rate limit a view function based on IP address, user or all requests.

# Installation

You can install Django Rate Limit using pip:

`pip install django_happy_decorators`


# Usage

To use the rate_limit decorator, import it from the package and apply it to a view function. The decorator accepts three parameters: num_requests, time_frame and redirect_url.

```python
from django_rate_limit.decorators import rate_limit

@rate_limit(num_requests=100, time_frame=3600, redirect_url='/rate_limit_exceeded', mode='ip')
def my_view(request):
    # View logic goes here

```

# Modes:

- ip: limits the number of requests per IP address
- user: limits the number of requests per user
- all: limits the number of requests

In the example above, the view will only allow 100 requests per hour and when the limit is reached it will redirect the user to '/rate_limit_exceeded'


# Documentation

For more information on how to use Django Rate Limit, please refer to the documentation at:

https://django-rate-limit.readthedocs.io/


# Contributing

We welcome contributions to Django Rate Limit. If you want to contribute, please read our contributing guidelines for more information.

# License

Django Rate Limit is released under the MIT License.

This is just a sample and you can adjust the content as per your package and also add more details like screenshots, sample code etc.
