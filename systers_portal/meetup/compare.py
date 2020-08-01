import gensim
import numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords


def clean(word_tokens):
    """Cleaning Data for tf-idf"""
    filtered_sentence = []
    stop_words = set(stopwords.words('english'))
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    data = ' '.join(filtered_sentence)
    return data


def sentence_tokenize(data):
    """Tokenize text into sentences"""
    sent = []
    tokens = sent_tokenize(data)
    for line in tokens:
        sent.append(line)
    return sent


def compare(data1, data2):
    """Calculate and Return percentage similarity"""
    sent1 = []
    sent2 = []
    avg_simscore = []
    word_tokens1 = word_tokenize(data1)
    word_tokens2 = word_tokenize(data2)
    data1 = clean(word_tokens1)
    data2 = clean(word_tokens2)
    if len(data1) < len(data2):
        data1, data2 = data2, data1
    sent1 = sentence_tokenize(data1)
    sent2 = sentence_tokenize(data2)
    gen_docs = [[w.lower() for w in word_tokenize(text)]
                for text in sent1]
    dictionary = gensim.corpora.Dictionary(gen_docs)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    # Creating tf-df document and similarity object to compare with the other tf-idf document
    tf_idf = gensim.models.TfidfModel(corpus)
    sims = gensim.similarities.Similarity('workdir', tf_idf[corpus],
                                          num_features=len(dictionary))
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
