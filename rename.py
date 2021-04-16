import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
import re

get_word         = lambda s:" ".join((re.findall(r'\w+', s)))
get_lower_word   = lambda s:" ".join((re.findall(r'\w+', s))).lower()
get_letter       = lambda s: "".join((re.findall(r'\w+', s)))
get_lower_letter = lambda s: "".join((re.findall(r'\w+', s))).lower()

pd.options.display.max_colwidth = 200


soup = BeautifulSoup(open('oral.html'),'lxml')
#soup = BeautifulSoup(open('spotlight.html'),'lxml')
#soup = BeautifulSoup(open('poster.html'),'lxml')

note_list = soup.find_all(class_='note')

paper_list = []
for note in note_list:
    url   = note.h4.a['href']
    title = note.h4.a.text
    title = title.strip()
    paper_list.append([url, title])

#print(paper_list)

paper_df = pd.DataFrame(paper_list)

#print(paper_df)

for filename in Path('../.').glob('pdf?id=*'):
    paper_id = filename.name[7:]
    paper_name = paper_df.loc[(paper_df[0] == 'https://openreview.net/forum?id=' + paper_id)][1]
    if len(paper_name) == 0:
       continue
    new_name = get_word(paper_name.to_string(index=False))+'.pdf'
    print(new_name)
    filename.rename(filename.with_name(new_name))
