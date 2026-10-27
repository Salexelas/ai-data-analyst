from agents.filters import detect_language_fast


class LanguageService:

    def detect(self, question):

        return detect_language_fast(question)