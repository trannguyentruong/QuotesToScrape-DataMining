import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sys
sys.stdout.reconfigure(encoding='utf-8')

data = pd.read_csv('Quote.csv')

authors = data['Author'].tolist()

#2.3
cv = CountVectorizer()
sentences = cv.fit_transform(data['Quote'])
count_array = sentences.toarray()
df_count = pd.DataFrame(data=count_array,columns = cv.get_feature_names())
df_count.to_csv('features.csv', index=False)

#2.4
features_train, features_test, labels_train, labels_test = train_test_split(sentences, authors, test_size=0.1, random_state=10)
#vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english')
#features_train = vectorizer.fit_transform(features_train)
#features_test = vectorizer.transform(features_test)

#Apply classification model
clf = MultinomialNB()
clf.fit(features_train, labels_train)
accuracy_score(labels_test,clf.predict(features_test))

test = ["I have not failed. I've just found 10,000 ways that won't work"]

vect = cv.transform(test).toarray()
print('Tác giả của câu nói:', test," chính là:" ,clf.predict(vect))

#2.4.2
dict_df = {}
author_list = data['Author'].unique().tolist()
for author in author_list:
    df_callback = data.loc[data['Author'] == author]
    key = author
    dict_df.setdefault(key,[])
    df_callback.reset_index()
    list_quotes = df_callback['Quote'].tolist()
    string = ' '.join(list_quotes)
    dict_df[key] = string

key_list = list(dict_df.keys())
val_list = list(dict_df.values())
model = SentenceTransformer('bert-base-nli-mean-tokens')
sen_embeddings = model.encode(val_list)
sen_embeddings.shape
for j in range(len(sen_embeddings)):
    temp_sen_embeddings = sen_embeddings[np.arange(len(sen_embeddings))!=j]
    similarity = cosine_similarity([sen_embeddings[j]], temp_sen_embeddings)
    list_key = key_list.copy()
    list_key.pop(j)
    for n in range(len(similarity[0])-1, 0, -1):
        for i in range(n):
            if(similarity[0][i] < similarity[0][i+1]):
                similarity[0][i], similarity[0][i+1] = similarity[0][i+1], similarity[0][i]
                list_key[i], list_key[i+1] = list_key[i+1], list_key[i]
    print(list_key)
    print("Các tác giả có độ tương đồng cao nhất với ",key_list[j], 'lần lượt là:', list_key)


