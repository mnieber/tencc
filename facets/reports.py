from lib.report import find_report_paths, save_report


class Reports():
    def __init__(self):
        self.root_dir = ""
        self.reset_report_paths()
        self.reports = []

    def reset_report_paths(self):
        self.report_paths = ["."]

    def find_report_paths(self):
        self.report_paths = find_report_paths(self.root_dir)

    def save_reports(self):
        for report in self.reports:
            save_report(report, self.root_dir)

    @staticmethod
    def get(ctr):
        return ctr.reports


def init_reports(self, root_dir):
    self.root_dir = root_dir
    return self
