from facets import Packages
from lib.src_package import get_package_map


def action_find_packages(ctr):
    packages = Packages.get(ctr)
    packages.package_map = get_package_map(packages.root_dir)
