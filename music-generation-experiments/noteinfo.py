note_list = 'C,C^/D_,D,D^/E_,E,F,F^/G_,G,G^/A_,A,A^/B_,B'
note_list = [n.split('/') for n in note_list.split(',')]
num_notes = len(note_list)

naturals = list('CDEFGAB')
num_naturals = len(naturals)
