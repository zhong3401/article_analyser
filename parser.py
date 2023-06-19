import pandas as pd
import json

# extract content string
# get response contents (a list of content), a content contains a list of answer string 
def extract_contents(openai_objects):
    if isinstance(openai_objects, dict):
        openai_objects = [openai_objects]

    contents = []
    for obj in openai_objects:
        choices = obj['choices']
        content = []
        for choice in choices:
            content.append(choice['message']['content'])
        contents.append(content)
    return contents

# parse string to json
def extract_answers(contents):
    answers = []
    for content in contents:
        answer_ls = []
        for answer_str in content:
#             answer_str = answer_str.replace('null', '"null"')
#             answer_str = answer_str.replace("\n", "")

            try:
                answer = json.loads(answer_str)
                answer_ls.append(answer)
            except json.JSONDecodeError:
                answer_ls.append(None)
                continue
        answers.append(answer_ls)
    return answers

# extract values from json
def extract_values(answers):
    values = []
    for answer in answers:
        value = []
        for an in answer:
            if an is not None:
                value.append(an.get('current_inflation', None))
                value.append(an.get('current_inflation_sentiment', None))
                value.append(an.get('expected_inflation', None))
                value.append(an.get('expected_inflation_sentiment', None))
                value.append(an.get('explanation', None))
            else:
                value.extend([999, 999, 999, 999, 999])
        values.append(value)
    return values

def create_dataframe(openai_objects, values):
    response_id = []
    for obj in openai_objects:
        response_id.append(obj['id'])
        
    column_labels = ['ci_0', 'cis_0', 'ei_0', 'eis_0', 'exp_0',
                     'ci_1', 'cis_1', 'ei_1', 'eis_1', 'exp_1',
                     'ci_2', 'cis_2', 'ei_2', 'eis_2', 'exp_2',
                     'ci_3', 'cis_3', 'ei_3', 'eis_3', 'exp_3',
                     'ci_4', 'cis_4', 'ei_4', 'eis_4', 'exp_4']
    df_values = pd.DataFrame(values, columns=column_labels)
    df_values['response_id'] = response_id
    return df_values

def parse_response(path_csv, path_response_json, path_output):
    # Read the JSON file
    with open(path_response_json, 'r', encoding='utf-8') as file:
        json_data = file.readlines()

    # Parse each JSON object
    openai_objects = []
    for line in json_data:
        try:
            json_object = json.loads(line)
            openai_objects.append(json_object)
        except json.JSONDecodeError as e:
            pass
        
    contents = extract_contents(openai_objects)
    answers = extract_answers(contents)
    values = extract_values(answers)
    df_values = create_dataframe(openai_objects, values)
    
    df_articles = pd.read_csv(path_csv)
    
    merged_df = pd.merge(df_articles, df_values, on='response_id')
    
    merged_df.to_csv(path_output, index=False, encoding='utf-8')
