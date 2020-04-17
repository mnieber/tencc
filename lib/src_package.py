import ast
import glob
import os

from lib.utils import import_path, propOrCreate


def _get_syntax_tree(filename):
    with open(filename) as ifs:
        return ast.parse(ifs.read())


def _create_module(module_filename, root_dir):
    return Module(
        import_path(module_filename, root_dir), _get_syntax_tree(module_filename)
    )


def _get_component_by_name(syntax_tree):
    component_by_name = dict()

    for node in syntax_tree.body:
        is_class = isinstance(node, ast.ClassDef)
        is_function = isinstance(node, ast.FunctionDef)
        if is_class or is_function:
            component_by_name[node.name] = Component(node.name, node, is_class)

    return component_by_name


# A component is a top-level function or class
class Component:
    def __init__(self, name, syntax_tree, is_class):
        self.name = name
        self.is_class = is_class
        self.syntax_tree = syntax_tree
        self.domain_concepts = []
        self.tech_terms = []


class Module:
    def __init__(self, path, syntax_tree):
        self.path = path
        self.syntax_tree = syntax_tree
        self.component_by_name = _get_component_by_name(syntax_tree)


class Package:
    def __init__(self, path):
        self.path = path
        self.module_by_path = {}


def get_package_by_path(root_dir):
    package_by_path = {}

    pattern = os.path.join(os.path.abspath(root_dir), "**/*.py")
    for module_filename in glob.glob(pattern, recursive=True):
        module = _create_module(module_filename, root_dir)

        package_path = import_path(os.path.dirname(module_filename), root_dir)
        package = propOrCreate(lambda x: Package(x), package_path, package_by_path)
        package.module_by_path[package_path] = module

    return package_by_path
