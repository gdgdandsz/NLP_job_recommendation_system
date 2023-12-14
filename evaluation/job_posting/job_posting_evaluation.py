import pandas as pd
import Levenshtein
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

labeled = pd.read_csv("labeled_data.csv")
result_df = pd.DataFrame(columns=['job_id', 'labeled_skills'])

for job_id, group in labeled.groupby('Job ID'):
    labeled_skills = []
    current_skill = ''
    current_tag = ''

    for _, row in group.iterrows():
        tag = row['Tag']
        skill = row['Skill'].strip()

        if tag == 'O':
            if current_skill:
                labeled_skills.append(current_skill)
                current_skill = ''
        elif tag == 'B':
            if current_skill:
                labeled_skills.append(current_skill)
            current_skill = skill
        elif tag == 'I':
            current_skill += ' ' + skill

    if current_skill:
        labeled_skills.append(current_skill)

    result_df = result_df.append({'job_id': job_id, 'labeled_skills': labeled_skills}, ignore_index=True)

result_df.to_csv('labeled_skills.csv', index=False)

def similarity(word1,word2):
    distance = Levenshtein.distance(word1,word2)
    similarity = 1-distance/max(len(word1),len(word2))
    return similarity

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
    
prediction_df = pd.read_csv('result_all.csv')

import ast
precision_list = []
recall_list = []
f1_list = []

for index, row in result_df.iterrows():
    job_id = row['job_id']
    try:
        labeled_skills = row['labeled_skills']
        prediction_row = prediction_df[prediction_df['Job ID'] == job_id].iloc[0]
        prediction_skills = ast.literal_eval(prediction_row['Extracted_Skills'])
        precision_result = soft_precision(labeled_skills, prediction_skills)
        precision_list.append(precision_result)
        recall_result = soft_recall(labeled_skills, prediction_skills)
        recall_list.append(recall_result)
        f1_result = soft_f1(labeled_skills, prediction_skills)
        f1_list.append(f1_result)
    except IndexError:
        print(f"Job ID {job_id} not found in prediction_df. Handling the exception...")
    except Exception as e:
        print(f"An error occurred for Job ID {job_id}: {e}")
        print(f"row['labeled_skills']: {row['labeled_skills']}")
        print(f"prediction_row['Extracted_Skills']: {prediction_row['Extracted_Skills']}")
    
print("average precision:", sum(precision_list)/len(precision_list))
print("average recall:", sum(recall_list)/len(recall_list))
print("average f1:", sum(f1_list)/len(f1_list))

prediction_df_2 = pd.read_csv('result_quanliang.csv')

precision_list = []
recall_list = []
f1_list = []

for index, row in result_df.iterrows():
    job_id = row['job_id']
    try:
        labeled_skills = row['labeled_skills']
        prediction_row = prediction_df_2[prediction_df_2['Job ID'] == job_id].iloc[0]
        prediction_skills = ast.literal_eval(prediction_row['Extracted_Skills'])
        precision_result = soft_precision(labeled_skills, prediction_skills)
        precision_list.append(precision_result)
        recall_result = soft_recall(labeled_skills, prediction_skills)
        recall_list.append(recall_result)
        f1_result = soft_f1(labeled_skills, prediction_skills)
        f1_list.append(f1_result)
    except IndexError:
        print(f"Job ID {job_id} not found in prediction_df. Handling the exception...")
    except Exception as e:
        print(f"An error occurred for Job ID {job_id}: {e}")
        print(f"row['labeled_skills']: {row['labeled_skills']}")
        print(f"prediction_row['Extracted_Skills']: {prediction_row['Extracted_Skills']}")
    

# print(precision_list)
# print(recall_list)
# print(f1_list)

print("average precision:", sum(precision_list)/len(precision_list))
print("average recall:", sum(recall_list)/len(recall_list))
print("average f1:", sum(f1_list)/len(f1_list))
