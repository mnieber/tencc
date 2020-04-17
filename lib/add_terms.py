from lib.names import get_names
from lib.term_book import TermList


def _get_terms(names, term_list: TermList):
    result = list()
    for name in names:
        term = term_list.find_term_by_name(name)
        if term:
            result.append(term)
    return result


def add_terms(package, term_book):
    for module in package.module_by_path.values():
        for component in module.component_by_name.values():
            names = get_names(component.syntax_tree)
            component.domain_concepts = _get_terms(names, term_book.domain_concepts)
            component.tech_terms = _get_terms(names, term_book.tech_terms)
