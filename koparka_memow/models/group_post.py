from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.conf import settings
from copy import copy
import pytz
import json

from koparka_memow.models import Author

local_tz = pytz.timezone('Poland')


class GroupPost:
    def __init__(self, raw_post):
        self.facebook_id = str(raw_post.get('id'))
        try:
            self.creation = local_tz.localize(datetime.strptime(raw_post.get('created_time'), '%Y-%m-%dT%H:%M:%S+0000'),
                                              is_dst=None)
        except pytz.AmbiguousTimeError as e:
            print(e)
            self.creation = local_tz.localize(datetime.strptime(raw_post.get('created_time'), '%Y-%m-%dT%H:%M:%S+0000')
                                              + timedelta(hours=1),
                                              is_dst=None)
        self.author = Author(raw_post.get('from'))
        self.message = raw_post.get('message')

        self.reaction_count = int(raw_post.get('reactions', copy({}))
                                  .get('summary', copy({}))
                                  .get('total_count', copy({})))
        self.image_url = raw_post.get('full_picture')

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other) -> bool:
        return self.facebook_id == other.facebook_id
