# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'jawaltv'
SITE_NAME = 'Jawal TV -TEST-'
SITE_DESC = 'arabic live'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://jawaltv.com/land/?id=liban')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'لبنان', 'live.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://jawaltv.com/land/?id=iraq')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'عراق', 'live.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://jawaltv.com/ar/islam/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'اسلامية', 'live.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://jawaltv.com/news/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'اخبار', 'live.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://jawaltv.com/srt/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'رياضة', 'live.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://jawaltv.com/land/?id=saoudia')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'السعودية', 'live.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://jawaltv.com/ar/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'قنوات عربية اخرى', 'live.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()

   
def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sStart = ' class="countent">'
    sEnd = '<div class="Descrip"'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    # (.+?) .+? ([^<]+)
    sPattern = '<a href="(.+?)">.+?src="(.+?)".+?alt="(.+?)" />'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 

            sTitle = aEntry[2]
            
            sThumb = URL_MAIN+aEntry[1]
            siteUrl = URL_MAIN+aEntry[0]
            sDesc = ''

			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

        
        progress_.VSclose(progress_)
 
    oGui.setEndOfDirectory() 
    
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

     # (.+?) ([^<]+) .+?
    sStart = 'class="countent">'
    sEnd = '<div class="DivPB2">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern =  'src="(.+?)"'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        m3url = aResult[1][0]
        if m3url.startswith('/'):
            m3url = URL_MAIN+m3url
        oRequestHandler = cRequestHandler(m3url)
        sHtmlContent = oRequestHandler.request() 

    sPattern = 'file : "(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
       for aEntry in aResult[1]:
            url = aEntry
            url = url
            if url.startswith('//'):
                url = 'http:' + url
            sHosterUrl = url
			
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)


                
    oGui.setEndOfDirectory()