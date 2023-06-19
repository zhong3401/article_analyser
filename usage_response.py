from response import get_response

api_key = "you_api_key"
path_csv = "test_data/2011_files_2.csv"
path_prompt = "prompt/prompt.txt"
path_response = "test_data/2011_files_2.json"

get_response(path_csv=path_csv, path_prompt=path_prompt, path_response_json=path_response, verbose=True)

