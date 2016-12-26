## Usage

``` bash
$ cd src/
$ python demo.py
Training...
Initializing spellchecker...
Բարեւ
> անուշաթիռ
անուշադիր անուշադի անուշաթիռ
```

## Test

``` bash
$ cd test/
$ python test.py tests/rubina.json ../db/freq_dict.txt ../db/corr_dict.txt --v
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
