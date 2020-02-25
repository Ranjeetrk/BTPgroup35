 

from nltk.corpus import wordnet as wn
from textblob import TextBlob
import re
import nltk

class Article:
    def __init__(self, title):
        self.title = title
        with open(title, mode="r") as fp:
            self.summary = fp.read()

    def generate_trivia_sentences(self):
        sentences = nltk.sent_tokenize(self.summary)
        trivia_sentences = list()
        for sentence in sentences:
            trivia = self.evaluate_sentence(sentence)
            if trivia:
                if len(trivia["Answer"])>0:
                    trivia_sentences.append(trivia)
        return trivia_sentences


    def get_similar_words(self, word):
        # In the absence of a better method, take the first synset
        synsets = wn.synsets(word, pos="n")

        # If there aren't any synsets, return an empty list
        if len(synsets) == 0:
            return []
        else:
            synset = synsets[0]

        # Get the hypernym for this synset (again, take the first)
        hypernym = synset.hypernyms()[0]

        # Get some hyponyms from this hypernym
        hyponyms = hypernym.hyponyms()

        # Take the name of the first lemma for the first 8 hyponyms
        similar_words = []
        for hyponym in hyponyms:
            similar_word = hyponym.lemmas()[0].name().replace("_", " ")
            if similar_word != word:
                similar_words.append(similar_word)
            if len(similar_words) == 8:
                break
        return similar_words


    def evaluate_sentence(self, sentence):
        # print("sentence",sentence)
        tags = nltk.pos_tag(sentence)
        # print("tags",tags)
        tag_map = {word.lower(): tag for word, tag in tags}

        noun_phrases = list()
        grammar1 =r""" CHUNK: {<IN.*>*<IN.*>} """
        chunker = nltk.RegexpParser(grammar1)
        tokens = nltk.word_tokenize(sentence)
        # print(tokens)
        pos_tokens = nltk.tag.pos_tag(tokens)
        # print("pos_tag ",pos_tokens)
        tree = chunker.parse(pos_tokens)
        # print("Tree: ",tree)

        # select phrase
        for subtree in tree.subtrees():
            if subtree.label() == "CHUNK":
                temp = ""
                for sub in subtree:
                    temp += sub[0]
                    temp += " "
                temp = temp.strip() # strip extra whitespace
                noun_phrases.append(temp)

        # print(noun_phrases)
        flag=0
        # replace nouns
        replace_nouns = []
        for word, tag in tags:
            # print('\n',word ,tag)
            for phrase in noun_phrases:
                # print(phrase)
                # if phrase[0] == :
                #     break
                if word in phrase:
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
            "Anser_key": val
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
        return trivia
