def nice_print(doc):
    print('{:<10} {:<10} {:<12} {:<10}'.format('text', 'pos_', 'dep_', 'tag_'))
    print('_'* 55)
    for token in doc:
        print('{:<10} {:<10} {:<12} {:<10}'.format(token.text, token.pos_, token.dep_, token.tag_))
    print('_'* 55)
    