import os
from typing import Generator


def listdir(path, recursive=True, extensions=None, join_parts=True):

    def generator(recursive):
        # Helper method
        if recursive:
            for dir_path, _, files in os.walk(path):
                for f in files:
                    yield dir_path, f

        else:
            for f in os.listdir(path):
                yield path, f

    files = generator(recursive)

    # Filter based on extensions
    if extensions is not None:
        if not isinstance(extensions, (tuple, list)):
            extensions = [extensions]

        files = filter(lambda x: os.path.splitext(
            x[1])[1] in extensions, files)

    # Join parts
    if join_parts:
        files = map(lambda x: os.path.join(*x), files)

    yield from files
