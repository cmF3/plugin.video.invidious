# -*- coding: utf-8 -*-





from iapc import Client

from tools import log

from . import __trending_types__
from .objects import Channel, Channels, Playlists, Video, Videos


# ------------------------------------------------------------------------------
# InvidiousClient
# ------------------------------------------------------------------------------

class InvidiousClient(object):

    __defaults__ = {
        "playlists": {
            "playlists": [],
            "continuation": None
        },
        "playlist": {
            "videos": [],
            "title": None,
            "authorId": None
        }
    }

    __search__ = {
        "channel": Channels,
        "playlist": Playlists,
        "video": Videos
    }

    def __init__(self):
        self.__client__ = Client()

    # --------------------------------------------------------------------------

    def _query(self, key, *args, **kwargs):
        return (
            self.__client__.query(key, *args, **kwargs) or
            self.__defaults__.get(key, [])
        )

    def _channel(self, authorId):
        return Channel(self.__client__.channel(authorId))

    def _instances(self, **kwargs):
        return [
            instance[0] for instance in self.__client__.instances(**kwargs)
            if instance[1]["type"] in ("http", "https")
        ]

    # --------------------------------------------------------------------------

    def pushQuery(self, query):
        self.__client__.pushQuery(query)

    # --------------------------------------------------------------------------

    def video(self, **kwargs):
        video = Video(self.__client__.video(kwargs.pop("videoId"), **kwargs))
        if video:
            url, manifestType, mimeType = (
                video.dashUrl, "mpd", "video/vnd.mpeg.dash.mpd"
            )
            if video.liveNow and hasattr(video, "hlsUrl"):
                url, manifestType, mimeType = (
                    video.hlsUrl, "hls", "application/vnd.apple.mpegurl"
                )
            log("video.url: {}".format(url))
            return (video.makeItem(url), manifestType, mimeType)

    def channel(self, page=1, limit=60, **kwargs):
        category = None
        authorId = kwargs.pop("authorId")
        data = self._query("videos", authorId, page=page, **kwargs)
        channel = self._channel(authorId)
        if channel:
            category = channel.author
            if channel.autoGenerated:
                limit = 0
        return Videos(data, limit=limit, category=category)

    def playlist(self, page=1, limit=100, **kwargs):
        data = self._query(
            "playlist", kwargs.pop("playlistId"), page=page, **kwargs
        )
        authorId = data.get("authorId")
        if authorId:
            channel = self._channel(authorId)
            if channel and channel.autoGenerated:
                limit = 0
        return Videos(data["videos"], limit=limit, category=data["title"])

    # feed ---------------------------------------------------------------------

    def feed(self, ids, page=1, **kwargs):
        data, limit = self.__client__.feed(ids, page=page, **kwargs)
        return Videos(data, limit=limit)

    # top ----------------------------------------------------------------------

    def top(self, **kwargs):
        return Videos(self._query("top", **kwargs))

    # popular ------------------------------------------------------------------

    def popular(self, **kwargs):
        return Videos(self._query("popular", **kwargs))

    # trending -----------------------------------------------------------------

    def trending(self, **kwargs):
        return Videos(
            self._query("trending", **kwargs),
            category=__trending_types__.get(kwargs.get("type"))
        )

    # playlists ----------------------------------------------------------------

    def playlists(self, **kwargs):
        category = None
        authorId = kwargs.pop("authorId")
        data = self._query("playlists", authorId, **kwargs)
        channel = self._channel(authorId)
        if channel:
            category = channel.author
            if channel.autoGenerated:
                data["continuation"] = None
        return Playlists(
            data["playlists"], continuation=data["continuation"],
            category=category
        )

    # autogenerated ------------------------------------------------------------

    def autogenerated(self, **kwargs):
        category = None
        authorId = kwargs.pop("authorId")
        data = self.__client__.autogenerated(authorId, **kwargs)
        channel = self._channel(authorId)
        if channel:
            category = channel.author
        return Playlists(data, category=category)

    # search -------------------------------------------------------------------

    def search(self, query, page=1, limit=20, **kwargs):
        return self.__search__[kwargs["type"]](
            self._query("search", q=query, page=page, **kwargs),
            limit=limit, category=query
        )


client = InvidiousClient()

