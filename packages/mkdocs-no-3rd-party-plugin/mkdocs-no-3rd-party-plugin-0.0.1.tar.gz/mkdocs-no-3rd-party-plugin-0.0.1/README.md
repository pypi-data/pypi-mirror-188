# mkdocs-no-3rd-party-plugin

An MkDocs plugin to remove 3rd party assets and download them locally.

## Setup

Install the plugin using pip:

`pip install mkdocs-no-3rd-party-plugin`

Activate the plugin in `mkdocs.yml`:

```yaml
plugins:
  - no3rdparty
```

## Options

- `download_js`:
  - Defaults to `True`.
  - Sets whether to download 3rd party JS and provide it locally.
- `download_css`:
  - Defaults to `True`.
  - Sets whether to download 3rd party CSS and provide it locally.
- `directory`:
  - Defaults to `3rd_party`.
  - Sets the folder in which the 3rd party resources will be download and served from.
