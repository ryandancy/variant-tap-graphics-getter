# Utilities for getting and processing VariantTap graphics

This repository contains Python utilities for downloading, filtering, and quickly editing graphics for the VariantTap app (coppercoder/variant-tap).

## The Utilities

* `openclipart.py` - gets graphics from [openclipart.org](http://openclipart.org) and places them in `graphics/`.
* `edit.py` - opens each SVG graphic in `graphics/` and opens Inkscape for the user to edit them, then sorts them into `variants/` and `normals/`.
* `process.py` - uses Inkscape to convert each SVG in `variants/` and `normals/` to PNG.
