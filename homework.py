import wikipedia as wiki
import wikitools as wkt
import random as r
import re
from random import random as p

# maximum length of nouns from wikipedia
MAX = 50

# holds the question templates
global questions
questions = []
f = open("questions.txt", "r")
s = f.readlines()
for q in s:
    questions.append(q[:-1])
f.close()

# holds the answer templates
global answers
answers = []
f = open("answers.txt", "r")
s = f.readlines()
for a in s:
    answers.append(a[:-1])
f.close()

# holds the dictionary
global dict
dict = []
f = open("vocab.txt", "r")
s = f.readlines()
for line in s:
    list = line[:-1].split(" ")[1:]
    dict.append([word.replace("_", " ") for word in list])
f.close()


def wikirand():
    title = "!" * (MAX + 1)
    while len(title) > MAX:
        title = wkt.page_rand()
    if title[0:8] == "List of ":
        title = title[8:].capitalize()
    title = re.sub(" \(.*?\)", "", title)
    return title


def get_keyterms():
    terms = []
    for i in range(r.randint(4, 10)):
        terms.append(wikirand())
    return terms


def pick(list, remove=0):
    res = str(r.sample(list, 1)[0])
    if remove == 1:
        list.remove(res)
    return res


def year():
    y = r.randint(17, 20)
    y = str(y) + str(r.randint(0, 1 if y == 20 else 9)) + str(r.randint(0, 9))
    # info.append(int(y))
    return y


def grab(n, keyterms):
    speech = {
        0: pick(keyterms),
        1: pick(dict[1]) if p() < 0.7 else pick(dict[3]) + " " + pick(keyterms),
        2: pick(dict[2]) if p() < 0.7 else pick(dict[4]) + " " + pick(keyterms),
        3: year(),
        5: pick(dict[5]),
        6: pick(dict[6]),
    }
    return speech.get(n)


def ask(keyterms):
    Q = pick(questions)
    i = 0
    while i < len(Q):
        if Q[i].isdigit():
            W = grab(int(Q[i]), keyterms)
            Q = Q[:i] + W + Q[i + 1 :]
            i += len(W)
        else:
            i += 1
    return Q


def ans(keyterms):
    A = pick(answers, 1)
    i = 0
    while i < len(A):
        if A[i].isdigit():
            W = grab(int(A[i]), keyterms)
            A = A[:i] + W + A[i + 1 :]
            i += len(W)
        else:
            i += 1
    return A


def question(keyterms):
    q = ask(keyterms) + "\n\n"
    for choice in [" A. ", " B. ", " C. "]:
        a = ans(keyterms)
        while a.endswith("above."):
            a = ans(keyterms)
        q += choice + a + "\n"
    q += " D. " + ans(keyterms) + "\n"
    return q


def replace(text, target, fix):
    if target not in text:
        return text

    if target[0] == " " and target[-1] == " ":
        return (
            text[: text.find(target)]
            + " "
            + pick(fix)
            + " "
            + text[text.find(target) + len(target) :]
        )
    else:
        return (
            text[: text.find(target)]
            + pick(fix)
            + text[text.find(target) + len(target) :]
        )


def explanation(keyterms):
    expl = ""
    blob = []
    while len(blob) < r.randint(1, 5):
        title = wiki.search(wiki.random(), results=1)[0]
        try:
            blob.append(pick(wiki.summary(title).split(". ")))
        except (wiki.exceptions.DisambiguationError, wiki.exceptions.PageError):
            return explanation(keyterms)

    bomb = ["he", "He", "she", "She", "it", "It", "The"]

    for s in blob:
        if s.endswith("."):
            s = s[:-1]
        if " is " in s:
            s = pick(keyterms) + s[s.find(" is ") :]
        if " was " in s:
            s = pick(keyterms) + s[s.find(" was ") :]
        for b in bomb:
            s = replace(s, " " + b + " ", pick(keyterms))

        expl += s + ". "

    return expl
