import actions
from facets import Concepts, Packages, init_concepts, init_packages


class Container:
    def _create_facets(self, root_dir, concept_list_filename):
        self.packages = init_packages(Packages(), root_dir)
        self.concepts = init_concepts(Concepts(), concept_list_filename)
        # self.concept_stats = ConceptStats()

    def __init__(self, root_dir, concept_list_filename):
        self._create_facets(root_dir, concept_list_filename)

    def run_actions(self):
        actions.packages.action_find_packages(self)

        actions.concepts.action_load_concepts(self)
        actions.concepts.action_add_concepts_to_packages(self)
