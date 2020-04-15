import ast
from argparse import ArgumentParser

from container import Container


def _get_class_map(source_tree, module_import_path, root_dir):
    class_map = dict()

    top_level_classes = [n for n in source_tree.body if isinstance(n, ast.ClassDef)]
    for class_node in top_level_classes:
        class_map[class_node.name] = Class(class_node.name, class_node)

    return class_map


class Class:
    def __init__(self, name, st_node):
        self.name = name
        self.st_node = st_node
        self.concepts = []


def _args():  # noqa
    parser = ArgumentParser(description=(""))

    parser.add_argument("concept_list")
    parser.add_argument("root_dir")
    return parser.parse_args()


if __name__ == "__main__":
    args = _args()

    container = Container(args.root_dir, args.concept_list)
    container.run_actions()
    print(container.packages.package_map.keys())
