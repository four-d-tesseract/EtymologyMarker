import os
import re
import json
import io
    
def getOrigin(word, allWords):
    """ Returns the language etymology of a word.
    """
    return allWords.get(word)
 
def aAn(word):
    """ Returns 'a' or 'an' based on the preceding word.
    """
    if word[0] in 'aeiouAEIUO':
        return 'an'
    else:
        return 'a'

def whitespaceNum(number):
    """ Creates white-space for evenly distributing numbers.
    """
    if number < 10:
        return ' ' * 2
    elif number < 100:
        return  ' '
    else:
        return ''

def stripForDictionary(splitString, formattedList):
    """ Takes the user's input, strips out the punctuation, and makes it lower-case.
    """
    for word in splitString:
        stripped = re.sub('[^a-zA-Z]+', '', word) # Removes all non-alphabet characters.
        strippedLower = stripped.lower()
        formattedList.append(strippedLower)

def removeAffixes(formattedList, allWords):
    """ If the program can't find a word in the dictionary,
    this function tries removing prefixes and suffixes.
    """
    for x in xrange(len(formattedList)):
        if getOrigin(formattedList[x], allWords) == None:
            formattedList[x] = re.sub('es$', "", formattedList[x])
            if getOrigin(formattedList[x], allWords) == None:
                formattedList[x] = re.sub('s$', "", formattedList[x])
                
            if getOrigin(formattedList[x], allWords) == None:
                formattedList[x] = re.sub('est$', "", formattedList[x])
                formattedList[x] = re.sub( 'er$', "", formattedList[x])
                
            for suffix in ['ed$', 'ial$', 'al$', 'ing$', 'ful$', 'age$', 'ist$', 'ism$']:
                formattedList[x] = re.sub(suffix, "", formattedList[x])
                
            if getOrigin(re.sub('ly$', "le", formattedList[x]), allWords) != None:  # Replaces -ly with -le if that produces a word.
                formattedList[x] = re.sub('ly$', "le", formattedList[x])    
            else:
                formattedList[x] = re.sub('ly$', "",   formattedList[x])            # Otherwise, strips off -ly.
                
                if getOrigin(re.sub('$',"e", formattedList[x]), allWords) != None:      # Adds -e back onto words that had -e removed.
                   formattedList[x] = re.sub('$',  "e", formattedList[x])
                
                elif getOrigin(formattedList[x], allWords) == None:                       # Handles words that end in -y, which gets changed to -ie when a suffix is added.
                    formattedList[x] = re.sub('i$', "y", formattedList[x])
                
                    if getOrigin(formattedList[x], allWords) == None:
                        formattedList[x] = re.sub('^re', "", formattedList[x])
                        formattedList[x] = re.sub('^un', "", formattedList[x])
                
                    if getOrigin(formattedList[x], allWords) == None:                       # Handles consonants that are doubled before -ed.
                        for consonant in ['b', 'p', 'r', 'n', 't', 'd', 'g']:
                            suffix = consonant*2 + '$'
                            formattedList[x] = re.sub(suffix, consonant, formattedList[x])

def lookupInDictionary(formattedList, languages, splitString, allWords, greekRoots):
    """ Looks up the words that are lower-case and stripped of punctuation and affixes (formattedList). 
    Then it adds HTML tags to the corresponding words from the user's input (splitString).
    """
    for x, word in enumerate(formattedList):
        origin = getOrigin(word, allWords)
        
        if origin in languages.keys():
            splitString[x] = '<span style="background-color: #' + languages[origin]['colour']  + '">' + splitString[x] + '</span>'
            languages[origin]['word count'] += 1
            
        elif any(root in word for root in greekRoots):
            splitString[x] = '<span style="background-color: #' + languages['Greek']['colour'] + '">' + splitString[x] + '</span>'
            languages['Greek']['word count'] += 1
            
    return languages

def removeExtraHTML(formattedList, splitString, allWords):
    """ If two words next to each other are the same colour, 
    removes the first HTML tag from the second word and the second HTML tag from the first word. 
    This keeps the output from looking like a ransom letter.
    """
    for x, word in enumerate(formattedList[:-1]):
        nextWord = formattedList[x+1]
        originW1 = getOrigin(word, allWords)
        originW2 = getOrigin(nextWord, allWords)
        if originW1 == originW2 and originW1 in languages.keys():
            splitString[x+1] = splitString[x+1].replace('<span style="background-color: #' + languages[originW1]['colour'] + '">', '')
            splitString[x]   = splitString[x].replace('</span>', '')

# Defining dictionary of languages with associated meta-data
languages = {'Anglo':    {'colour': '8BC34A', 'word count': 0, 'colour name': 'Green',      'long name': 'Anglo-Saxon' },
             'Germanic': {'colour': '43A047', 'word count': 0, 'colour name': 'Dark green', 'long name': 'other Germanic (Old Norse, Scandinavian, German, Dutch)'},
             'French':   {'colour': 'FDD835', 'word count': 0, 'colour name': 'Yellow',     'long name': 'French'},
             'Latin':    {'colour': 'F44336', 'word count': 0, 'colour name': 'Red',        'long name': 'Latin'},
             'Arabic':   {'colour': 'AF7AC5', 'word count': 0, 'colour name': 'Purple',     'long name': 'Arabic'},
             'Greek':    {'colour': '26C6DA', 'word count': 0, 'colour name': 'Blue',       'long name': 'Greek'},
             'Spanish':  {'colour': 'FA7921', 'word count': 0, 'colour name': 'Orange',     'long name': 'Spanish'}
            }

def main():
    # Initialise working directory
    directory = raw_input("Input working directory: ")
    if len(directory) < 1:
        directory = 'WORKING DIRECTORY GOES HERE'
    os.chdir(directory)

    fileName = raw_input("Input text file to analyse (Note: must be in UTF format): ")
    if len(fileName) < 1:
        fileName = 'usertext.txt'
    
    # Reads in the dictionary and list of Greek roots from json files.
    with open('etymologyDictionary.json', 'r') as dictionaryfile:
        allWords = json.load(dictionaryfile)

    with open('greekRootsList.json', 'r') as greekfile:
        greekRoots = json.load(greekfile)

    # Opens an output file and adds a legend.
    markedUp = io.open('markedUp.html', encoding='utf-16', mode='w')

    markedUp.write(unicode('<p> Key: </p>'))

    for language in sorted(languages.keys()):
        markedUp.write(unicode('<p>' + '<span style="background-color: #' 
                               + languages[language]['colour']      + '">' 
                               + languages[language]['colour name'] + '</span>'  + ' words have ' 
                           + aAn(languages[language]['long name'])  + ' ' 
                               + languages[language]['long name']   + ' origin.' + '</p>'))
    markedUp.write(unicode('<br></br>'))

    # Opens the user's input file, runs the functions on each line of text,
    # then writes the results to the output file.
    with io.open(fileName, encoding='utf-16', mode='r') as f:
        usertext       = f.readlines()
        TotalWordCount = 0
        for line in usertext:
            formattedList = []
            splitString = line.split()
            TotalWordCount += len(splitString)
            stripForDictionary(splitString, formattedList)
            removeAffixes(formattedList, allWords)
            lookupInDictionary(formattedList, languages, splitString, allWords, greekRoots)
            removeExtraHTML(formattedList, splitString, allWords)
            joinedString = ' '.join(splitString)
            joinedString = joinedString.replace('</span> ', ' </span>')            # highlights spaces between words
            markedUp.write(unicode('<p>' + joinedString + '</p>'))

    # Calculates the percent composition of the text and writes it to the file.
    markedUp.write(unicode('<br></br><p>' + 'Percent composition:' + '</p>'))

    # Sorts dictionary as a list ordered by descending Word Count and writes %age composition.
    for language in sorted(languages.iteritems(), key=lambda (k, v): v['word count'], reverse = True):     
        percent = language[1]['word count'] * 100.0 / TotalWordCount
        if percent > 0:
            markedUp.write(unicode('<pre>' + whitespaceNum(percent) + '{:.2f} percent '.format(percent) + language[1]['long name'] + '</pre>'))

    markedUp.close()

if __name__ == "__main__":
    main()