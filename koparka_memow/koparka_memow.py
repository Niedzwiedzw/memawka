import requests
from pprint import pprint
from typing import List
from exceptions import ResponseParsingException
from settings import SETTINGS  # PyCharm is crying but this works just fine

from models import Author, GroupPost  # PyCharm is crying but this works just fine


# .format(groupID, postLimitPerRequest, accessToken)
QUERY_SCHEME = ("https://graph.facebook.com/v2.11/{}/feed?"
                "fields=reactions.limit(0)"  # requested fields
                ".summary(1)%2Cmessage%2Cfrom%2Cmessage_tags%2Ccreated_time%2Cfull_picture%2Cid&"  # requested fields
                "limit={}"
                "&access_token={}")


class KoparkaMemow:

    def __init__(self, settings=SETTINGS, limit: int=None):
        self._current_chunk = None
        self._link_next = None
        self._link_previous = None

        self.settings = settings
        if limit is not None:
            self.settings['postsLimit'] = limit

        self.initialize_scraping()

    def initialize_scraping(self) -> None:
        response = requests.get(QUERY_SCHEME.format(*list(SETTINGS.values()))).json()

        try:
            self._link_next = response['paging']['next']
            self._current_chunk = response
        except KeyError as e:
            raise ResponseParsingException(f"\n\nSomething is wrong with the response, check the access token?"
                                           f"Response looks something like this:\n\n{response}")

    def next(self) -> None:
        try:
            response = requests.get(self._current_chunk['paging']['next']).json()
        except KeyError as e:
            raise ResponseParsingException(f"\n\nSomething is wrong with the response, check the access token?"
                                           f"Response looks something like this:\n\n{response}")
        self._current_chunk = response
        self._link_next = self._current_chunk['paging']['next']

    @property
    def posts(self) -> List[GroupPost]:
        return [GroupPost(post) for post in self._current_chunk['data']]


if __name__ == '__main__':
    print(KoparkaMemow(limit=5).posts)
