from lib.report import find_root_paths, save_report


class Reports():
    def __init__(self):
        self.root_dir = ""
        self.reset_root_paths()
        self.reports = []

    def reset_root_paths(self):
        self.root_paths = ["."]

    def find_root_paths(self):
        self.root_paths = find_root_paths(self.root_dir)

    def save_reports(self):
        for report in self.reports:
            save_report(report)

    @staticmethod
    def get(ctr):
        return ctr.reports


def init_reports(self, root_dir):
    self.root_dir = root_dir
    return self
