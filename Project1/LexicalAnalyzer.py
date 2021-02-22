import re
import sys

# Declaring the regular expressions utilized in the code
keywords = re.compile(r'(?:^|\W)(else|if|int|return|void|while)(?:$|\W)')
symbols = re.compile(r'(<=|>=|==|!=|/\*|\*/|\+|-|\*|/|<|>|=|;|,|\(|\)|\[|\]|{|\})')
letters = re.compile(r'[a-zA-Z]+')
digits = re.compile(r'[0-9]+')
errors = re.compile(r'.')

# The function used for removing the comments in the input file
def commentRemoval(text):
    text = re.sub(r"(//.*\n)|(/\*(.|\n)*?\s\*/)|(//.*\n)|(/\*(.|\n)*?\*/)", '', text)
    return text

# The function used for splitting the
def splitter(text):
    text = re.sub(r'(<=|>=|==|!=|/\*|\*/|\+|-|\*|/|<|>|=|;|,|\(|\)|\[|\]|{|\})', r' \1 ', text)
    text = re.sub(r'((@|#|\$|%|\^|&|_|;|\?|\.|\||!|[0-9])\S+)', r' \1', text)
    text = re.split(r'\s+', text.strip())
    return text

# The function used for tokenizing the input
def tokenizer(Input):
    words_list = commentRemoval(Input)
    words_list = splitter(words_list)

    tokenized_list = []

    for match in words_list:
        # Checking to see if this is a special keyword
        if keywords.search(match):
            print(f"KW: {match}")
            tokenized_list.append(f"KW: {match}")
        # Checking to see if the sequence is one of the listed characters of operators and etc.
        elif symbols.search(match):
            print(f"{match}")
            tokenized_list.append(f"{match}")
        # Checking to see if the sequence is letters to comprise of ID
        elif letters.search(match) and not re.compile(r"[^a-zA-Z]+").search(match):
            print(f"ID: {match}")
            tokenized_list.append(f"ID: {match}")
        # Checking to see if the sequence is numbers
        elif digits.search(match):
            # Don't judge me for this code but there was an annoying bug that would split twice in a sequence of
            # characters that contained both numbers and special characters/errors. This if statement checks to see if
            # its just a string of numbers and the else is to make sure to split any non numbers
            if digits.search(match) and not re.compile(r"[^0-9]+").search(match):
                print(f"INT: {match}")
                tokenized_list.append(f"INT: {match}")
            else:
                temp = re.sub(r'(@|#|\$|%|\^|&|_|;|\?|\.|\|)', r' \1', match)
                temp = re.split(r'\s+', temp)
                for match2 in temp:
                    if digits.search(match2) and not re.compile(r"[^0-9]+").search(match2):
                        print(f"INT: {match2}")
                        tokenized_list.append(f"INT: {match2}")
                    else:
                        print(f"Error: {match2}")
        # Catch all for errors
        elif errors.search(match):
            print(f"Error: {match}")
    return tokenized_list

# Opening the file
with open(sys.argv[1], "r") as file:
    characters = file.read()
    output = re.split(r'\n', characters)

    for x in range(len(output)):
        if output[x]:
            print(fr"Input: {output[x]}")

# Puts the tokenized list into the token_list variable
token_list = tokenizer(characters)
