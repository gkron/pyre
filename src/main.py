import os

#from . import try1
import constant
import try1
import spacy
import en_core_web_sm
import pprint

from spacy.matcher import Matcher

import multiprocessing as mp
import pandas as pd
import io
#nlp = en_core_web_sm.load()
import csv

file_path1='D:/eclipse-workspace/sampletest/src/resumes'
file_path2='D:/eclipse-workspace/sampletest/src/PDFRESUME'
class ResumeParser(object):

    def __init__(self, resume):
        nlp = en_core_web_sm.load()
        #nlp = spacy.load('en_core_web_sm')

        self.__matcher = Matcher(nlp.vocab)

        self.__details = {

            'name'              : None,

            'email'             : None,

            'mobile_number'     : None,

            'skills'            : None,

            'education'         : None,

            'experience'        : None,
            
            'company'           : None,

            #'competencies'      : None,

           # 'measurable_results': None,

           # 'no_of_pages'       : None,

          #  'total_experience'  : None,

        }

        self.__resume      = resume

        if not isinstance(self.__resume, io.BytesIO):

            ext = os.path.splitext(self.__resume)[1].split('.')[1]

        else:

            ext = self.__resume.name.split('.')[1]

        self.__text_raw    = try1.extract_text(self.__resume, '.' + ext)

        self.__text        = ' '.join(self.__text_raw.split())

        self.__nlp         = nlp(self.__text)

        self.__noun_chunks = list(self.__nlp.noun_chunks)

        self.__get_basic_details()



    def get_extracted_data(self):

        return self.__details



    def __get_basic_details(self):

        name       = try1.extract_name(self.__nlp, matcher=self.__matcher)

        email      = try1.extract_email(self.__text)

        mobile     = try1.extract_mobile_number(self.__text)

        skills     = try1.extract_skills(self.__nlp, self.__noun_chunks)

        edu        = try1.extract_education([sent.string.strip() for sent in self.__nlp.sents])

        #entities   = try1.extract_entity_sections_grad(self.__text_raw)
        
        exp        = try1.extract_Experience(self.__text)
        
        companies     = try1.extract_companyDeatils(self.__nlp, self.__noun_chunks)
        #print(entities)
        
        self.__details['name'] = name

        self.__details['email'] = email

        self.__details['mobile_number'] = mobile

        self.__details['skills'] = skills

        self.__details['education'] = edu
        
        self.__details['experience']  = exp
        
        self.__details['company'] = companies


def resume_result_wrapper(resume):

        parser = ResumeParser(resume)

        return parser.get_extracted_data()



if __name__ == '__main__':

    pool = mp.Pool(mp.cpu_count())



    resumes = []

    data = []

    for root, directories, filenames in os.walk(file_path1):

        for filename in filenames:

            file = os.path.join(root, filename)

            resumes.append(file)



    results = [pool.apply_async(resume_result_wrapper, args=(x,)) for x in resumes]
    results = [p.get() for p in results]
    r1 = pd.DataFrame(results)
    frame = r1[['name', 'email','mobile_number','skills','experience','education','company']]
    htmltble= frame.to_html("D:/eclipse-workspace/ResumeParsrerUtilty/result.html")
    #print(frame)
    R2= frame.to_csv("D:/eclipse-workspace/ResumeParsrerUtilty/finalOutPut.csv")
    pprint.pprint(results)


    #print (df)