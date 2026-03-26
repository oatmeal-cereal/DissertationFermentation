with open('list_files\\compounds_list.json', 'r', encoding='utf-8') as f:
    compounds = json.load(f)
    
with open('list_files\\fatty_acid_list.json', 'r', encoding='utf-8') as f:
    fatty_acids = json.load(f)
    
with open('list_files\\compound_5_endings.json', 'r', encoding='utf-8') as f:
    compound_endings = json.load(f)

compound_endings_regex = f'[A-Za-z0-9\\(\\)]({'|'.join(compound_endings)})'

compound_regex_patterns = [
    [{'TEXT': {'REGEX': '[0-9],[0,9](\\-)[A-z]+(\\-)[A-Za-z]', 'NOT_IN': regular_vocab}}],
    [{'TEXT': {'REGEX': '[0-9](-)[A-Za-z]+'}}, {'TEXT': {'REGEX': '[A-Za-z]+ol'}}],
    [{'IS_DIGIT': True, 'SPACY': False}, {'TEXT': ',', 'SPACY': False}, {'IS_DIGIT': True}, {'TEXT': '-?'}, {'IS_ALPHA': True}, {'TEXT': {'REGEX': compound_endings_regex, 'NOT_IN': regular_vocab}}],
    [{'TEXT': {'REGEX': '[0-9],[0-9]'}}, {'TEXT': '-'}, {'TEXT': {'REGEX': '[A-Za-z]+ol'}}],
    [{'IS_DIGIT': True, 'SPACY': False}, {'TEXT': ',', 'SPACY': False}, {'TEXT': {'REGEX': '[0-9]-?'}}, {'IS_ALPHA': True}, {'TEXT': {'REGEX': compound_endings_regex, 'NOT_IN': regular_vocab}}],
    [{'IS_DIGIT': True, 'SPACY': False}, {'TEXT': '-', 'SPACY': False}, {'IS_ALPHA': True}, {'TEXT': {'REGEX': compound_endings_regex}}],
    [{'LOWER': {'IN': compounds, 'NOT_IN': regular_vocab}}],
    [{'TEXT': {'REGEX': '[A-Za-z]+ic', 'NOT_IN': ['organic']}}, {'TEXT': 'acid'}],
    [{'TEXT': {'IN': fatty_acids, 'NOT_IN': regular_vocab}}, {'LOWER': 'acid'}],
    [{'TEXT': {'IN': ['acetate', 'butyrate', 'valerate']}}],
    [{'IS_DIGIT': True}, {'TEXT': '-'}, {'TEXT': {'IN': compounds, 'NOT_IN': fatty_acids}}],
    #'2', '-', 'amino-3', '-', 'butanone'
    [{'IS_DIGIT': True}, {'TEXT': '-'}, {'TEXT': {'REGEX': compound_endings_regex}}],
    [{'IS_DIGIT': True}, {'TEXT': '-'}, {'TEXT': {'REGEX': '[A-Za-z0-9|(-)]'}}, {'TEXT': {'REGEX': '-?'}}, {'TEXT': {'REGEX': compound_endings_regex}}],
    [{'IS_ALPHA': True, 'TEXT': {'REGEX': compound_endings_regex, 'NOT_IN': regular_vocab}}],
    #d-xxx-d-xxx
    [{'IS_DIGIT': True, 'SPACY': False}, {'TEXT': '-', 'SPACY': False}, {'SHAPE': 'xxx', 'SPACY': False}, {'TEXT': '-', 'SPACY': False}, {'IS_DIGIT': True, 'SPACY': False}, {'SHAPE': 'xxx'}],
    [{'IS_DIGIT': True, 'SPACY': False}, {'TEXT': '-', 'SPACY': False}, {'TEXT': {'REGEX': '[A-Za-z]+-\\d'}, 'SPACY': False}, {'TEXT': '-', 'SPACY': False}, {'SHAPE': 'xxx'}],
    #d,d-xxx-xxx
    [{'TEXT': {'REGEX': '\\d,\\d'}, 'SPACY': False}, {'TEXT': '-', 'SPACY': False}, {'SHAPE': 'xxx', 'SPACY': False}, {'TEXT': '-', 'SPACY': False}, {'SHAPE': 'xxx'}]
]