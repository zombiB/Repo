# -*- coding: utf-8 -*-
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.util import cUtil, Unquote

	
SITE_IDENTIFIER = 'ytxmx'
SITE_NAME = 'YTX.MX'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

UA = 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'


MOVIE_4k = (URL_MAIN + '/browse-movies/0/2160p/all/0/latest/0/all', 'showMovies')
MOVIE_EN = (URL_MAIN + '/browse-movies/0/all/all/0/year/0/all', 'showMovies')
KID_MOVIES = (URL_MAIN + '/browse-movies/0/all/animation/0/year/0/all', 'showMovies')

MOVIE_GENRES = (True, 'moviesGenres')

URL_SEARCH = (URL_MAIN + '/ajax/search?query=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/ajax/search?query=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
	
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4k[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', ' 4k أفلام', '4k.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab2.png', oOutputParameterHandler)
     
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'anim.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', 'film.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'ajax/search?query='+sSearchText
        showSearchMovies(sUrl)
        oGui.setEndOfDirectory()
        return  

def showSearchMovies(sSearch = ''):
    import requests
    oGui = cGui()
    sUrl = sSearch

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+? (.+?)
    sPattern = '{"url":"([^"]+)","img":"([^"]+)","title":"([^"]+)","year":"(.+?)"}'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    VSlog(aResult)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace('download','').replace('télécharger','')
            siteUrl = aEntry[0].replace('\/','/')
            sThumb = aEntry[1]
            sDesc = ''
            sYear = aEntry[3]


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:

        oGui.setEndOfDirectory()  

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + 'browse-movies/0/all/action/0/year/0/all'])
    liste.append(['Adventure', URL_MAIN + 'browse-movies/0/all/adventure/0/year/0/all'])
    liste.append(['Animated', URL_MAIN + 'browse-movies/0/all/animation/0/year/0/all'])
    liste.append(['Biography', URL_MAIN + 'browse-movies/0/all/biography/0/year/0/all'])
    liste.append(['Comedy', URL_MAIN + 'browse-movies/0/all/comedy/0/year/0/all'])
    liste.append(['Crime', URL_MAIN + 'browse-movies/0/all/crime/0/year/0/all'])
    liste.append(['Drama', URL_MAIN + 'browse-movies/0/all/drama/0/year/0/all'])
    liste.append(['Documentary', URL_MAIN + 'browse-movies/0/all/documentary/0/year/0/all'])
    liste.append(['Family', URL_MAIN + 'browse-movies/0/all/family/0/year/0/all'])
    liste.append(['Fantasy', URL_MAIN + 'browse-movies/0/all/fantasy/0/year/0/all'])
    liste.append(['History', URL_MAIN + 'browse-movies/0/all/history/0/year/0/all'])
    liste.append(['Horror', URL_MAIN + 'browse-movies/0/all/horror/0/year/0/all'])
    liste.append(['Music', URL_MAIN + 'browse-movies/0/all/music/0/year/0/all'])
    liste.append(['Mystery', URL_MAIN + 'browse-movies/0/all/mystery/0/year/0/all'])
    liste.append(['Romance', URL_MAIN + 'browse-movies/0/all/romance/0/year/0/all'])
    liste.append(['Sci-Fi', URL_MAIN + 'browse-movies/0/all/sci-fi/0/year/0/all'])
    liste.append(['Thriller', URL_MAIN + 'yts.mx/browse-movies/0/all/thriller/0/year/0/all'])
    liste.append(['War', URL_MAIN + 'browse-movies/0/all/war/0/year/0/all'])
    liste.append(['Western', URL_MAIN + 'browse-movies/0/all/western/0/year/0/all'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    import requests
    oGui = cGui()
    if sSearch:
      sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+? (.+?)
    sPattern = '<div class="browse-movie-wrap col-xs-10 col-sm-4 col-md-5 col-lg-4"><a href="([^"]+)".+?src="([^"]+)" alt="([^"]+)' 

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    VSlog(aResult)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace('download','').replace('télécharger','')
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''
            sYear = ''


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:

        oGui.setEndOfDirectory()  

 
def showSeries(sSearch = ''):
    import requests
    oGui = cGui()
    if sSearch:
      sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+?
    sPattern = '<div class="BlockItem"><a href="([^<]+)">.+?data-src="([^"]+)".+?<h2>(.+?)</h2>'

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
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("مسلسل","").replace("Web-dl","").replace("بجودة","").replace("اونلاين","").replace("بجوده","").replace("كامل","").replace("والأخيره","").replace("و الأخيرة","").replace("والأخيرة","").replace("والاخيرة","").replace("Full Episodes","").replace("وتحميل","").replace("شاهد","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sTitle = sTitle.split('جميع حلقات :')[-1].replace("الموسم","S").replace("موسم","S").replace("S "," S")
            sDesc = ''
            sYear = ''
            sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").split('الحلقة')[0].replace("العاشر","10").replace("الحادي عشر","11").replace("الثاني عشر","12").replace("الثالث عشر","13").replace("الرابع عشر","14").replace("الخامس عشر","15").replace("السادس عشر","16").replace("السابع عشر","17").replace("الثامن عشر","18").replace("التاسع عشر","19").replace("العشرون","20").replace("الحادي و العشرون","21").replace("الثاني و العشرون","22").replace("الثالث و العشرون","23").replace("الرابع والعشرون","24").replace("الخامس و العشرون","25").replace("السادس والعشرون","26").replace("السابع والعشرون","27").replace("الثامن والعشرون","28").replace("التاسع والعشرون","29").replace("الموسم الثلاثون","30").replace("الحادي و الثلاثون","31").replace("الثاني والثلاثون","32").replace("الاول","1").replace("الثاني","2").replace("الثانى","2").replace("الثالث","3").replace("الثالث","3").replace("الرابع","4").replace("الخامس","5").replace("السادس","6").replace("السابع","7").replace("الثامن","8").replace("التاسع","9").replace(" : ", "")


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:

        oGui.setEndOfDirectory()  


def showSeasons():
	oGui = cGui()
    
	oInputParameterHandler = cInputParameterHandler()
	sUrl = oInputParameterHandler.getValue('siteUrl')
	sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
	sThumb = oInputParameterHandler.getValue('sThumb')
 
	oRequestHandler = cRequestHandler(sUrl)
	sHtmlContent = oRequestHandler.request()
	oParser = cParser()
	sStart = '<h2 class="title.+?">أجزاء المسلسل</h2>'
	sEnd = '<div id="isdiv" style></div>'
	sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    # .+? ([^<]+)
	sPattern = '<a class="ipc-metadata.+?href="([^"]+)" aria-label="([^"]+)'

	oParser = cParser()
	aResult = oParser.parse(sHtmlContent, sPattern)
		
	if aResult[0]:
		oOutputParameterHandler = cOutputParameterHandler()
		for aEntry in aResult[1]:
 
			sTitle = aEntry[1].replace("الموسم"," S").replace("موسم","S").replace("الأول"," S1").replace("S "," S")
			siteUrl = aEntry[0]
			sThumb = ''
			sDesc = ''
			
			oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			oOutputParameterHandler.addParameter('sThumb', sThumb)
			oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

	else:

		sStart = '<h2 class="titleh3">'
		sEnd = '</section>'
		sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    # (.+?) .+? ([^<]+)
		sPattern = '<a href="([^"]+)" title="([^"]+).+?<div class="ipc-inline-list__item">(.+?)</div>'

		oParser = cParser()
		aResult = oParser.parse(sHtmlContent, sPattern)
    
		if aResult[0] is True:
			oOutputParameterHandler = cOutputParameterHandler() 
			for aEntry in aResult[1]:
                            sEp = aEntry[1].replace("حلقة ","E")
                            sEp = sEp.replace(" ","")
                            if "مدبلج" in sMovieTitle:
                                sMovieTitle = sMovieTitle.replace("مدبلج","")
                                sMovieTitle = "مدبلج"+sMovieTitle
                            sTitle = aEntry[2]+' '+sEp
                            siteUrl = aEntry[0]
                            sThumb = sThumb
                            sDesc = ''
                            sHost = ''

                            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                            oOutputParameterHandler.addParameter('sHost', sHost)
                            oOutputParameterHandler.addParameter('sThumb', sThumb)
            

 
                            oGui.addEpisode(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

	oGui.setEndOfDirectory()
    
def showEps():
    import requests
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sStart = '<h2 class="title.+?">أجزاء المسلسل</h2>'
    sEnd = '<div id="isdiv" style></div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    # (.+?) .+? ([^<]+)
    sPattern = '<a href="([^"]+)" title="([^"]+).+?<div class="ipc-inline-list__item">(.+?)</div>' 

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sEp = aEntry[1].replace("حلقة ","E")
            sEp = sEp.replace(" ","")
            sTitle = aEntry[2]+' '+sEp
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''
            sYear = ''
			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
               
       
    oGui.setEndOfDirectory() 
 
	
def showServer():
    import xbmc
    oGui = cGui()
    import requests

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = '<div class="modal-torrent">.+?<span>(.+?)</span>.+?class="quality-size">(.+?)</p>.+?href="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    VSlog(aResult)
    if aResult[0]:
        for aEntry in aResult[1]:
            m = re.search('([0-9]{4})', sMovieTitle)
            if m:
               sYear = str(m.group(0))
               sMovieTitle = sMovieTitle.replace(sYear,'')
            

            url = aEntry[2]+'ttmxtt'
            qual = aEntry[0].replace('p','')
            sSize = aEntry[1].replace(' ','')
            sTitle = ('%s  [COLOR coral](%sp)[/COLOR] [COLOR red]%s[/COLOR]') % (sMovieTitle, qual, sSize)	
					
            
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = sTitle
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()  



def __checkForNextPage(sHtmlContent):
    sPattern = 'li class="pagination-bordered">.+?</li><li><a href="([^"]+)'	 
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0] :
        return URL_MAIN + aResult[1][0]

    return False

    return False