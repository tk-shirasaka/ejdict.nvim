import zipfile
import urllib.request
import sqlite3
import json

EJDICT_PATH = 'ejdic-hand-sqlite/ejdict.sqlite3'


def download_ejdict():
    url = 'https://kujirahand.com/web-tools/EJDictFreeDL.php'
    params = 'key=__KEY__&type=1'

    with urllib.request.urlopen('%s?%s' % (url, params)) as res:
        with open('ejdict', 'bw') as f:
            f.write(res.read())
        with zipfile.ZipFile('ejdict') as ejdict:
            ejdict.extract(EJDICT_PATH)


def load_verbdict(con):
    url = 'https://raw.githubusercontent.com/monolithpl/verb.forms.dictionary'
    path = 'master/json/verbs-dictionaries.json'

    con.execute('CREATE TABLE verbs (word varchar, verb varchar)')
    with urllib.request.urlopen('%s/%s' % (url, path)) as res:
        for line in json.loads(res.read()):
            word = line[0]
            for verb in line[1:]:
                sql = 'INSERT INTO verbs values(?, ?)'
                con.execute(sql, (word, verb, ))


download_ejdict()
with sqlite3.connect(EJDICT_PATH) as con:
    load_verbdict(con)
