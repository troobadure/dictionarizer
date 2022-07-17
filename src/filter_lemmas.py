import src.progress_bar as progress_bar

from nltk import FreqDist
from nltk.corpus import brown, words


def filter_lemmas_by_words_and_brown(lemmas, book):

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

    with open(f'resources/results/{book}-wordbrown.txt', 'w', encoding='utf-8') as stats:
        stats.write(f'LEMMAS: {lemmas_len}\n')
        stats.write(f'WORD LEMMAS: {len(words_lemmas)}\n')
        stats.write(f'TRASH LEMMAS: {len(words_trash)}\n')
        stats.close()

    with open(f'resources/results/{book}-wordbrown-trash.txt', 'w', encoding='utf-8') as f:
        f.writelines([lemma + '\n' for lemma in words_trash])

    brown_freq = FreqDist(brown.words())
    lemmas_freq = {lemma: brown_freq[lemma] for lemma in words_lemmas}

    with open(f'resources/results/{book}-wordbrown-lemmas.txt', 'w', encoding='utf-8') as f:
        f.writelines(['{0:20}{1:20}\n'.format(lemma[0],lemma[1]) 
                        for lemma in sorted(lemmas_freq.items(), key=lambda item: item[1], reverse=True)])


def filter_lemmas_by_frequency(lemmas, book):

    frequencies = {}
    with open("resources/corpora/en.txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            word, freq = line.split()
            frequencies[word] = int(freq)


    words = frequencies.keys()
    words_lemmas = []
    lemmas_len = len(lemmas)
    words_trash = []
    for index, lemma in enumerate(lemmas):
        if lemma in words:
            words_lemmas.append(lemma)
        else:
            words_trash.append(lemma)
        progress_bar.printProgressBar(index+1, lemmas_len, length=40)

    print('LEMMAS: ', lemmas_len)
    print('WORD LEMMAS: ', len(words_lemmas))
    print('TRASH LEMMAS: ', len(words_trash))

    with open(f'resources/results/{book}-frequency.txt', 'w', encoding='utf-8') as stats:
        stats.write(f'LEMMAS: {lemmas_len}\n')
        stats.write(f'WORD LEMMAS: {len(words_lemmas)}\n')
        stats.write(f'TRASH LEMMAS: {len(words_trash)}\n')
        stats.close()

    with open(f'resources/results/{book}-frequency-trash.txt', 'w', encoding='utf-8') as f:
        f.writelines([lemma + '\n' for lemma in words_trash])

    lemmas_freq = {lemma: frequencies[lemma] for lemma in words_lemmas}
    
    with open(f'resources/results/{book}-frequency-lemmas.txt', 'w', encoding='utf-8') as f:
        f.writelines(['{0:20}{1:20}\n'.format(lemma[0],lemma[1]) 
                        for lemma in sorted(lemmas_freq.items(), 
                                            key=lambda item: item[1],
                                            reverse=True)])
