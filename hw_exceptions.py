#!/usr/bin/env python3
import sys
import os


def stderr_redirect(dest=None):

    def inner_decorator(func):

        class Wrapper:

            def __call__(self, *args, **kwargs):
                '''
                Preserving previous destination
                for nested functions, after getting
                result of wrapped function set
                previous destination.
                '''
                prev_dest = sys.stderr.name
                if dest is None:
                    sys.stderr = sys.__stdout__
                    result = func(*args, *kwargs)
                    if prev_dest != sys.__stderr__.name and prev_dest != sys.__stdout__.name:
                        sys.stderr = open(prev_dest, 'a')
                    return result

                elif prev_dest is sys.__stdout__.name:
                    sys.stderr = sys.__stdout__
                    result = func(*args, *kwargs)
                    if prev_dest != sys.__stderr__.name and prev_dest != sys.__stdout__.name:
                        sys.stderr = open(prev_dest, 'a')
                else:
                    sys.stderr = open(dest, 'a')
                    result = func(*args, *kwargs)
                    if prev_dest != sys.__stderr__.name and prev_dest != sys.__stdout__.name:
                        sys.stderr = open(prev_dest, 'a')
                    return result

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, exc_tb):
                if exc_type is None:
                    return False
                elif dest is None:
                    pass
                else:
                    sys.__stderr__

        return Wrapper()
    
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


@stderr_redirect(dest='file1')
def test1():
    sys.stderr.write('test1 func\n')
    return 10


@stderr_redirect(dest='file2')
def test2():
    test1()
    sys.stderr.write('test2 func\n')
    test1()
    return 10


test1()
test2()
