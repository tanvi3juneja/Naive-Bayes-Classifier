from __future__ import division
from sys import argv
from collections import Counter
import glob
import re
import os, os.path
import pickle

script,path=argv

listofdocs=glob.glob(path+'/*/*/*[2-4]/*.txt')
N=len(listofdocs)
Vstr=''
stopwords=['to','at','a','an','the','of','for']
for name in listofdocs:
# 	print '\t',name
	doc=open(name,'r');
	Vstr+=doc.read().lower()
	doc.close()
Vstr=re.sub(r'[?|.|,|(|)|"|\'|!|/|-|;|:|#|>|<]',r' ',Vstr)
Vstr=re.sub(r'[0-9]','',Vstr)
Vstr=Vstr.replace('-',' ')
Vstr=Vstr.replace('*',' ')
Vstr=re.sub(r' [a-zA-Z] ',r' ',Vstr)
Vstr=Vstr.split()
# print len(Vstr)
V=[]
[V.append(x) for x in Vstr if x not in V]
len_V=len(V)
# print len(V)
# 	print V
# 	raw_input('')


classes=['pos_truth','pos_dec','neg_truth','neg_dec']

docs_in_pos_truth=len(glob.glob(path+'/positive_polarity/truthful*/*/*.txt'))
docs_in_pos_dec=len(glob.glob(path+'/positive_polarity/deceptive*/*/*.txt'))
docs_in_neg_truth=len(glob.glob(path+'/negative_polarity/truthful*/*/*.txt'))
docs_in_neg_dec=len(glob.glob(path+'/negative_polarity/deceptive*/*/*.txt'))

prior={}
prior['pos_truth']=docs_in_pos_truth/N
prior['pos_dec']=docs_in_pos_dec/N
prior['neg_truth']=docs_in_neg_truth/N
prior['neg_dec']=docs_in_neg_dec/N

text_pos_truth=''
for name in glob.glob(path+'/positive_polarity/truthful*/*/*.txt'):
	doc=open(name,'r')
# 	print '\t',name
	text_pos_truth+=doc.read().lower()
	doc.close()
text_pos_truth=re.sub(r'[?|.|,|(|)|"|\'|!|/|-|;|:|#|>|<]',r' ',text_pos_truth)
text_pos_truth=re.sub(r'[0-9]','',text_pos_truth)
text_pos_truth=text_pos_truth.replace('-',' ')
text_pos_truth=text_pos_truth.replace('*',' ')
text_pos_truth=re.sub(r' [a-zA-Z] ',r' ',text_pos_truth)
text_pos_truth=text_pos_truth.split()
len_pos_truth= len(text_pos_truth)

tct_pos_truth={}
for words in text_pos_truth:
	if words in tct_pos_truth:
		tct_pos_truth[words]+=1
	else:
		tct_pos_truth[words]=1
# print tct_pos_truth

text_pos_dec=''
for name in glob.glob(path+'/positive_polarity/deceptive*/*/*.txt'):
	doc=open(name,'r')
# 	print '\t',name
	text_pos_dec+=doc.read().lower()
	doc.close()
text_pos_dec=re.sub(r'[?|.|,|(|)|"|\'|!|/|-|;|:|#|>|<]',r' ',text_pos_dec)
text_pos_dec=re.sub(r'[0-9]','',text_pos_dec)
text_pos_dec=text_pos_dec.replace('-',' ')
text_pos_dec=text_pos_dec.replace('*',' ')
text_pos_dec=re.sub(r' [a-zA-Z] ',r' ',text_pos_dec)
text_pos_dec=text_pos_dec.split()

len_pos_dec= len(text_pos_dec)

tct_pos_dec={}
for words in text_pos_dec:
	if words in tct_pos_dec:
		tct_pos_dec[words]+=1
	else:
		tct_pos_dec[words]=1
# print tct_pos_dec

text_neg_truth=''
for name in glob.glob(path+'/negative*/truth*/*/*.txt'):
	doc=open(name,'r')
# 	print '\t',name
	text_neg_truth+=doc.read().lower()
	doc.close()
text_neg_truth=re.sub(r'[?|.|,|(|)|"|\'|!|/|-|;|:|#|>|<]',r' ',text_neg_truth)
text_neg_truth=re.sub(r'[0-9]','',text_neg_truth)
text_neg_truth=text_neg_truth.replace('-',' ')
text_neg_truth=text_neg_truth.replace('*',' ')
text_neg_truth=re.sub(r' [a-zA-Z] ',r' ',text_neg_truth)
text_neg_truth=text_neg_truth.split()
len_neg_truth= len(text_neg_truth)

tct_neg_truth={}
for words in text_neg_truth:
	if words in tct_neg_truth:
		tct_neg_truth[words]+=1
	else:
		tct_neg_truth[words]=1
# print tct_neg_truth

text_neg_dec=''
for name in glob.glob(path+'/negative*/dec*/*/*.txt'):
	doc=open(name,'r')
# 	print '\t',name
	text_neg_dec+=doc.read().lower()
	doc.close()
text_neg_dec=re.sub(r'[?|.|,|(|)|"|\'|!|/|-|;|:|#|>|<]',r' ',text_neg_dec)
text_neg_dec=re.sub(r'[0-9]','',text_neg_dec)
text_neg_dec=text_neg_dec.replace('-',' ')
text_neg_dec=text_neg_dec.replace('*',' ')
text_neg_dec=re.sub(r' [a-zA-Z] ',r' ',text_neg_dec)
text_neg_dec=text_neg_dec.split()
len_neg_dec= len(text_neg_dec)

tct_neg_dec={}
for words in text_neg_dec:
	if words in tct_neg_dec:
		tct_neg_dec[words]+=1
	else:
		tct_neg_dec[words]=1
# print tct_neg_dec

cond_prob_t_p={}
cond_prob_d_p={}
cond_prob_t_n={}
cond_prob_d_n={}

for t in V:
	if t in tct_pos_truth:
		cond_prob_t_p[t]=1.0*(tct_pos_truth[t]+1)/(len_pos_truth+len_V)
	else:
		cond_prob_t_p[t]=1.0/(len_V+len_pos_truth)
# 		print len(cond_prob_t_p)
	
	if t in tct_pos_dec:
		cond_prob_d_p[t]=1.0*(tct_pos_dec[t]+1)/(len_pos_dec+len_V)
	else:
		cond_prob_d_p[t]=1.0/(len_V+len_pos_dec)

	if t in tct_neg_truth:
		cond_prob_t_n[t]=1.0*(tct_neg_truth[t]+1)/(len_neg_truth+len_V)
	else:
		cond_prob_t_n[t]=1.0/(len_V+len_neg_truth)
	
	if t in tct_neg_dec:
		cond_prob_d_n[t]=1.0*(tct_neg_dec[t]+1)/(len_neg_dec+len_V)
	else:
		cond_prob_d_n[t]=1.0/(len_V+len_neg_dec)
		
modelfile=open('nbmodel.txt','wb')

pickle.dump(V,modelfile)
pickle.dump(prior,modelfile)
pickle.dump(cond_prob_t_p,modelfile)
pickle.dump(cond_prob_d_p,modelfile)
pickle.dump(cond_prob_t_n,modelfile)
pickle.dump(cond_prob_d_n,modelfile)

modelfile.close()
	
	

