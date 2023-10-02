from pdfminer.high_level import extract_text
import re, os
import spacy
from spacy.matcher import Matcher
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from tabulate import tabulate

def extract_text_from_pdf(path):
    text = extract_text(path)                  #extracting text from the pdf resume
    return text.lower()

def extract_contact_information(text, skills_list):
    profile = dict()
    profile['Name'] = None
    nlp = spacy.load('en_core_web_md')
    '''print(nlp(text).ents)
    print('---------------------\r')
    for matche in nlp(text).ents:
        if matche.label_ == 'PERSON':
            profile['Name'] = matche.text'''
    matcher = Matcher(nlp.vocab)
    patterns = [
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name and Last name
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name, Middle name, and Last name
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]]
    for pattern in patterns:
        matcher.add('NAME', patterns=[pattern])
    doc = nlp(text)
    matches = matcher(doc)
    for match_id, start, end in matches:            #Name matching
        span = doc[start:end]
        profile['Name'] = span.text
        break

    profile['Contact_number'] = None
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    matche = re.search(pattern, text)      #phone number matching
    if matche:
        profile['Contact_number'] = matche.group()

    profile['Email'] = None
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    matche = re.search(pattern, text)       #email matching
    if matche:
        profile['Email'] = matche.group()
        
    skills = []
    for skill in skills_list:               #skills matching
        pattern = r"\b{}\b".format(re.escape(skill))
        matche = re.search(pattern, text)
        if matche:
            skills.append(skill)
    profile['Skills'] = ','.join(skills)
    del skills
    
    return profile

def match_score(jd, text):
    cv = CountVectorizer()                   #Using cosine similarity to find similarities in jd and resume
    matrix = cv.fit_transform((text, jd))
    similarity_matrix = cosine_similarity(matrix)
    #print(similarity_matrix)
    return similarity_matrix[0][1]

def main():
    resumes = os.listdir("Resumes")       #getting resumes list
    n = len(resumes)
    percent_inc = 100/n                   #calculating percent increment for progress indicator
    percent_complete = 0
    job_description = None                #getting the job description
    with open('Job Description.txt', 'r') as f:
        job_description = f.read()
    job_description = job_description.lower()
    
    index_ranks = []
    profiles = []
    for i in range(n):
        percent_complete += percent_inc                              #incrementing the progress percentage
        resume = extract_text_from_pdf("Resumes/" + resumes[i])      #getting text resume
        #print(resume)                                               #parsing resume for contact information and skills
        profile = extract_contact_information(resume, ['cloud', 'python', 'machine learning', 'artificial intelligence', 'java', 'flutter', 'programming', 'theory and mathematics of computation', 'problem analysis', 'programming languages', 'data science'])
        #print(profile)
        profile['Match score'] = match_score(job_description, resume)#calculating the cosine similarities between jd and resume
        profile['Resume file'] = resumes[i]
        profiles.append(profile)
        os.system('cls')                                             #clearing screen
        print('Please wait... Processing resumes...\n' + str(int(percent_complete)) + '% complete')  #updating the progress indicator
        index_ranks.append(i+1)                                      #maintaining a list for table index
        
    data_frame = pd.DataFrame(profiles)                              #creating DataFrame
    data_frame.sort_values(by = 'Match score', ascending = False, inplace = True)      #sorting the DataFrame according to non-incresing order of matching percentage
    data_frame['Rank'] = index_ranks                                 #placing new column
    data_frame.set_index('Rank', inplace = True)                     #using the new column as index
    data_frame.drop(['Match score'], axis = 1, inplace = True)       #table cleaning
    print('Profiles according to relevancy to job description are listed as follows.')
    print(tabulate(data_frame, headers = 'keys', showindex = 'always', tablefmt = 'grid'))        #display of complete table
    while 1:
        n = int(input('How many top relevant results you want?  '))  #get only top n results
        os.system('cls')
        print(tabulate(data_frame.iloc[:n], headers = 'keys', showindex = 'always', tablefmt = 'grid'))      #slicing the table
    

if __name__ == '__main__':
    main()    
