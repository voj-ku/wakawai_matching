import json
from compute_score import Matcher
import random
import pandas as pd
import streamlit as st


# Data Source
# 1
category = ['Lidé', 'Zvířata', 'Příroda', 'Společnost', 'Udržitelnost']

# 2
sub_category_dict = {
    'Lidé': [
        'Děti, mládež a rodiny',
        'Senioři',
        'Hospicová a paliativní péče',
        'Humanitární pomoc',
        'Lidé s postižením',
        'Lidé bez domova',
        'Lidská práva',
        'Legislativní a právní pomoc',
        'Zdraví'
    ],
    'Zvířata': [
        'Ochrana zvířat',
        'Boj s lovem divoké zvířaty',
        'Práva zvířat a dobré životní podmínky',
        'Výcvik zvířat a speciální služby',
        'Ohrožené druhy',
        'Zoologické zahrady a akvária',
        'Útulky',
        'Rezervace pro ryby, divokou zvěř a ptáky'
    ],
    'Příroda': [
        'Klimatická změna',
        'Okyselení oceánu',
        'Chemické znečištění',
        'Zatížení dusíkem a fosforem',
        'Voda',
        'Degradace půdy',
        'Ztráta biodiverzity',
        'Znečištění ovzduší',
        'Úbytek ozónové vrstvy',
        'Potraviny/zero waste'
    ],
    'Společnost': [
        'Vzdělávání, věda a výzkum',
        'Inovace a spolupráce',
        'Mír a spravedlnost',
        'Politický hlas',
        'Sociální spravedlnost a znevýhodněné skupiny',
        'Rovnost žen a mužů',
        'Příjem a práce',
        'Komunitní a regionální rozvoj',
        'Osvěta a poskytování informací',
        'Kultura, umění a historie / Sport a volný čas'
    ],
    'Udržitelnost': [
        'Snížení/vymýcení chudoby',
        'Nulový hlad',
        'Dobré zdraví a životní podmínky',
        'Kvalitní vzdělávání',
        'Rovnosti žen a mužů',
        'Čistá voda a hygiena',
        'Cenově dostupná a čistá energie',
        'Slušná práce a hospodářský růst',
        'Průmysl, inovace a infrastruktura',
        'Snížení nerovnosti',
        'Udržitelná města a komunity',
        'Odpovědná spotřeba a výroba',
        'Klimatická akce',
        'Život pod vodou',
        'Život Na Zemi',
        'Mír, spravedlnost a silné instituce',
        'Partnerství pro cíle'
    ]
}

# 3
fields_of_influence = ['Svět', 'ČR', 'Region']
regions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# 4
collab_intensities = ['Aktivní spolupráce', 'Jednorázová pomoc']

# 5
employee_involvement = ['Zapojení Zaměstnanců', 'Bez zapojení zaměstanců']

# 6 form of help
forms_of_help = ['Finance', 'Hmotná pomoc', 'Dobrovolnictví',
                 'Expertní dobrovolnictví', 'Společný projekt']

# 7 expertises
expertises = ['Marketing', 'IT', 'HR', 'Právo', 'Sales',
              'Projektový Management', 'Výzkum', 'Management', 'Podnikání', 'Účetnictví', 'Jiné']

# 8 barriers
barriers = ['Žádná', 'Nemáme čas/Není to priorita', 'Omezené zdroje', 'Nedostatek znalostí a zkušeností', 'Složitá legislativa',
            'Majitelé v tom nevidí smysl', 'Rozdílné cíle a hodnoty', 'Komunikační bariéry', 'Nedůvěra a obavy', 'Neshody v očekávání a výsledcích']

# 9 reasons for impact
reason_for_impact = ['Je to součastí našich hodnot', 'Zapojení zaměstnanců', 'Zlepšení brandu', 'Plnění ESG legislativy', 'Konkurenční výhoda',
                     'Zvýšit loajalitu zákazníků', 'Pozitivní odkaz naší společnosti', 'Zvýšení atraktivnosti u ESG investorů', 'Chceme zlepšit své vlastní okolí']


# Functions

# Function to select random values and return a list
def select_random_values(keys, sub_category_dict):
    selected_values = []
    for key in keys:
        if key in sub_category_dict:
            selected_values.extend(random.sample(sub_category_dict[key], min(
                # Add up to 5 random values from each key
                10, len(sub_category_dict[key]))))
    return selected_values

# Org data generation


def dict_to_dataframe(data):
    # Ensure all values are lists
    processed_data = {}
    for key, value in data.items():
        if not isinstance(value, list):
            value = [value]
        processed_data[key] = value
    # Create DataFrame
    df = pd.DataFrame(list(processed_data.items()), columns=['Key', 'Value'])

    df.index = df['Key']

    return df.drop('Key', axis=1)


@st.cache_data
def generate_org_data():
    org_data = {
        # pick one or two category
        'category': random.sample(category, random.randint(1, 2)),
        # pick on randomly
        'field-of-influence': fields_of_influence[random.randint(1, len(fields_of_influence))-1],
        # pick on randomly
        'collab-intensity': collab_intensities[random.randint(1, len(collab_intensities))-1],
        # pick on randomly
        'employee-involvement': employee_involvement[random.randint(1, len(employee_involvement))-1],
        # pick one to five random forms
        'form-of-help': random.sample(forms_of_help, random.randint(1, 5)),
        # pick one to five random expertises
        'expertises': random.sample(expertises, random.randint(1, 5)),
        # pick one to three random barriers
        'barriers': random.sample(barriers, random.randint(1, 3)),
        # pick two to five random reasons for impact
        'reason-for-impact': random.sample(reason_for_impact, random.randint(2, 5)),
    }

    # # pick one to ten random subcategory
    org_data['sub-category'] = select_random_values(
        keys=org_data['category'], sub_category_dict=sub_category_dict)

    with open('org_data.json', 'w', encoding='utf-8') as f:
        json.dump(org_data, f, indent=4, ensure_ascii=False)

    return org_data

# Firm data generation


@st.cache_data
def generate_firm_data():
    firm_data = {
        # pick one or two category
        'category': random.sample(category, random.randint(1, 2)),
        # pick on randomly
        'field-of-influence': fields_of_influence[(random.randint(1, len(fields_of_influence)))-1],
        # pick on randomly
        'collab-intensity': collab_intensities[(random.randint(1, len(collab_intensities)))-1],
        # pick on randomly
        'employee-involvement': employee_involvement[(random.randint(1, len(employee_involvement)))-1],
        # pick one to five random forms
        'form-of-help': random.sample(forms_of_help, random.randint(1, 5)),
        # pick one to five random expertises
        'expertises': random.sample(expertises, random.randint(1, 5)),
        # pick one to three random barriers
        'barriers': random.sample(barriers, random.randint(1, 3)),
        # pick two to five random reasons for impact
        'reason-for-impact': random.sample(reason_for_impact, random.randint(2, 5)),
    }

    firm_data['sub-category'] = select_random_values(
        keys=firm_data['category'], sub_category_dict=sub_category_dict)

    with open('firm_data.json', 'w', encoding='utf-8') as f:
        json.dump(firm_data, f, indent=4, ensure_ascii=False)

    return firm_data
