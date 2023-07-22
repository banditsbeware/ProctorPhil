import requests
from bs4 import BeautifulSoup

corps_lookup = {
    "7th regiment"      : "001j000000IWwSlAAL",
    "the academy"       : "001j000000IWxAEAA1",
    "arsenal"           : "001j000000qNXAYAA4",
    "atlanta cv"        : "001j000000IWwSnAAL",
    "the battalion"     : "001j0000012Y6bqAAC",
    "blue devils"       : "001j000000I6I9SAAV",
    "blue devils b"     : "001j000000I6JmbAAF",
    "blue devils c"     : "001j000000I6KALAA3",
    "blue knights"      : "001j000000IWwSoAAL",
    "blue stars"        : "001j000000IWwSqAAL",
    "bluecoats"         : "001j000000IWwSrAAL",
    "boston crusaders"  : "001j000000IWwSsAAL",
    "the cadets"        : "001j000000I6KFgAAN",
    "carolina crown"    : "001j000000IWx91AAD",
    "the cavaliers"     : "001j000000IWxAFAA1",
    "colts"             : "001j000000IWx98AAD",
    "crossmen"          : "001j000000IWx9AAAT",
    "jersey surf"       : "001j000000IWx9wAAD",
    "madison scouts"    : "001j000000I6LENAA3",
    "mandarins"         : "001j000000IWxA3AAL",
    "pacific crest"     : "001j000000IWxA7AAL",
    "phantom regiment"  : "001j000000H3XrNAAV",
    "seattle cascades"  : "001j000000IWx93AAD",
    "spirit of atlanta" : "001j000000IWxADAA1",
    "troopers"          : "001j000000IWxAJAA1",
}

def corps_schedule(corps=None):

    cstr = ""
    if corps is not None:
        cstr = "corpId=" + corps_lookup[corps] + "&"
    
    html = requests.get( f"https://www.dci.org/events?{cstr}limit=-1&viewMode=print&sort=startDate" ).text

    soup = BeautifulSoup( html, "html.parser" )

    ret = list()

    for el in soup.tbody.find_all( "tr" )[1:]:

        cols = el.find_all( "td" ) 

        ret.append( {
            "date":     cols[0].select(".print-date")[0].get_text().strip(),
            "title":    cols[1].a.get_text().strip(),
            "location": cols[2].select(".location-item")[0].get_text().strip()
        } )

    return ret


if __name__ == '__main__': 
    print( corps_schedule( "blue devils" ) )
