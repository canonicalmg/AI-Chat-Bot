from textblob import TextBlob
from textblob import Word
from textblob.wordnet import ADJ
import random

class UserInput:

    def __init__(self, sentence, conversation_stack):
        self.sentence = sentence
        self.conversation_stack = conversation_stack

        self.parsed = TextBlob(sentence)
        self.check_for_interesting_info()

        self.pronoun = self.get_or_create_pronoun()
        self.noun = self.get_or_create_noun()
        self.adjective = self.get_or_create_adjective()
        self.verb = self.get_or_create_verb()
        self.subject = self.get_or_create_subject()

    def check_for_interesting_info(self):
        """
        This function checks for interesting information in the parsed data.
        It iterates over the pos_tags of the parsed data and if the part of speech is 'VBG', 
        it appends the word to the interesting_stack of the conversation_stack.
        """
        for word, part_of_speech in self.parsed.pos_tags:
            # Loop through each word and its part of speech in the parsed data
            if part_of_speech in ["VBG"]:
                # If the part of speech is 'VBG' (gerund or present participle), consider it as interesting
                self.conversation_stack.interesting_stack.append(word)
                # Append the interesting word to the conversation stack

    def get_or_create_pronoun(self):
        try:
            return self.pronoun
        except AttributeError:
            pronouns = []
            for word, part_of_speech in self.parsed.pos_tags:
                if part_of_speech in ["PRP", "PRP$", "WP", "WP$"]:
                    pronouns.append(word)

            return pronouns

    def get_or_create_noun(self):
        try:
            return self.noun
        except AttributeError:
            nouns = []
            for word, part_of_speech in self.parsed.pos_tags:
                if part_of_speech == "NN":
                    nouns.append(word)

            return nouns

    def get_or_create_adjective(self):
        try:
            return self.adjective
        except AttributeError:
            adjectives = []
            for word, part_of_speech in self.parsed.pos_tags:
                if part_of_speech == "JJ":
                    adjectives.append(word)

            return adjectives

    def get_or_create_verb(self):
        try:
            return self.verb
        except AttributeError:
            blacklist = ["is", "yeah"]
            verbs = []
            for word, part_of_speech in self.parsed.pos_tags:
                if part_of_speech in ["VB", "VBZ", "VBP", "VBD", "VBN", "VBG"]:
                    if word not in blacklist:
                        verbs.append(word)

            return verbs

    def get_or_create_subject(self):
        try:
            return self.subject
        except AttributeError:
            subject = self.parsed.noun_phrases
            return subject