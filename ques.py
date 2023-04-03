import ru_core_news_lg
import spacy as sp
import sys

from spacy.symbols import ORTH, LEMMA
from IPython.display import Image
from spacy.tokens.doc import Doc
from spacy.vocab import Vocab

from spacy import displacy
from IPython.display import Image


# Возвращение прямого дополнения (по книжке это dobj, однако в русском spacy есть только obj, iobj)
def find_chunk(doc):
    chunk = ''
    for i, token in enumerate(doc):
        if token.dep_ == 'obj':
            shift = len([w for w in token.children])
            #print([w for w in token.children])
            chunk = doc[i-shift:i+1]
            break
    return chunk

def determine_question_type(chunk):
    question_type = 'yesno'
    for token in chunk:
        # ищет модификатор прилагательного (пример: "красный" шар)
        if token.dep_ == 'amod':
            question_type = 'info'
    return question_type


def generate_question(doc, question_type):
    sent = ''

    for i, token in enumerate(doc):
        if token.tag_ == 'PRON ' and token.text == 'Я':
            sent = doc[:i].text + ' вы ' +  doc[i+1:].text
            break

    doc = nlp(sent)
    if question_type == 'info':
        for i, token in enumerate(doc):
            if token.dep_ == 'obj':
                sent = 'Хотите ли ' + doc[:i].text + ' одно ' +  doc[i+1:].text
                break
    if question_type == 'yesno':
        for i, token in enumerate(doc):
            if token.dep_ == 'obj':
                sent = doc[:i-1].text + ' зеленое ' + doc[i:].text
                break
            
    doc = nlp(sent)
    sent = doc[0].text.capitalize() + ' ' + doc[1:len(doc)-1].text + '?'
    return sent


# пробуем использовать модель чат бота
if len(sys.argv) > 1:
    sent = sys.argv[1]
    nlp = sp.load('ru_core_news_lg')
    doc = nlp(sent)
    chunk = find_chunk(doc)
    if str(chunk) == '':
        print('The sentence does not contain a direct object.')
        sys.exit()
    question_type = determine_question_type(chunk)
    question = generate_question(doc, question_type)
    print(question)
else:
    print('You did not submit a sentence!')