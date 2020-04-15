import ast

import ruamel.yaml


def load_concept_list(filename):
    with open(filename) as f:
        return ruamel.yaml.round_trip_load(f.read())['concepts']


def _get_names(syntax_tree):
    result = []

    class VisitClasses(ast.NodeVisitor):
        def visit_Name(self, node):  # noqa
            result.append(node.id)
            ast.NodeVisitor.generic_visit(self, node)

    v = VisitClasses()
    v.visit(syntax_tree)
    return result


def _get_concepts(names, concept_list):
    result = list()
    for concept in concept_list:
        for name in names:
            if name in concept["forms"]:
                result.append(concept)
                break
    return result


def add_concepts(package, concept_list):
    for module in package.modules:
        names = _get_names(module.syntax_tree)
        module.concepts = _get_concepts(names, concept_list)
