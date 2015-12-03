#!/usr/bin/python2.7
from __future__ import division
import itertools
import math
import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)

# P(message|class)
def calc_pmc(mess, klass, l, d):
    # Get word count of class
    klass_n = 0
    for word in klass:
        klass_n += klass[word]

    # Add values for words that don't exist
    t_klass = klass.copy()
    for word in mess:
        if word not in t_klass:
            t_klass[word] = 0
    
    # Calc P(message|class)
    log_prob = 1
    for word in mess:
        log_prob += math.log(((t_klass[word]+l)/(klass_n+l*d))**(mess[word]))

    return log_prob

# P(class)
def calc_pc(mess_n, total_mess_n, l, class_n):
    return (mess_n + l)/(total_mess_n + l*class_n)

def calc_probs(mess, class_list, mess_num_list, l):
    # Calc distinct number of words
    unique_words = set()
    for klass in class_list:
        for word in klass:
            unique_words.add(word)
    
    # Total messages
    total_mess_n = 0
    for mess_n in mess_num_list:
        total_mess_n += mess_n

    pmc_list = [] # List of P(message|class)
    pc_list = []  # List of P(class)
    for klass, mess_n in itertools.izip(class_list, mess_num_list):
        pmc_list.append(calc_pmc(mess, klass, l, len(unique_words)))
        pc_list.append(calc_pc(mess_n, total_mess_n, l, len(class_list)))
    
    # Normalize P(message|class) log values
    max_num = max(pmc_list)
    for i in range(len(pmc_list)):
        pmc_list[i] -= max_num
        pmc_list[i] = math.exp(pmc_list[i])    

    # P(message)
    pm = 0
    for prob_mc, prob_c in itertools.izip(pmc_list, pc_list):
        pm += prob_mc * prob_c
        logging.debug(prob_mc, prob_c)

    # P(class|message) for each class in pmc_list
    prob_cm = []
    for prob_mc, prob_c in itertools.izip(pmc_list, pc_list):
        prob_cm.append((prob_mc * prob_c)/pm)

    return prob_cm
