class Sw: 
    
    custom={
    "day":["lund","mard","mercred","jeud","vendred","samed","dimanch"],

    "month":["janvi","fevri","mar","avril","juin","juillet","aout",\
           "septembr","octobr","novembr","decembr"],

    "tempo":["anne","mois","matin","soir","jour","temp","aujourd",\
                     "hui","heur","an","mid","journe","minut"\
                       ,"semain","lendemain","semaine","recent"\
                        "avant","apres"],
    
    "polite":["oui","non","bonjour","bonsoir","veuill","monsieur","madam"\
              ,"merc","pourquoi","comment","prealabl"],

    "thing":["machin","action","point","etc","chos","situat","objet","moment","instant"\
                "facon","dossi","lieu","etap","fois","vrai","environ"\
                    "mond","person","piec","normal","commun","autr","suit","quoi"],
    
    "verb" : ["font","fais","fait","fair","mettr","etre","etais"\
                      ,"etait","etant","etaient","dit",
               "pris","dis","dir","prendr","utilis","avoir","fass",\
                "peux","peut","peuvent","sais","met","voulu"],  

    "det":["cet","son","quel","chaqu"],

    "pron":["tien","leur","cel","quelqu","tous","celui"],

    "adj":["derni","dernier"],

    "subord":["qui","auxquel","lequel","dont"],

    "conj":["puis","car","quand","alor","ains","afin","lorsqu","comm","donc"],

    "adv":["autour","ici","parfois","tout","ensemble","aussi",\
         "surtout","parfois","toujour","tot","tard","trop","mem",\
            "tant","plus","moin","ailleur","assez","rien","tre","dej","auss"],

    "prep":["chez","malgr","san","entre","sous","depuis","peu"\
             "selon","aupr","avant","jusqu","sauf"],

    "neg":["scandal","deplor","exasp","grav","dec","navr"],

    "subj":["plais","ami","collegu","compagnon","epoux","croir",\
                  "croit","avis","sembl","dout","constat","envi","heureux"\
                    ,"pens","sent","bon","bien","parfait"],

    "zero":["aucun","seul"],

    "nb":["deux","centain","plusieur"],

    "gender":["fill","homm","femm","garc"]

    }

    def __init__(self,sw_list):

        self.sw_list=sw_list 

    def add_sw(self,family_list):
        self.sw_list+=family_list

    def rem_sw(self,list):
        for item in list: 
            self.sw_list.remove(item)

    #Be careful with this !
    def add_full_package(self):
        for key in Sw.custom.keys():
            self.add_sw(Sw.custom[key])
    

    