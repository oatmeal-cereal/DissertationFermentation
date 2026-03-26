from pybtex.database import BibliographyData, Entry

bib_data = BibliographyData({
    'articlename': Entry('article', [
        ('author', 'L[eslie] B. Lamport'),
        ('title', 'The Gnats and Gnus Document Preparation System'),
        ('journal', "G-Animal's Journal"),
        ('year', '1986'),
    ]),
})

bib_data.to_file('bibli.bib')