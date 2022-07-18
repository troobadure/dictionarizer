from fnmatch import translate
import string
import src.filter_lemmas as filter_lemmas
import src.translate as translate
import src.progress_bar as progress_bar
from collections import defaultdict

from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer


book = 'Red Rising'
ADD_TOS = False


progress_bar.printProgressBar(0, 1, length=30, prefix='PREP')
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

wordbrown_freqs = filter_lemmas.filter_lemmas_by_words_and_brown(lemmas, book)
frequency_freqs = filter_lemmas.filter_lemmas_by_frequency(lemmas, book)

if ADD_TOS:
    words, freqs = zip(*wordbrown_freqs)
    words = ['to ' + word if tag_map[tag[0]] == wordnet.VERB 
                else word for word, tag in pos_tag(words)]
    wordbrown_freqs = list(zip(words, freqs))
    
    words, freqs = zip(*frequency_freqs)
    words = ['to ' + word if tag_map[tag[0]] == wordnet.VERB 
                else word for word, tag in pos_tag(words)]
    frequency_freqs = list(zip(words, freqs))

wordbrown_trans = translate.translate_lemmas(wordbrown_freqs, book, 'wordbrown')
frequency_trans = translate.translate_lemmas(frequency_freqs, book, 'frequency')
