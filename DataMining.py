from pydoc import classname
from bs4 import BeautifulSoup
from urllib import request
from matplotlib import legend
import requests
import codecs
import csv
import sys
import re
import datetime
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(15,8))
sys.stdout.reconfigure(encoding='utf-8')

#read csv file
data = pd.read_csv("Quote.csv")

#Fill NaN values in column
data['Birthday'] = data["Birthday"].fillna("No Birthday") 

#Write dataframe after edit to csv
data.to_csv(r'Quote.csv',sep=',', encoding='utf-8-sig',index=False)

#2.1 b
col_birthday = data['Birthday'].tolist()
array_age = []
array_year = []
for i in range(len(col_birthday)):
    split_array = col_birthday[i].split(',')
    year = split_array[1]
    date = datetime.date.today()
    current_year = date.strftime("%Y")
    age = int(current_year) - int(year)
    if(age > 100):
        age = 100
    array_age.append(age)
    array_year.append(year)
if('Age' not in data):
    data.insert(4, "Age", array_age, True)
data.to_csv(r'Quote.csv',sep=',', encoding='utf-8-sig',index=False)

#Create col year born for author
data.insert(5,"Born", array_year, True)
#2.2.1
df_author = data.pivot_table(columns=['Author'], aggfunc='size')
df_author = df_author.reset_index()
df_author.columns = ['Author', 'Quotes']
#graph = df_author.plot(kind='bar',x='Author',y='Quotes')
#plt.show()
 
# who v/s fare barplot
sns.set(font_scale = 0.5)
ax = sns.barplot(x = 'Author',
            y = 'Quotes',
            data = df_author)
ax.set_xticklabels(ax.get_xticklabels(),rotation = 90)
# Show the plot
plt.savefig('TotalQuotesOfAuthor.png')
df_author = df_author.sort_values(by=['Quotes'], ascending=False)
list_author = df_author['Author'].tolist()
print("Tác giả có nhiều châm ngôn nhất là: ", list_author[0])


#2.2.2
author_and_year_df = data[["Author","Born","Age"]]
df_author_year_dups = data.pivot_table(columns=['Author','Born',"Age"], aggfunc='size')
df_author_year_dups = df_author_year_dups.reset_index()
df_author_year_dups = df_author_year_dups.sort_values(by=['Born'], ascending=True)
g = sns.barplot(
    data=df_author_year_dups,
    x="Born", y="Age", hue="Author"
)
plt.savefig('BornAndAgeOfAuthor.png')
df_author_year_dups_count = df_author_year_dups.pivot_table(columns=['Born'], aggfunc='size')
df_author_year_dups_count = df_author_year_dups_count.reset_index()
df_author_year_dups_count.columns = ['Born', 'Count']
df_author_year_dups_count = df_author_year_dups_count.sort_values(by=['Count'], ascending=False)
list_author_count = df_author_year_dups_count['Born'].tolist()
print("Năm có nhiều tác giả được sinh ra nhất là: ", list_author_count[0])



#df_pivot = pd.pivot_table(data, values='points', index='team', columns='position')

#2.2.3
data.insert(5,"Count_Words", data["Quote"].apply(lambda x: len(str(x).split(' '))), True)
df_count_word = data[['Author','Quote','Count_Words']]
gs = sns.barplot(
    data=df_count_word,
    x="Author", y="Count_Words", hue="Quote",
)
gs.legend_.remove()
plt.savefig('CountWordQuoteByAuthor.png')
df_count_word = df_count_word.sort_values(by=['Count_Words'], ascending=False)
list_count_word = df_count_word['Author'].tolist()
number_of_word = df_count_word['Count_Words'].tolist()
print("Tác giả có châm ngôn với số từ nhiều nhất là: ",list_count_word[0], ' với số từ trong một châm ngôn là: ', number_of_word[0], ' từ')






    
