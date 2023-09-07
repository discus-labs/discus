# Cleaning Functions

## Find the Most Unique Elements

Extracts the n most unique elements from a list of text inputs or a DataFrame.

This function takes either a list of text inputs or a pandas DataFrame with exactly two columns
and returns a list of n text inputs with the most unique content based on TF-IDF cosine similarity.

Parameters:
data (list or pd.DataFrame): The input data containing text inputs and optionally corresponding outputs.
n (int): The number of most unique elements to extract.

Returns:
list or pd.DataFrame: If the input 'data' is a list, returns a list of n most unique text input strings. If the input 'data' is a DataFrame, returns a DataFrame containing n rows of most unique text input and output pairs.

```Python
gen = Dataset(generated_data)
result = gen.n_most_unique_elements(1000)
```

Note: The function calculates TF-IDF cosine similarity between text inputs and outputs. It then sorts the text inputs based on their maximum similarity scores, choosing the n most unique elements. If 'data' is a DataFrame, the function returns a DataFrame containing the selected text input and output pairs.

## Elements Below Similarity Threshold

Filters elements based on a similarity threshold using TF-IDF cosine similarity.

This function takes either a list of text inputs or a pandas DataFrame with exactly two columns. It filters and returns elements whose similarity scores with all previous elements are below the specified threshold.

Parameters:
data (list or pd.DataFrame): The input data containing text inputs and optionally corresponding outputs. If data is a list, it should contain text input strings. If data is a DataFrame, it must have two columns: text inputs and text outputs.
threshold (float): The similarity threshold (exclusive) between 0 and 1. Elements with all similarity scores below this threshold will be selected.

Returns:
list or pd.DataFrame: If the input 'data' is a list, returns a list of selected text input and output tuples. If the input 'data' is a DataFrame, returns a DataFrame containing selected text input and output pairs.

Note:
The function calculates TF-IDF cosine similarity between text inputs. It filters elements based on the provided similarity threshold, selecting elements whose similarity scores with all previous elements are below the threshold. If 'data' is a DataFrame, the function returns a DataFrame containing the selected text input and output pairs.
