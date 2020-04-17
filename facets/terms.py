from lib.term_book import TermBook


class Terms():
    def __init__(self):
        self.terms_filename = ""
        self.term_book = TermBook()

    def load_terms(self):
        self.term_book.load(self.terms_filename)

    @staticmethod
    def get(ctr):
        return ctr.terms


def init_terms(self, terms_filename):
    self.terms_filename = terms_filename
    return self
