import os
import random
import json

def split_code_into_small_parts(code, num_prefix=2, num_suffix=2):
    """
    Splits the code into many small parts, using 2-3 words for prefix and suffix, and 1 word for middle.

    Args:
        code (str): The entire code content as a string.
        num_prefix (int): Number of words in the prefix, defaults to 2.
        num_suffix (int): Number of words in the suffix, defaults to 2.

    Returns:
        list: A list of (prefix, middle, suffix) tuples, with one word in the middle.
    """
    words = code.split()  # Split the code into words
    examples = []

    if len(words) < num_prefix + num_suffix + 1:
        # Not enough words to create an example
        return examples

    # Create many small splits from the code
    for i in range(num_prefix, len(words) - num_suffix):
        prefix = ' '.join(words[i - num_prefix:i])  # 2-3 words before
        middle = words[i]  # 1 word in the middle
        suffix = ' '.join(words[i + 1:i + num_suffix + 1])  # 2-3 words after

        examples.append((prefix, middle, suffix))

    return examples


def process_files(directory, num_prefix=2, num_suffix=2):
    """
    Process code files in the directory and split them into small examples (prefix, middle, suffix).

    Args:
        directory (str): Path to the directory containing code files.
        num_prefix (int): Number of words in the prefix.
        num_suffix (int): Number of words in the suffix.

    Returns:
        list: A list of tuples with (prefix, middle, suffix) for each small code completion example.
    """
    examples = []

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):  # Ensure it's a file
            with open(file_path, 'r') as file:
                code = file.read()
                small_examples = split_code_into_small_parts(code, num_prefix, num_suffix)
                if small_examples:
                    examples.extend(small_examples)
                else:
                    # Just to track if no examples could be created
                    print(f"Skipping file {file_name}: Not enough words for prefix/middle/suffix.")

    return examples


if __name__ == '__main__':
    dataset = process_files('Code To Split/', num_prefix=2, num_suffix=2)  # Adjust prefix/suffix size if needed

    # Ensure we have at least 50 examples
    if len(dataset) < 50:
        print(f"Insufficient examples generated. Only {len(dataset)} examples found.")
    else:
        # Shuffle and limit the dataset to 50-70 examples
        random.shuffle(dataset)
        max_examples = min(len(dataset), random.randint(50, 70))
        limited_dataset = dataset[:max_examples]

        # Save the examples to a JSON file
        with open('code_completion_examples.json', 'w') as f:
            json.dump(limited_dataset, f, indent=4)

        print(f'Successfully saved {len(limited_dataset)} code completion examples to "code_completion_examples.json".')