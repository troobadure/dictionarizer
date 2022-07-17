import string
import src.filter_lemmas as filter_lemmas
import src.progress_bar as progress_bar
from collections import defaultdict

from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer


progress_bar.printProgressBar(0, 1, length=40)
book = 'Red Rising'
text = open(f'resources/{book}.txt', 'r', encoding='utf-8').read()

punctuation = string.punctuation + '—’“”�'
text = text.translate(str.maketrans(punctuation, ' '*len(punctuation)))

digits = '0123456789'
text = text.translate(str.maketrans('', '', digits))

text = text.lower()

tokens = word_tokenize(text)

stop_words = stopwords.words("english")
tokens = [token for token in tokens if token not in stop_words]

tag_map = defaultdict(lambda : wordnet.NOUN)
tag_map['J'] = wordnet.ADJ
tag_map['V'] = wordnet.VERB
tag_map['R'] = wordnet.ADV

lemmatizer = WordNetLemmatizer()
lemmas = []
for token, tag in pos_tag(tokens):
    lemma = lemmatizer.lemmatize(token, pos=tag_map[tag[0]])
    if lemma not in lemmas:
        lemmas.append(lemma)

lemmas = [lemma for lemma in lemmas if lemma not in stop_words]

filter_lemmas.filter_lemmas_by_words_and_brown(lemmas, book)
filter_lemmas.filter_lemmas_by_frequency(lemmas, book)