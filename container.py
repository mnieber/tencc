import actions
from facets import Packages, Terms, init_packages, init_terms


class Container:
    def _create_facets(self, root_dir, terms_filename):
        self.packages = init_packages(Packages(), root_dir)
        self.terms = init_terms(Terms(), terms_filename)
        # self.concept_stats = ConceptStats()

    def __init__(self, root_dir, terms_filename):
        self._create_facets(root_dir, terms_filename)

    def run_actions(self):
        __import__('pudb').set_trace()
        actions.packages.action_find_packages(self)

        actions.terms.action_load_terms(self)
        actions.terms.action_add_terms_to_packages(self)

        actions.reporting.action_report_terms(self)
