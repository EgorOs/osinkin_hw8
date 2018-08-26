#!/usr/bin/env python3
import sys

def stderr_redirect(dest=None):

    def inner_decorator(func):

        class wrapper:

            def __call__(self, *args, **kwargs):
                print('call', args)
                return func(*args, *kwargs)

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, exc_tb):
                if exc_type is None:
                    return False
                elif dest is None:
                    print(exc_type)
                else:
                    f = open(dest, 'w')
                    f.write(str(exc_value))
                    f.close()

        return wrapper()
    
    return inner_decorator


@stderr_redirect('test.txt')
def test(val_1, val_2):
    return val_1/val_2

# @stderr_redirect(dest=None)
# def test():
#     pass

with test as t:
    res = test(1,0)