import pandas as pd
import nltk
from nltk import word_tokenize
from nltk.stem import SnowballStemmer
from collections import Counter

class Tokenizer:

    def __init__(self,preprocessed_data):
        self.preprocessed_data=preprocessed_data
    
    def print_word_counter(self,data):
        data_list=data["desc_clean"].str.split()
        words= data_list.sum()
        compteur_mots = Counter(words)
        print(compteur_mots)
        return compteur_mots

    def token_processing(self,stoplist=[],stop_list_stemming=[],verbose=False,nb_occurence=1):
        #Tokenisation

        self.token_df=pd.DataFrame(self.preprocessed_data)
        self.token_df["desc_token"]= self.token_df["desc"].apply(lambda x: nltk.word_tokenize(x))   
        print("jaja")

        #Removing useless words           
        self.token_df["desc_stop"]= self.token_df["desc_token"].apply(lambda x: [item for item in x if item not in stoplist])
    
        #Stemming
        sstem=SnowballStemmer(language='french')
        self.token_df["desc_stem"]=self.token_df["desc_stop"].apply(lambda row:[sstem.stem(word) for word in row])     
        
        corpus_texte = ' '.join(self.token_df["desc_stem"].map(lambda x: ' '.join(x)).tolist())
        compteur_mots = Counter(corpus_texte.split())
        mots_uniques = set([mot for mot, occurence in compteur_mots.items() if occurence <=nb_occurence]) 
    
        self.token_df["desc_stem+"]=self.token_df["desc_stem"].apply(lambda x: [item for item in x if item not in mots_uniques])
    
        #Filtering the stemming words
        self.token_df["desc_stem++"]=self.token_df["desc_stem+"].apply(lambda x: [item for item in x if item not in stop_list_stemming])
   
        self.token_df["desc_clean"]=self.token_df["desc_stem++"].apply(lambda x: " ".join(x)) 

        if(verbose):
        #print(vectorizer.vocabulary_)        
            print("################################################################")
            self.print_word_counter(self.token_df)

        return self.token_df
    
    def relevant_word_selection(self,column1,target_list,new_column):
        self.token_df[new_column]=self.token_df["desc_stem++"].apply(lambda x: [item for item in x if item in target_list])
        self.token_df[new_column+"_untoken"]=self.token_df[new_column].apply(lambda x: " ".join(x))