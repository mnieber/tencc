import ruamel.yaml

from names import get_names


def load_concept_list(filename):
    with open(filename) as f:
        return ruamel.yaml.round_trip_load(f.read())['concepts']


def _get_concepts(names, concept_list):
    result = list()
    for concept in concept_list:
        for name in names:
            print(name)
            if name in concept["forms"]:
                result.append(concept)
                break
    return result


def add_concepts(package, concept_list):
    for module in package.modules:
        names = get_names(module.syntax_tree)
        module.concepts = _get_concepts(names, concept_list)
