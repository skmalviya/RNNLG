#-*- coding: utf-8 -*- 
from __future__ import unicode_literals
import numpy as np
from gensim.models import Word2Vec
import io

import json

# list of 500000 monolingu data
fin_hi = open('data/monolingual.hi/monolingual/monolingual.hi','r') 
fin_hin_list = []
z=0
for line in fin_hi :
	z=z+1
	if z==5000:
		break
	fin_hin_list.append(line)
#list of hindi sentence complited
print('double ,single ,thrice')
fin_name=input()#double ,single ,thrice
print('150-2 ,150-1')
fout_name=input()#150-2 ,150-1
print('150,100')
size=input()#150.100

file1 = 'delex_dactforexperi_'+fin_name+'.json'  #file for list of delexiclise sentence
file2 = 'semo/RNNLG/vec/hindi_wordtovec-'+fout_name+'.txt'   # file where w2v will be saved.
fin_json=open(file1,'r')
fin_text=open(file2,'a')
#fin_json.readline()
y = json.load(fin_json)
total_sentence = y + fin_hin_list

sentences = []
for s in total_sentence:
	sentences.append(s.split())
model = Word2Vec(sentences, size=150,min_count=1,sg=1)
print(len(total_sentence))
# summarize the loaded model
print(model)
# summarize vocabulary
words = list(model.wv.vocab)
for w in words :
	vec = w
	print(w)
	print(type(model[w]))
	for num in model[w]:   #model[w] is list of number represent vector
		w = w + ' ' +str(num)
	w = w + '\n' 
	fin_text.write(w)  #.encode('utf8'))	
# access vector for one word
#print(model['SLOT_NAME'])
'''print(len(words))
fout_vocab = open('semo/RNNLG/resource/hindi_vocab','a')
for word in words:
	fout_vocab.write(word +"\n")
# save model
model.save('model.bin')
# load model
new_model = Word2Vec.load('model.bin')
print(new_model)'''