import pandas as pd
import nltk
from nltk.corpus import stopwords 
from nltk import word_tokenize
from nltk.stem import SnowballStemmer
from collections import Counter

class Tokenizer:

    stopwords=stopwords.words("french")

    def __init__(self,preprocessed_data):
        self.preprocessed_data=preprocessed_data
    
    def print_word_counter(self):
        data_list=self.preprocessed_data.str.split()
        words= data_list.sum()
        compteur_mots = Counter(words)
        print(compteur_mots)
        return compteur_mots

    def token_processing(self,stoplist=stopwords,stop_list_stemming=[],verbose=False,nb_occurence=1):
        #Tokenisation
        token_df=pd.DataFrame(self.preprocessed_data)
        token_df["desc_token"]= token_df["desc"].apply(lambda x: nltk.word_tokenize(x))   
    
        #Removing useless words           
        token_df["desc_stop"]= token_df["desc_token"].apply(lambda x: [item for item in x if item not in stoplist])
    
        #Stemming
        sstem=SnowballStemmer(language='french')
        token_df["desc_stem"]=token_df["desc_stop"].apply(lambda row:[sstem.stem(word) for word in row])     
        
        corpus_texte = ' '.join(token_df["desc_stem"].map(lambda x: ' '.join(x)).tolist())
        compteur_mots = Counter(corpus_texte.split())
        mots_uniques = set([mot for mot, occurence in compteur_mots.items() if occurence <=nb_occurence]) 
    
        token_df["desc_stem+"]=token_df["desc_stem"].apply(lambda x: [item for item in x if item not in mots_uniques])
    
        #Filtering the stemming words
        token_df["desc_stem++"]=token_df["desc_stem+"].apply(lambda x: [item for item in x if item not in stop_list_stemming])
   
        if(verbose):
        #print(vectorizer.vocabulary_)        
            print("################################################################")
            self.print_word_counter()    
        return token_df