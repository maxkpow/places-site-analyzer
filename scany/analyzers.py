from abc import ABC, abstractmethod
import re
import string
from typing import Dict, List, Tuple
from urllib.parse import urlparse
from scany.constants import SEARCH_WORDS

class Analyzer(ABC):

    def __clean_symbols(self, content: str) -> List[str]:
        '''
        Removes:
        - punctuation symbols;
        - tabs;
        - spaces;
        - returns;
        - new line symbols;

        Returns list of words.
        '''
        removed_tabs = re.sub(r'\t+', ' ', content)
        removed_new_lines = re.sub(r'\n+', ' ', removed_tabs)
        removed_return = re.sub(r'\r+', ' ', removed_new_lines)
        removed_spaces = re.sub(r'\s+', ' ', removed_return)
        removed_punctuation = "".join([symbol for symbol in removed_spaces if symbol not in string.punctuation])

        words_list: List[str] = removed_punctuation.split(' ')
        return words_list
    
    def __match_coords(self, content: str) -> int:
        '''
        Functions searches for float spatial coordinates.
        Success seach for: 45.34234, 123.12414, -34.342, -1.231
        '''
        matched_coordinates: List[str] = re.findall(r"(?<!\d)\d{,3}(?<=\d)\.\d{,20}", content)
        points_amount: float = len(matched_coordinates) / 2

        return int(points_amount)
    
    def __calc_words(self, word_cloud: List[str]) -> Dict[str, int]:
        word_dict = {}

        for word in word_cloud:
            if word not in word_dict.keys():
                word_dict[word] = 1
            else:
                word_dict[word] += 1
        
        return word_dict
    

    def __match_words(self, content: List[str]) -> bool | dict:
        try:
            
            found_words = [word for word in SEARCH_WORDS if word in content.lower()]
            count_words = self.__calc_words(found_words)
            
            if len(count_words):
                return count_words
            else:
                return False
        except:
            return False
    

    def __is_same_host(self, src: str, website: str) -> bool:
        script_source = urlparse(src)
        website_source = urlparse(website)

        try:
            if website_source.netloc in script_source.netloc:
                return True
            else:
                return False
        except:
            return False
    
    @abstractmethod
    def analyze(self):
        pass


class ScriptAnalyzer(Analyzer):

    def __init__(
        self, 
        script_index: int, 
        src: str, 
        website: str, 
        body: str
    ):
        self.script_index = script_index
        self.src = src
        self.website = website
        self.body = body


    def words_coords_distance(self, word_stats: Dict[str, int], coords_amount: int):
        pass
    
    def analyze(self):
        is_same_host: bool = self.__is_same_host(self.src, self.website)
        coords_amount: int = self.__match_coords(self.body)
        cleaned_body: List[str] = self.__clean_symbols(self.body)
        found_search_words: bool | dict = self.__match_words(cleaned_body)
        words_stats: dict = self.__calc_words(self.body)

        yield {
            "src": self.src,
            "is_same_host": is_same_host,
            "coords_amount": coords_amount,
            "found_search_words": found_search_words,
            "words_stats": words_stats,
        }