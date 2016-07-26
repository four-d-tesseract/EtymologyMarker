import re
import json
import collections

def getOrigin(word, allWords):
    """ Returns the language origin of a word. """
    return allWords.get(word)

def stripForDictionary(splitString, formattedList):
    """ Takes input, strips punctuation, makes lower-case, then appends to formattedList. """
    for word in splitString:
        stripped = re.sub('[^a-zA-Z]+', '', word)
        formattedList.append(stripped.lower())

def removeAffixes(formattedList, allWords):
    """ If the program can't find a word in the dictionary, 
    this function tries removing prefixes and suffixes.
    """
    for x in range(len(formattedList)):
        if '</span>' in splitString[x]: #Escapes if a word already has HTML tags.
            continue
        if getOrigin(formattedList[x], allWords) == None:           
            formattedList[x] = re.sub('es$', '', formattedList[x])      # Handled separately to prevent words like 'flosses' from getting stripped to 'flos'.
            formattedList[x] = re.sub('bly$', 'ble', formattedList[x])
            
        suffix_list = ['ly$', 'ness$', 'less$', 's$', 'est$', 'ship$', 'er$',  'or$',  'ed$',  'ial$', 'able$', 'ity$', 'ful$',
                      'ible$', 'ibility$', 'al$', 'ful$', 'ing$', 'age$', 'ist$', 'ism$', 'en$', 'ment$', 'y$', 'ion$', 'ish$']
        for suffix in suffix_list:
            if getOrigin(formattedList[x], allWords) == None:
                formattedList[x] = re.sub(suffix, '', formattedList[x])

        if getOrigin(re.sub('$', 'se', formattedList[x]), allWords) != None: # Handles special cases like 'houses' that get stripped down to 'hou'.
            formattedList[x] = re.sub('$', 'se', formattedList[x])
        elif getOrigin(re.sub('$', 'e', formattedList[x]), allWords) != None: # Adds -e back onto words that had -e removed.
            formattedList[x] = re.sub('$',  'e', formattedList[x])
        elif getOrigin(re.sub('i$', 'y', formattedList[x]), allWords) != None: # Handles words that end in -y, which gets changed to -ie when a suffix is added.
            formattedList[x] = re.sub('i$', 'y', formattedList[x])

        if getOrigin(re.sub('^re', '', formattedList[x]), allWords) != None:
            formattedList[x] = re.sub('^re', '', formattedList[x])
        if getOrigin(formattedList[x], allWords) == None:
            formattedList[x] = re.sub('^un', '', formattedList[x])
        if getOrigin(re.sub('$', 'e', formattedList[x]), allWords) != None: # Adds -e back onto words that had -e removed.
            formattedList[x] = re.sub('$',  'e', formattedList[x])
        if getOrigin(re.sub('^sub', '', formattedList[x]), allWords) != None:
            formattedList[x] = re.sub('^sub', '', formattedList[x])

        if getOrigin(formattedList[x], allWords) == None:                       # Handles consonants that are doubled before a suffix.
            for consonant in ['b', 'd', 'g', 'l', 'm', 'n', 'p', 'r', 't', 'z']:
                suffix = consonant*2 + '$'
                formattedList[x] = re.sub(suffix, consonant, formattedList[x])

def hashtagSplitter(maybe_compound, allWords):
    """Splits word at all possible locations. If both smaller words are in the dictionary, returns them."""
    """Function courtesy of matchado on GitHub."""
    both_words = []
    split_possibility = [maybe_compound[:i] in allWords for i in reversed(range(len(maybe_compound)+1))]
    possible_split_positions = [i for i, x in enumerate(split_possibility) if x == True]
    for split_pos in possible_split_positions:
        split_words = []
        word_1, word_2 = maybe_compound[:len(maybe_compound)-split_pos], maybe_compound[len(maybe_compound)-split_pos:]
        if word_2 in allWords:
            split_words.append(word_1)
            split_words.append(word_2)
            both_words.append(split_words)
    return both_words

def handleCompounds(formattedList, languages, splitString, allWords, greekRoots):
    """If a word is compound, adds HTML tags to both parts of the compound word."""
    for x, maybe_compound in enumerate(formattedList):
        if '</span>' in splitString[x]: #Escapes if a word already has HTML tags.
            continue
        origin = getOrigin(maybe_compound, allWords)
        if len(hashtagSplitter(maybe_compound, allWords)) == 1 and origin == None:
            both_words = hashtagSplitter(maybe_compound, allWords)
            both_words = both_words[0]
            word_1 = both_words[0]
            word_2 = both_words[1]
            spuriousCompounds = ['it', 'ive', 'con', 'der', 'per', 'if', 'us', 'a', 'oy', 'age', 'ate', 'ally',
                                 'im', 'ship', 'or', 'led', 'red', 'able', 'less', 'i', 'is', 'in']
            if word_2 in spuriousCompounds:
                continue
            lower = splitString[x].lower() #Handles capitalized compound words.
            if len(lower.split(word_1)) != 2: #Escapes if a word doesn't split correctly.
                continue
            word_2_with_punctuation = (lower.split(word_1))[1]
            word_1_with_punctuation = splitString[x].replace(word_2_with_punctuation, '')
            origin = getOrigin(word_1, allWords)
            if origin != None:
                word_1_with_punctuation = '<span style="background-color: #' + languages[origin]['colour']  + '">' + word_1_with_punctuation + '</span>'
                languages[origin]['word count'] += 1
            if any(root in word_1 for root in greekRoots):
                word_1_with_punctuation = '<span style="background-color: #' + languages['Greek']['colour'] + '">' + word_1_with_punctuation + '</span>'
                languages['Greek']['word count'] += 1
            origin = getOrigin(word_2, allWords)
            if origin != None:
                word_2_with_punctuation = '<span style="background-color: #' + languages[origin]['colour']  + '">' + word_2_with_punctuation + '</span>'
            elif any(root in word_1 for root in greekRoots):
                word_2_with_punctuation = '<span style="background-color: #' + languages['Greek']['colour'] + '">' + word_2_with_punctuation + '</span>'
            splitString[x] = word_1_with_punctuation + word_2_with_punctuation

def lookupInDictionary(formattedList, languages, splitString, allWords, greekRoots):
    """ Looks up words and applies html tags based on language origin. """
    for x, word in enumerate(formattedList):
        if '</span>' in splitString[x]: #Escapes if a word already has HTML tags.
            continue
        origin = getOrigin(word, allWords)
        if origin != None:
            splitString[x] = '<span style="background-color: #' + languages[origin]['colour']  + '">' + splitString[x] + '</span>'
            languages[origin]['word count'] += 1
        elif any(root in word for root in greekRoots) and '</span>' not in splitString[x]:
            splitString[x] = '<span style="background-color: #' + languages['Greek']['colour'] + '">' + splitString[x] + '</span>'
            languages['Greek']['word count'] += 1
    return languages

def removeExtraHTML(formattedList, splitString, allWords):
    """ If two adjacent words are the same color, 
    removes the first HTML tag from the second word and the second HTML tag from the first word. 
    This keeps the output from looking like a ransom letter.
    """
    for x, word in enumerate(formattedList[:-1]):
        nextWord = formattedList[x+1]
        originW1 = getOrigin(word, allWords)
        originW2 = getOrigin(nextWord, allWords)
        
        if originW1 == originW2 and originW1 != None:
            splitString[x+1] = splitString[x+1].replace('<span style="background-color: #' + languages[originW1]['colour'] + '">', '')
            splitString[x]   = splitString[x].replace('</span>', '')

languages = {'Anglo':    {'colour': '00FF00', 'word count': 0, 'colour name': 'Green',      'long name': 'Anglo-Saxon' },
             'Germanic': {'colour': '008000', 'word count': 0, 'colour name': 'Dark green', 'long name': 'other Germanic (Old Norse, Scandinavian, German, Dutch)'},
             'French':   {'colour': 'FFFF00', 'word count': 0, 'colour name': 'Yellow',     'long name': 'French'},
             'Latin':    {'colour': 'FF0000', 'word count': 0, 'colour name': 'Red',        'long name': 'Latin'},
             'Arabic':   {'colour': 'FF00FF', 'word count': 0, 'colour name': 'Pink',       'long name': 'Arabic'},
             'Asian':    {'colour': 'B041FF', 'word count': 0, 'colour name': 'Purple',     'long name': 'Asian'},
             'Greek':    {'colour': '00FFFF', 'word count': 0, 'colour name': 'Blue',       'long name': 'Greek'},
             'Spanish':  {'colour': 'FA7921', 'word count': 0, 'colour name': 'Orange',     'long name': 'Spanish'},
             'Celtic':   {'colour': '3EA99F', 'word count': 0, 'colour name': 'Blue green', 'long name': 'other Celtic (Common Brittonic, Gaulish, Irish, Scottish Gaelic, Welsh)'}
            }
languages = collections.OrderedDict(sorted(languages.items()))

# Reads in the dictionary and list of Greek roots from json files.
with open('etymologyDictionary.json', 'r') as dictionaryFile:
    allWords = json.load(dictionaryFile)
with open('greekRootsList.json', 'r') as greekFile:
    greekRoots = json.load(greekFile)
    
# Opens an output file and adds a legend.
markedUp = open('markedUp.html', encoding='utf-16', mode='w')
markedUp.write('<p>Green words have an Anglo-Saxon origin.</p>'
               '<p>Blue green words have a Celtic origin.</p>'
               '<p>Dark green words have some other Germanic origin (Old Norse, Scandinavian, German, Dutch).</p>'
               '<p>Yellow words have a French origin.</p>'
               '<p>Red words have a Latin origin.</p>'
               '<p>Blue words have a Greek origin.</p>'
               '<p>Pink words have an Arabic or Persian origin.</p>'
               '<p>Purple words have an Asian origin (Chinese, Japanese, south Asian, Polynesian, etc.)</p>'
               '<p>Orange words have a New World origin (Spanish, Portuguese, or Native American).</p>')

# Opens the user's input file, runs the functions on each line of text, then
# writes the results to the output file.
with open('usertext.txt', encoding='utf-16', mode='r') as f:
    usertext = f.readlines()
    TotalWordCount = 0

    for line in usertext:
        formattedList = []
        splitString = line.split()
        TotalWordCount = TotalWordCount + len(splitString)
        stripForDictionary(splitString, formattedList)
        handleCompounds(formattedList, languages, splitString, allWords, greekRoots)
        removeAffixes(formattedList, allWords)
        handleCompounds(formattedList, languages, splitString, allWords, greekRoots)
        lookupInDictionary(formattedList, languages, splitString, allWords, greekRoots)
        removeExtraHTML(formattedList, splitString, allWords)
        joinedString = ' '.join(splitString)
        markedUp.write('<p>' + joinedString + '</p>')

# Calculates the percent composition of the text and writes it to the file.
float(TotalWordCount) #Forces Python to do true division.
AngloPercent = (languages['Anglo']['word count']/TotalWordCount)*100
GermanicPercent = (languages['Germanic']['word count']/TotalWordCount)*100
CelticPercent = (languages['Celtic']['word count']/TotalWordCount)*100
FrenchPercent = (languages['French']['word count']/TotalWordCount)*100
LatinPercent = (languages['Latin']['word count']/TotalWordCount)*100
GreekPercent = (languages['Greek']['word count']/TotalWordCount)*100
ArabicPercent = (languages['Arabic']['word count']/TotalWordCount)*100
AsianPercent = (languages['Asian']['word count']/TotalWordCount)*100
SpanishPercent = (languages['Spanish']['word count']/TotalWordCount)*100

markedUp.write('<p>Percent composition:</p>'
               '<p>{0:.2f} percent Anglo-Saxon'.format(AngloPercent) + '</p>'
               '<p>{0:.2f} percent Celtic'.format(CelticPercent) + '</p>'
               '<p>{0:.2f} percent other Germanic'.format(GermanicPercent) + '</p>'
               '<p>{0:.2f} percent French'.format(FrenchPercent) + '</p>'
               '<p>{0:.2f} percent Latin'.format(LatinPercent) + '</p>'
               '<p>{0:.2f} percent Greek'.format(GreekPercent) + '</p>'
               '<p>{0:.2f} percent Arabic or Persian'.format(ArabicPercent) + '</p>'
               '<p>{0:.2f} percent Asian'.format(AsianPercent) + '</p>'
               '<p>{0:.2f} percent New World'.format(SpanishPercent) + '</p>')

markedUp.close()


