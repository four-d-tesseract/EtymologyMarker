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

    fileName = 'celticDict.txt'
    
    markedUp = io.open('celticDictionary.json', encoding='utf-16', mode='w')
    
    markedUp.write(unicode('{'))
    with io.open(fileName, encoding='utf-16', mode='r') as f:
        pattern = '(?<=;\[\[)[^\[\]]+(?=\]\])'
        pattern2 = '^(;\s*\'*\[*(wikt\:)*)[^\[\]\:]+(\]{2}|:)'
        raw = f.readlines()
        for line in raw:
            match = re.search(pattern2, line)
            if match != None:
                match = match.group(0)
                if '|' in match:
                    match = match[match.index('|')+1:]      # to format words that have a hyperlink
                for badchar in ['\:', '\;', '\[+', '\]+', '\'+']:
                    match = re.sub(badchar, '', match).strip()
                match = match.split()                       # for phrases with multiple words
                for word in match:
                    markedUp.write(unicode('"' + word + '": "Celtic", \n'))

    markedUp.write(unicode('}'))
    markedUp.close()

if __name__ == "__main__":
    main()
