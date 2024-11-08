#! /usr/bin/python3

"""
Construct the initial result.json database.

Inspired by get-sources-links.py from
git@gitlab.cee.redhat.com:praiskup/konflux-praiskup-sandbox.git
"""

import json
import glob
import time
from urllib.parse import urlparse
from specfile import Specfile


def _get_source_info_tracebacks(spec_filename):
    spec = Specfile(spec_filename)
    sources = []
    for tag in spec.tags(spec.parsed_sections.package).content:
        if not tag.name.lower().startswith("source"):
            continue
        if tag.name.lower().startswith("sourcelicense"):
            continue
        source = {}
        result = urlparse(tag.value)
        source["tag_name"] = tag.name
        source["tag_value"] = tag.value
        if result.scheme in ["http", "https", "ftps"]:
            source["tag_type"] = "url"
        else:
            source["tag_type"] = "other"
        sources.append(source)
    return sources


def get_source_info(spec_filename):
    """ Generate a dictionary with info about used SourceN statements """
    try:
        return {"sources": _get_source_info_tracebacks(spec_filename)}
    except Exception:  # pylint: disable=broad-exception-caught
        return {
            "parse_error": "TODO",
        }


def save_data(data):
    """ save the results.json database file, override existing file """
    with open("results.json", "w", encoding="utf-8") as fd:
        fd.write(json.dumps(data, indent=2))


def _main():
    start = time.time()
    data = {}
    i = 0

    try:
        with open("results.json", "r", encoding="utf-8") as fd:
            data = json.loads(fd.read())
    except FileNotFoundError:
        pass

    try:
        for file in glob.glob("rpm-specs/*.spec"):
            if file in data:
                if "parse_error" not in data[file]:
                    # retry this one
                    continue
            takes = round(time.time() - start, 2)
            i = i+1
            print(f"{i:010d} {file} {takes}s")
            data[file] = get_source_info(file)

            if i % 500 == 0:
                save_data(data)

    except KeyboardInterrupt:
        pass

    save_data(data)


if __name__ == "__main__":
    _main()
