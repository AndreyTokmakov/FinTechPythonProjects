from enum import Enum


class HTTPHeader(str, Enum):
    Accept = 'Accept'
    Authorization = 'Authorization'
    AcceptLanguage = 'Accept-Language'
    Host = 'Host'
    UserAgent = 'User-Agent'
    ContentType = 'Content-Type'
    ContentLength = 'Content-Length'

    def __str__(self):
        return self.value
