import os
from collections import OrderedDict

import ruamel.yaml


class Report:
    def __init__(self):
        self.text = ""

    def _write(self, x):
        self.text += x + os.linesep

    def add_package(self, package):
        title = package.path or "Root package"
        self.write(title)
        self.write("*" * len(title))
        self.write("")

        for module_name in sorted(package.module_by_name.keys()):
            module = package.module_by_name[module_name]
            self._add_module(module)

    def _add_module(self, module):
        self.write(module.path)
        self.write("-" * len(module.path))
        self.write("")

        for component_name in sorted(module.component_by_name.keys()):
            component = module.component_by_name[component_name]
            self._add_component(component)

    def _add_component(self, component):
        title_template = "Class %s" if component.is_class else "Function %s()"
        title = title_template % component.name
        self.write(title)
        self.write("^" * len(title))
        self.write("")

        domain_concepts = sorted(term.forms[0] for term in component.domain_concepts)
        self.write("Domain concepts:")
        for domain_concept in domain_concepts:
            self.write("- %s" % domain_concept)


def create_report(package_by_path):
    report = Report()

    package_paths = sorted(package_by_path.keys())
    for package_path in package_paths:
        package = package_by_path[package_path]
        report.add_package(package)

    return report.text


def save_report(report, filename):
    with open(filename, "w") as ofs:
        ofs.write(ruamel.yaml.round_trip_dump(report))
