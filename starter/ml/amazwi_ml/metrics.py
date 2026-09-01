from __future__ import annotations
import re,unicodedata
class InvalidReference(ValueError): pass
def normalise_transcript(text:str)->str:return " ".join(re.sub(r"[^\w\s]"," ",unicodedata.normalize("NFC",text).casefold()).split())
def _distance(a,b):
    d=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        nd=[i]
        for j,y in enumerate(b,1):nd.append(min(d[j]+1,nd[-1]+1,d[j-1]+(x!=y)))
        d=nd
    return d[-1]
def word_error_rate(reference:str,hypothesis:str)->float:
    r=normalise_transcript(reference).split();h=normalise_transcript(hypothesis).split()
    if not r:return 0.0 if not h else (_ for _ in ()).throw(InvalidReference("non-empty hypothesis with empty reference"))
    return _distance(r,h)/len(r)
def character_error_rate(reference:str,hypothesis:str)->float:
    r=normalise_transcript(reference).replace(" ","");h=normalise_transcript(hypothesis).replace(" ","")
    if not r:return 0.0 if not h else (_ for _ in ()).throw(InvalidReference("non-empty hypothesis with empty reference"))
    return _distance(r,h)/len(r)
