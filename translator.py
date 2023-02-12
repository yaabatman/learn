import requests
from bs4 import BeautifulSoup
import sys


class UndetectedLanguage(Exception):
    pass


class NotConnection(Exception):
    pass


class UndetectedWord(Exception):
    pass


class Translator:

    def __init__(self, lang_in, lang_out, word_t, all_languages_t, headers_t, url_t):
        self.lang_in = lang_in
        self.lang_out = lang_out
        self.word = word_t
        self.all_languages = all_languages_t
        self.headers = headers_t
        self.URL = url_t

    def translate_all_languages(self):
        for language in self.all_languages:
            if language.lower() not in (self.lang_in, 'all'):
                self.lang_out = language.lower()
                self.translate(1)

    def _get_bs_req(self):
        url = self.URL
        lang_in = self.lang_in
        lang_out = self.lang_out
        word_tr = self.word
        headers_get = self.headers
        request = requests.get(f"{url}/{lang_in}-{lang_out}/{word_tr}", headers=headers_get)
        if request.status_code == 404:
            raise UndetectedWord
        elif request.status_code == 500:
            raise NotConnection('Something wrong with your internet connection')
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


def write_in_file(word):
    with open(f'{word}.txt', 'w', encoding='utf-8') as w:
        w.write('')


def check_lang(*args):
    for lang in args:
        if lang.capitalize() not in all_languages:
            raise UndetectedLanguage(f"Sorry, the program doesn't support {lang}")


def enter_data():
    args = sys.argv
    in_lang, to_lang, word = map(lambda x: x.lower(), args[1:])
    try:
        check_lang(in_lang, to_lang)
        translator = Translator(in_lang, to_lang, word, all_languages, headers, URL)
        write_in_file(word)

        if to_lang == 'all':
            translator.translate_all_languages()
        else:
            translator.translate()

        show_file(translator.word)
    except UndetectedWord:
        print(f'Sorry, unable to find {word}')
    except (UndetectedLanguage, NotConnection) as err:
        print(err)


all_languages = ('Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese',
                 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish', 'All'
                 )

headers = {"user-agent": "Mozilla/5.0",
           }

URL = "https://context.reverso.net/translation"

enter_data()
