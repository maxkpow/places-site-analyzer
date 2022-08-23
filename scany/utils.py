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