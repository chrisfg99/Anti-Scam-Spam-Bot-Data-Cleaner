#Candidate Number 184521
#University of Sussex

# file for the Pre-Processor Class
import heapq

from nltk.corpus import (stopwords,wordnet as wn)
from nltk.stem import WordNetLemmatizer
import re
import csv
import pandas as pd


class PreProcessor:

    # initialise pre processor class
    def __init__(self):
        self.tags = "abbr | area |w-auto | base | bdo | blockquote | br | button | caption | cite | code | col | colgroup | dd | del | dfn | div | dl | DOCTYPE | dt | em | fieldset | form | h1 | h2 | h3 | h4 | h5 | h6 | head | html | hr | i | img | input | ins | kbd | label | legend |-left | li | link | map | meta | noscript | object | ol | optgroup | option | p | px | param | pre | q | samp | script | select | small | span | strong | style | sub | sup |-right | table | tbody | td | textarea | tfoot | th  |  thead  |  title | tr | tt | ul | var"

    def clean(self):
        paths=0
        index,indexes=[],[]
        while paths<3:
            messages=[]
            if(paths==0):
                print("spam")
                dataset_reader,path = csv.reader(open('spam_ham_dataset.csv', 'rU')),'spam_ham_dataset_vector.csv'
            elif(paths==1):
                print("fraud")
                dataset_reader,path = csv.reader(open('fraud_email_.csv', 'rU')),'fraud_email_vector.csv'
            elif(paths==2):
                print("processed")
                dataset_reader,path = csv.reader(open('processedEmails.csv', 'rU',encoding="utf8")),'processedEmails_vector.csv '
            else:
                print("ques")
                dataset_reader,path = csv.reader(open('questionaireScam.csv', 'rU')),'questionaireScam_vector.csv'
            i=0
            for line in dataset_reader:
                try:
                    i=i+1
                    messages.append([line[1], line[5]])
                except:
                    print("UnicodeDecodeError")
            stageTwo = self.removeHTML(messages)
            stageThree = self.tokenise(stageTwo)
            stageFour = self.removeStop(stageThree)
            stageFive = self.removeSymbols(stageFour)
            stageSix=self.lemmatize(stageFive)
            stageSeven=self.getFrequencies(stageSix)
            cleanTxt = self.getNouns(stageSeven)

            vectors,index=self.getWordVectors(cleanTxt,index,paths)
            indexes.append(index)
            self.write(cleanTxt, vectors, indexes,path)
            paths = paths + 1

    # function to remove all HTML
    def removeHTML(self, messages):
        for i in range(len(messages)):
            cleaned_part = re.sub("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|(?P<url>https?://[^\s]+)","",str(messages[i][0]))
            cleaned_part = re.sub(self.tags, "", str(cleaned_part))
            messages[i] = [cleaned_part, messages[i][1]]
        return messages

    # function to tokenise words in Subject and Body
    def tokenise(self, messages):
        new_messages=[]
        for i in range(len(messages)):
            tokens = messages[i][0].split()
            new_messages.append([tokens, messages[i][1]])
        return new_messages

    # function to remove any stop words in the text
    def removeStop(self, messages):
        new_messages = []
        stop_words = set(stopwords.words('english'))
        for i in range(len(messages)):
            filtered = []
            for word in messages[i][0]:
                if word[0] not in stop_words:
                    word = re.sub(r"[^\x00-\x7F]+|\\n|\\.*?\\x*?|\\\.*?\\\n|\\.*?\\n|\\t| n", " ", str(word))
                    if word != "":
                        filtered.append(word)
            new_messages.append([filtered, messages[i][1]])
        return new_messages

    def removeSymbols(self, messages):
        new_messages = []
        for i in range(len(messages)):
            filtered = []
            for word in messages[i][0]:
                word = re.sub(r"[\\~#%&*{}/:<>?|\"-.]|'n'| |-|", "", str(word))
                if word != '' or word != "n" or word is not None:
                    filtered.append(word)
            new_messages.append([filtered,messages[i][1]])
        return new_messages

    def lemmatize(self,messages):
        new_messages = []
        for i in range(len(messages)):
            lemmatized = []
            for word in messages[i][0]:
                lemmatized.append(WordNetLemmatizer.lemmatize(self,word=word))
            new_messages.append([lemmatized,messages[i][1]])
        return messages


    def getFrequencies(self,messages):
        new_messages=[]
        for i in range(len(messages)):
            frequency_dictionary = {}
            for word in messages[i][0]:
                if(word.isnumeric()==True):
                    frequency_dictionary['Number'] = messages[i][0].count(word)
                else:
                    frequency_dictionary[word] = messages[i][0].count(word)
            new_messages.append([frequency_dictionary,messages[i][1]])
        return new_messages

    def getNouns(self,messages):
        new_messages=[]
        for i in range(len(messages)):
            noun_dictionary = {}
            for word in messages[i][0]:
                pos_l = set()
                for tmp in wn.synsets(word):
                    if tmp.name().split('.')[0] == word:
                        pos_l.add(tmp.pos())
                #if(pos_l.__contains__('n') or pos_l.__contains__('v')  or pos_l.__contains__('a')  or pos_l.__contains__('r') ):
                if (pos_l=={'n'} or pos_l=={'v'} or pos_l=={'a'} or pos_l=={'n','v'}):
                #if (pos_l.__contains__('n') and len(word)>=2):
                #if (pos_l!=set()):
                    noun_dictionary[word] = messages[i][0][word]
            #if (len(noun_dictionary)>=2):
            new_messages.append([noun_dictionary, [], [], [], messages[i][1],messages[i][0]])
        return new_messages

    def getWordVectors(self, messages,index,paths):
        #get freq matrix
        freq={}
        for i in range(len(messages)):
            dict =messages[i][0]
            for w in dict.keys():
                if w not in freq.keys():
                    freq[w]=dict[w]
                else:
                    freq[w]+=dict[w]
        if(paths==0 or paths==2):
            index= heapq.nlargest(1000, freq, key=freq.get)
        #get vectors
        vectors=[]
        for i in range(len(messages)):
            vec,dict=[],messages[i][0]
            for word in index:
                if word in dict.keys():
                    vec.append(1)
                else:
                    vec.append(0)
            vectors.append(vec)
        return vectors,index

    def write(self,txt,vectors,index,path):
        #path = 'fraud_email_cleaned.csv'
        #path = 'spam_ham_dataset_cleaned.csv'
        #path = 'processedEmails_cleaned.csv'
        #path = 'questionaireScam_cleaned.csv'
        #df = pd.DataFrame(txt)
        #headers = ['Subject Freq', 'Email Address', 'Email Body', 'Links', 'Tag','Subject Cleaned']
        #df.columns = headers
        #df.to_csv(path)

        df = pd.DataFrame(vectors)
        df.to_csv(path)

        path = 'index.csv'
        df = pd.DataFrame(index)
        df.to_csv(path)

p = PreProcessor()
p.clean()