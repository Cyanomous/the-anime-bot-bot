"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
import re
def finder(text, collection, *, key=None, lazy=True):
    maybe = []
    text = str(text)
    to_compile = '.*?'.join(map(re.escape, text))
    regex = re.compile(to_compile, flags=re.IGNORECASE)
    for item in collection:
        to_search = key(item) if key else item
        r = regex.search(to_search)
        if r:
            maybe.append((len(r.group()), r.start(), item))

    def sort_(var):
        if key:
            return var[0], var[1], key(var[2])
        return var

    if lazy:
        return (z for _, _, z in sorted(maybe, key=sort_))
    else:
        return [z for _, _, z in sorted(maybe, key=sort_)]