import os

import ramda as _


def propOrCreate(f, prop, container):
    is_container = isinstance(container, dict)
    if is_container and prop in container:
        return container.get(prop)
    elif not is_container and _.has(container, prop):
        return _.prop(container, prop)

    result = f(prop)
    container[prop] = result
    return result


def values_sorted_on_key(x):
    sorted_keys = sorted(x.keys())
    return [x[k] for k in sorted_keys]


def import_path(filename, root_dir):
    relpath = os.path.relpath(filename, root_dir)
    return os.path.splitext(relpath)[0].replace("/", ".")
