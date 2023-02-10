import requests
from bs4 import BeautifulSoup
import sys

class Translator:
    ALL_LANGUAGES = ('Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese',
                     'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish',
                     )

    HEADERS = {"user-agent": "Mozilla/5.0",
               }

    URL = "https://context.reverso.net/translation"

    def __init__(self, lang_in, lang_out, word):
        self.lang_in = lang_in
        self.lang_out = lang_out
        self.word = word

    def translate_all_language(self):
        for language in self.ALL_LANGUAGES:
            if language.lower() != self.lang_in:
                self.lang_out = language
                self.translate(1)

    def _get_bs_req(self):
        url = self.URL
        lang_in = self.lang_in.lower()
        lang_out = self.lang_out.lower()
        word_tr = self.word.lower()
        headers = self.HEADERS
        request = requests.get(f"{url}/{lang_in}-{lang_out}/{word_tr}", headers=headers)
        return BeautifulSoup(request.text, 'lxml')

    def _write_in_file(self, sentences):
        with open(f'{self.word}.txt', 'a', encoding='utf-8') as file:
            for sentence in sentences:
                file.write(sentence)
            file.write('\n')

    def _print_clear_words(self, clear_words, count):
        self._write_in_file(f'{self.lang_out.capitalize()} Translations:')
        words = map(lambda x: f'{x}\n', clear_words[:count])
        self._write_in_file(words)

    def _print_clear_sentences(self, clear_sentences, count):
        self._write_in_file(f'{self.lang_out.capitalize()} Examples:')
        sentences = tuple(zip(clear_sentences[::2], clear_sentences[1::2]))[:count]
        for par in sentences:
            self._write_in_file(map(lambda x: f'{x}\n', par))

    def translate(self, count=5):
        soup = self._get_bs_req()
        words = soup.find_all('span', {'class': 'display-term'})
        sentences = soup.find(id="examples-content").find_all('span', {'class': 'text'})
        clear_words = tuple(map(lambda x: x.get_text(), words))
        clear_sentences = tuple(map(lambda x: x.get_text().strip(), sentences))
        self._print_clear_words(clear_words, count)
        self._print_clear_sentences(clear_sentences, count)


def show_file(file_name):
    with open(f'{file_name}.txt', encoding='utf-8') as file:
        for line in file:
            print(line.strip())


args = sys.argv
in_lang, to_lang, word = args[1:]
translator = Translator(in_lang, to_lang, word)

with open(f'{word}.txt', 'w', encoding='utf-8') as w:
    w.write('')

if to_lang == 'all':
    translator.translate_all_language()
else:
    translator.translate()

show_file(translator.word)