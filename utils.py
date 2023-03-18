import os


def join_path(arg1, arg2):
    return os.path.join(arg1, arg2)


def is_file(arg1):
    return os.path.isfile(arg1)


def split(arg1):
    return os.path.splitext(arg1)


def list(arg1):
    return os.listdir(arg1)


def is_dir(arg1):
    return os.path.isdir(arg1)
