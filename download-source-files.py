#! /usr/bin/python3

"""
Update result.json with contents of source files and spec files
Download files like this:
$ curl https://src.fedoraproject.org/rpms/libecpg/raw/rawhide/f/sources
"""

import json
import os

import requests


def _get_url_from_spec(spec):
    specname = os.path.basename(spec)
    pkgname = os.path.basename(spec)[:-5]

    url = f"https://src.fedoraproject.org/rpms/{pkgname}/" \
        + "raw/rawhide/f/sources"
    req = requests.get(url, timeout=60)
    fname = f"sources/sources.{pkgname}"
    with open(fname, 'wb') as f:
        f.write(req.content)

    url = f"https://src.fedoraproject.org/rpms/{pkgname}/" \
        + f"raw/rawhide/f/{specname}"
    req = requests.get(url, timeout=60)
    fname = f"specs/{specname}"
    with open(fname, 'wb') as f:
        f.write(req.content)


def _main():
    with open("results.json", "r", encoding="utf-8") as fd:
        data = json.loads(fd.read())

    i = 1
    for spec in data:
        print(f"download #{i} - {spec}")
        _get_url_from_spec(spec)
        i = i + 1


if __name__ == "__main__":
    _main()
