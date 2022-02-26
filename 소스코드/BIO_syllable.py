def BIO(txt):

    sentence = []
    test = []; val = []
    strA = ['F','EA', 'EB', 'NA', 'NB', 'PA', 'PB']
    
    f = open(txt + '.txt','r')

    for line in f:
        count = 1

        for x in range(len(strA)):
            p = re.compile('(?<=\<'+strA[x]+'>)(.*?)(?=<\/' + strA[x] + '>)')

            L = list(line)
            for m in p.finditer(''.join(L)):

                cc = str(count) + 'X'*((m.span()[1]-m.span()[0])-1)

                test.append([L[m.span()[0]:m.span()[1]],cc, strA[x]])
                L[m.span()[0]:m.span()[1]] = cc
                count += 1

            line = ''.join(L)
            line = line.replace('<'+strA[x]+'>',' ').replace('</'+strA[x]+'>',' ').replace('  ',' ').rstrip().lstrip()

        splits = line.split(' ')

        for i in splits:
            b = [z[1] for z in test]

            if i in b:
                x = ''.join(test[b.index(i)][0]).split(' ')
                for j in range(len(x)):
                    if x[j] =='': continue
                    if x[j] in b:
                        if ''.join(test[b.index(x[j])][0])!='':
                            val.append([''.join(test[b.index(x[j])][0]), test[b.index(x[j])][2]])
                    else:
                        val.append([x[j], test[b.index(i)][2]] )
            else:
                val.append([i,'O'])

        for z in val:
            tag = z[1]
            for x in range(len(z[0])):
                if tag == 'O':
                    sentence.append([z[0][x],tag])
                else:
                    if x == 0:
                        sentence.append([z[0][x],'<B-' + tag + '>'])
                    else:
                        sentence.append([z[0][x],'<I-' + tag + '>'])

        if len(sentence) > 0:
            tagged_sentences.append(sentence)
            sentence = []
            test = []
            val = []
