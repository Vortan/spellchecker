## Usage

``` bash
cd src/
# produce dictionary
python collector.py .../corpus/ > words.txt
# train and use spellchecker
python
>>> from spellchecker import *
>>> sp = spellchecker()
>>> sp.train('words.txt')
>>> word = 'առաջչն'.decode('utf-8')
>>> printUs(sp.correct(word))
```

## Test

``` bash
cd test/
python test.py ../src/words.txt ./tests/rubina.json 3 1000 100 1
```

## Relevant Links

Code based on
http://norvig.com/spell-correct.html

Corpus Sources
http://www.eanc.net/
http://www.digilib.am/

## Armenian Spell Checker

#### Introduction

It is an unfortunate fact that, more often than not, when Armenian is “spoken” online, it is written in Latin script. That is, instead of using the Armenian alphabet to write something like “Բարեւ, ինչպես եք,” instead, it is transliterated to “barev/parev, inchbes ek.” We believe that an Armenian Spell Checker is the solution to this issue. This project will aim to address the main issue that has led to this trend. We believe that if this problem is resolved, more people will begin to write in Armenian on their computers, thus creating a larger online Armenian presence. This will not only help give the Armenian online community a more serious look and feel, but it will also give the diaspora a chance to practice reading and writing in Armenian non-phonetically. We have a beautiful and unique alphabet, with a long and interesting history. It not only a shame to not put it to use, but it could prove to be dangerous if the youth of the current generation, the first to have mainstream internet, doesn't begin the practice of using it in an everyday setting, especially in the most used medium.

#### Motivation

There are two main reasons as to why Armenian script is not used in online live communication, such as email or chat. The first is accessibility. This problem is more prevalent in the world of chatting, since chatting is often something that is used between other tasks. For instance, you might reply to a message from your friend, continue typing up a report, then return to the chat again. In cases such as this, turning Armenian script on and off each time you're going to chat is a hassle. This isn’t the case when writing an email, since you can turn on Armenian script, write and send the email, and then turn it off. This ease of access is also the main reason that Armenian script isn't used in online communication in Armenia.


The second, reason, which is more relevant to the diaspora, is spelling. Since Armenian isn’t read as often in the diaspora, it becomes difficult to be certain about the spelling of particular words. Another reason spelling is difficult in the diaspora is because Mesrobian spelling is objectively more difficult than non-Mesrobian Armenian spelling. The reason for this is because the main rule of non-Mesrobian spelling, “write it like you hear it,” does not apply because the distinction between դ-թ, գ-ք, բ-փ, etc is not audibly clear.


In-browser and in-document spell checkers have become an integral part of our daily lives, so much so that we only acknowledge them when we need them and they are missing. An Armenian spell checker and possibly an easily accessible Armenian script switch would be a plug-and-play solution that would both increase the quantity and improve the quality of online Armenian communication.


#### Implementation

The objective of this project is to create a spell checker that can be seamlessly integrated into the everyday life and tasks of a casual user. Since the creation of Google Docs and Cloud Storage, even document writing has switched the online platforms, therefore we believe that creating a browser plugin might be the best medium in which to implement this project. Ideally, the plugin or extension would work exactly like the existing English spell checker, as in, when you type something in Armenian, if you spelled it incorrectly, it would underline it with a red squiggle. If you right click the word, it would show you the closest alternatives, which, if clicked, would replace the word you had written. In addition to that, it would have a switch that would turn on Armenian script for you in the tab you are currently in. The conversion from software to plugin/extension would be relatively easy since the two most commonly used browsers, Google Chrome and Mozilla Firefox, are built to accommodate plugins/extensions of this kind.

#### Complications

Whereas creating a spellchecker is within the scope of our capabilities, creating a grammar checker is much more difficult. There are many reasons for this, but the classic one is that correcting grammar means understanding intended meaning, and that is something that computers aren’t able to do perfectly yet.


Another issue is the distinction between Mesrobian and non-Mesrobian spelling. The easiest solution would be to include both, but this would have to be something that would need to be discussed. 

#### Conclusion and Looking Ahead

There are many reasons as to why an Armenian online presence has yet to be established, especially in the diaspora, but we believe that spell checker is the first step on the path to fixing that. Other ideas that are related to language and its representation and execution in the online world is fixing the Armenian keyboard layout and creating a modern dictionary for non-existent Armenian words.


The first of these problems is an obvious one. The current Armenian keyboard takes over the punctuation and number keys, thus making it difficult to write Armenian in an uninhibited manner.


The second issue is the fact that although Armenian versions of most words might exist, they are either not appropriate or not known. Creating a crowdsourced online Armenian dictionary where people can suggest or share new words which can be voted on could be the solution to having online consensus to how the language moves forward.


It is clear that the main method of communication right now and in the future is the internet. It is also clear that the amount of Armenian online is currently lacking. This needs to be fixed, and the best way to do it is to give people the confidence and accessibility that they need to make their voices read.

#### Credits

Thanks to:
* Vahakn
* Ani
* Ani
* Gohar
* Neli

For helping in the development of the project.
