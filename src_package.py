import ast
import glob
import os


def _get_st(filename):
    with open(filename) as ifs:
        return ast.parse(ifs.read())


def _module_import_path(full_module_filename, root_dir):
    relpath = os.path.relpath(full_module_filename, root_dir)
    return os.path.splitext(relpath)[0].replace("/", ".")


def _create_module(full_module_filename, root_dir):
    module_import_path = _module_import_path(full_module_filename, root_dir)
    return Module(module_import_path, _get_st(full_module_filename))


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
        self.concepts = []


class Module:
    def __init__(self, filename, syntax_tree):
        self.filename = filename
        self.syntax_tree = syntax_tree
        self.component_map = _get_component_map(syntax_tree)


class Package:
    def __init__(self, path):
        self.path = path
        self.modules = []


def get_package_map(root_dir):
    package_map = {}

    pattern = os.path.join(os.path.abspath(root_dir), "**/*.py")
    full_module_filenames = glob.glob(pattern, recursive=True)

    for full_module_filename in full_module_filenames:
        module = _create_module(full_module_filename, root_dir)
        package_path = os.path.dirname(module.filename)
        if package_path not in package_map:
            package_map[package_path] = Package(package_path)
        package_map[package_path].modules.append(module)

    return package_map
