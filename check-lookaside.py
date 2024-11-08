#! /usr/bin/python3

"""
Given the file in SourceX statement, check if it present in sources file
(= hosted in the lookaside cache).
"""

import json
import os


def _update_spec_data(data, sources):
    if "sources" not in data:
        # this happens if crawler failed to parse spec file
        return

    for spec_source in data["sources"]:
        spec_file_base = os.path.basename(spec_source["tag_value"])
        spec_source["in_lookaside"] = spec_file_base in sources

    # no check for an unused lookaside cache here!


def save_data(data):
    """ save the results.json database file, override existing file """
    with open("results.json", "w", encoding="utf-8") as fd:
        fd.write(json.dumps(data, indent=2))


def _check_sources(spec, data):
    spec = os.path.basename(spec)
    pkgname = spec[:-5]

    with open(f"sources/sources.{pkgname}", "r", encoding="utf-8") as fd:
        lookaside_sources = []
        for line in fd.readlines():
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) == 4:
                filename = parts[1]
                filename = filename.strip('()')
            else:
                filename = parts[1]
            lookaside_sources.append(filename)

        _update_spec_data(data, lookaside_sources)


def _main():
    with open("results.json", "r", encoding="utf-8") as fd:
        data = json.loads(fd.read())

    for spec in data:
        spec_data = data[spec]
        _check_sources(spec, spec_data)

    save_data(data)


if __name__ == "__main__":
    _main()
