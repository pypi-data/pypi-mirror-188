# Django Rate Limit

Django Rate Limit is a package that provides a decorator for views that limits the number of requests a user can make to a specific view within a given time frame, also it allows to redirect the user to a specific url when the limit is reached


# Installation

You can install Django Rate Limit using pip:

`pip install django-rate-limit`


# Usage

To use the rate_limit decorator, import it from the package and apply it to a view function. The decorator accepts three parameters: num_requests, time_frame and redirect_url.

```python
from django_rate_limit.decorators import rate_limit

@rate_limit(num_requests=100, time_frame=3600, redirect_url='/rate_limit_exceeded')
def my_view(request):
    # View logic goes here

```

In the example above, the view will only allow 100 requests per hour and when the limit is reached it will redirect the user to '/rate_limit_exceeded'


# Documentation

For more information on how to use Django Rate Limit, please refer to the documentation at:

https://django-rate-limit.readthedocs.io/


# Contributing

We welcome contributions to Django Rate Limit. If you want to contribute, please read our contributing guidelines for more information.

# License

Django Rate Limit is released under the MIT License.

This is just a sample and you can adjust the content as per your package and also add more details like screenshots, sample code etc.
