from argparse import ArgumentParser

from container import Container


def _args():  # noqa
    parser = ArgumentParser(description=(""))

    parser.add_argument("concept_list")
    parser.add_argument("root_dir")
    return parser.parse_args()


if __name__ == "__main__":
    args = _args()

    __import__("pudb").set_trace()
    container = Container(args.root_dir, args.concept_list)
    container.run_actions()
    print(container.packages.package_map.keys())
