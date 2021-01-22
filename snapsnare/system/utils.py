import logging
import logging.config
import tempfile
import os
import shutil
import errno
import json

from logging.config import dictConfig

FILE_NOT_FOUND = "File '{}' not found."


def html_audio_source_type(path):
    result = ''
    if path:
        filename, extension = os.path.splitext(path)
        if extension.lower().lstrip('.') == 'wav':
            return 'audio/wav'
        if extension.lower().lstrip('.') == 'mp3':
            return 'audio/mpeg'
        if extension.lower().lstrip('.') == 'ogg':
            return 'audio/ogg'

    # if we have to guess, then audio/mpeg is returned
    return 'audio/mpeg'


def load_logger(properties, filename, name=None):
    path = lookup(properties, filename)

    with open(path) as fp:
        settings = json.load(fp)

        dictConfig(settings)
        if name:
            logging.root.name = name


def lookup(properties, *filename):
    """
    Return a the absolute path of the given filename, after looking in the current folder,
    .name folder located in the home folder, package folder or
    the path the filename itself points to

    :param properties
    :param filename:
    :return:
    """

    current = properties.get('current.dir')
    if current:
        url = os.path.join(current, *filename)
        if os.path.isfile(url):
            return url

    home = properties.get('home.dir')
    name = properties.get('app.name')
    if home and name:
        work = '.{}'.format(name)
        url = os.path.join(home, work, *filename)
        if os.path.isfile(url):
            return url

    package = properties.get('package.dir')
    if package:
        url = os.path.join(package, *filename)
        if os.path.isfile(url):
            return url

    url = os.path.join(*filename)
    if os.path.isfile(url):
        return url

    raise FileNotFoundError(FILE_NOT_FOUND.format(str(*filename)))


def load_json(properties, *filename):
    path = lookup(properties, *filename)
    with open(path) as fp:
        properties = json.load(fp)
        return properties


def create_tmp(folder_name, sub_folder_name=None):
    folder = os.path.join(tempfile.gettempdir(), folder_name)
    if sub_folder_name:
        folder = os.path.join(folder, sub_folder_name)

    if not os.path.isdir(folder):
        os.mkdir(folder)
    return folder


def recreate_tmp(folder_name, sub_folder_name=None):
    folder = os.path.join(tempfile.gettempdir(), folder_name)
    if sub_folder_name:
        folder = os.path.join(folder, sub_folder_name)

    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)
    return folder


def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)


