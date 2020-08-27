from os.path import exists
from typing import Sequence, Union, List

import flask
from werkzeug.utils import import_string


def import_and_find_all(reference: Union[str, object, List[object]],
                        target_class: type) -> List[object]:
    if isinstance(reference, str):
        reference = import_string(reference)
    if isinstance(reference, (list, tuple)):
        if not all(isinstance(ref, target_class) for ref in reference):
            raise ValueError("Not all entries in sequence are instances of {}".format(target_class.__name__))
        return reference
    if isinstance(reference, target_class):
        return [module]
    objects = [obj for obj in vars(reference).values() if isinstance(obj, target_class)]
    if not objects:
        raise ValueError("Could not find any instances of {}".format(target_class.__name__))
    return objects


def import_extension(extension):
    # str -> module
    if isinstance(extension, str):
        extension = import_string(extension)
    # module -> class
    if not callable(extension) and hasattr(extension, 'Extension'):
        extension = extension.Extension
    # class -> object
    if callable(extension):
        extension = extension()
    return extension


def set_if_exists(bp, var, value):
    if not getattr(bp, var, None):
        setattr(bp, var, value)
        if not exists(getattr(bp, var)):
            setattr(bp, var, None)


def get_config_processor(app):
    context = {
        'version': version,
        'apps': app.config['apps'],
    }
    return lambda: context
