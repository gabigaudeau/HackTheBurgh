
import nltk
import pronouncing
import re
import random


#takes sample_text, finds last words of each sentence in document, returns list of all last words
def find_last_word(sample_text):
    # dictionary with all CMU tokens, all tokens
    all_words={}
    # split each line into its sentences, each sentence into its word token
    split_sentences = re.split('\n|\.', sample_text)


    # for each sentence: find last token
    for sentence in split_sentences:
        #print("sentence",sentence)
        if sentence.replace(' ','').isalpha():

            last_word = find_last_token(sentence)

            all_words.update(((last_word, sentence),))

        #if sentence == "" or sentence == " " or sentence == "." or sentence == "," or sentence=="\n":

        else:
            pass

    return  all_words

def find_last_token(sentence):
    #split sentence into words
    tokenized_words = nltk.word_tokenize(sentence)
    #remove all tokens which are punctuation
    for token in tokenized_words:
        if token == '.' or token == ',':
            tokenized_words.remove(token)

    #specificy last token
    last_token = tokenized_words[-1]
    return last_token

#make dictionary with each word as key and its CMU token as value
def make_CMU_dict(all_words):
    all_CMU_tokens = {}
    for word in all_words:
        if word=="":
            pass
        else:
            #convert each word to CMU phonetics token
            CMU_token= pronouncing.phones_for_word(word)
            #adds last token and CMU of token to dictionary
            all_CMU_tokens.update(((word, CMU_token),))


    all_CMU_tokens = { k:v for k,v in all_CMU_tokens.items() if v != [] }
    print("all")
    print(all_CMU_tokens)
    for k,v in all_CMU_tokens.items():
        all_CMU_tokens[k]= tuple(v[0].split())
    return all_CMU_tokens

def prep_database(filepath): #takes filepath as a string
    # open file with all roasts
    f = open(filepath, 'r')
    sample_text = f.read()
    f.close()

    # making dictionary of all last words + their sentence in roasts-file (key:last words, value: sentence the last word belonged to)
    all_last_words = find_last_word(sample_text)
    #print("last")
    #print(all_last_words)
    # dictionary containing all CMU tokens
    cmu_dict = make_CMU_dict(all_last_words)
    print("cpm")
    print(cmu_dict)


    return cmu_dict

def prep_database2(filepath): #takes filepath as a string
    # open file with all roasts
    f = open(filepath, 'r')
    sample_text = f.read()
    f.close()

    # making dictionary of all last words + their sentence in roasts-file (key:last words, value: sentence the last word belonged to)
    all_last_words = find_last_word(sample_text)
    return all_last_words

def parse_dict(filepath):
    pho_dict = dict()

    with open(filepath) as fileA:
        for line in fileA:
            words = line.split()  # splits the line on any whitespace
            pho_dict[words[0]] = tuple(words[1:])
    return pho_dict

#cmu_dict= prep_database('./trainingSet/formatedRoasts/roastDatabase.txt')
cmu_dict= {}
#pho_dict=parse_dict('./python-rhyme-master/phodict.txt')
pho_dict= {}

STRESSES = {'AA1', 'AE1', 'AH1', 'AO1', 'AW1', 'AY1', 'EH1', 'ER1', 'EY1', 'IH1', 'IY1', 'OW1', 'OY1', 'UH1', 'UW1'}
#returns whether or not word1 and word2 rhyme#
def is_rhyme(wordA, wordB,dict):
    # set of all stressed vowel sounds
    soundsA, soundsB = dict[wordA], dict[wordB]
    if isSubList(soundsA, soundsB):
        # makes sure rhyming words are not contained within each other
        return False


    for index,sound in enumerate(reversed(soundsA)):
        if sound in STRESSES:
            break
    return soundsA[-index-1:] == soundsB[-index-1:]




#returns whether or not one list contains the other
def isSubList(listA, listB):
    if len(listA) < len(listB):
        return isSubList(listB, listA)
    n = len(listB)
    for start in range(len(listA)-n+1):
        if all(listA[start+i] == listB[i] for i in range(n)):
            return True
    return False



def syllable_count(word):
    #returns the number of syllables in word
    sounds = pho_dict[word.upper()]
    return sum(int(sound[0] in "AEIOU") for sound in sounds)

def makeSyllableMap():

    """returns a dictionary where a key is a number of syllables and its value
    is the set of all words with that many syllables"""

    dictA = {i: set() for i in range(0, 30)}
    for word in pho_dict.keys():
        dictA[syllable_count(word)].add(word)
    return dictA

SYLDICT = ()

def getRhymes(word):
    "yields all words that rhyme with word"
    sounds = pho_dict[word]
    for index, sound in enumerate(reversed(sounds)):
        if sound in STRESSES:
            ending = sounds[-index - 1:]
            break

    yielded = set()
    for wordB, soundsB in pho_dict.items():
        if (ending == soundsB[-index - 1:]) and (soundsB not in yielded) and (not isSubList(sounds, soundsB)):
            yielded.add(soundsB)
            yield wordB

def findWord(n):
    "returns a random n syllable word"
    return random.sample(SYLDICT[n], 1)[0]

def replace_with_rhyme(roast):

    roast_words=roast.split()
    tagged_words = nltk.pos_tag(roast_words)
    index = 0
    for (word,tag) in tagged_words:
        # if tag is noun
        if tag in ['NN','NNS','NNP','JJ',"RB"]:
            #find syllable length
            length=syllable_count(word)
            #if not last word...
            if word != roast_words[-1]:

                # find random other word with same syllable length
                replace2 = findWord(length)

                # replace word with random other word
                roast_words[index] = replace2.lower()


            #if last word...
            if word == roast_words[-1]:
                # replace with rhyming word of same syllable length
                r1 = tuple(getRhymes(word.upper()))
                if r1 is not ():
                    replace1 = random.choice(r1)
                    roast_words[index] = replace1.lower()


        index += 1
        string_roast_words = " ".join(roast_words)
    return string_roast_words





def roast_me_poem(roast, roast_path):
    # make dictionary from which to make poem
    my_roast_poem = {}
    final_poem_string=''
    #make dictionary for all last roast words in roasts + corresponding sentence
    last_roast_words = find_last_word(roast)

    all_last_roast_words=prep_database2(roast_path)

    # loop through every last roast word--> find if it rhymes with any other word in corpus
    for key1,value1 in last_roast_words.items():
        for key2,value2 in cmu_dict.items():

            # if they rhyme, add value of word1 and value of word2 to my_roast_poem
            if (key1 in cmu_dict and key2 in cmu_dict):
                if is_rhyme(key1, key2,cmu_dict) == True:

                    my_roast_poem.update(((value1, all_last_roast_words[key2]),))
                else:
                    pass
            else:
                rhyme = replace_with_rhyme(value1)

                my_roast_poem.update(((value1, rhyme),))


        if value1 not in my_roast_poem.keys():

            rhyme = replace_with_rhyme(value1)

            my_roast_poem.update(((value1, rhyme),))

    for key,value in my_roast_poem.items():
        final_poem_string+= str(key)+'.' +'\n' +str(value)+'.'+'\n'


    print(final_poem_string)
    return final_poem_string

#API
def main(text, roast_path, phodict_path):
    global SYLDICT
    global cmu_dict
    global pho_dict
    cmu_dict = prep_database(roast_path)
    pho_dict = parse_dict(phodict_path)
    SYLDICT = makeSyllableMap()
    roast_me_poem(text, roast_path)

main("wipe your lip after rimming",'./trainingSet/formatedRoasts/roastDatabase.txt',
     './python-rhyme-master/phodict.txt')