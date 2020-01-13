#-*- coding: utf-8 -*-
######################################################################
######################################################################
#  Copyright Tsung-Hsien Wen, Cambridge Dialogue Systems Group, 2016 #
######################################################################
######################################################################
import os
import json
import sys
import operator
import re

fin = file('utils/nlp/mapping.pair')
replacements = []
for line in fin.readlines():
    tok_from, tok_to = line.replace('\n','').split('\t')
    replacements.append((' '+tok_from+' ',' '+tok_to+' '))

def insertSpace(token,text):
    sidx = 0
    while True:
        sidx = text.find(token,sidx)
        if sidx==-1:
            break
        if sidx+1<len(text) and re.match('[0-9]',text[sidx-1]) and \
                re.match('[0-9]',text[sidx+1]):
            sidx += 1
            continue
        if text[sidx-1]!=' ':
            text = text[:sidx] + ' ' + text[sidx:]
            sidx +=1
        if sidx+len(token)<len(text) and text[sidx+len(token)]!=' ':
            text = text[:sidx+1] + ' ' + text[sidx+1:]
        sidx+=1
    return text

def normalize(text):

    # lower case every word
    text = text.lower()

    # replace white spaces in front and end
    text = re.sub(r'^\s*|\s*$','',text)
    
    # normalize phone number
    ms = re.findall('\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})',text)
    if ms:
        sidx = 0
        for m in ms:
            sidx = text.find(m[0],sidx)
            if text[sidx-1]=='(':
                sidx -= 1
            eidx = text.find(m[-1],sidx)+len(m[-1])
            text = text.replace(text[sidx:eidx],''.join(m))
    
    # replace st.
    text = text.replace(';',',')
    text = re.sub('$\/','',text)
    text = text.replace('/',' and ')

    # replace other special characters
    text = re.sub('[\":\<>@]','',text)
    #text = re.sub('[\":\<>@\(\)]','',text)
    text = text.replace(' - ','')

    # insert white space before and after tokens:
    for token in ['?','.',',','!']:
        text = insertSpace(token,text)
          
    # replace it's, does't, you'd ... etc
    text = re.sub('^\'','',text)
    text = re.sub('\'$','',text)
    text = re.sub('\'\s',' ',text)
    text = re.sub('\s\'',' ',text)
    for fromx, tox in replacements:
		text = ' '+text+' '
		text = text.replace(fromx,tox)[1:-1]

    # insert white space for 's
    text = insertSpace('\'s',text)

    # remove multiple spaces
    text = re.sub(' +',' ',text)
    
    # concatenate numbers
    tmp = text
    tokens = text.split()
    i = 1
    while i<len(tokens):
        if re.match(u'^\d+$',tokens[i]) and \
                re.match(u'\d+$',tokens[i-1]):
            tokens[i-1]+=tokens[i]
            del tokens[i]
        else:
            i += 1
    text = ' '.join(tokens)
    
    return text

def hindi_normalize(sent, slot, value, special_values):
    value = value.strip()
    if value == 'not available': value = u'नहीं'
    if slot == u'name': pass
    if slot == u'phone': sent = phone_normalize(sent,value)
    if slot == u'goodformeal' and value  not in special_values: value=good_meal_normalize(value)
    if slot ==u'type' and value != u'भोजनालय': sent = type_normalize(value ,sent)
    if (slot ==u'type') and (value == u'भोजनालय'): sent = t_type_normalize(value ,sent)
    if slot == u'pricerange': sent = pricerange_normalize(sent,value)
    if slot == u'postcode': sent =postcode_normalize(sent,value)
    if slot == u'count': sent = count_normalize(sent,value)    
    return sent, slot, value

def good_meal_normalize(text):
    return [u'रात्रिभोज',u'रात्रि',u' रात',u'बैकफास्ट', u'लंच', u'दिनर',u'dinner',u'दोपहर',u'डिनर',u'lunch',u'dinne']

def type_normalize(value,sent):
    #print 't1'
    sent = re.sub(u'भोजनालय','restaurant',sent)
    sent = re.sub(u'रेस्टोरेंट','restaurant',sent)
    sent = re.sub(u'रेस्टॉरेंट','restaurant',sent) 
    sent = re.sub(u'रेस्तरां','restaurant',sent) 
    sent = re.sub(u'रेस्ट्रोरेंट','restaurant',sent) 
    return sent

def t_type_normalize(value,sent):
    sent = re.sub(u'restaurant',u'भोजनालय',sent)
    sent = re.sub(u'रेस्टोरेंट',u'भोजनालय',sent) 
    sent = re.sub(u'रेस्टॉरेंट',u'भोजनालय',sent)
    sent = re.sub(u'जगह',u'भोजनालय',sent) 
    sent = re.sub(u'भोजनायलय',u'भोजनालय',sent) 
    sent = re.sub(u'भोजनालायें',u'भोजनालय',sent)
    return sent

def pricerange_normalize(sent,value):
    sent = re.sub(u'महंगी',u'महंगा',sent)
    sent = re.sub(u'महंगी',u'महंगा',sent) 
    sent = re.sub(u'मेहेंगे',u'महंगा',sent)
    sent = re.sub(u' कम ',u' सस्ता ',sent) 
    sent = re.sub(u'सस्ते',u'सस्ता',sent)  
    sent = re.sub(u'मेहेंगा',u'महंगा',sent) 
    sent = re.sub(u'महँगा',u'महंगा',sent)
    sent = re.sub(u'महंगे',u'महंगा',sent) 
    sent = re.sub(u'माध्यम',u'मध्यम',sent) 
    return sent

def phone_normalize(sent,value):
    x = re.findall("\d\d\d\d\d \d\d\d\d\d\d", sent)
    y = re.findall("\d\d\d\d\d\d\d\d\d\d\d", sent)
    z = re.findall("\D\d\d\d\d \d\d\d\d\d\d", sent)
    if x:
        return re.sub(x[0]," "+ value + " ",sent)
    if y:
        return re.sub(y[0]," "+ value + " ",sent)
    if z:
        return re.sub(z[0]," "+ value + " ",sent)
    
    return sent

def postcode_normalize(sent,value):
    x = re.findall("\D\d\d\d\d\d\d\D\D", sent)
    if x:
        return re.sub(x[0]," "+ value+ " ",sent)
    else:
        return sent

def name_normalize(sent,value):
    x = re.findall("value", sent)
    if x:
        return value
    else:

        return re.sub('  ',' ',value)

def count_normalize(sent,value): #सात आठ पांच  एक दो तीन चार छह नौ  दस 
    sent = re.sub(u'सात',u'7',sent) 
    sent = re.sub(u'आठ',u'8',sent) 
    sent = re.sub(u'पांच',u'5',sent)
    sent = re.sub(u'पाच',u'5',sent) 
    sent = re.sub(u'पाच',u'5',sent)
    sent = re.sub(u'चार',u'4',sent)
    sent = re.sub(u'तीन',u'3',sent)
    sent = re.sub(u'दो',u'2',sent)
    sent = re.sub(u'एक',u'1',sent)
    sent = re.sub(u'छह',u'6',sent)
    sent = re.sub(u'नौ',u'9',sent)
    return sent
