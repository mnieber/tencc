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
            super(VisitClasses, self).generic_visit(node)

        def visit_ClassDef(self, node):  # noqa
            result.append(node.name)
            super(VisitClasses, self).generic_visit(node)

        def visit_FunctionDef(self, node):  # noqa
            result.append(node.name)
            super(VisitClasses, self).generic_visit(node)

        def visit_Attribute(self, node):  # noqa
            result.append(node.attr)
            super(VisitClasses, self).generic_visit(node)

        def visit_arg(self, node):  # noqa
            result.append(node.arg)
            super(VisitClasses, self).generic_visit(node)

        def generic_visit(self, node):  # noqa
            super(VisitClasses, self).generic_visit(node)

    v = VisitClasses()
    v.visit(syntax_tree)
    return result


def _get_concepts(names, concept_list):
    result = list()
    for concept in concept_list:
        for name in names:
            print(name)
            if name in concept["forms"]:
                result.append(concept)
                break
    return result


def add_concepts(package, concept_list):
    for module in package.modules:
        names = _get_names(module.syntax_tree)
        module.concepts = _get_concepts(names, concept_list)
