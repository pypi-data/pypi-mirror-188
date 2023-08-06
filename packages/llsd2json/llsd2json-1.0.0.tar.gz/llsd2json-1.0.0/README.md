# llsd2json

[![codecov](https://codecov.io/gh/bennettgoble/llsd2json/branch/main/graph/badge.svg?token=PABF3Y1DJP)](https://codecov.io/gh/bennettgoble/llsd2json)

CLIs to convert between [Linden Lab Structured Data (LLSD)][llsd] and JSON.

Example:
```
$ echo '<llsd><map><key>name</key><string>Ruth</string></map></llsd>' | llsd2json | jq -r .name
Ruth
```

## Install and use

Install **llsd2json** with pip or [pipx][]

```text
pipx install llsd2json
```

### llsd2json

```text
usage: llsd2json [-h] [--format {auto,xml,binary,notation}] [input]

Convert LLSD to JSON

positional arguments:
  input                 LLSD string (default: stdin)

options:
  -h, --help            show this help message and exit
  --format {auto,xml,binary,notation}, -f {auto,xml,binary,notation}
                        LLSD format
```

### json2llsd

```text
usage: json2llsd [-h] [--format {xml,binary,notation}] [input]

Convert JSON to LLSD

positional arguments:
  input                 JSON string (default: stdin)

options:
  -h, --help            show this help message and exit
  --format {xml,binary,notation}, -f {xml,binary,notation}
                        LLSD format
```

## Notes

Conversion between LLSD and JSON is not perfectly bi-directional. JSON does not
support several LLSD data types such as `date`, `binary`, `uri`, and has no
distinct number types.

[llsd]: https://wiki.secondlife.com/wiki/LLSD
[pipx]: https://pypa.github.io/pipx/