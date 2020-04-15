class Concepts():
    concept_list_filename = ""
    concept_list = []

    @staticmethod
    def get(ctr):
        return ctr.concepts


def init_concepts(self, concept_list_filename):
    self.concept_list_filename = concept_list_filename
    return self
