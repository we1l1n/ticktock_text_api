#!/usr/bin/etc python

import galbackend_online
import sys
import socket
import time
import pickle
from collections import Counter
#socket = None
#sys.path.append("~/nltk_data")
#target = galbackend.GalInterface()
#print(target)
#gt = galbackend.Thread(target=galbackend.GalInterface)
galbackend_online.InitLogging()
galbackend_online.InitResource('v3')
oov_state =1
name_entity_state =1
anaphra_state =1
short_answer_state=1
previous_history ={}
word2vec_ranking_state =1
tfidf_state =1
theme = {}
#while(1):
    #galbackend.LaunchQueryDebug('can you say that again')
#connection.send('ready')
f = open('user_input_v2_conversations_previous_word2vec_ranking_state','w')
with open('user_input_v2.pkl') as ff:
    user_input = pickle.load(ff)
turn_number =1
trigger = []
user_id_old = 1
word2vec_acc = 0
turn_total = 1
for turn in user_input:
        print turn
        question = turn['question']
        answer = turn['answer']
        app_value = turn['app_value']
        user_id = turn['user_id']
        if user_id_old != user_id:
            turn_number =1
            f.write('======================'+'\n')
        theme, strategy, response,previous_history, word2vec = galbackend_online.get_response(question, user_id, previous_history,theme, oov_state,name_entity_state,short_answer_state,word2vec_ranking_state,anaphra_state,tfidf_state)
        if 'oov' is 'oov':
            f.write('Turn: ' + str(turn_number)+'\n' )
            f.write('User: '+ question +'\n')
	    f.write('TickTock: ' +response+'\n')
            f.write('Strategy: ' + str(strategy) +'\n')
            f.write('TickTock_old: ' + answer +'\n' )
            f.write('Appropriateness_score: ' +app_value +'\n')
            f.write('\n')
            if word2vec ==1:
                word2vec_acc = word2vec_acc+1
        trigger = trigger + [item for item in strategy]
        turn_number = turn_number +1
        turn_total = turn_total +1
        user_id_old = user_id
hist_trigger = Counter(trigger)
print hist_trigger
print word2vec_acc
print float(word2vec_acc)/float(turn_total)
