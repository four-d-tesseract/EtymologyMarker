import os
os.chdir('YOUR FAVORITE DIRECTORY')

import re

# Reads in the dictionary and list of Greek roots from json files.
import json
with open('etymologyDictionary.json', 'r') as f:
    allWords = json.load(f)
with open('greekRootsList.json', 'r') as f:
    greekRoots = json.load(f)

# Takes the user's input, strips out the punctuation, and makes it lowercase.
def stripForDictionary(splitString):
    for word in splitString:
        stripped = re.sub('[^a-zA-Z]+', '', word) #Removes all non-alphabet characters.
        strippedLower = stripped.lower()
        formattedList.append(strippedLower)

# If the program can't find a word in the dictionary, this function tries
# removing prefixes and suffixes.
def removeAffixes(formattedList):
    x = 0
    while (x < len(formattedList)):
        if allWords.get(formattedList[x]) == None:
            formattedList[x] = re.sub('es$',"", formattedList[x])
            if allWords.get(formattedList[x]) == None:
                formattedList[x] = re.sub('s$',"", formattedList[x])
            if allWords.get(formattedList[x]) == None:
                formattedList[x] = re.sub('est$',"", formattedList[x])
                formattedList[x] = re.sub('er$',"", formattedList[x])
            formattedList[x] = re.sub('ed$',"", formattedList[x])
            formattedList[x] = re.sub('ial$',"", formattedList[x])
            formattedList[x] = re.sub('al$',"", formattedList[x])
            formattedList[x] = re.sub('ing$',"", formattedList[x])
            formattedList[x] = re.sub('ful$',"", formattedList[x])
            formattedList[x] = re.sub('age$',"", formattedList[x])
            formattedList[x] = re.sub('ist$',"", formattedList[x])
            formattedList[x] = re.sub('ism$',"", formattedList[x])
            if allWords.get(re.sub('ly$',"le", formattedList[x])) != None: #Replaces -ly with -le if that gets you a word.
                formattedList[x] = re.sub('ly$',"le", formattedList[x]) #Otherwise, strips off -ly.
            else:
                formattedList[x] = re.sub('ly$',"", formattedList[x])
            if allWords.get(re.sub('$',"e", formattedList[x])) != None: # Adds -e back onto words that get -e removed.
                formattedList[x] = re.sub('$',"e", formattedList[x])
            if allWords.get(formattedList[x]) == None: # Handles words that end in -y, which gets changed to -ie when a suffix is added.
                formattedList[x] = re.sub('i$',"y", formattedList[x])
            if allWords.get(formattedList[x]) == None:
                formattedList[x] = re.sub('^re',"", formattedList[x])
                formattedList[x] = re.sub('^un',"", formattedList[x])
            if allWords.get(formattedList[x]) == None: # Handles consonants that get doubled before -ed.
                formattedList[x] = re.sub('bb$',"b", formattedList[x])
                formattedList[x] = re.sub('pp$',"p", formattedList[x])
                formattedList[x] = re.sub('rr$',"r", formattedList[x])
                formattedList[x] = re.sub('nn$',"n", formattedList[x])
                formattedList[x] = re.sub('tt$',"t", formattedList[x])
                formattedList[x] = re.sub('dd$',"d", formattedList[x])
                formattedList[x] = re.sub('gg$',"g", formattedList[x])
        x = x + 1

# Looks up the words that are lowercase and stripped of punctuation and affixes (formattedList). 
# Then it adds HTML tags to the corresponding words from the user's input (splitString).
def lookupInDictionary(formattedList, WordCountList):
    x = 0
    while (x < len(formattedList)):
        y = formattedList[x]
        if allWords.get(y) == 'Anglo':
            splitString[x] = '<span style="background-color: #00FF00">' + splitString[x] + '</span>'
            WordCountList[0] = WordCountList[0] + 1
        elif allWords.get(y) == 'Germanic':
            splitString[x] = '<span style="background-color: #008000">' + splitString[x] + '</span>'
            WordCountList[1] = WordCountList[1] + 1
        elif allWords.get(y) == 'French':
            splitString[x] = '<span style="background-color: #FFFF00"><em>' + splitString[x] + '</em></span>'
            WordCountList[2] = WordCountList[2] + 1
        elif allWords.get(y) == 'Latin':
            splitString[x] = '<span style="background-color: #FF0000"><strong>' + splitString[x] + '</strong></span>'
            WordCountList[3] = WordCountList[3] + 1
        elif allWords.get(y) == 'Arabic':
            splitString[x] = '<span style="background-color: #FF00FF">' + splitString[x] + '</span>'
            WordCountList[4] = WordCountList[4] + 1
        elif any(root in y for root in greekRoots): # Checks whether any Greek roots are inside the word.
            splitString[x] = '<span style="background-color: #00FFFF"><ins>' + splitString[x] + '</ins></span>'
            WordCountList[5] = WordCountList[5] + 1
        x = x + 1
    return WordCountList

# If two words next to each other are the same color, removes the first HTML tag from the second
# word and the second HTML tag from the first word. This keeps the output from looking like a
# ransom letter.
def removeExtraHTML(formattedList):
    x = 1
    while (x < len(formattedList)):
        y = formattedList[x]
        z = formattedList[x-1]
        if allWords.get(y) == 'Anglo' and allWords.get(z) == 'Anglo':
            splitString[x] = splitString[x].replace('<span style="background-color: #00FF00">', '')
            splitString[x-1] = splitString[x-1].replace('</span>', '')
        elif allWords.get(y) == 'Germanic' and allWords.get(z) == 'Germanic':
            splitString[x] = splitString[x].replace('<span style="background-color: #008000">', '')
            splitString[x-1] = splitString[x-1].replace('</span>', '')
        elif allWords.get(y) == 'French' and allWords.get(z) == 'French':
            splitString[x] = splitString[x].replace('<span style="background-color: #FFFF00"><em>', '')
            splitString[x-1] = splitString[x-1].replace('</em></span>', '')
        elif allWords.get(y) == 'Latin' and allWords.get(z) == 'Latin':
            splitString[x] = splitString[x].replace('<span style="background-color: #FF0000"><strong>', '')
            splitString[x-1] = splitString[x-1].replace('</strong></span>', '')
        elif allWords.get(y) == 'Arabic' and allWords.get(z) == 'Arabic':
            splitString[x] = splitString[x].replace('<span style="background-color: #FF00FF">', '')
            splitString[x-1] = splitString[x-1].replace('</span>', '')
        x = x + 1
    
# Opens an output file and adds a legend.
markedUp = open('markedUp.html', encoding='utf-16', mode='w')
markedUp.write('<p>' + '<span style="background-color: #00FF00">Green</span> words have an Anglo-Saxon origin.' + '</p>')
markedUp.write('<p>' + '<span style="background-color: #008000">Dark green</span> words have some other Germanic origin (Old Norse, Scandinavian, German, Dutch).' + '</p>')
markedUp.write('<p>' + '<span style="background-color: #FFFF00"><em>Yellow italic</em></span> words have a French origin.' + '</p>')
markedUp.write('<p>' + '<span style="background-color: #FF0000"><strong>Red bold</strong></span> words have a Latin origin.' + '</p>')
markedUp.write('<p>' + '<span style="background-color: #FF00FF">Pink</span> words have an Arabic origin.' + '</p>')
markedUp.write('<p>' + '<span style="background-color: #00FFFF"><ins>Blue underlined</ins></span> words have a Greek origin.' + '</p>')

# Opens the user's input file, runs the functions on each line of text, then
# writes the results to the output file.
with open('usertext.txt', encoding='utf-16', mode='r') as f:
    usertext = f.readlines()
    TotalWordCount = 0
    WordCountList = [0,0,0,0,0,0]
    for line in usertext:
        splitString = line.split()
        TotalWordCount = TotalWordCount + len(splitString)
        formattedList = []
        stripForDictionary(splitString)
        removeAffixes(formattedList)
        lookupInDictionary(formattedList, WordCountList)
        removeExtraHTML(formattedList)
        splitString2 = ' '.join(splitString)
        markedUp.write('<p>' + splitString2 + '</p>')

# Calculates the percent composition of the text and writes it to the file.
float(TotalWordCount) #Forces Python to do true division.
AngloPercent = (WordCountList[0]/TotalWordCount)*100
GermanicPercent = (WordCountList[1]/TotalWordCount)*100
FrenchPercent = (WordCountList[2]/TotalWordCount)*100
LatinPercent = (WordCountList[3]/TotalWordCount)*100
ArabicPercent = (WordCountList[4]/TotalWordCount)*100
GreekPercent = (WordCountList[5]/TotalWordCount)*100
markedUp.write('<p>' + 'Percent composition:' + '</p>')
markedUp.write('<p>' + '{0:.2f} percent Anglo-Saxon'.format(AngloPercent) + '</p>')
markedUp.write('<p>' + '{0:.2f} percent other Germanic'.format(GermanicPercent) + '</p>')
markedUp.write('<p>' + '{0:.2f} percent French'.format(FrenchPercent) + '</p>')
markedUp.write('<p>' + '{0:.2f} percent Latin'.format(LatinPercent) + '</p>')
markedUp.write('<p>' + '{0:.2f} percent Arabic'.format(ArabicPercent) + '</p>')
markedUp.write('<p>' + '{0:.2f} percent Greek'.format(GreekPercent) + '</p>')

markedUp.close()


