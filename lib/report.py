import glob
import os
from collections import defaultdict

from lib.utils import import_path, values_sorted_on_key


class Report:
    def __init__(self):
        self.text = ""

    def _write(self, x):
        self.text += x + os.linesep

    def add_package(self, package):
        memo = self.text

        title = "Package %s" % package.path if package.path else "Root package"
        self._write(title)
        self._write("*" * len(title))
        self._write("")

        has_content = False
        modules = values_sorted_on_key(package.module_by_path)
        for module in modules:
            if self._add_module(module):
                has_content = True
        if not has_content:
            self.text = memo
        return has_content

    def _add_module(self, module):
        memo = self.text

        title = "Module %s" % module.path
        self._write(title)
        self._write("-" * len(title))
        self._write("")

        has_content = False
        components = values_sorted_on_key(module.component_by_name)
        for component in components:
            if self._add_component(component):
                has_content = True

        if not has_content:
            self.text = memo
        return has_content

    def _add_component(self, component):
        domain_concepts = sorted(term["forms"][0] for term in component.domain_concepts)
        has_content = bool(domain_concepts)
        if has_content:
            title_template = "class %s" if component.is_class else "def %s()"
            title = title_template % component.name
            self._write(title)
            self._write("^" * len(title))
            self._write("")

            self._write("Domain concepts:")
            for domain_concept in domain_concepts:
                self._write("- %s" % domain_concept)
            self._write("")
        return has_content


def _find_root_paths(root_dir):
    root_paths = [""]
    pattern = os.path.join(os.path.abspath(root_dir), "**/tencc.rst")
    for subreport_filename in glob.glob(pattern, recursive=True):
        root_paths.append(import_path(os.path.dirname(subreport_filename), root_dir))
    return root_paths


def _get_root_path(path, root_paths):
    best_path = ""
    for root_path in root_paths:
        if path.startswith(root_path):
            if len(root_path) > len(best_path):
                best_path = root_path
    return best_path


def create_reports(package_by_path, root_paths):
    reports = []

    package_by_path_by_root_path = defaultdict(lambda: dict())
    for path, package in package_by_path.items():
        root_path = _get_root_path(path, root_paths)
        pbp = package_by_path_by_root_path[root_path]
        pbp[path] = package

    for root_path in root_paths:
        pbp = package_by_path_by_root_path[root_path]

        report = Report(root_path)
        reports.append(report)

        package_paths = sorted(pbp.keys())
        for package_path in package_paths:
            package = package_by_path[package_path]
            report.add_package(package)

    return reports


def save_report(report, filename):
    with open(filename, "w") as ofs:
        ofs.write(report)
