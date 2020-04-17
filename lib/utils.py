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
