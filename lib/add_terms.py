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
    for module in package.modules:
        names = get_names(module.syntax_tree)
        module.domain_concepts = _get_terms(names, term_book.domain_concepts)
        module.tech_terms = _get_terms(names, term_book.tech_terms)
