import ast


def get_names(syntax_tree):
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
