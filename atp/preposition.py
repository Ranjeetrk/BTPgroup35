

import nltk
from nltk.corpus import wordnet as wn
from textblob import TextBlob
import re
sentence = """Automation Testing is used to re-run the test scenarios that were performed manually, quickly, and repeatedly."""
# sentence = """He traveled seventy miles in two hours"""
#tags = nltk.pos_tag(sentence)
#tag_map = {word.lower(): tag for word, tag in tags}

noun_phrases = list()
#grammar1 = r""" CHUNK: {<NN.*|JJ>*<NN.*>} """
grammar1 =r""" CHUNK: {<IN.*|>*<IN.*>} """
#grammar1 =r""" CHUNK: {<VB.*|>*<VB.*>} """)
chunker = nltk.RegexpParser(grammar1)
#tokens = nltk.word_tokenize(sentence)
tokens = nltk.word_tokenize(sentence)

#print(tokens)
pos_tokens = nltk.tag.pos_tag(tokens)
print("pos_tokens ",pos_tokens)
tags = nltk.tag.pos_tag(tokens)
tree = chunker.parse(pos_tokens)
# print("Tree: ",tree)
# print(tags)
# print(tags[0][0])

# select phrase
for subtree in tree.subtrees():
    if subtree.label() == "CHUNK":
        temp = ""
        for sub in subtree:
            temp += sub[0]
            temp += " "
        temp = temp.strip() # strip extra whitespace
        noun_phrases.append(temp)

print("noun_prase",noun_phrases)
flag=0
# replace nouns

print(tags)
replace_nouns = []
for word, tag in tags:
    # print('\n',word ,tag)
    for phrase in noun_phrases:
        # print(phrase)
        # if phrase[0] == :
        #     break
        if word in phrase:
            if phrase==tags[0][0]:
                continue
            flag=1
            # Blank out the last two words in this phrase
            [replace_nouns.append(phrase_word) for phrase_word in phrase.split()[-2:]]
            break
    # If we couldn't find the word in any phrases,
    # replace it on its own
    # if len(replace_nouns) == 0:
    #     replace_nouns.append(word)
    # break
    if flag==1:
        break
val = 99
for i in replace_nouns:
    if len(i) < val:
        val = len(i)  

trivia = {
    "Answer": " ".join(replace_nouns),
    "Answer_key": val
}

# if len(replace_nouns) == 1:
#     # If we're only replacing one word, use WordNet to find similar words
#     trivia["similar_words"] = get_similar_words(replace_nouns[0])
# else:
#     # If we're replacing a phrase, don't bother - it's too unlikely to make sense
#     trivia["similar_words"] = []

# Blank out our replace words (only the first occurrence of the word in the sentence)
replace_phrase = " ".join(replace_nouns)
blanks_phrase = ("____" * len(replace_nouns)).strip()

expression = re.compile(re.escape(replace_phrase), re.IGNORECASE)
sentence = expression.sub(blanks_phrase, str(sentence), count=1)
trivia["Question"] = sentence
print(trivia)