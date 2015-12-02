#!/usr/bin/python2.7
from __future__ import division
import itertools

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
    prob = 1
    for word in mess:
        prob *= ((t_klass[word]+l)/(klass_n+l*d))**(mess[word])

    return prob
# END #

def calc_pc(mess_n, total_mess_n, l, class_n):
    return (mess_n + l)/(total_mess_n + l*class_n)
# END #

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
    
    # P(message)
    pm = 0.0001
    for prob_mc, prob_c in itertools.izip(pmc_list, pc_list):
        pm += prob_mc * prob_c

    # P(class|message) for each class in pmc_list
    prob_cm = []
    for prob_mc, prob_c in itertools.izip(pmc_list, pc_list):
        prob_cm.append((prob_mc * prob_c)/pm)

    return prob_cm

# END #
