import pandas as pd
import json
import openai
import time
from tenacity import retry, stop_after_attempt, wait_random_exponential, RetryError

def read_prompt(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except IOError:
        print(f"Error reading file '{file_path}'.")

def completion_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

def chat_completion(prompt_text, article, model="gpt-3.5-turbo", verbose=False):

    @retry(stop=stop_after_attempt(6), retry_error_cls=RetryError, wait=wait_random_exponential(min=1, max=60), retry_error_callback=lambda _: print("Retrying..."))
    def completion_with_retry(**kwargs):
        return completion_with_backoff(**kwargs)

    start_time = time.time()

    # Define the conversation history as a list of messages
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt_text},
        {"role": "user", "content": f"Article text:'''{article}'''"}
    ]

    if verbose:
        print(f"Processing Article - Time: {time.strftime('%H:%M:%S')}")

    try:
        response = completion_with_retry(model=model, temperature=0.5, messages=conversation, n=5, stop=None)
    except RetryError:
        # Handle the retry error by returning a default value
        response = None

    end_time = time.time()
    elapsed_time = end_time - start_time

    if verbose:
        print("Processing complete.")
        print(f"Time taken to process the article: {elapsed_time:.2f} seconds")

    return response

def get_response(path_csv, path_prompt, path_response_json, api_key, verbose=True):
    openai.api_key = api_key
    
    df_articles = pd.read_csv(path_csv)
    
    prompt_text = read_prompt(path_prompt)
    
    with open(path_response_json, 'w', encoding='utf-8') as output_file:
        for index, row in df_articles.iterrows():
            article = row['body']
            response = chat_completion(prompt_text, article, model="gpt-3.5-turbo", verbose=verbose)

            if response is not None:
                response_id = response['id']
                response_data = response.to_dict()

                df_articles.at[index, 'response_id'] = response_id

                # Write the response data to the output JSON file
                json.dump(response_data, output_file, ensure_ascii=False)
                output_file.write('\n')
                
    df_articles.to_csv(path_csv, index=False, encoding='utf-8')

