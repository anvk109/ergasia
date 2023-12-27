import os,codecs
import pandas as pd
from nltk import*
import matplotlib.pyplot as plt


TC = 'standardized_scores.xlsx' 
sa = pd.read_excel(TC) #           

# open sample text
fn = 'arthro.txt' 
with codecs.open(fn,'r','utf-8') as f:
    raw = f.read().replace('\n',' ').replace('\r','').replace('!',' ')  
tokens = [[t for t in word_tokenize(raw) if t.isalpha()] ]

#compute mean valence (or mean fear etc.) per sentence
sent_mean_val_z = [];sent_mean_fear_z = [];sent_mean_ang_z=[];sent_mean_disg_z=[]
sent_mean_hap_z=[];sent_mean_sad_z=[];sent_mean_surp_z=[]
for t in tokens:
    dt = sa.query('word in @t')
    sent_mean_val_z.append(dt.val_z.mean())
    sent_mean_ang_z.append(dt.ang_z.mean())
    sent_mean_fear_z.append(dt.fear_z.mean())
    sent_mean_disg_z.append(dt.disg_z.mean())
    sent_mean_hap_z.append(dt.hap_z.mean())
    sent_mean_sad_z.append(dt.sad_z.mean())
    sent_mean_surp_z.append(dt.surp_z.mean())

#panda & save results
df = pd.DataFrame()
df['sent'] = tokens
df['val_z'] = sent_mean_val_z
df['fear_z'] = sent_mean_fear_z
df['ang_z'] = sent_mean_ang_z
df['disg_z'] = sent_mean_disg_z
df['hap_z'] = sent_mean_hap_z
df['sad_z'] = sent_mean_sad_z
df['surp_z'] = sent_mean_surp_z
df = round(df,3)
#df.to_csv('results.txt')

print('val_z:',sent_mean_val_z)
print('fear_z:',sent_mean_fear_z)
print('ang_z:',sent_mean_ang_z)
print('disg_z:',sent_mean_disg_z)
print('hap_z:',sent_mean_hap_z)
print('sad_z:',sent_mean_sad_z)
print('surp_z:',sent_mean_surp_z)

#plot hap_z, fear_z etc.
df.set_index(df.index,inplace=True)
df.plot(kind='bar',alpha=0.75, rot=0)
plt.xlabel("Sentence #")
plt.ylabel("Sentiment Value (z)")
plt.show()

#get most beautiful and ugliest words in corpus
#topb = sa.sort_values(by=['val_z']).tail()
#print('top beauty words','\n',topb.word)
#print()
#topu = sa.sort_values(by=['val_z']).head()
#print('top ugly words','\n',topu.word)

#get most beautiful and fearful sents in text
#print('top val sent','\n',df.sort_values(by=['val_z']).tail(1))
#print()
#print('top FEAR sent','\n',df.sort_values(by=['fear_z']).tail(1))