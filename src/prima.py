import string
import src.progress_bar as progress_bar
from collections import defaultdict

from nltk import pos_tag, word_tokenize, FreqDist
from nltk.corpus import wordnet, stopwords, brown, words
from nltk.stem import WordNetLemmatizer


progress_bar.printProgressBar(0, 1, length=40)
book = 'Red Rising'
text = open(f'resources/{book}.txt', 'r', encoding='utf-8').read()
stats = open(f'resources/results/{book}.txt', 'w', encoding='utf-8')

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

words_words = words.words()
words_lemmas = []
lemmas_len = len(lemmas)
words_trash = []
for index, lemma in enumerate(lemmas):
    if lemma in words_words:
        words_lemmas.append(lemma)
    else:
        words_trash.append(lemma)
    progress_bar.printProgressBar(index+1, lemmas_len, length=40)

print('LEMMAS: ', lemmas_len)
print('WORD LEMMAS: ', len(words_lemmas))
print('TRASH LEMMAS: ', len(words_trash))

stats.write(f'LEMMAS: {lemmas_len}\n')
stats.write(f'WORD LEMMAS: {len(words_lemmas)}\n')
stats.write(f'TRASH LEMMAS: {len(words_trash)}\n')
stats.close()

with open(f'resources/results/{book}-trash.txt', 'w', encoding='utf-8') as f:
    f.writelines([lemma + '\n' for lemma in words_trash])

lemmas_brown = [word.lower() for word in brown.words() if word.lower() in words_lemmas]
lemmas_freq = FreqDist(lemmas_brown)

with open(f'resources/results/{book}-lemmas.txt', 'w', encoding='utf-8') as f:
    f.writelines(['{0:20}{1:20}\n'.format(lemma[0],lemma[1]) 
                    for lemma in lemmas_freq.most_common()])

