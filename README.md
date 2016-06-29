## Usage

``` bash
pip install epub

cd src/
# produce dictionary (make sure you have a corpus directory)
python collector.py .../corpus/ txt,html,epub > words.txt
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


## Credits

Thanks to:
* Vahakn
* Ani
* Ani
* Gohar
* Neli

For helping in the development of the project.
