from facets import Packages, Terms, i_, io_, map_datas
from lib.add_terms import add_terms


def action_add_terms_to_packages(ctr):
    def transform(package_by_path, term_book):
        for package in package_by_path.values():
            add_terms(package, term_book)

    return map_datas(
        i_(Packages, "package_by_path"),
        io_(Terms, "term_book"),
        #
        transform=transform,
    )(ctr)
