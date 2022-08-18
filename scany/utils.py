import bs4
from typing import Dict, List, Tuple
import re
import string


def filter_blank_html_elements(html_elements_list: List[bs4.element.Tag]) -> List[Tuple[int, str]]:
    '''
    Function generates new list of text from tags, 
    which contain any content with length higher than 100 symbols.
    '''
    not_blank_html_elements = []

    for index, html_element in enumerate(html_elements_list):
        if len(html_element.text) > 100:
            not_blank_html_elements.append((index, html_element.text))
    
    return not_blank_html_elements
    

def match_coords_amount(content: str) -> int:
    '''
    Functions searches for float spatial coordinates.
    Success seach for: 45.34234, 123.12414, -34.342, -1.231
    '''
    matched_coordinates: List[str] = re.findall(r"(?<!\d)\d{,3}(?<=\d)\.\d{,20}", content)
    points_amount: float = len(matched_coordinates) / 2

    return int(points_amount)
    

def filter_content_without_coords(scripts_list: List[Tuple[int, str]] ):
    '''
    Function generates new list of scripts, 
    which contain any content which length higher than 100 symbols.
    '''
    for script_index, script_content in scripts_list:
        amount_of_coords: int = match_coords_amount(script_content)

        if amount_of_coords:
            yield (script_index, amount_of_coords)


def symbol_clean(content: str) -> List[str]:
    removed_tabs = re.sub(r'\t+', ' ', content)
    removed_new_lines = re.sub(r'\n+', ' ', removed_tabs)
    removed_return = re.sub(r'\r+', ' ', removed_new_lines)
    removed_spaces = re.sub(r'\s+', ' ', removed_return)
    removed_punctuation = "".join([symbol for symbol in removed_spaces if symbol not in string.punctuation])

    tokenized_words = removed_punctuation.split(' ')
    return tokenized_words


def calculate_words(word_cloud: List[str]) -> Dict[str, int]:
    word_dict = {}

    for word in word_cloud:
        if word not in word_dict.keys():
            word_dict[word] = 1
        else:
            word_dict[word] += 1
    
    return word_dict