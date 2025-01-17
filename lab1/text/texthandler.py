class Reader:
    sentenceTerminators = ['.', '!', '?']
    wordSeparators = [',', '-', ':', ';', '(', ')', '\'', '"', '...', ' ', '\n']
    wordSeparators.extend(sentenceTerminators)
    innerWordNonBreakingPunct = ['-', '\'']
    paragraphSeparators = ['\n\n']
    buffSize = 64

    def __init__(self, fileHandle):
        """Each reader should be initialized with a unique file handle"""
        self.fileHandle = fileHandle
        self.buff = ''
        self.eof = False
        self.iterType = None

    def __iter__(self):
        return self

    def __next__(self):
        raise Exception("__next__ is not implemented in Reader")

    def readAll(self):
        return [] if self.eof and len(self.buff) == 0 else list(self)

    def readMore(self):
        if not self.eof:
            buff = self.fileHandle.read(self.buffSize)
            if len(buff) == 0:
                self.eof = True
            self.buff += buff

class ParagraphReader(Reader):
    def __init__(self, *args):
        super(ParagraphReader, self).__init__(*args)
        self.paragraphs = 0

    def __next__(self):
        if self.eof and len(self.buff) == 0:
            raise StopIteration()
        paragraph = None
        while paragraph is None:
            self.readMore()
            sep = None
            index = -1
            for s in self.paragraphSeparators:
                idx = self.buff.find(s)
                if idx != -1 and (index == -1 or idx < index):
                    index = idx
                    sep = s
            if index != -1:
                endIndex = index + len(sep)
                paragraph = self.buff[:index]
                self.buff = self.buff[endIndex:]
            elif self.eof:
                paragraph = self.buff
                self.buff = ''
        self.paragraphs += 1
        return paragraph

    def countParagraphs(self):
        return self.paragraphs

class SentenceReader(Reader):
    def __init__(self, *args):
        super(SentenceReader, self).__init__(*args)
        self.sentences = 0

    def __next__(self):
        if self.eof and len(self.buff) == 0:
            raise StopIteration()
        sentence = None
        while sentence is None:
            self.readMore()
            sep = None
            index = -1
            for s in self.sentenceTerminators:
                idx = self.buff.find(s)
                if idx != -1 and (index == -1 or idx < index):
                    index = idx
                    sep = s
            if index != -1:
                endIndex = index + len(sep)
                sentence = self.buff[:endIndex]
                self.buff = self.buff[endIndex:]
            elif self.eof:
                sentence = self.buff
                self.buff = ''
        self.sentences += 1
        return sentence.lstrip()

    def countSentences(self):
        return self.sentences

class WordReader(Reader):
    def __init__(self, *args):
        super(WordReader, self).__init__(*args)
        self.wordMap = {}

    def __next__(self):
        if self.eof and len(self.buff) == 0:
            raise StopIteration()
        word = None
        while word is None:
            # TODO this should probably only be called if nothing is found
            # (in each of the reader classes)
            self.readMore()
            sep = None
            index = -1
            for s in self.wordSeparators:
                idx = self.buff.find(s)
                if idx != -1 and (index == -1 or idx < index):
                    if s in self.innerWordNonBreakingPunct:
                        # "sup chief-man"
                        #           ^
                        self.readMore()
                        if len(self.buff) > idx + 1:
                            if self.buff[idx+1] == ' ':
                                s += ' '
                            elif idx == 0:
                                self.buff = self.buff[1:]
                                return self.__next__()
                            else:
                                continue
                    index = idx
                    sep = s
            if index != -1:
                endIndex = index + len(sep)
                word = self.buff[:index]
                self.buff = self.buff[endIndex:]
            elif self.eof:
                word = self.buff
                self.buff = ''

        word = word.strip()
        if word == '':
            return self.__next__()
        else:
            val = self.wordMap.get(word, 0)
            self.wordMap[word] = val + 1
            return word

    def uniqWords(self):
        return list(self.wordMap.keys())

    def freqWordsMap(self):
        return self.wordMap.copy()

    def countWords(self):
        return sum(list(self.wordMap.values()))

    def countUniqWords(self):
        return len(self.uniqWords())

    def mostFreqWords(self):
        maxFreq = max(self.wordMap.values())
        return self.wordsWithFreq(maxFreq)

    def wordsWithFreq(self, freq):
        return [w for w,f in self.wordMap.items() if f == freq]

    def wordsWithGreaterFreq(self, freq):
        return [w for w,f in self.wordMap.items() if f > freq]

    def wordFound(self, word):
        return word in self.wordMap
