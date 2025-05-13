# Instalations

## Install htmx

Used for SPA building and dynamic content loading.

```bash
poetry add django-htmx

mkdir webserver/web/static

wget https://unpkg.com/htmx.org@latest -O webserver/web/static/js/htmx.min.js
```

Add these lines into settings.py:

```python
INSTALLED_APPS = [
    ...,
    "django_htmx",
    ...,
]

MIDDLEWARE = [
    ...,
    "django_htmx.middleware.HtmxMiddleware",
    ...,
]
```
