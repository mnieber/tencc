from concepts import add_concepts, load_concept_list
from facets import Concepts, Packages, i_, map_datas, o_


def action_load_concepts(ctr):
    def transform(
        concept_list_filename,
    ):
        return (load_concept_list(concept_list_filename),)

    return map_datas(i_(Concepts, "concept_list_filename"),
                     o_(Concepts, 'concept_list'),
                     transform=transform)(ctr)


def action_add_concepts_to_packages(ctr):
    def transform(
        package_map,
        concept_list,
    ):
        for package in package_map.values():
            add_concepts(package, concept_list)

    return map_datas(i_(Packages, "package_map"),
                     i_(Concepts, 'concept_list'),
                     transform=transform)(ctr)
