from argparse import ArgumentParser

from container import Container


def _args():  # noqa
    parser = ArgumentParser(description=(""))

    parser.add_argument("terms_filename")
    parser.add_argument("root_dir")
    return parser.parse_args()


if __name__ == "__main__":
    args = _args()

    container = Container(args.root_dir, args.terms_filename)
    container.run_actions()
    print(container.packages.package_map.keys())
