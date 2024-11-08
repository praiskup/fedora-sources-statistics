#! /bin/python

"""
Dump some statistics for results.json.
"""

import json

# pylint: disable=too-few-public-methods,too-many-branches
# pylint: disable=missing-function-docstring,line-too-long
# pylint: disable=too-many-statements,too-many-locals
# noqa


def _get_data():
    with open("results.json", "r", encoding="utf-8") as fd:
        return json.loads(fd.read())


def _is_archive(filename):
    if ".tar" in filename:
        return True
    for suffix in [".tgz", ".txz", ".tbz"]:
        if filename.endswith(suffix):
            return True
    if ".gem" in filename:
        return True
    if ".zip" in filename:
        return True
    if ".crate" in filename:
        return True
    return False


def _is_binary_file(filename):
    for suffix in ["png", "jpg", "jpeg", "pdf", "xz", "gz", "bz2"]:
        if filename.endswith("." + suffix):
            return True
    return False


def _is_text_file(filename):
    for suffix in ["desktop", "conf", "yaml", "cfg", "sh", "gpg", "asc", "txt",
                   "md", "xml", "pom", "svg", "cabal", "1", "8", "c", "h", "py",
                   "service", "key", "rpmlintrc", "sysconfig", "logrotate",
                   "sysusers", "config", "pgp", "socket", "json"]:
        if filename.endswith("." + suffix):
            return True

    if filename.startswith("macros."):
        return True

    for pattern in ["readme", "license"]:
        if pattern in filename.lower():
            return True
    return False


class _OnlineMeasure:
    def __init__(self):
        self.online = 0
        self.offline = 0
        self.lookaside = 0
        self.lookaside_online = 0
        self.lookaside_offline = 0
        self.specfiles_online = set()
        self.specfiles_offline = set()
        self.specfiles = set()
        self.sources = set()

    def add_online(self, specfile, source, lookaside):
        self.online += 1
        self.specfiles_online.add(specfile)
        if lookaside:
            self.lookaside_online += 1
        self._add_all(specfile, source, lookaside)

    def add_offline(self, specfile, source, lookaside):
        self.offline += 1
        self.specfiles_offline.add(specfile)
        if lookaside:
            self.lookaside_offline += 1
        self._add_all(specfile, source, lookaside)

    def _add_all(self, specfile, source, lookaside):
        self.specfiles.add(specfile)
        self.sources.add(source)
        if lookaside:
            self.lookaside += 1

    @property
    def total(self):
        return self.online + self.offline

    def __str__(self):
        files = f"{self.online}/{self.offline}/{self.total} (online/offline/total, SourceN files)"
        specfiles = f"{len(self.specfiles_online)}/{len(self.specfiles_offline)}/{len(self.specfiles)} (specfiles referencing online/offline/any such source(s))"
        lookaside = f"{self.lookaside_online}/{self.lookaside_offline}/{self.lookaside} (lookaside online/offline/all)"
        return f"{files} || {specfiles} || {lookaside}"


def _main():
    data = _get_data()

    spec_files = 0

    source_files = _OnlineMeasure()

    # online vs offline
    source_archives = _OnlineMeasure()
    source_textfiles = _OnlineMeasure()
    source_binaryfiles = _OnlineMeasure()
    source_others = _OnlineMeasure()

    no_sources = 0
    parse_errors = 0

    for spec in data:
        spec_files += 1
        spec_data = data[spec]
        if 'parse_error' in spec_data:
            parse_errors += 1
            continue

        sources = spec_data["sources"]
        if not sources:
            no_sources += 1
            continue

        for source in sources:
            value = source["tag_value"]
            lookaside = source["in_lookaside"]
            stats = source_others
            if _is_archive(value):
                stats = source_archives
            elif _is_binary_file(value):
                stats = source_binaryfiles
            elif _is_text_file(value):
                stats = source_textfiles

            if source["tag_type"] == "url":
                stats.add_online(spec, value, lookaside)
                source_files.add_online(spec, value, lookaside)
            else:
                stats.add_offline(spec, value, lookaside)
                source_files.add_offline(spec, value, lookaside)

    specfiles_with_sources = set()
    all_measures = [source_archives, source_binaryfiles, source_textfiles, source_others]
    for measure in all_measures:
        specfiles_with_sources = specfiles_with_sources.union(measure.specfiles)

    specfiles_with_online_sources = set()
    specfiles_with_offline_sources = set()
    for measure in all_measures:
        specfiles_with_online_sources = specfiles_with_online_sources.union(measure.specfiles_online)
        specfiles_with_offline_sources = specfiles_with_offline_sources.union(measure.specfiles_offline)

    specfiles_online_only = specfiles_with_sources - specfiles_with_offline_sources
    specfiles_offline_only = specfiles_with_sources - specfiles_with_online_sources

    print(f"spec_files:                 {spec_files}")
    print(f"source_files:               {source_files}")
    print(f"source_archives:            {source_archives}")
    print(f"source_textfiles:           {source_textfiles}")
    print(f"source_binaryfiles:         {source_binaryfiles}")
    print(f"source_others:              {source_others}")
    print(f"online only sources in:     {len(specfiles_online_only)} spec files")
    print(f"offline only sources in:    {len(specfiles_offline_only)} spec files")
    print(f"source without category in: {len(source_others.specfiles)}")
    print(f"no_sources:                 {no_sources}")
    print(f"parse_errors:               {parse_errors}")

    # stats = {}
    # for src in source_others.sources:
    #     suffix = src.split(".")[-1]
    #     if suffix not in stats:
    #         stats[suffix] = 0
    #     stats[suffix] += 1
    # import pprint
    # pprint.pprint(sorted(stats.items(), key=lambda x: x[1]))

    # print("\n".join(source_others.sources))


if __name__ == "__main__":
    _main()
