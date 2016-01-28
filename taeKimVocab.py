__author__ = 'MisturDust319'
import requests, re
from bs4 import BeautifulSoup


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
url = requests.get(home + "/learn/complete/kanji")

#open files to store data in
vocabFile = open("taeKimVocab.txt", "w", encoding="utf-8")
kanjiFile = open("taeKimKanji.txt", "w", encoding="utf-8")

#while there are more urls to look at
while 1==1:
    soup = BeautifulSoup(url.content)
    print("Current Section: " + str(soup.find("title").text))
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

                vocabFormat = (data.group("vocab") + '*' + data.group("reading")
                               + '*' + data.group('translation') + '*' + 'tae_kim\n')
                #write the vocab in the vocab file
                vocabFile.write(vocabFormat)
                #write all kanji in a seperate file
                if kanji:
                    for i in kanji:
                        kanjiFile.write(str(i) + '\n')

    #flush the file i/o buffers
    vocabFile.flush()
    kanjiFile.flush()

    #find next URL
    #first check if there is one
    if (soup.find("a", {"class" : "page-next"})):
        urlNext = home + (soup.find("a", {"class" : "page-next"})).get("href")
        url = requests.get(urlNext)
    #if not, break loop
    else:
        break




#close data files
url.close()
vocabFile.close()
kanjiFile.close()
