import gensim
import numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords


def compare(data1, data2):
    sent1 = []
    sent2 = []
    avg_simscore = []
    stop_words = set(stopwords.words('english'))
    word_tokens1 = word_tokenize(data1)
    word_tokens2 = word_tokenize(data2)
    filtered_sentence1 = []
    filtered_sentence2 = []
    for w in word_tokens1:
        if w not in stop_words:
            filtered_sentence1.append(w)

    for w in word_tokens2:
        if w not in stop_words:
            filtered_sentence2.append(w)

    data1 = ' '.join(filtered_sentence1)
    data2 = ' '.join(filtered_sentence2)
    # print(data1)
    # print(data2)
    if len(data1) < len(data2):
        data1, data2 = data2, data1
    tokens = sent_tokenize(data1)
    for line in tokens:
        sent1.append(line)
    gen_docs = [[w.lower() for w in word_tokenize(text)]
                for text in sent1]
    dictionary = gensim.corpora.Dictionary(gen_docs)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    tf_idf = gensim.models.TfidfModel(corpus)
    sims = gensim.similarities.Similarity('workdir', tf_idf[corpus],
                                          num_features=len(dictionary))
    tokens = sent_tokenize(data2)
    for line in tokens:
        sent2.append(line)
    for line in sent2:
        query_doc = [w.lower() for w in word_tokenize(line)]
        query_doc_bow = dictionary.doc2bow(query_doc)
        query_doc_tf_idf = tf_idf[query_doc_bow]
        sum_of_sims = (np.sum(sims[query_doc_tf_idf], dtype=np.float32))
        avg = sum_of_sims / len(sent1)
        avg_simscore.append(avg)
        total_avg = np.sum(avg_simscore, dtype=np.float)
        percentage_of_similarity = round(float(total_avg) * 100)
        if percentage_of_similarity >= 100:
            percentage_of_similarity = 100
    return percentage_of_similarity
