# Wakawai Matching Algorithm Demo

This is a Streamlit application that demonstrates a simple matching algorithm for connecting non-profit organizations (NGOs) and companies based on their shared interests and goals.

## Features:

- **Random Data Generation:** The app generates sample data for both NGOs and firms, including categories, sub-categories, fields of influence, collaboration preferences, and more.
- **Matching Score Calculation:** A `Matcher` class calculates a match score based on the overlap between the NGO and firm data, weighted by the importance of each attribute.
- **Interactive Visualization:** The results are displayed in an interactive Streamlit app, showing the overall match score and a breakdown of scores for each attribute.
- **Importance Score Display:** Users can choose to view the relative importance assigned to each matching attribute.

## How it Works:

1. **Data Generation:** The app randomly selects values from predefined lists for various attributes of NGOs and firms.
2. **Matcher Class:** The `Matcher` class contains logic for calculating scores based on the overlap between NGO and firm data. Different scoring functions are used for different attributes.
3. **Score Calculation:** The `compute_match_score` method calculates the overall match score by summing the weighted scores for each attribute.
4. **Streamlit App:** The Streamlit app displays the generated data, the overall match score, and a detailed breakdown of scores for each attribute in a user-friendly table format.

## Files:

- `st_random_generation_matching.py`: v1 of the Streamlit application.
- `user_input_ui.py`: v2 of the Streamlit application file.
- `compute_score.py`: Contains the `Matcher` class with the matching algorithm logic.
- `randomly_generate.py`: NGO/Firm random generation functions.

## How to Run:

1. Make sure you have Streamlit installed: `pip install streamlit`
2. Navigate to the project directory in your terminal.
3. Run the app: `streamlit run user_input_ui.py`

## Future Improvements:

✅ **User Input:** Allow users to input their own data for NGOs and firms instead of relying on random generation.
🛠️ **Match User Input:** Run the matching and display results same way as in `st_random_generation_matching.py`.
📋 **Database Integration:** Connect the app to a database of real NGO and firm data for more realistic matching.
📋 **Advanced Matching Algorithms:** Explore and implement more sophisticated matching algorithms for improved accuracy.
📋 **Recommendation System:** Develop a recommendation system that suggests potential NGO-firm partnerships based on their match scores.
