import streamlit as st
import pandas as pd
from randomly_generate import generate_org_data, generate_firm_data, dict_to_dataframe
from compute_score import Matcher

# Initialize session state for NGO and Firm data if not already done
if 'ngo_data' not in st.session_state:
    st.session_state['ngo_data'] = {}
    st.session_state['ngo_status'] = 0
if 'firm_data' not in st.session_state:
    st.session_state['firm_data'] = {}
    st.session_state['firm_status'] = 0
if 'show_importances' not in st.session_state:
    st.session_state['show_importances'] = False

# Set page configuration
st.set_page_config(page_title='NGO-Firm Matching',
                   page_icon='🤝', layout='wide')

# Title
st.title('NGO-Firm Matching')

# Instructions
st.write('Vyplň údaje o firmě a neziskovce, nebo je náhodně vygeneruj.')

# Data definitions
category = ['Lidé', 'Zvířata', 'Příroda', 'Společnost', 'Udržitelnost']

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

fields_of_influence = ['Svět', 'ČR', 'Region']
collab_intensities = ['Aktivní spolupráce', 'Jednorázová pomoc']
employee_involvement = ['Zapojení Zaměstnanců', 'Bez zapojení zaměstanců']
forms_of_help = ['Finance', 'Hmotná pomoc', 'Dobrovolnictví',
                 'Expertní dobrovolnictví', 'Společný projekt']
expertises = ['Marketing', 'IT', 'HR', 'Právo', 'Sales',
              'Projektový Management', 'Výzkum', 'Management', 'Podnikání', 'Účetnictví', 'Jiné']
barriers = ['Žádná', 'Nemáme čas/Není to priorita', 'Omezené zdroje', 'Nedostatek znalostí a zkušeností', 'Složitá legislativa',
            'Majitelé v tom nevidí smysl', 'Rozdílné cíle a hodnoty', 'Komunikační bariéry', 'Nedůvěra a obavy', 'Neshody v očekávání a výsledcích']
reason_for_impact = ['Je to součastí našich hodnot', 'Zapojení zaměstnanců', 'Zlepšení brandu', 'Plnění ESG legislativy', 'Konkurenční výhoda',
                     'Zvýšit loajalitu zákazníků', 'Pozitivní odkaz naší společnosti', 'Zvýšení atraktivnosti u ESG investorů', 'Chceme zlepšit své vlastní okolí']

create_own = st.toggle('Vygenerovat vlastní NGO / Firmu')


# Initialize ngo_variable
ngo_data = None

# Initialize ngo_variable
firm_data = None

ngo_df = None

firm_df = None

if create_own:
    # Create tabs for NGO and Firm input
    tab1, tab2 = st.tabs(["NGO Input", "Firm Input"])

    # NGO Input Form
    with tab1:
        st.header('NGO Input Form')

        with st.form(key='ngo_form'):
            # Category
            ngo_category = st.multiselect(
                'Select Category (Max 2)', category, help='Select up to 2 categories.')

            # Validate category selection
            if len(ngo_category) > 2:
                st.error('You can select a maximum of 2 categories.')

            # Sub-category
            if ngo_category:
                ngo_sub_category_options = []
                for cat in ngo_category:
                    ngo_sub_category_options.extend(sub_category_dict[cat])
                ngo_sub_category = st.multiselect(
                    'Select Sub-Category', ngo_sub_category_options)
            else:
                ngo_sub_category = []
                st.info('Please select at least one category to see sub-categories.')

            # Field of Influence
            ngo_field_of_influence = st.selectbox(
                'Field of Influence', fields_of_influence)

            # Collaboration Intensity
            ngo_collab_intensity = st.selectbox(
                'Collaboration Intensity', collab_intensities)

            # Employee Involvement
            ngo_employee_involvement = st.selectbox(
                'Employee Involvement', employee_involvement)

            # Form of Help
            ngo_form_of_help = st.multiselect('Form of Help', forms_of_help)

            # Expertises
            ngo_expertises = st.multiselect('Expertises', expertises)

            # Barriers
            ngo_barriers = st.multiselect('Barriers', barriers)

            # Reason for Impact
            ngo_reason_for_impact = st.multiselect(
                'Reasons for Impact (Select 2-5)', reason_for_impact)
            if len(ngo_reason_for_impact) < 2 or len(ngo_reason_for_impact) > 5:
                st.error('Please select between 2 and 5 reasons for impact.')

            # Submit Button
            ngo_submit_button = st.form_submit_button(label='Submit NGO Data')

            if ngo_submit_button:
                # Validate inputs
                if len(ngo_category) > 2 or len(ngo_reason_for_impact) < 2 or len(ngo_reason_for_impact) > 5:
                    st.error('Please correct the errors above before submitting.')
                else:
                    # Process the NGO data
                    ngo_data = {
                        'category': ngo_category,
                        'sub-category': ngo_sub_category,
                        'field-of-influence': ngo_field_of_influence,
                        'collab-intensity': ngo_collab_intensity,
                        'employee-involvement': ngo_employee_involvement,
                        'form-of-help': ngo_form_of_help,
                        'expertises': ngo_expertises,
                        'barriers': ngo_barriers,
                        'reason-for-impact': ngo_reason_for_impact,
                    }

                    st.session_state['ngo_data'] = ngo_data
                    st.session_state['ngo_status'] = 1

                    st.success('NGO Data Submitted Successfully!')

    # Firm Input Form
    with tab2:
        st.header('Firm Input Form')

        with st.form(key='firm_form'):
            # Category
            firm_category = st.multiselect(
                'Select Category (Max 2)', category, help='Select up to 2 categories.')

            # Validate category selection
            if len(firm_category) > 2:
                st.error('You can select a maximum of 2 categories.')

            # Sub-category
            if firm_category:
                firm_sub_category_options = []
                for cat in firm_category:
                    firm_sub_category_options.extend(sub_category_dict[cat])
                firm_sub_category = st.multiselect(
                    'Select Sub-Category', firm_sub_category_options)
            else:
                firm_sub_category = []
                st.info('Please select at least one category to see sub-categories.')

            # Field of Influence
            firm_field_of_influence = st.selectbox(
                'Field of Influence', fields_of_influence)

            # Collaboration Intensity
            firm_collab_intensity = st.selectbox(
                'Collaboration Intensity', collab_intensities)

            # Employee Involvement
            firm_employee_involvement = st.selectbox(
                'Employee Involvement', employee_involvement)

            # Form of Help
            firm_form_of_help = st.multiselect('Form of Help', forms_of_help)

            # Expertises
            firm_expertises = st.multiselect('Expertises', expertises)

            # Barriers
            firm_barriers = st.multiselect('Barriers', barriers)

            # Reason for Impact
            firm_reason_for_impact = st.multiselect(
                'Reasons for Impact (Select 2-5)', reason_for_impact)
            if len(firm_reason_for_impact) < 2 or len(firm_reason_for_impact) > 5:
                st.error('Please select between 2 and 5 reasons for impact.')

            # Submit Button
            firm_submit_button = st.form_submit_button(
                label='Submit Firm Data')

            if firm_submit_button:
                # Validate inputs
                if len(firm_category) > 2 or len(firm_reason_for_impact) < 2 or len(firm_reason_for_impact) > 5:
                    st.error('Please correct the errors above before submitting.')
                else:
                    # Process the Firm data
                    firm_data = {
                        'category': firm_category,
                        'sub-category': firm_sub_category,
                        'field-of-influence': firm_field_of_influence,
                        'collab-intensity': firm_collab_intensity,
                        'employee-involvement': firm_employee_involvement,
                        'form-of-help': firm_form_of_help,
                        'expertises': firm_expertises,
                        'barriers': firm_barriers,
                        'reason-for-impact': firm_reason_for_impact,
                    }

                    st.session_state['firm_data'] = firm_data
                    st.session_state['firm_status'] = 1

                    st.success('Firm Data Submitted Successfully!')


# Two columns for displaying NGO and Firm data
col1, col2 = st.columns(2)

# Display NGO data in the first column
with col1:

    st.write("### NGO Data")

    if st.button("Vygeneratovat náhodnou NGO"):

        ngo_data = generate_org_data()

        st.session_state['ngo_data'] = ngo_data
        st.session_state['ngo_status'] = 1

    ngo_df_data = {"Key": list(st.session_state['ngo_data'].keys()), "Values": [", ".join(map(
        str, v)) if isinstance(v, list) else v for v in st.session_state['ngo_data'].values()]}
    ngo_df = pd.DataFrame(ngo_df_data['Values'],
                          index=ngo_df_data['Key'], columns=['Odpovědi'])
    st.dataframe(ngo_df, use_container_width=True)


# Display Firm data in the second column
with col2:
    st.write("### Firm Data")

    if st.button("Vygenerovat náhodnou firmu"):

        firm_data = generate_firm_data()

        st.session_state['firm_data'] = firm_data
        st.session_state['firm_status'] = 1

    firm_df_data = {"Key": list(st.session_state['firm_data'].keys()), "Values": [", ".join(map(
        str, v)) if isinstance(v, list) else v for v in st.session_state['firm_data'].values()]}
    firm_df = pd.DataFrame(firm_df_data['Values'],
                           index=firm_df_data['Key'], columns=['Odpovědi'])

    st.dataframe(firm_df, use_container_width=True)

st.header('Matching')

if st.button('Vypočítat Match'):
    matcher = Matcher()

    overall_score = matcher.compute_match_score(
        st.session_state['ngo_data'], st.session_state['firm_data'])

    df = pd.DataFrame(
        columns=['Weighed_Score',  'Sample Firm', 'Score', 'Sample NGO'],
        index=['category', 'sub-category', 'field-of-influence', 'collab-intensity',
               'employee-involvement', 'form-of-help', 'expertises', 'barriers', 'reason-for-impact']
    )

    df.loc['category'] = [
        matcher.weighed_scores['category'],
        st.session_state['ngo_data']['category'],
        matcher.unweighed_scores['category'],
        st.session_state['firm_data']['category']
    ]
    df.loc['sub-category'] = [
        matcher.weighed_scores['sub-category'],
        st.session_state['ngo_data']['sub-category'],
        matcher.unweighed_scores['sub-category'],
        st.session_state['firm_data']['sub-category']
    ]
    df.loc['field-of-influence'] = [
        matcher.weighed_scores['field-of-influence'],
        [st.session_state['ngo_data']['field-of-influence']],
        matcher.unweighed_scores['field-of-influence'],
        [st.session_state['firm_data']['field-of-influence']]
    ]
    df.loc['collab-intensity'] = [
        matcher.weighed_scores['collab-intensity'],
        [st.session_state['ngo_data']['collab-intensity']],
        matcher.unweighed_scores['collab-intensity'],
        [st.session_state['firm_data']['collab-intensity']]
    ]
    df.loc['employee-involvement'] = [
        matcher.weighed_scores['employee-involvement'],
        [st.session_state['ngo_data']['employee-involvement']],
        matcher.unweighed_scores['employee-involvement'],
        [st.session_state['firm_data']['employee-involvement']]
    ]
    df.loc['form-of-help'] = [
        matcher.weighed_scores['form-of-help'],
        st.session_state['ngo_data']['form-of-help'],
        matcher.unweighed_scores['form-of-help'],
        st.session_state['firm_data']['form-of-help']
    ]

    df.loc['expertises'] = [
        matcher.weighed_scores['expertises'],
        st.session_state['ngo_data']['expertises'],
        matcher.unweighed_scores['expertises'],
        st.session_state['firm_data']['expertises']
    ]
    df.loc['barriers'] = [
        matcher.weighed_scores['barriers'],
        st.session_state['ngo_data']['barriers'],
        matcher.unweighed_scores['barriers'],
        st.session_state['firm_data']['barriers']
    ]
    df.loc['reason-for-impact'] = [
        matcher.weighed_scores['reason-for-impact'],
        st.session_state['ngo_data']['reason-for-impact'],
        matcher.unweighed_scores['reason-for-impact'],
        st.session_state['firm_data']['reason-for-impact']
    ]

    df.loc[:, 'Score'] = df.loc[:, 'Score']*100
    df.loc[:, 'Weighed_Score'] = df.loc[:, 'Weighed_Score']*100

    df = df.sort_values(by='Weighed_Score', ascending=False)

    # Streamlit App

    color = 'green' if overall_score > 0.7 else 'orange' if overall_score > 0.5 else 'red'
    percentages = {k: str(round(v * 100, 2))+'%' for k,
                   v in matcher.nimps.items()}

    st.header(f'''
            Výsledné Match Skóre: :{color}[{
        round(overall_score*100, 4)}%]
            ''')

    st.subheader('Match Results')

    st.dataframe(
        df,
        use_container_width=True,
        column_config=dict(
            Score=st.column_config.NumberColumn(
                'Match Score', format='%.0f %%'),
            Weighed_Score=st.column_config.NumberColumn(
                'Weighed_Score', format='%.0f %%'),
        ))

    st.write('Důležitosti')
    st.write(percentages)
