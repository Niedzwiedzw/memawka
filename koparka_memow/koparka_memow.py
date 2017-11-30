import requests
from time import sleep
from pprint import pprint
from typing import List
from koparka_memow.exceptions import ResponseParsingException
from koparka_memow.settings import SETTINGS  # PyCharm is crying but this works just fine

from koparka_memow.models import GroupPost  # PyCharm is crying but this works just fine

from koparka_memow.token_manager.token_manager import TokenManager

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
        self.settings['accessToken'] = TokenManager.get_token()
        if limit is not None:
            self.settings['postsLimit'] = limit
        try:
            self.initialize_scraping()
        except ResponseParsingException as e:
            print(e)
            exit(-1)

    def initialize_scraping(self) -> None:
        response = requests.get(QUERY_SCHEME.format(*list(self.settings.values()))).json()

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
    koparka = KoparkaMemow(limit=5)

    for i in range(5):
        print(koparka.posts)
        sleep(1)
        koparka.next()
