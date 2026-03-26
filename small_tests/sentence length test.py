sentences = ['This sentence contains one microbe: Gluconobacter oxydans',
             'And this one doesnt contain anything',
             'These two microbes are usually found together: Lactobacillus curvatus and Lactobacillus plantarum',
             'Some are lonely though',
             'S. cerevisiae is da yeasty boi']

all_ents = [[('MICROBE', 'Gluconobacter oxydans', 36, 57)],
            [],
            [('MICROBE', 'Lactobacillus curvatus', 47, 69), ('MICROBE', 'Lactobacillus plantarum', 74, 97)],
            [],
            [('MICROBE', 'S. cerevisiae', 0, 13)]]

merge_sent = ''
merge_ents = []
last_sent_length = 0

final_ents = []

for i, sent in enumerate(sentences):
    ents = all_ents[i]
    if not merge_sent:
        #if there are entities which are not empty
        if ents:
            merge_sent = sent
            merge_ents = ents
    #but if there is a sentence awaiting merging
    else:
        #if there are any entities to merge with
        if ents:
            merge_sentence = merge_sent + ' ' + sent
            last_sent_length += len(sent)
            ents = [(l, t, s+last_sent_length, e+last_sent_length) for l, t, s, e in ents]
            merge_ents = merge_ents + ents
            final_ents.append(merge_ents)
            merge_sent = ''
            merge_ents = []
                
print(final_ents)