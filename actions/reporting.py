import os

from facets import Packages
from lib.report import create_report, save_report


def action_report_terms(ctr):
    packages = Packages.get(ctr)

    report = create_report(packages.package_by_path)
    save_report(report, os.path.join(packages.root_dir, "tencc.rst"))
