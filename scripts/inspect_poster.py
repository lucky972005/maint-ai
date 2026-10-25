import re
import os

with open(r'c:\dev\pro\MaintAI_Poster_A2_Portrait.html', 'r', encoding='utf-8') as f:
    text = f.read()

headers = re.findall(r'sec-header">([^<]+)<', text)
print('Headers in Portrait:', headers)

captions = re.findall(r'diag-caption">([^<]+)<', text)
print('\nCaptions in Portrait:')
for c in captions:
    print(' -', c)

with open(r'c:\dev\pro\MaintAI_Poster_A2_Landscape.html', 'r', encoding='utf-8') as f:
    l_text = f.read()

l_headers = re.findall(r'sec-header">([^<]+)<', l_text)
print('\nHeaders in Landscape:', l_headers)
