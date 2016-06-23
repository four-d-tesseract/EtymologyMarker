import os
import re
import json
import io

os.chdir('DIRECTORY GOES HERE')

# Reads in the dictionary and list of Greek roots from json files.
with open('etymologyDictionary.json', 'r') as dictionaryfile:
    allWords = json.load(dictionaryfile)

with open('greekRootsList.json', 'r') as greekfile:
    greekRoots = json.load(greekfile)
    
def getOrigin(word):
    """ Returns the language etymology of a word
    """
    return allWords.get(word)
    
    
def stripForDictionary(splitString):
    """ Takes the user's input, strips out the punctuation, and makes it lowercase.
    """
    for word in splitString:
        stripped      = re.sub('[^a-zA-Z]+', '', word) #Removes all non-alphabet characters.
        strippedLower = stripped.lower()
        formattedList.append(strippedLower)

# If the program can't find a word in the dictionary, this function tries
# removing prefixes and suffixes.
def removeAffixes(formattedList):
    for x, word in enumerate(formattedList):
        if allWords.get(formattedList[x]) == None:
            formattedList[x] = re.sub('es$',"", formattedList[x])
            if allWords.get(formattedList[x]) == None:
                formattedList[x] = re.sub('s$',"", formattedList[x])
            if allWords.get(formattedList[x]) == None:
                formattedList[x] = re.sub('est$',"", formattedList[x])
                formattedList[x] = re.sub('er$', "", formattedList[x])
            formattedList[x] = re.sub('ed$',"", formattedList[x])
            formattedList[x] = re.sub('ial$',"", formattedList[x])
            formattedList[x] = re.sub('al$',"", formattedList[x])
            formattedList[x] = re.sub('ing$',"", formattedList[x])
            formattedList[x] = re.sub('ful$',"", formattedList[x])
            formattedList[x] = re.sub('age$',"", formattedList[x])
            formattedList[x] = re.sub('ist$',"", formattedList[x])
            formattedList[x] = re.sub('ism$',"", formattedList[x])
            if allWords.get(re.sub('ly$',"le", formattedList[x])) != None: # Replaces -ly with -le if that gets you a word.
                formattedList[x] = re.sub('ly$',"le", formattedList[x])    # Otherwise, strips off -ly.
            else:
                formattedList[x] = re.sub('ly$',"", formattedList[x])
            if allWords.get(re.sub('$',"e", formattedList[x])) != None:    # Adds -e back onto words that get -e removed.
                formattedList[x] = re.sub('$',"e", formattedList[x])
            if allWords.get(formattedList[x]) == None:                     # Handles words that end in -y, which gets changed to -ie when a suffix is added.
                formattedList[x] = re.sub('i$',"y", formattedList[x])
            if allWords.get(formattedList[x]) == None:
                formattedList[x] = re.sub('^re',"", formattedList[x])
                formattedList[x] = re.sub('^un',"", formattedList[x])
            if allWords.get(formattedList[x]) == None:                     # Handles consonants that get doubled before -ed.
                formattedList[x] = re.sub('bb$',"b", formattedList[x])
                formattedList[x] = re.sub('pp$',"p", formattedList[x])
                formattedList[x] = re.sub('rr$',"r", formattedList[x])
                formattedList[x] = re.sub('nn$',"n", formattedList[x])
                formattedList[x] = re.sub('tt$',"t", formattedList[x])
                formattedList[x] = re.sub('dd$',"d", formattedList[x])
                formattedList[x] = re.sub('gg$',"g", formattedList[x])

colours = {'Anglo':    '00FF00', 
           'Germanic': '008000', 
           'French':   'FFFF00', 
           'Latin':    'FF0000', 
           'Arabic':   'FF00FF', 
           'Greek':    '00FFFF'}
                
                
# Looks up the words that are lowercase and stripped of punctuation and affixes (formattedList). 
# Then it adds HTML tags to the corresponding words from the user's input (splitString).
def lookupInDictionary(formattedList, WordCountDict):
    for x, word in enumerate(formattedList):
        origin = getOrigin(word)
        if origin in colours.keys():
            splitString[x] = '<span style="background-color: #' + colours[origin] + '">' + splitString[x] + '</span>'
            WordCountDict[origin] += 1
        elif any(root in word for root in greekRoots): # Checks whether any Greek roots are inside the word.
            splitString[x] = '<span style="background-color: #00FFFF">' + splitString[x] + '</span>'
            WordCountDict['Greek'] += 1
    return WordCountDict

# If two words next to each other are the same colour, removes the first HTML tag from the second
# word and the second HTML tag from the first word. This keeps the output from looking like a
# ransom letter.

def removeExtraHTML(formattedList):
    for x, word in enumerate(formattedList[:-1]):
        nextWord = formattedList[x+1]
        originW1 = getOrigin(word)
        originW2 = getOrigin(nextWord)
        if originW1 == originW2 and originW1 in colours.keys():
            splitString[x+1]   = splitString[x+1].replace('<span style="background-color: #' + colours[originW1] + '">', '')
            splitString[x]     = splitString[x].replace('</span>', '')

    
# Opens an output file and adds a legend.
markedUp = io.open('markedUp.html', encoding='utf-16', mode='w')
markedUp.write(unicode('<p>' + '<span style="background-color: #00FF00">' + 'Green'      + '</span>' + ' words have an Anglo-Saxon origin.' + '</p>'))
markedUp.write(unicode('<p>' + '<span style="background-color: #008000">' + 'Dark green' + '</span>' + ' words have some other Germanic origin (Old Norse, Scandinavian, German, Dutch).' + '</p>'))
markedUp.write(unicode('<p>' + '<span style="background-color: #FFFF00">' + 'Yellow'     + '</span>' + ' words have a French origin.' + '</p>'))
markedUp.write(unicode('<p>' + '<span style="background-color: #FF0000">' + 'Red'        + '</span>' + ' words have a Latin origin.' + '</p>'))
markedUp.write(unicode('<p>' + '<span style="background-color: #FF00FF">' + 'Pink'       + '</span>' + ' words have an Arabic origin.' + '</p>'))
markedUp.write(unicode('<p>' + '<span style="background-color: #00FFFF">' + 'Blue'       + '</span>' + ' words have a Greek origin.' + '</p>'))

# Opens the user's input file, runs the functions on each line of text, then
# writes the results to the output file.
with io.open('usertext.txt', encoding='utf-16', mode='r') as f:
    usertext       = f.readlines()
    TotalWordCount = 0
    WordCountDict  = {'Anglo':    0, 
                      'Germanic': 0, 
                      'French':   0, 
                      'Latin':    0, 
                      'Arabic':   0, 
                      'Greek':    0}
    for line in usertext:
        splitString    = line.split()
        TotalWordCount += len(splitString)
        formattedList  = []
        stripForDictionary(splitString)
        removeAffixes(formattedList)
        lookupInDictionary(formattedList, WordCountDict)
        removeExtraHTML(formattedList)
        joinedString   = ' '.join(splitString)
        markedUp.write('<p>' + joinedString + '</p>')

# Calculates the percent composition of the text and writes it to the file.
AngloPercent    = (WordCountDict['Anglo']*100.0 / TotalWordCount)
GermanicPercent = (WordCountDict['Germanic']*100.0 / TotalWordCount)
FrenchPercent   = (WordCountDict['French']*100.0 / TotalWordCount)
LatinPercent    = (WordCountDict['Latin']*100.0 / TotalWordCount)
ArabicPercent   = (WordCountDict['Arabic']*100.0 / TotalWordCount)
GreekPercent    = (WordCountDict['Greek']*100.0 / TotalWordCount)
markedUp.write(unicode('<p>' + 'Percent composition:' + '</p>'))
markedUp.write(unicode('<p>' + '{:.2f} percent Anglo-Saxon'.format(AngloPercent) + '</p>'))
markedUp.write(unicode('<p>' + '{:.2f} percent other Germanic'.format(GermanicPercent) + '</p>'))
markedUp.write(unicode('<p>' + '{:.2f} percent French'.format(FrenchPercent) + '</p>'))
markedUp.write(unicode('<p>' + '{:.2f} percent Latin'.format(LatinPercent)   + '</p>'))
markedUp.write(unicode('<p>' + '{:.2f} percent Arabic'.format(ArabicPercent) + '</p>'))
markedUp.write(unicode('<p>' + '{:.2f} percent Greek'.format(GreekPercent)   + '</p>'))

markedUp.close()
