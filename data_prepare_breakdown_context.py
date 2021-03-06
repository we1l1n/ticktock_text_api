import readall
import gensim
import nltk
import numpy as np
import pickle
# we need to extract some features, now we make it easy now to just use the word2vec, one turn previous turn.
#
model = gensim.models.Word2Vec.load('/tmp/word2vec_50_break')

all_v1 = readall.readall('/home/ubuntu/zhou/Backend/rating_log/v1')
all_v2 = readall.readall('/home/ubuntu/zhou/Backend/rating_log/v2')
all_v3 = readall.readall('/home/ubuntu/zhou/Backend/rating_log/v3')
all_logs = dict(all_v1.items() + all_v2.items() + all_v3.items())
sent_vec = None
for item in all_logs:
        print item
        conv = all_logs[item]["Turns"]
        sent_pre = None
        for turn in conv:
                turn_vec_1 = sum(model[nltk.word_tokenize(conv[turn]["You"])])
                if len(nltk.word_tokenize(conv[turn]["TickTock"])) ==0:
                    continue
                #print 'TickTock'
                #print conv[turn]["TickTock"]
                turn_vec_2 = sum(model[nltk.word_tokenize(conv[turn]["TickTock"])])
                #print turn_vec_1
                #print turn_vec_2
                if sent_vec is None:
                    sent_vec = turn_vec_1 + turn_vec_2 + turn_vec_1 + turn_vec_2
                    target = np.array(int(conv[turn]["Appropriateness"]))
                else:
                    if sent_pre is None:
                        sent_vec =  np.vstack((sent_vec,turn_vec_1+turn_vec_2+turn_vec_1+turn_vec_2))
                    else:
                        sent_vec = np.vstack((sent_vec, sent_pre + turn_vec_1 + turn_vec_2))
                    target = np.hstack((target,int(conv[turn]["Appropriateness"])))
                sent_pre = turn_vec_1 + turn_vec_2

sent_context = {'data':sent_vec,'target':target}
print len(sent_vec)
with open('sent_context.pkl','w') as f:
    pickle.dump(sent_context,f)

