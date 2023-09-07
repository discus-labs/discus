import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Dataset:
    """the class that holds all operations for a dataset"""

    def __init__(self, df: pd.DataFrame = None):
        """Initialize the Dataset with a given CSV file path."""
        self.data = df
        
    def _load_data(self, file_path):
        """Load data from the CSV file."""
        try:
            data = pd.read_csv(file_path)
            return data
        except Exception as e:
            raise ValueError(f"Error loading data from {file_path}: {str(e)}")

    def n_most_unique_elements(self, n):
        """
        Extracts the n most unique elements from a list of text inputs or a DataFrame.

        This function takes either a list of text inputs or a pandas DataFrame with exactly two columns
        and returns a list of n text inputs with the most unique content based on TF-IDF cosine similarity.

        Parameters:
        data (list or pd.DataFrame): The input data containing text inputs and optionally corresponding outputs.
                                    If data is a list, it should contain text input strings.
                                    If data is a DataFrame, it must have two columns: text inputs and text outputs.
        n (int): The number of most unique elements to extract.

        Returns:
        list or pd.DataFrame: If the input 'data' is a list, returns a list of n most unique text input strings.
                            If the input 'data' is a DataFrame, returns a DataFrame containing n rows of
                            most unique text input and output pairs.

        Raises:
        ValueError: If 'n' is less than or equal to 0.
        ValueError: If 'data' is not a list or a DataFrame with two columns.
        ValueError: If 'data' is a DataFrame with incorrect number of columns.
        ValueError: If the number of text inputs and outputs in the DataFrame is not the same.
        ValueError: If 'n' is greater than the number of elements in the input data.

        Note:
        The function calculates TF-IDF cosine similarity between text inputs and outputs. It then sorts the text
        inputs based on their maximum similarity scores, choosing the n most unique elements. If 'data' is a
        DataFrame, the function returns a DataFrame containing the selected text input and output pairs.
        """
        if n <= 0:
            raise ValueError("n must be greater than 0.")

        if isinstance(self.data, list):
            text_inputs = self.data
            text_outputs = []
            output_is_dataframe = False
        elif isinstance(self.data, pd.DataFrame):
            if self.data.shape[1] != 2:
                raise ValueError("The DataFrame must have exactly two columns for text inputs and outputs.")
            text_inputs = self.data.iloc[:, 0].tolist()
            text_outputs = self.data.iloc[:, 1].tolist()
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
            output_df = self.data[self.data.iloc[:, 0].isin(most_unique_elements)]
            return output_df
        else:
            return most_unique_elements 
    
    def elements_below_similarity_threshold(self, threshold):
        """
        Filters elements based on a similarity threshold using TF-IDF cosine similarity.

        This function takes either a list of text inputs or a pandas DataFrame with exactly two columns.
        It filters and returns elements whose similarity scores with all previous elements are below the specified threshold.

        Parameters:
        data (list or pd.DataFrame): The input data containing text inputs and optionally corresponding outputs.
                                    If data is a list, it should contain text input strings.
                                    If data is a DataFrame, it must have two columns: text inputs and text outputs.
        threshold (float): The similarity threshold (exclusive) between 0 and 1. Elements with all similarity scores below
                        this threshold will be selected.

        Returns:
        list or pd.DataFrame: If the input 'data' is a list, returns a list of selected text input and output tuples.
                            If the input 'data' is a DataFrame, returns a DataFrame containing selected
                            text input and output pairs.

        Raises:
        ValueError: If 'threshold' is less than or equal to 0 or greater than or equal to 1.
        ValueError: If 'data' is not a list or a DataFrame with two columns.
        ValueError: If 'data' is a DataFrame with incorrect number of columns.

        Note:
        The function calculates TF-IDF cosine similarity between text inputs. It filters elements based on the provided
        similarity threshold, selecting elements whose similarity scores with all previous elements are below the threshold.
        If 'data' is a DataFrame, the function returns a DataFrame containing the selected text input and output pairs.
        """
        if threshold <= 0 or threshold >= 1:
            raise ValueError("threshold must be between 0 and 1 exclusive.")

        if isinstance(self.data, list):
            text_inputs = self.data
            output_is_dataframe = False
        elif isinstance(self.data, pd.DataFrame):
            if self.data.shape[1] != 2:
                raise ValueError("The DataFrame must have exactly two columns for text inputs and outputs.")
            text_inputs = self.data.iloc[:, 0].tolist()
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
                selected_elements.append((input_text, self.data.iloc[idx, 1]))

        if output_is_dataframe:
            output_df = pd.DataFrame(selected_elements, columns=["Input", "Output"])
            return output_df
        else:
            return selected_elements

    
    def cleaning(self):
        """Include shnu's cleaning function for datasets.
        """

    def get_data(self):
        """Return the loaded dataset."""
        return self.data

    def __len__(self):
        """Return the number of examples in the dataset."""
        return len(self.data)

    def __repr__(self):
        """Return a string representation of the dataset."""
        return f"<SeedDataset with {len(self)} examples>"