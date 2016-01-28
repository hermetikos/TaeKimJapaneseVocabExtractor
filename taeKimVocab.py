__author__ = 'MisturDust319'
import requests, re
from bs4 import BeautifulSoup
import winsound

#find the section of the website where the data is coming from
def getSection(html):
    #given a web soup, find the "up" link, which is the current segment
    link = html.find_all("link", rel="up")
    #isolate the section title from the link
    chapter = re.search('<link href="/learn/complete/(?P<chapter>.*?)" rel="up"/>', str(link))
    if chapter:
        return str(chapter.group("chapter"))
    else:
        return ""


"""
outline of process:
    start with seed page on Tae Kim grammar
        open page on Tae Kim
        grab all data in <li> tags (which is vocab)
         format data:
            'kanji/vocab' * 'reading' * 'translation' * section * tags
            (delimeter is * backslash)
        save line in new file
        find next chapter
    afterwords, extract kanji
    you may wanna take the radicals from kanji damage
"""


#all pages somehow branch off this one
home = "http://www.guidetojapanese.org"
#start at this web page
url = requests.get(home + "/learn/complete/writing")

#open files to store data in
vocabFile = open("taeKimVocab.txt", "w", encoding="utf-8")
kanjiFile = open("taeKimKanji.txt", "w", encoding="utf-8")
#sets to hold the data w/o repeats
#kanjiSet = set()
#vocabSet = set()
kanjiDict = dict()
vocabDict = dict()

#int to store # of pages visited
count = 1
#while there are more urls to look at
while count==count:
    #prep data for use
    soup = BeautifulSoup(url.content)
    #find the current chapter
    section = getSection(soup)
    
    print("Pages Visited: " + str(count) + " Current Page: "
          + str(soup.find("title").text) + " Current Section: " + section)
    
    #isolate all vocab, which are tagged <li>
    #in <ol> tags, and extract the text
    for list in soup.find_all("ol"):
        for elem in list.find_all("li"):
            #extract vocab, reading and translation
            data = re.search("(?P<vocab>[\u3000-\u9faf]+) 【(?P<reading>.*?)】 - (?P<translation>[\u0000-\u00ff]*)", elem.text)

            #only process data that matches the regex, other data isn't vocab
            if data:
                #extract kanji for seperate storage
                kanji = re.findall("[\u4e00-\u9faf]", str(data.group("vocab")))

                #vocabFormat = (data.group("vocab") + '*' + data.group("reading")
                #               + '*' + data.group('translation') + '*' + section + ' tae_kim\n')
                vocabFormat = (data.group("vocab") + '*' + data.group("reading")
                               + '*' + data.group('translation'))
                #write the vocab in the vocab file
                #vocabFile.write(vocabFormat)
                #store all vocab in a set
                #vocabSet.add(vocabFormat)
                if vocabFormat in vocabDict:
                    vocabDict[vocabFormat] = vocabDict[vocabFormat] + " " + section
                else:
                    vocabDict[vocabFormat] = section + " tae_kim"
                #write all kanji in a seperate file
                #store all kanji in a set if there are any
                if kanji:
                    for i in kanji:
                        #kanjiFile.write(str(i) + '\n')
                        if i in kanjiDict:
                            kanjiDict[i] = kanjiDict[i] + " " + section
                        else:
                            kanjiDict[i] = section + " tae_kim"
                        #kanjiSet.add(str(i) + '*' + section + '\n')

    #find next URL
    #first check if there is one
    if (soup.find("a", {"class" : "page-next"})):
        urlNext = home + (soup.find("a", {"class" : "page-next"})).get("href")
        url = requests.get(urlNext)
        count += 1
    #if not, break loop
    else:
        break

#save data
for i in vocabDict:
    #flush the file i/o buffers
    vocabFile.write(i + "*" + vocabDict[i] + '\n')
    vocabFile.flush()
for i in kanjiDict:
    #flush the file i/o buffers
    kanjiFile.write(i + "*" + kanjiDict[i] + '\n')
    kanjiFile.flush()


#close data files
url.close()
vocabFile.close()
kanjiFile.close()

print("FINISHED")
winsound.Beep(440, 1000)
