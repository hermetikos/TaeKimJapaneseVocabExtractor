import os
import requests
import re
from bs4 import BeautifulSoup
import winsound

#total # of kanji to process
total_count = 0
#number of values processed
cur_count = 0

#function to simplify storing data
def storeData(kanji, field, info):
    if(info):
        kanjiDict[kanji][field] = str(info)
    else:
        kanjiDict[kanji][field] = ""

def progress(currentVal, maxVal):
    percent = int(100*currentVal/maxVal)
    readout = "% complete: " + str(percent) + " "
    for i in range(0,percent):
        readout += "#"
    print(readout)

"""extract data from kanji file"""
kanjiFile = open("taeKimKanji.txt","r", encoding="utf-8")
kanji = ""
kanjiDict = dict()
for i in kanjiFile:
    regex = re.search("(?P<kanji>[\u4e00-\u9faf])\*(?P<tags>.*)", i)
    #create a dictionary to store the Kanji and tags
    kanjiDict[str(regex.group("kanji"))] = { "onyomi" : "", "kunyomi": "", "translation" : "", "tags": str(regex.group("tags") + " kanji japanese")}
    #create a string to append to the URL
    kanji = kanji + regex.group("kanji")
    #increment total count by 1
    total_count += 1    
kanjiFile.close()

print("processing " + str(total_count) + " kanji")
print(kanji + '\n\n')

for char in kanji:
    
    cur_count += 1
    #open tangorin at a specific Kanji
    url = "http://tangorin.com/kanji/" + char
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    
    data = soup.find_all("div", {"class" : "entry"})
    for entry in data:
        #extract kanji
        cur_kanji = str(entry.find("dt", {"class" : "k-dt"}).h2.text)

        #extract kana
        #to store onyomi & kunyomi
        kunyomi = ""
        onyomi = ""
        for i in entry.find_all("span", { "class" : "kana"}):
            for kana in i.find_all("rb"):
                #kana.text contains all KANA, should be further seperated
                #print(kana.text)
                #extract on & kun yomi
                hira = re.findall(r"[\u3000-\u303f\u3040-\u309f.]+", str(kana.text))
                kata = re.findall(r"[\u3000-\u303f\u30a0-\u30ff\uff00-\uffef]+", str(kana.text))
                
                for hiragana in hira:
                    #link all kunyomi readings
                    kunyomi += str(hiragana)+", "
                for katakana in kata:
                    #link all onyomi readings
                    onyomi += str(katakana)+", "
        #extract reading
        translation = ""            
        for i in entry.find_all("span", { "class" : "k-lng-en" }):
            for trans in i.find_all("b"):
                #trans.text contains all translations
                translation += trans.text + ", "

        storeData(cur_kanji, "onyomi", onyomi)
        storeData(cur_kanji, "kunyomi", kunyomi)
        storeData(cur_kanji, "translation", translation)
    #show progress
    progress(cur_count, total_count) 
    #close old link
    r.close()

#save data
print("saving data")
winsound.Beep(660, 100)
#open save file
saveFile = open("taeKimKanji2.txt","w", encoding="utf-8")
#store contents
for i in kanji:
    saveData = i + "~" + "~" + kanjiDict[i]['translation']+ "~" + "~" + kanjiDict[i]['onyomi']+ "~" + "~" +kanjiDict[i]['kunyomi']+ "~" + "~" + kanjiDict[i]["tags"] + "\n"
    saveFile.write(saveData)
    saveFile.flush()
#close save file
saveFile.close()

#alert the user process finished & play sound
print("finished")
winsound.Beep(440, 100)
