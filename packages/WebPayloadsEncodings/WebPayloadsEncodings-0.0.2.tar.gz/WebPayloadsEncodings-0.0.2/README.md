![WebPayloadsEncodings logo](https://mauricelambert.github.io/info/python/security/WebPayloadsEncodings_small.png "WebPayloadsEncodings logo")

# WebPayloadsEncodings

## Description

This tool encodes Web payloads with some different encoding.

## Requirements

This package require :
 - python3
 - python3 Standard Library

## Installation

```bash
pip install WebPayloadsEncodings
```

## Usages

### Command line

```bash
python3 -m WebPayloadsEncodings 'my payload'
python3 WebPayloadsEncodings.pyz 'all' 'first payload' 'second payload'
WebPayloadsEncodings 'html' 'my payload'

WebPayloadsEncodings 'url' 'first payload' 'payload2' 'payload3'
WebPayloadsEncodings 'unicode' 'first payload' 'payload2' 'payload3'
WebPayloadsEncodings 'javascript' 'first payload' 'payload2' 'payload3'
WebPayloadsEncodings 'sqlite' 'first payload' 'payload2' 'payload3'
WebPayloadsEncodings 'hexa escaping' 'first payload' 'payload2' 'payload3'
```

### Python script

```python
from WebPayloadsEncodings import payloads_encodings, unicode_html_escaping

payloads_encodings('postgresql', 'my payload', 'second payload')
print(unicode_html_escaping("payload", leading_zeros=8))
```

## Links

 - [Github Page](https://github.com/mauricelambert/WebPayloadsEncodings/)
 - [Documentation](https://mauricelambert.github.io/info/python/security/WebPayloadsEncodings.html)
 - [Pypi package](https://pypi.org/project/WebPayloadsEncodings/)
 - [Executable](https://mauricelambert.github.io/info/python/security/WebPayloadsEncodings.pyz)

## Licence

Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
