#!/usr/bin/env python3
import sys
import os


def stderr_redirect(dest=None):

    def inner_decorator(func):

        class wrapper:

            def __call__(self, *args, **kwargs):
                return func(*args, *kwargs)

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, exc_tb):
                if exc_type is None:
                    return False
                elif dest is None:
                    pass
                else:
                    sys.stderr = open(dest, 'w')

        return wrapper()
    
    return inner_decorator


class pidfile:

    def __init__(self, file_name: str):
        self.file_name = file_name
        if not os.path.isfile(file_name):
            # Create temporary pidfile
            open(file_name, 'a').close()
        else:
            raise IOError('The instance of this code is already ran by another process.')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        # Remove temporary pidfile
        os.remove(self.file_name)
