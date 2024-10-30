import json
from compute_score import Matcher
import random
import pandas as pd
import streamlit as st


# 1
category = ['Lidé', 'Zvířata', 'Příroda', 'Společnost', 'Udržitelnost']
# NGO_select_category = st.multiselect("Select category for NGO", category)
# firm_select_category = st.multiselect(
#     "Select category for firm", category)
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


# Generate a new list with the randomly chosen number of items
org1_category = random.sample(category, random.randint(1, 2))
fir1_category = random.sample(category, random.randint(1, 2))

org1 = {'category': org1_category}
fir1 = {'category': fir1_category}

# Example usage:
matcher = Matcher()

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
# Function to select random values


# Function to select random values and return a list
def select_random_values(keys, sub_category_dict):
    selected_values = []
    for key in keys:
        if key in sub_category_dict:
            selected_values.extend(random.sample(sub_category_dict[key], min(
                # Add up to 5 random values from each key
                10, len(sub_category_dict[key]))))
    return selected_values


# # pick one to ten random subcategory
org_data['sub-category'] = select_random_values(
    keys=org_data['category'], sub_category_dict=sub_category_dict)
firm_data['sub-category'] = select_random_values(
    keys=firm_data['category'], sub_category_dict=sub_category_dict)


with open('org_data.json', 'w', encoding='utf-8') as f:
    json.dump(org_data, f, indent=4, ensure_ascii=False)


with open('firm_data.json', 'w', encoding='utf-8') as f:
    json.dump(firm_data, f, indent=4, ensure_ascii=False)


matcher = Matcher()
overall_score = matcher.compute_match_score(org_data, firm_data)

df = pd.DataFrame(
    columns=['Weighed_Score',  'Sample Firm', 'Score', 'Sample NGO'],
    index=['category', 'sub-category', 'field-of-influence', 'collab-intensity',
           'employee-involvement', 'form-of-help', 'expertises', 'barriers', 'reason-for-impact']
)

df.loc['category'] = [
    matcher.weighed_scores['category'],
    org_data['category'],
    matcher.unweighed_scores['category'],
    firm_data['category']
]
df.loc['sub-category'] = [
    matcher.weighed_scores['sub-category'],
    org_data['sub-category'],
    matcher.unweighed_scores['sub-category'],
    firm_data['sub-category']
]
df.loc['field-of-influence'] = [
    matcher.weighed_scores['field-of-influence'],
    [org_data['field-of-influence']],
    matcher.unweighed_scores['field-of-influence'],
    [firm_data['field-of-influence']]
]
df.loc['collab-intensity'] = [
    matcher.weighed_scores['collab-intensity'],
    [org_data['collab-intensity']],
    matcher.unweighed_scores['collab-intensity'],
    [firm_data['collab-intensity']]
]
df.loc['employee-involvement'] = [
    matcher.weighed_scores['employee-involvement'],
    [org_data['employee-involvement']],
    matcher.unweighed_scores['employee-involvement'],
    [firm_data['employee-involvement']]
]
df.loc['form-of-help'] = [
    matcher.weighed_scores['form-of-help'],
    org_data['form-of-help'],
    matcher.unweighed_scores['form-of-help'],
    firm_data['form-of-help']
]

df.loc['expertises'] = [
    matcher.weighed_scores['expertises'],
    org_data['expertises'],
    matcher.unweighed_scores['expertises'],
    firm_data['expertises']
]
df.loc['barriers'] = [
    matcher.weighed_scores['barriers'],
    org_data['barriers'],
    matcher.unweighed_scores['barriers'],
    firm_data['barriers']
]
df.loc['reason-for-impact'] = [
    matcher.weighed_scores['reason-for-impact'],
    org_data['reason-for-impact'],
    matcher.unweighed_scores['reason-for-impact'],
    firm_data['reason-for-impact']
]

df.loc[:, 'Score'] = df.loc[:, 'Score']*100
df.loc[:, 'Weighed_Score'] = df.loc[:, 'Weighed_Score']*100

df = df.sort_values(by='Weighed_Score', ascending=False)

# Streamlit App
st.set_page_config(layout="wide")

color = 'green' if overall_score > 0.7 else 'orange' if overall_score > 0.5 else 'red'
percentages = {k: str(round(v * 100, 2))+'%' for k, v in matcher.nimps.items()}

st.header(f'''
          Score for this match: :{color}[{
          round(overall_score*100, 4)}%]
          ''')

if st.checkbox("Jak pracovat s touto stránkou?"):
    st.info('''Toto prostředí slouží k testování matchingu. 
            Na této stránce se náhodně vygeneruje firma a neziskovka, poté jsou _namatchovány_.
            ''', icon="ℹ️")

    st.info('''Nahoře je vidět celkové výsledné skóre. Pod __Match Results__ je detail tohoto matche.
            Data jsou seřazeny podle __Weighed Score__, tedy skóre dané otázky vynásobené důležitostí. Důležitosti (vzaté z Google Sheets > Matching Matrix) jsou na spodu stránky.
            ''', icon="ℹ️")

    st.info('''Kliknutím na `Generate New Firm & NGO` se náhodně vygeneruje nová firma a neziskovka a obnoví se skóre a matching.
            ''', icon="ℹ️")

st.button("Generate New Firm & NGO")

st.subheader('Match Results')

st.dataframe(
    df,
    use_container_width=True,
    column_config=dict(
        Score=st.column_config.NumberColumn('Match Score', format='%.0f %%'),
        Weighed_Score=st.column_config.NumberColumn(
            'Weighed_Score', format='%.0f %%'),
    ))

st.subheader('Importance of Categories')
st.write(percentages)
