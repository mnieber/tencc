class Packages():
    root_dir = ""
    package_by_path = {}

    @staticmethod
    def get(ctr):
        return ctr.packages


def init_packages(self, root_dir):
    self.root_dir = root_dir
    return self
