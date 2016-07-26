# EtymologyMarker

This code was born out of an interest in the relationship between etymology – the origin of a word – and the register of people's writing. You can find more information about the rationale behind Etymology Marker here: https://steamtrainsandghosts.wordpress.com/2016/06/20/2780/

etymologyMarker.py is the main script. It takes "usertext.txt" as an input. Make sure to save the file with UTF-16 encoding so special characters like em dashes don't get turned into gibberish like this: â€“.

Etymology Marker strips words of their punctuation, prefixes, and suffixes, then looks each word up in etymologyDictionary.json. If it finds a match, it adds HTML tags to the word that will color-code it according to its etymolgy.

If it doesn't find an etymology, then it looks for Greek roots from GreekRootsList.json inside the word. If it still doesn't find a match, it leaves the word alone.

Etymology Marker outputs the HTML file "markedUp.html".

DictionaryMaker.py and GreekListMaker.py contain the data inside their respective JSON files plus code to dump to the JSON files. I found these were a convenient way to view and edit the JSON files.

I used the following resources to write this code:

Word etymologies
https://en.wikipedia.org/wiki/Lists_of_English_words_by_country_or_language_of_origin
https://en.wikipedia.org/wiki/List_of_Greek_and_Latin_roots_in_English
http://etymonline.com/

Code
https://github.com/matchado/HashTagSplitter

Lists of common English words to check Etymology Marker's performance
http://splasho.com/upgoer5/
https://github.com/first20hours/google-10000-english

*What needs to be done*

I plan to make Etymology Marker into a Web app. If you want to take a crack at this yourself, that's cool. Go for it! If you have any other improvements or suggestions, that is also cool.

