import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def n_most_unique_elements(data, n):
    if n <= 0:
        raise ValueError("n must be greater than 0.")

    if isinstance(data, list):
        text_inputs = data
        text_outputs = []
        output_is_dataframe = False
    elif isinstance(data, pd.DataFrame):
        if data.shape[1] != 2:
            raise ValueError("The DataFrame must have exactly two columns for text inputs and outputs.")
        text_inputs = data.iloc[:, 0].tolist()
        text_outputs = data.iloc[:, 1].tolist()
        output_is_dataframe = True
    else:
        raise ValueError("Input data must be a list or a pandas DataFrame with two columns.")

    num_elements = len(text_inputs)

    if len(text_outputs) != 0 and len(text_outputs) != num_elements:
        raise ValueError("If 'data' is a DataFrame, the number of text inputs and outputs must be the same.")

    if n > num_elements:
        raise ValueError(f"n cannot be greater than the number of elements in the input data ({num_elements}).")

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(text_inputs)

    if len(text_outputs) != 0:
        tfidf_matrix_outputs = vectorizer.transform(text_outputs)
        similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix_outputs)
    else:
        similarity_matrix = cosine_similarity(tfidf_matrix)

    max_similarity_scores = []
    for idx, input_text in enumerate(text_inputs):
        max_similarity = max(similarity_matrix[idx][:idx], default=0)
        max_similarity_scores.append((input_text, max_similarity))

    max_similarity_scores.sort(key=lambda x: x[1])
    most_unique_elements = [element[0] for element in max_similarity_scores[:n]]

    if output_is_dataframe:
        output_df = data[data.iloc[:, 0].isin(most_unique_elements)]
        return output_df
    else:
        return most_unique_elements

def elements_below_similarity_threshold(data, threshold):
    if threshold <= 0 or threshold >= 1:
        raise ValueError("threshold must be between 0 and 1 exclusive.")

    if isinstance(data, list):
        text_inputs = data
        output_is_dataframe = False
    elif isinstance(data, pd.DataFrame):
        if data.shape[1] != 2:
            raise ValueError("The DataFrame must have exactly two columns for text inputs and outputs.")
        text_inputs = data.iloc[:, 0].tolist()
        output_is_dataframe = True
    else:
        raise ValueError("Input data must be a list or a pandas DataFrame with two columns.")

    num_elements = len(text_inputs)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(text_inputs)

    similarity_matrix = cosine_similarity(tfidf_matrix)

    selected_elements = []
    for idx, input_text in enumerate(text_inputs):
        similarity_scores = similarity_matrix[idx]
        if all(similarity < threshold for similarity in similarity_scores[:idx]):
            selected_elements.append((input_text, data.iloc[idx, 1]))

    if output_is_dataframe:
        output_df = pd.DataFrame(selected_elements, columns=["Input", "Output"])
        return output_df
    else:
        return selected_elements
