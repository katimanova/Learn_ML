# distutils: language=c++
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
from distutils.core import setup
from cymem.cymem cimport Pool
from spacy.tokens.doc cimport Doc
from spacy.structs cimport TokenC
from spacy.typedefs cimport hash_t


cdef struct DocStruct:
    # структура 
    # структуру TokenC, которая используется в spaCy в качестве контейнера данных для объекта Token.
    TokenC* c # указатель
    int length


cdef int counter(DocStruct* doc, hash_t tag):
    # кол-во личных местоимений в тексте 
    cdef int cnt = 0
    for c in doc.c[:doc.length]:
        if c.tag == tag:
            cnt += 1
    return cnt

cpdef main(Doc mydoc):
    cdef int cnt
    cdef Pool mem = Pool()
    cdef DocStruct* doc_ptr = <DocStruct*>mem.alloc(1, sizeof(DocStruct))
    doc_ptr.c = mydoc.c
    doc_ptr.length = mydoc.length
    tag = mydoc.vocab.strings.add('PRP')
    cnt = counter(doc_ptr, tag)
    print(doc_ptr.length)
    print(cnt)