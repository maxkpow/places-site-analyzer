from abc import ABC, abstractmethod
from enum import Enum
import gzip
import brotli
from urllib.parse import urlparse
from analyzer.constants import CONTENT_TYPES, SEARCH_WORDS
from analyzer.models import HTTPResponse
from typing import List

class ContentEncoding(Enum):
    GZIP = "gzip"
    BR = "br"


class Parser(ABC):
    
    @abstractmethod
    def parse(content):
        pass

    @classmethod
    def search_words(self, content: str = "") -> bool:
        try:
            if any(map(lambda x: x in content.lower(), SEARCH_WORDS)):
                return True
            else:
                return False
        except:
            return False
    
    @classmethod
    def is_same_host(self, src: str, website: str) -> bool:
        script_source = urlparse(src)
        website_source = urlparse(website)

        try:
            if website_source.netloc in script_source.netloc:
                return True
            else:
                return False
        except:
            return False


class HTTPParser(Parser):

    def content_decoder(self, content: str, content_encoding: ContentEncoding):
        if content_encoding == ContentEncoding.GZIP.value:
            return gzip.decompress(content).decode("utf-8")
        elif content_encoding == ContentEncoding.BR.value:
            return brotli.decompress(content).decode("utf-8")
        else:
            return content

    def parse(self, requests: List):
        for request in requests:
            if request.response:
                response_content_type = request.response.headers.get("content-type", "")
                is_target_content_type = any(map(lambda x: x in response_content_type, CONTENT_TYPES))

                if is_target_content_type:
                    headers = dict((key, value) for key, value in request.response.headers.items())
                    response_content_encoding = request.response.headers['content-encoding']
                    
                    response_body = self.content_decoder(request.response.body, response_content_encoding)
                    are_search_words_in_body = self.search_words(response_body)

                    captured_request: HTTPResponse = {
                        "location_words": are_search_words_in_body,
                        "host": request.host,
                        "url": request.url, 
                        "path": request.path,
                        "method": request.method,
                        "status": request.response.status_code,
                        "headers": headers,
                        "content_encoding": response_content_encoding,
                        "content_type": response_content_type,
                        "content_length": request.response.headers["content-length"],
                        "body": response_body,
                    }

                    yield captured_request

class ScriptsParser(Parser):

    def parse(self, scripts: List, website: str =None) -> List[dict]:
        if scripts:
            # import pdb;pdb.set_trace()
            for script in scripts:
                src = script.get_attribute("src")
                content = script.get_attribute("innerHTML")

                are_search_words_in_body = self.search_words(content)

                if website:
                    is_same_host: bool = self.is_same_host(src, website)
                else:
                    is_same_host: bool = False

                yield {
                    "location_words": are_search_words_in_body,
                    "src": src,
                    "is_same_host": is_same_host,
                    "content_length": len(content),
                    "text": content if content else False,
                }


class ListsParser(Parser):

    def parse(self, html_lists: List):
        if html_lists:
            for html_list in html_lists:
                content = html_list.text
                content_length = len(content)

                are_search_words_in_body = self.search_words(content)

                if content_length:
                    yield {
                        "location_words": are_search_words_in_body,
                        "tag": html_list.tag_name,
                        "text": content,
                        "content_length": content_length,
                    }


class LinksParser(Parser):

    def parse(self, links_list: List, website):
        if links_list:
            for link in links_list:
                content = link.text
                href = link.get_attribute("href")
                content_length = len(content)

                if website:
                    is_same_host: bool = self.is_same_host(href, website)
                else:
                    is_same_host: bool = False
                
                are_search_words_in_body = self.search_words(content)

                if content_length:
                    yield {
                        "is_same_host": is_same_host,
                        "location_words": are_search_words_in_body,
                        "tag": link.tag_name,
                        "text": content,
                        "href": href,
                        "content_length": content_length,
                    }