# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# from resources.lib.handler.requestHandler import cRequestHandler

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

import re

from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'googledrive', 'GoogleDrive', 'google')

    def __getIdFromUrl(self, sUrl):
        sPattern = 'google.+?([a-zA-Z0-9-_]{20,40})'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if aResult[0]:
            return aResult[1][0]

        return ''

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        url = []
        qua = []
        api_call = ''

        # reformatage du lien
        sId = self.__getIdFromUrl(self._url)
        sUrl = 'https://drive.google.com/file/d/' + sId + '/view'

        req = urllib2.Request(sUrl)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()

        Headers = response.headers
        response.close()

        # listage des cookies
        c = Headers['Set-Cookie']
        c2 = re.findall('(?:^|,) *([^;,]+?)=([^;,\/]+?);', c)
        if c2:
            cookies = ''
            for cook in c2:
                cookies = cookies + cook[0] + '=' + cook[1] + ';'

        sPattern = '\["fmt_stream_map","([^"]+)"]'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if not aResult[0]:
            if '"errorcode","150"]' in sHtmlContent:
                dialog().VSinfo("Nombre de lectures max dépassé")
            return False, False

        sListUrl = aResult[1][0]

        if sListUrl:
            aResult2 = oParser.parse(sHtmlContent, '([0-9]+)\/([0-9]+x[0-9]+)\/')

        # liste les qualitee
            r = oParser.parse(sListUrl, '([0-9]+)\|([^,]+)')
            for item in r[1]:
                url.append(item[1].decode('unicode-escape'))
                for i in aResult2[1]:
                    if item[0] == i[0]:
                        qua.append(i[1])

        # Affichage du tableau
        api_call = dialog().VSselectqual(qua, url)
        api_call = api_call + '|User-Agent=' + UA + '&Cookie=' + cookies

        if api_call:
            return True, api_call

        return False, False
