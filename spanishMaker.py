import os
import re
import json
import io

def main():
    # Initialise working directory
    directory = raw_input("Input working directory: ")
    if len(directory) < 1:
        directory = 'DIRECTORY GOES HERE'
    os.chdir(directory)

    fileName = 'spanishDict.txt'
    
    markedUp = io.open('spanishDictionary.json', encoding='utf-16', mode='w')
    
    markedUp.write(unicode('{'))
    with io.open(fileName, encoding='utf-16', mode='r') as f:
        pattern = '(?<=;\[\[)[^\[\]]+(?=\]\])'
        raw = f.readlines()
        for line in raw:
            if line.startswith(';[['):
                match = line[3:line.index(']]')]
                if '|' in match:
                    match = match[match.index('|')+1:]        # to format words that have a hyperlink
                match = match.split()                       # for phrases with multiple words
                for word in match:
                    markedUp.write(unicode('"' + word + '": "Spanish", \n'))

    markedUp.write(unicode('}'))
    markedUp.close()

if __name__ == "__main__":
    main()