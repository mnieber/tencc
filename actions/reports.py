from facets import Packages, Reports, i_, map_datas, o_
from lib.report import create_reports


def action_generate_reports(ctr):
    def transform(package_by_path, root_paths):
        return create_reports(package_by_path, root_paths)

    return map_datas(
        i_(Packages, "package_by_path"),
        i_(Reports, "root_paths"),
        o_(Reports, "reports"),
        #
        transform=transform,
    )(ctr)
