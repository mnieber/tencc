from facets import Packages, i_, map_datas, o_
from src_package import get_package_map


def action_find_packages(ctr):
    def transform(
        root_dir,
    ):
        return (get_package_map(root_dir),)

    return map_datas(i_(Packages, "root_dir"),
                     o_(Packages, 'package_map'),
                     transform=transform)(ctr)
