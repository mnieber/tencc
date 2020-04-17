import ruamel.yaml


class TermList:
    def __init__(self, terms):
        self.terms = terms

    def find_term_by_name(self, name):
        for term in self.terms:
            if name in term["forms"]:
                return term
        return None


class TermBook:
    def __init__(self):
        self.domain_concepts = None
        self.tech_terms = None

    def load(self, filename):
        with open(filename) as f:
            data = ruamel.yaml.round_trip_load(f.read())
            self.domain_concepts = TermList(data["domain_concepts"])
            self.tech_terms = TermList(data["tech_terms"])
