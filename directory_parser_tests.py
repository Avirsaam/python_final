import pytest
import os
from directory_parser import FileSystemObject, argparser, parse_directory
from pytest import fixture

TEST_DIR = 'test_dir'

@pytest.fixture(autouse=True)
def run_around_each_test():

    if not os.path.exists(TEST_DIR):
        os.mkdir(TEST_DIR)

    yield

    if os.path.exists(TEST_DIR):
        os.rmdir(TEST_DIR)



def test_arg_parser():
    command_line_argument = ['good_dir']
    assert argparser(command_line_argument) == 'good_dir'

def test_arg_parser_bad_arguments():
    command_line_argument = ['arg1', 'arg2', 'arg3']
    with pytest.raises(SystemExit):
        result = argparser(command_line_argument)

def test_empty():
    assert parse_directory(TEST_DIR) == []

def test_single_file():
    test_file = os.path.join(TEST_DIR,'test_file.txt')
    f = open(test_file, 'w')
    result = parse_directory(TEST_DIR)
    os.remove(test_file)
    assert result == [FileSystemObject(node_name='test_file', extension='txt', is_dir=False, parent_name='test_dir')]

def test_empty_dir():
    empty_dir = os.path.join(TEST_DIR, 'empty_dir')
    if not os.path.exists(empty_dir):
        os.mkdir(empty_dir)
    result = parse_directory(TEST_DIR)
    os.rmdir(empty_dir)
    assert result == [FileSystemObject(node_name='empty_dir', extension='', is_dir=True, parent_name='test_dir')]

def test_single_file_in_sub_dir():
    empty_dir = os.path.join(TEST_DIR, 'empty_dir')
    if not os.path.exists(empty_dir):
        os.mkdir(empty_dir)

    test_file = os.path.join(empty_dir, 'test_file.txt')
    f = open(test_file, 'w')

    result = parse_directory(TEST_DIR)

    os.remove(test_file)
    os.rmdir(empty_dir)
    assert result == [FileSystemObject(node_name='empty_dir', extension='', is_dir=True, parent_name='test_dir'),\
                      FileSystemObject(node_name='test_file', extension='txt', is_dir=False, parent_name='empty_dir')]

