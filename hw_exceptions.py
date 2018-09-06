#!/usr/bin/env python3
import sys
import os
import time

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
                    # redirect if dest is None
                    sys.stderr = sys.__stdout__
                else:
                    # redirect if dest is file
                    sys.stderr = open(dest, 'a')

                result = func(*args, *kwargs)

                if prev_dest != sys.__stderr__.name and prev_dest != sys.__stdout__.name:
                    # return stderr to the previous state if it was not stdout
                    sys.stderr = open(prev_dest, 'a')
                elif prev_dest is sys.__stdout__.name:
                    # return stderr to the previous state if it was stdout
                    sys.stderr = sys.__stdout__
                return result

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, exc_tb):
                if exc_type is None:
                    return False
                else:
                    # reset stderr back to normal
                    sys.stderr = sys.__stderr__

        return Wrapper()
    
    return inner_decorator


class pidfile:

    def __init__(self, file_name: str):
        self.file_name = file_name

        if '/' in file_name:
            # if path to directory is given
            path = file_name.split('/')
            file_name = path.pop(-1)
            path = '/'.join(path) + '/'
            os.chdir(path)

        if not os.path.isfile(file_name):
            # Create temporary pidfile
            f = open(file_name, 'w')
            f.write(str(os.getpid()))
            f.close()

        else:
            # pid file already exists
            pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
            f = open(file_name, 'r')
            for line in f:
            # check if pid of the original process is still exists
                if line in pids:
                    f.close()
                    raise OSError('The instance of this code is already ran by another process.')
                else:
                    # write a new pid
                    f = open(file_name, 'w')
                    f.write(str(os.getpid()))
                    f.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        # Remove temporary pidfile
        os.remove(self.file_name)


# Tests
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

def slow_func():
    print('Running slow_func with pid: {}'.format(os.getpid()))
    time.sleep(60)

# test1()
# test2()
# with pidfile('/home/egor/epam/homework/osinkin_hw8/pidfile.txt'):
#     slow_func()