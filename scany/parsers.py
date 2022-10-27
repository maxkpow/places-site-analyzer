from abc import ABC, abstractmethod
from enum import Enum
from typing import List
import re
import gzip
import brotli
import logging
from urllib.parse import urlparse
from scany.constants import CONTENT_TYPES, SEARCH_WORDS
from scany.models import HTTPResponse
from scany.analyzers import ScriptAnalyzer, HTTPAnalyzer


class ContentEncoding(Enum):
    GZIP = "gzip"
    BR = "br"


class Parser(ABC):
    
    @abstractmethod
    def parse(content: str):
        pass

    def search_words(self, content: str = "") -> bool:
        try:
            
            found_words = [{word: re.findall(word, content.lower())} for word in SEARCH_WORDS if re.findall(word, content.lower())]
            
            if len(found_words):
                return found_words
            else:
                return False
        except:
            return False
    
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

    def is_target_contenttype(self, contenttype: str):
        return any(map(lambda x: x in contenttype, CONTENT_TYPES))

    def content_decoder(self, content: str, content_encoding: ContentEncoding):
        try:
            if content_encoding == ContentEncoding.GZIP.value:
                return gzip.decompress(content).decode("utf-8")
            elif content_encoding == ContentEncoding.BR.value:
                return brotli.decompress(content).decode("utf-8")
            else:
                return content
        except UnicodeDecodeError:
            logging.warning(msg="Error while decoding content!")
            return content

    def parse(self, requests: List):
        for request in requests:
            if request.response:
                content_length = len(request.response.body)
                response_content_type = request.response.headers.get("content-type", "")
                is_target_content_type = self.is_target_contenttype(response_content_type)

                if is_target_content_type and content_length > 100:
                    headers = dict((key, value) for key, value in request.response.headers.items())
                    response_content_encoding = request.response.headers['content-encoding']
                    
                    response_body = self.content_decoder(request.response.body, response_content_encoding)
                    
                    if type(response_body) == "str":
                        http_analyzer = HTTPAnalyzer(
                            host=request.host, 
                            request_url=request.url,
                            method=request.method,
                            status=request.response.status_code,
                            headers=headers,
                            content_encoding=response_content_encoding,
                            content_type=response_content_type,
                            content_length=request.response.headers["content-length"],
                            body=response_body,
                        )

                        yield http_analyzer.analyze()
                    
                    else:
                        yield {
                            "host": request.host,
                            "request_url": request.url,
                            "method": request.method,
                            "status": request.response.status_code,
                            "headers": headers,
                            "content_encoding": response_content_encoding,
                            "content_type": response_content_type,
                            "content_length": request.response.headers["content-length"],
                            "is_same_host": "",
                            "coords_amount": "",
                            "found_search_words": "",
                            "raw_body": response_body,
                        }


class ScriptsParser(Parser):

    def parse(self, scripts: List, website: str = None) -> List[dict]:
        if scripts:
            for script_index, script in enumerate(scripts):
                src = script.get_attribute("src")
                body = script.get_attribute("innerHTML")
                content_length = len(body)

                if content_length > 100:
                    scripts_analyzer = ScriptAnalyzer(script_index, src, website, body)
                    yield scripts_analyzer.analyze()


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
                        "content_length": content_length,
                        "body": content,
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
                        "href": href,
                        "content_length": content_length,
                        "body": content,
                    }