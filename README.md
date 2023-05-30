# COLLABORATION HETIC - DITP

## Création d'un ensemble d'algo pour faire un reporting des google reviews 

### Requirements

- python3: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- pipenv: [https://pypi.org/project/pipenv/](https://pypi.org/project/pipenv/)
  
### Le but

Cibler la collecte des avis 
Sur le périmètre du programme Services Publics + 

Conformité au cadre légal et administratif
Réglementation européenne, en particulier le RGPD (et son interprétation par la CNIL)
Code des relations entre le public et l’administration
Cadre réglementaire propre à SP+ [https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000043965490](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000043965490)


Pas d’outils payants

Aucune action autre que l’extraction et l’analyse des données 
Pas de création de compte
Pas de formulaire
Pas de démarche active auprès des usagers

Vous verrez ci dessous un schéma d'architecture qui illustre nos idées.

<p align="center">
    <img src="image/schemaarchi.png" height="1028" align="center">
</p>

Afin de réaliser toutes ces étapes on a crée différents algo.
Le premier étant un algo qui a pour but de scrapper les avis des google reviews à partir d'adresses que l'on a récupéré sur un [le référentiel de structure](https://www.data.gouv.fr/fr/datasets/referentiel-structure-de-la-plateforme-services-publics-plus-de-la-ditp/).

À noter que l'on a ensuite fait un autre algo de scrapping, [scrapping_adresse_gouv.py](https://github.com/LonneQuent/PE-x-DTIP/blob/main/scrapping/scrapping_adresse_gouv.py), cet algo là avait pour but d'utiliser [l'api gratuite du gouvernement](https://api.gouv.fr/documentation/api_etablissements_publics) afin de récupérer des avis sur d'autres services que celui qu'on a utilisé de base (les gendarmeries nationales).

<p align="center">
    <img src="image/scrappingalgo.png" height="1028">
</p>

Une fois l'algorythmede scrapping finis il nous sort un csv avec comme entête ce format:

```bash
| Index | Adresse | Auteur | Date | Note | Commentaire |
```

[lien vers le streamlit](https://lonnequent-pe-x-dtip-streamlit-eagk6f.streamlit.app/)