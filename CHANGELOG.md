# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project is trying to converge towards [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2023-07-30

### Adds
- Adds filtering of overlapping regions using Non-Max-Suppression and Sub-Section Suppression.

## [0.1.1] - 2023-07-26

### Changes
- **Breaking:** parse_single_pdf now accepts a layout_model rather than loading one.

### Fixed
- Fixes handling of articles with no figures or tables
- Fixes handling of figures and tables with no captions

### Removes
- Removes tqdm progress bar on page iteration.

## [0.1.0] - 2023-07-23

_Initial release._

[Unreleased]: https://github.com/alanmeeson/article-parser/compare/0.2.0...HEAD
[0.2.0]: https://github.com/alanmeeson/article-parser/compare/0.1.1...0.2.0
[0.1.1]: https://github.com/alanmeeson/article-parser/compare/0.1.0...0.1.1
[0.1.0]: https://github.com/alanmeeson/article-parser/releases/tag/0.1.0
