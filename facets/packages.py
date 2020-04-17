from lib.src_package import get_package_by_path


class Packages():
    root_dir = ""
    package_by_path = {}

    def find_packages(self):
        self.package_by_path = get_package_by_path(self.root_dir)

    @staticmethod
    def get(ctr):
        return ctr.packages


def init_packages(self, root_dir):
    self.root_dir = root_dir
    return self
