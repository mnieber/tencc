from argparse import ArgumentParser
import inspect
import ast
import glob
import os
# import sys
import ruamel.yaml


class Visit(ast.NodeVisitor):
    def generic_visit(self, node):
        print(node)
        ast.NodeVisitor.generic_visit(self, node)


def doit():
    src = inspect.getsource(eval('Foo'))
    st = ast.parse(src)
    print(st)


def get_st(filename):
    with open(filename) as ifs:
        return ast.parse(ifs.read())


def _get_class_map(source_tree, module_import_path, root_dir):
    class_map = dict()

    top_level_classes = [n for n in source_tree.body if isinstance(n, ast.ClassDef)]
    for class_node in top_level_classes:
        class_map[class_node.name] = Class(class_node.name, class_node)

    return class_map


class Module:
    def __init__(self, filename, st, class_map):
        self.filename = filename
        self.st = st
        self.class_map = class_map
        self.concepts = []


class Package:
    def __init__(self, path):
        self.path = path
        self.modules = []


class Class:
    def __init__(self, name, st_node):
        self.name = name
        self.st_node = st_node
        self.concepts = []


def _module_import_path(full_module_filename, root_dir):
    relpath = os.path.relpath(full_module_filename, root_dir)
    return os.path.splitext(relpath)[0].replace('/', '.')


def create_module(full_module_filename, root_dir):
    __import__('pudb').set_trace()
    module_import_path = _module_import_path(full_module_filename, root_dir)
    st = get_st(full_module_filename)
    class_map = _get_class_map(st, module_import_path, root_dir)
    module = Module(module_import_path, st, class_map)
    return module


def get_package_map(root_dir):
    packages = dict()
    pattern = os.path.join(os.path.abspath(root_dir), '**/*.py')
    full_module_filenames = glob.glob(pattern, recursive=True)

    for full_module_filename in full_module_filenames:
        module = create_module(full_module_filename, root_dir)

        package_path = os.path.dirname(module.filename)
        if package_path not in packages:
            packages[package_path] = Package(package_path)
        package = packages[package_path]
        package.modules.append(module)

    return packages


def _get_classes(source_tree):
    result = []

    class VisitClasses(ast.NodeVisitor):
        def visit_ClassDef(self, node):  # noqa
            result.append(node.name)
            ast.NodeVisitor.generic_visit(self, node)

    v = VisitClasses()
    v.visit(source_tree)
    return result


def read_concept_list(filename):
    with open(filename) as f:
        return ruamel.yaml.round_trip_load(f.read())


def _args():  # noqa
    parser = ArgumentParser(description=(''))

    parser.add_argument('concept_list')
    parser.add_argument('root_dir')
    return parser.parse_args()


if __name__ == '__main__':
    args = _args()

    concepts = read_concept_list(args.concept_list)
    package_map = get_package_map(args.root_dir)
    print(package_map.keys())
