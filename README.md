# Article_analysier

Leveraging ChatGPT to do sentiment analysis on a large amount of articles. Thus require using the api of OpenAI, more specifically requires api keys. It is also possible to do other anaysises on articels, depends on the capability of GPT you need to pass the suitable prompt for the task. The response just got responses of GPT and store them as json. The parser parses these json file and format them to dataframes. Note that the response of the GPT are strings, even when specified output as json for example. Thus need the parser to convert strings to proper json. Also note that GPT output can be invalid format therefor parsing error can occur.



## Usage

CSV file contains features of new articles including a column named body that is the raw text of the article body.

The response json file stores responses from GPT and suggestion is that it has the same name as the csv file for convience.

```python
# api_key is the openai api key
# path_csv is the csv file contains articles want to be analysed, and must contain a column named body which is the
# body part of each article.
# path_prompt is the path to the txt file that you store prompt
# path_response is the file path that you store responses
from response import get_response

api_key = "you_api_key"
path_csv = "test_data/2011_files_2.csv"
path_prompt = "prompt/prompt.txt"
path_response = "test_data/2011_files_2.json"

get_response(path_csv=path_csv, path_prompt=path_prompt, path_response_json=path_response, api_key=api_key, verbose=True)
```

Output file contains all contents from csv and parsed response from GPT response, suggested name convention is csv file name + "_final".

```python
# path_csv is the csv file contains articles want to be analysed, and must contain a column named body which is the
# body part of each article.
# path_response is the json file stores responses
# path_output is the output csv file

path_csv = "test_data/2011_files_2.csv"
path_response = "test_data/2011_files_2.json"
path_output = "test_data/2011_files_2_final.csv"

parse_response(path_csv, path_response, path_output)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

MIT License

Copyright (c) 2023 zhong3401
