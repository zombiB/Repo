# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.hosters.hoster import iHoster
import resolveurl


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'resolver', 'ResolveURL')
        self.__sRealHost = ''

    def setRealHost(self, host):
        self.__sRealHost = "/" + host

    def setDisplayName(self, displayName):
        self._displayName = displayName + ' [COLOR violet]'+ self._defaultDisplayName + self.__sRealHost + '[/COLOR]'


    def _getMediaLinkForGuest(self):
        hmf = resolveurl.HostedMediaFile(url=self._url)
        if hmf.valid_url():
            stream_url = hmf.resolve()
            if stream_url:
                return True, stream_url

        return False, False
