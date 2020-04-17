import glob
import os
from collections import defaultdict

from lib.utils import import_path, values_sorted_on_key


class Report:
    def __init__(self, rel_path):
        self.rel_path = rel_path
        self._init_text()

    def _init_text(self):
        title = "Packages"
        self.text = ""
        self._write("#" * len(title))
        self._write(title)
        self._write("#" * len(title))
        self._write("")

    def _write(self, x):
        self.text += x + os.linesep

    def _rel_path(self, path):
        return os.path.relpath(path, self.rel_path)

    def add_package(self, package):
        memo = self.text
        rel_path = self._rel_path(package.rel_path)

        title = (
            "Root package"
            if rel_path == "."
            else "Package %s" % import_path(rel_path, "")
        )
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

        title = "Module %s" % self._rel_path(module.rel_path)
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


def find_report_paths(root_dir):
    report_paths = ["."]
    pattern = os.path.join(root_dir, "**/tencc.rst")
    for subreport_filename in glob.glob(pattern, recursive=True):
        report_path = os.path.relpath(os.path.dirname(subreport_filename), root_dir)
        if report_path not in report_paths:
            report_paths.append(report_path)
    return report_paths


def _get_report_path(path, report_paths):
    best_path = ""
    for report_path in report_paths:
        if report_path == "." or path.startswith(report_path):
            if len(report_path) > len(best_path):
                best_path = report_path
    return best_path


def create_reports(package_by_path, report_paths):
    reports = []

    package_by_path_by_report_path = defaultdict(lambda: dict())
    for path, package in package_by_path.items():
        report_path = _get_report_path(path, report_paths)
        pbp = package_by_path_by_report_path[report_path]
        pbp[path] = package

    for report_path in report_paths:
        pbp = package_by_path_by_report_path[report_path]

        report = Report(report_path)
        reports.append(report)

        package_paths = sorted(pbp.keys())
        for package_path in package_paths:
            package = package_by_path[package_path]
            report.add_package(package)

    return reports


def save_report(report, root_dir):
    filename = os.path.join(root_dir, report.rel_path, "tencc.rst")
    with open(filename, "w") as ofs:
        ofs.write(report.text)
