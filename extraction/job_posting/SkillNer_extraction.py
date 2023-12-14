import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import spacy
import en_core_web_lg
from spacy.matcher import PhraseMatcher
from skillNer.skill_extractor_class import SkillExtractor
from skillNer.general_params import SKILL_DB

# init params of skill extractor
nlp = en_core_web_lg.load()
# init skill extractor
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

df = pd.read_csv("Jobs_NYC_Postings_20231126.csv") # change the input path
df = df.dropna(subset=['Minimum Qual Requirements', 'Preferred Skills'], how='all')
target = df.loc[:, ['Job ID', 'Minimum Qual Requirements', 'Preferred Skills']]
target = target.fillna('nan')

dic = ['€', '¢', 'â', '*','']
def remove_special_character(text, dic):
    s = ''
    for word in text:
        if word not in dic:
            s += word
    return s

target['Minimum Qual Requirements'] = target['Minimum Qual Requirements'].apply(lambda x : remove_special_character(x, dic))
target['Preferred Skills'] = target['Preferred Skills'].apply(lambda x : remove_special_character(x, dic))
target['skills'] = target['Minimum Qual Requirements'] + target['Preferred Skills']
target = target.drop(columns = ['Minimum Qual Requirements', 'Preferred Skills'])

def skillner(sentences):
    annotations = skill_extractor.annotate(sentences)
    answer=[]
    for k,v in annotations.items():
        if k == 'results':
            for k1,v1 in v.items():
                for i in v1:
                    for k2,v2 in i.items():
                        if k2=="doc_node_value":
                            answer.append(v2)
    return answer

def process_skills(x):
    try:
        result = skillner(x)
        return result
    except IndexError as e:
        print(f"Error processing skills: {e}. Input data: {x}")
        return None  
    
# Apply the function to the 'skills' column
target['Extracted_Skills'] = target['skills'].apply(process_skills)
target.to_csv('result_all.csv', index=False) # change the output path
