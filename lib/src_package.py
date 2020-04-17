import ast
import glob
import os

from lib.utils import propOrCreate


def _get_syntax_tree(filename):
    with open(filename) as ifs:
        return ast.parse(ifs.read())


def _create_module(module_filename, root_dir):
    def _module_import_path():
        relpath = os.path.relpath(module_filename, root_dir)
        return os.path.splitext(relpath)[0].replace("/", ".")

    return Module(_module_import_path(), _get_syntax_tree(module_filename))


def _get_component_map(syntax_tree):
    component_map = dict()

    for node in syntax_tree.body:
        is_class = isinstance(node, ast.ClassDef)
        is_function = isinstance(node, ast.FunctionDef)
        if is_class or is_function:
            component_map[node.name] = Component(node.name, node, is_class)

    return component_map


class Component:
    def __init__(self, name, syntax_tree_node, is_class):
        self.name = name
        self.is_class = is_class
        self.syntax_tree_node = syntax_tree_node
        self.domain_concepts = []
        self.tech_terms = []


class Module:
    def __init__(self, path, syntax_tree):
        self.path = path
        self.syntax_tree = syntax_tree
        self.component_map = _get_component_map(syntax_tree)


class Package:
    def __init__(self, path):
        self.path = path
        self.modules = []


def get_package_map(root_dir):
    package_map = {}

    pattern = os.path.join(os.path.abspath(root_dir), "**/*.py")
    for module_filename in glob.glob(pattern, recursive=True):
        rel_module_filename = os.path.relpath(module_filename, root_dir)
        module = _create_module(module_filename, root_dir)

        __import__('pudb').set_trace()
        package_path = os.path.dirname(rel_module_filename)
        package = propOrCreate(lambda x: Package(x), package_path, package_map)
        package.modules.append(module)

    return package_map
