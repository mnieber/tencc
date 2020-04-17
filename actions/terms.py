from facets import Packages, Terms, i_, map_datas
from lib.add_terms import add_terms


def action_load_terms(ctr):
    terms = Terms.get(ctr)
    terms.term_book.load(terms.terms_filename)


def action_add_terms_to_packages(ctr):
    def transform(
        package_map, term_book,
    ):
        for package in package_map.values():
            add_terms(package, term_book)

    return map_datas(
        i_(Packages, "package_map"),
        i_(Terms, "term_book"),
        #
        transform=transform
    )(ctr)
