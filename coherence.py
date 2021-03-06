import fasttext
from nltk import ngrams
import numpy as np
import pandas as pd 


ftModelFile = "cc.it.300.bin"

print("Loading FastText\n")
model_ft = fasttext.load_model(ftModelFile)

print("Loading stopwords\n")
stopwords = []
with open("stopwords.txt") as file:
    for line in file:
        line = line.strip().lower()
        if len(line) == 0:
            continue
        stopwords.append(line)


def CleanStopWords(sentence):
    sentenceSplitted = sentence.split(" http://dh-server.fbk.eu:19003/simp-engines/tae/simpform")  # METTERE UN VERO TOKENIZZATORE
    sentence = [w for w in sentenceSplitted if w not in stopwords]
    return (sentence)

df_complete = pd.DataFrame()

with open("inputFile/archeo.tsv", "r") as f:
    for line in f:
        parts = line.split("\t")
        
        # DESCRIPTION
        mydesc = parts[1]

        sentencearray = CleanStopWords(mydesc.lower())
        sentence = ' '.join(sentencearray)

        embeddings_descr = model_ft.get_sentence_vector(sentence)

        print(sentence, embeddings_descr[:3])
        print()

        bigrams = ngrams(sentence.split(), 2)
        trigrams = ngrams(sentence.split(), 3)

        for t in trigrams:
            emb = model_ft.get_sentence_vector(''.join(t))
            print(t, emb[:3])

        for b in bigrams:
            emb = model_ft.get_sentence_vector(''.join(b))
            print(b, emb[:3])

        # SUBJECT
        
        mysubj = parts[2]

        subjarray = CleanStopWords(mysubj.lower())
        subject = ' '.join(subjarray)

        embeddings_subj = model_ft.get_sentence_vector(subject)

        print(subject, embeddings_subj[:3])
        print()

        a = embeddings_descr

        b = embeddings_subj

        def cos_sim(a, b):
            dot_product = np.dot(a, b)
            norm_a = np.linalg.norm(a)
            norm_b = np.linalg.norm(b)
            return dot_product / (norm_a * norm_b)

        cosine = [(cos_sim(a,b))]

        print(cosine)
    
        df = pd.DataFrame(cosine)

        df_complete = df_complete.append(df)

    df_complete.to_csv('archeo.csv')

      
        
    

    
