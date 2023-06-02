import regex as re
from unidecode import unidecode

class Preprocessor: 

    def __init__(self,data):
        self.data=data 

    def filter_words(self,texte,min_word_size=3):
        filtered_words = [mot for mot in texte.split() if len(mot) >= min_word_size]
        return ' '.join(filtered_words)

    def text_processing(self,column_name):
        self.data['desc']=self.data[column_name].apply(lambda x : re.sub(r'[^a-zA-Z]\s',' ', x))
        self.data['desc']=self.data['desc'].apply(lambda x: x.lower())
        self.data['desc']=self.data['desc'].apply(lambda x: re.sub(r'\d+',' ',x))
        self.data['desc']=self.data['desc'].str.replace('\W', ' ', regex=True)
        self.data['desc']=self.data['desc'].map(lambda x: unidecode(x))    
        self.data['desc']=self.data['desc'].apply(lambda x: self.filter_words(x,min_word_size=3)) 