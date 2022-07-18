from googletrans import Translator
import src.progress_bar as progress_bar
import src.chunks as chunks

def translate_lemmas(lemmas_freqs, book, subnaming):

    progress_bar.printProgressBar(0, 1, length=30, prefix='TRANS')

    translator = Translator()

    translations = []
    no_translations = []
    chunks_count = chunks.count(lemmas_freqs, 1000)
    for index, words_chunk in enumerate(chunks.chunks(lemmas_freqs, 1000)):
        words, freqs = zip(*words_chunk)

        origin = '\n'.join(words)
        trans = translator.translate(origin, src='en', dest='uk').text

        translations_chunk = list(zip(words, freqs, trans.split('\n')))

        translations += [(src, dest, freq) for src, freq, dest in translations_chunk if src != dest]
        no_translations += [(src, freq) for src, freq, dest in translations_chunk if src == dest]
        progress_bar.printProgressBar(index+1, chunks_count, length=30, prefix='TRANS')

    with open(f"resources/results/{book}-{subnaming}-trans.txt", 'w', encoding='utf-8') as f:
        f.writelines(['{0:20}{1:20}{2:20}\n'.format(*trans) for trans in translations])

    with open(f"resources/results/{book}-{subnaming}-notrans.txt", 'w', encoding='utf-8') as f:
        f.writelines(['{0:20}{1:20}\n'.format(*word) for word in no_translations])

    with open(f'resources/results/{book}-{subnaming}-stats.txt', 'a', encoding='utf-8') as stats:
        stats.write(f'NOTRANS LEMMAS: {len(no_translations)}\n')

    return translations