import sys
from argparse import ArgumentParser

import actions
from container import Container


def _args():  # noqa
    parser = ArgumentParser(description=(""))

    parser.add_argument("terms_filename")
    parser.add_argument("root_dir")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--ignore-subreports", action="store_true")
    group.add_argument("--recreate-subreports", action="store_true")
    return parser.parse_args()


def _exit():
    print(
        "Subreports were found. "
        + "Please specify either --ignore-subreports or --recreate-subreports"
    )
    sys.exit(1)


if __name__ == "__main__":
    __import__("pudb").set_trace()
    args = _args()
    ctr = Container(args.root_dir, args.terms_filename)

    ctr.packages.find_packages()
    ctr.terms.load_terms()
    ctr.reports.find_report_paths()

    if len(ctr.reports.report_paths) > 1:
        if args.ignore_subreports:
            ctr.reports.reset_report_paths()
        elif not args.recreate_subreports:
            _exit()

    actions.terms.action_add_terms_to_packages(ctr)
    actions.reports.action_generate_reports(ctr)

    ctr.reports.save_reports()

    print(ctr.packages.package_by_path.keys())
