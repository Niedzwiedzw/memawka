from datetime import datetime
from copy import copy
import json

from models import Author


class GroupPost:
    def __init__(self, raw_post):
        self.id = int(raw_post.get('id'))
        self.creation = datetime.strptime(raw_post.get('created_time'), '%Y-%m-%dT%H:%M:%S+0000')
        self.author = Author(raw_post.get('from'))
        self.message = raw_post.get('message')

        self.reaction_count = int(raw_post.get('reactions', copy({}))
                                  .get('summary', copy({}))
                                  .get('total_count', copy({})))

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other: Author) -> bool:
        return self.id == other.id
