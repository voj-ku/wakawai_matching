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
subcategory = ['sub1', 'sub2', 'sub3', 'sub4',
               'sub5', 'sub6', 'sub7', 'sub8', 'sub9',
               'sub10', 'sub11', 'sub12', 'sub13', 'sub14', 'sub15']

# 3
fields_of_influence = ['global', 'czechia', 'region']
regions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# 4
collab_intensities = ['one-time', 'multiple']

# 5
employee_involvement = ['yes', 'no']

# 6 form of help
forms_of_help = ['monetary', 'physical', 'volunteering',
                 'expert-knowledge', 'shared-project']

# 7 expertises
expertises = ['marketing', 'hr', 'it', 'law', 'sales',
              'labour', 'other1', 'other2', 'other3', 'other4', 'other5']

# 8 barriers
barriers = ['Žádná', 'Nemáme čas/Není to priorita', 'Omezené zdroje', 'Nedostatek znalostí a zkušeností', 'Složitá legislativa',
            'Majitelé v tom nevidí smysl', 'Rozdílné cíle a hodnoty', 'Komunikační bariéry', 'Nedůvěra a obavy', 'Neshody v očekávání a výsledcích']

# 9 reasons for impact
reason_for_impact = ['Je to součastí našich hodnot', 'Zapojení zaměstnanců', 'Zlepšení brandu', 'Plnění ESG legislativy', 'Konkurenční výhoda',
                     'Zvýšit loajalitu zákazníků', 'Pozitivní odkaz naší společnosti', 'Zvýšení atraktivnosti u ESG investorů', 'Chceme zlepšit své vlastní okolí']

# Select a random number between 1 and 3
num_items_org1 = random.randint(1, 2)
num_items_fir1 = random.randint(1, 2)

# Generate a new list with the randomly chosen number of items
org1_category = random.sample(category, num_items_org1)
fir1_category = random.sample(category, num_items_fir1)

org1 = {'category': org1_category}
fir1 = {'category': fir1_category}

# Example usage:
matcher = Matcher()

org_data = {
    # pick one or two category
    'category': random.sample(category, random.randint(1, 2)),
    # pick one to ten random subcategory
    'sub-category': random.sample(subcategory, random.randint(1, 10)),
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
    # pick one to ten random subcategory
    'sub-category': random.sample(subcategory, random.randint(1, 10)),
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

# if st.checkbox('Show total importance scores'):
#     st.write(percentages)
#     color = st.color_picker("Pick A Color", "#00f900")
#     st.write("The current color is", color)
