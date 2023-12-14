import Levenshtein

def similarity(word1,word2):
    distance = Levenshtein.distance(word1,word2)
    sim = 1-distance/max(len(word1),len(word2))
    return sim

def card(set):
    card = 0
    for word in set:
        sum = 0
        for other_word in set:
            sum += similarity(word,other_word)
        if sum != 0:
            count = 1/sum
        else:
            count = 0
        card += count
    return card

def card_intersection(g,p):
    union = g+p
    card_union = card(union)
    card_g = card(g)
    card_p = card(p)
    return card_g+card_p-card_union

def soft_precision(g,p):
    return card_intersection(g,p)/card(p)

def soft_recall(g,p):
    return card_intersection(g,p)/card(g)

def soft_f1(g,p):
    precision = soft_precision(g,p)
    recall = soft_recall(g,p)
    if precision+recall != 0:
        return 2*precision*recall/(precision+recall)
    else:
        return 0
