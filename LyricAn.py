import os
import json
import pandas as pd
import random

def cleaner():
    artist = "MyChemicalRomance"
    os.chdir(r"C:\Users\Administrator\source\repos\LyricGen\PythonApplication1\Songs")
    with open('Lyrics_MyChemicalRomance.json') as json_data:
        data = json.load(json_data)
    f = open("lyrics.txt", "w")
    f.close()
    lines = list()
    i = 0
    for song in data['songs']:
        f = open("lyrics.txt", "a", encoding = 'utf-8')
        f.write(song['lyrics'])
        i+=1
        f.close()
    f = open("lyrics.txt", "r", encoding = 'utf-8')
    lines = f.readlines()
    f.close()
    clean = list()
    for line in lines:
        if '[' in line:
            line = line[line.find(']')+1:]
        if '"' in line:
            lines.remove(line)
        else:
            clean.append(line.rstrip().lower())
    f = open("lyrics.txt", "w", encoding = 'utf-8')
    for line in clean:
        if line != '\n':
            f.write(line + "\n")
    f.close()
    return clean

def model(clean):
    words = dict()
    cache = False
    """
    for line in clean:
        for word in line.split():
            if word.lower() not in words:
                words[word.lower()] = 1
            else:
                words[word.lower()] += 1
    """
    for line in clean:
        for word in line.split():
            if word in words:
                words[word][0] += 1
            else:
                words[word] = [1, dict()]
            if cache:
                if word in words[cache][1]:
                    words[cache][1][word] += 1
                else:
                    words[cache][1][word] = 1
            cache = word
        cache = False
    worddata = list(words.keys())
    freqdata = list(words.values())
    for freq in freqdata:
        for value in freq[1].keys():
            freq[1][value] = freq[1][value] / freq[0]
    df = pd.DataFrame(freqdata, index = worddata)
    df.columns = ['freq', 'next']        
    return df

def nextword(word, worddict):
    r = random.uniform(0, 1)
    s = 0.0
    if worddict.loc[word]['next'].keys():
        for choice in worddict.loc[word]['next'].keys():
            prob = worddict.loc[word]['next'][choice]
            s += prob
            if r < s:
                return choice
        return choice
    else:
        return str('.')

def gensent(start, worddict):
    line = start
    it = 0
    while(1):
        nxt = nextword(start, worddict)
        line += ' ' + nxt
        it += 1
        if nxt != ('.') and it < 10:
            start = nxt
        else:
            break
    print(line)
        
def main():
    clean = cleaner()
    words = model(clean)
    sentence = gensent('i', words)
    #probs = prob(words)
    #gendf(probs)
if __name__ == "__main__":
    main()
