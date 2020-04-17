from facets import (Packages, Reports, Terms, init_packages, init_reports,
                    init_terms)


class Container:
    def _create_facets(self, root_dir, terms_filename):
        self.packages = init_packages(Packages(), root_dir)
        self.terms = init_terms(Terms(), terms_filename)
        self.reports = init_reports(Reports(), root_dir)
        # self.concept_stats = ConceptStats()

    def __init__(self, root_dir, terms_filename):
        self._create_facets(root_dir, terms_filename)
