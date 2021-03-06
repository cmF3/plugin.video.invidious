# -*- coding: utf-8 -*-





__all__ = [
    "getWindowId", "ICONINFO", "ICONWARNING", "ICONERROR", "notify",
    "selectDialog", "inputDialog", "contextMenu", "ListItem"
]


from six import iteritems
from kodi_six import xbmcgui

from .kodi import getAddonName, getAddonIcon, maybeLocalize


__addon_name__ = getAddonName()
__addon_icon__ = getAddonIcon()


# getWindowId -------------------------------------------------------------------

def getWindowId():
    return xbmcgui.getCurrentWindowId()


# notify -----------------------------------------------------------------------

ICONINFO = xbmcgui.NOTIFICATION_INFO
ICONWARNING = xbmcgui.NOTIFICATION_WARNING
ICONERROR = xbmcgui.NOTIFICATION_ERROR

def notify(message, heading=__addon_name__, icon=__addon_icon__, time=5000):
    xbmcgui.Dialog().notification(
        maybeLocalize(heading), maybeLocalize(message), icon, time
    )


# select -----------------------------------------------------------------------

def selectDialog(_list, heading=__addon_name__, multi=False, **kwargs):
    if multi:
        return xbmcgui.Dialog().multiselect(
            maybeLocalize(heading), _list, **kwargs
        )
    return xbmcgui.Dialog().select(maybeLocalize(heading), _list, **kwargs)


# input -----------------------------------------------------------------------

def inputDialog(heading=__addon_name__, **kwargs):
    return xbmcgui.Dialog().input(maybeLocalize(heading), **kwargs)


# contextmenu -----------------------------------------------------------------------

def contextMenu(_list):
    return xbmcgui.Dialog().contextmenu(_list)


# listitem ---------------------------------------------------------------------

class ListItem(xbmcgui.ListItem):

    def __new__(cls, label, path, **kwargs):
        return super(ListItem, cls).__new__(cls, label=label, path=path)

    def __init__(self, label, path, isFolder=False, isPlayable=True,
                 infos=None, streamInfos=None, contextMenus=None, **art):
        self.setIsFolder(isFolder)
        self.setIsPlayable(False if isFolder else isPlayable)
        if infos:
            for info in iteritems(infos):
                self.setInfo(*info)
        if streamInfos:
            for info in iteritems(streamInfos):
                self.addStreamInfo(*info)
        if contextMenus:
            self.addContextMenuItems(contextMenus)
        if art:
            self.setArt(art)

    def setIsFolder(self, isFolder):
        super(ListItem, self).setIsFolder(isFolder)
        #self.setProperty("IsFolder", str(isFolder).lower())
        self.isFolder = isFolder

    def setIsPlayable(self, isPlayable):
        self.setProperty("IsPlayable", str(isPlayable).lower())
        self.isPlayable = isPlayable

    def asItem(self):
        return self.getPath(), self, self.isFolder

