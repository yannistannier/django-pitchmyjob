INDUSTRIES = [
    'Indifférent',
    'Accueil / Secrétariat',
    'Achats',
    'Aéronautique / Ferroviaire / Navale',
    'Agriculture',
    'Architecture',
    'Armée / Sécurité',
    'Art',
    'Audiovisuel',
    'Audit / Comptabilité / Gestion',
    'Automobile',
    'Banque / Finance / Assurance',
    'BTP',
    'Chimie',
    'Commerce / Distribution / Vente',
    'Communication / Marketing / Pub',
    'Culture',
    'Design',
    'Droit / Justice',
    'Edition / Journalisme',
    'Electronique',
    'Energie',
    'Enseignement / Formation',
    'Fonction publique',
    'Hôtellerie / Restauration',
    'Immobilier',
    'Import / Export',
    'Informatique',
    'Métiers du web',
    'Mode',
    'Recherche',
    'Recrutement',
    'Santé',
    'Social',
    'Sport',
    'Télécommunication',
    'Tourisme',
]


EMPLOYEES = [
    '1 à 9 (TPE)',
    '10 à 49 (PE)',
    '50 à 499 (ME)',
    '500 à 999 (GE)',
    '1000 à 4999 (TGE)',
    'Plus de 5000',
]


CONTRACT_TYPES = [
    'CDI',
    'CDD',
    'Stage',
    'Intérim',
    'Alternance',
    'Freelance',
    'Temps partiel',
    'Saisonnier',
    'VIE',
]


EXPERIENCES = [
    'Débutant (0 - 1)',
    'Intermédiaire (2 - 5)',
    'Confirmé (5 et plus)',
]


STUDY_LEVELS = [
    'Aucun diplôme',
    'CAP, BEP ou équivalent',
    'Bac (Obtenu)',
    'Bac +2 (DUT, BTS)',
    'Bac +3 (Licence / Bachelor)',
    'Bac +4 (Master 1)',
    'Bac +5 (Master 2)',
    'Bac +7 (Doctorat)',
]

GROUPS = [
    {'name': 'handle_collaborator', 'permissions': [
        {'app_label': 'authentication', 'model': 'user', 'codenames': ['add_user', 'change_user', 'delete_user']},
    ]},
    {'name': 'handle_pro', 'permissions': [
        {'app_label': 'pro', 'model': 'pro', 'codenames': ['change_pro', 'delete_pro']},
    ]},
    {'name': 'handle_dashboard', 'permissions': []},
]

ADMINS = [
    {'username': 'yannis', 'email': 'tannier.yannis@gmail.com', 'password': 'xxxx'},
    {'username': 'maximilien', 'email': 'raulic.maximilien@gmail.com', 'password': 'xxxx'},
]
