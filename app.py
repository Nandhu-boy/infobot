import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

# Load the CSV data into a pandas DataFrame
df = pd.read_csv('data.csv')

# Initialize Flask app
app = Flask(__name__)
CORS(app)



# Function to get fees of a college
def get_college_fees(college_name):
    college = df[df['college_name'].str.contains(college_name, case=False, na=False)]
    if not college.empty:
        return f"The fees of {college.iloc[0]['college_name']} is {college.iloc[0]['fees']}."
    else:
        return "Sorry, I couldn't find the fees for that college."

# Function to get college code
def get_college_code(college_name):
    college = df[df['college_name'].str.contains(college_name, case=False, na=False)]
    if not college.empty:
        return f"The code of {college.iloc[0]['college_name']} is {college.iloc[0]['college_code']}."
    else:
        return "Sorry, I couldn't find the code for that college."

# Function to get full details of a college
def find_college_details(college_name):
    college = df[df['college_name'].str.contains(college_name, case=False, na=False)]
    if not college.empty:
        college_info = college.iloc[0].to_dict()
        return f"College Name: {college_info['college_name']}, Review: {college_info['review']}, Placement: {college_info['placement']}, Fees: {college_info['fees']}"
    else:
        return "Sorry, I couldn't find any details for that college."

# Function to process user input and determine response
def process_query(user_input):
    user_input = user_input.lower()

    # Determine the intent based on keywords
    if 'fees' in user_input:
        college_name = user_input.split('fees of')[-1].strip()
        return get_college_fees(college_name)
    elif 'code' in user_input:
        college_name = user_input.split('code of')[-1].strip()
        return get_college_code(college_name)
    elif 'about' in user_input:
        college_name = user_input.split('about')[-1].strip()
        return find_college_details(college_name)
    else:
        return "I'm not sure how to help with that. Please ask about fees, college code, or details."

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message')

        if user_input:
            response = process_query(user_input)
        else:
            response = "Sorry, I didn't understand that."
        
        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'response': 'There was an error processing your request.'})

if __name__ == '__main__':
    app.run(debug=True)
