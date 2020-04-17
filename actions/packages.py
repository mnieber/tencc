from facets import Packages
from lib.src_package import get_package_by_path


def action_find_packages(ctr):
    packages = Packages.get(ctr)
    packages.package_by_path = get_package_by_path(packages.root_dir)
