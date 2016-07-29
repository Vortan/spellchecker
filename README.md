## Usage

``` bash
$ cd src/
$ python
>>> from spellchecker import *
>>> sp = spellchecker()
>>> sp.trainDict('../db/dict.txt')
>>> word = 'առաջչն'.decode('utf-8')
>>> printUs(sp.correct(word, 3))
```

## Test

``` bash
$ cd test/
$ python test.py ../db/dict.txt ./tests/rubina.json 3 1000 100 1
```

## Armenian spelling

Rubina Nazaryan's "Մայրենի Բոլորի Համար" considers these letters tricky in Armenian spelling.

* Է - Ե
* Օ - Ո
* Ը
* Բ - Պ - Փ
* Գ - Կ - Ք
* Դ - Տ - Թ
* Ձ - Ծ - Ց
* Ջ - Ճ - Չ
* Ղ - Խ
* Ր - Ռ
* Հ
* Վ - Ֆ
* Ն - Մ
* Զ - Ս
* Ժ - Շ
