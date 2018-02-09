from textblob import TextBlob
from textblob import Word
from textblob.wordnet import ADJ
import random
import user_mod


class Conversation:

    def __init__(self):
        self.stack = []
        self.task_stack = []
        self.interesting_stack = []

        self.user_name = None
        self.user_location_city = None

    def talk_about_interests(self):
        INTERESTING_SENTENCE = [
            "You mentioned {word}, is that something you usually do?",
            "So I knew a guy that used to do a lot of {word}, what are your thoughts on that?",
            "People who go {word} are just the worst you know?",
            "I absolutely hate when people talk about {word}."
        ]
        INTERESTING_SENTENCE_WITH_LOC = [
            "Do they do a lot of {word} in {location}?",
            "I'm willing to bet that {location} has a lot of people who like {word}",
            "There is something odd about people in {location} and {word}..."
        ]
        response = None
        interesting_word = self.get_interesting_word()
        if interesting_word:
            if self.user_location_city:
                if random.choice([True,True,False]):
                    response = random.choice(INTERESTING_SENTENCE_WITH_LOC).format(**{"word": interesting_word, "location": self.user_location_city})
            if not response:
                response = random.choice(INTERESTING_SENTENCE).format(**{"word": interesting_word})
        return response

    def get_interesting_word(self):
        if self.interesting_stack:
            interesting_word = random.choice(self.interesting_stack)
            self.interesting_stack.remove(interesting_word)
            return interesting_word
        else:
            return None

    def learn_user(self):
        # find what we don't know first
        unknown_user_values = self.unknown_user_values()
        unknown_val = None
        if unknown_user_values:
            unknown_val = random.choice(unknown_user_values)

        if unknown_val == "user_name":
            self.task_stack.append({'type': "Name Enquiry", 'sender': "bot"})
            return "What is your name?"

        if unknown_val == "user_location_city":
            self.task_stack.append({'type': "City Enquiry", 'sender': "bot"})
            if self.user_name:
                return "So %s where are you from?" % self.user_name
            else:
                return "Sooo where are you from anyways?"

        return None

    def unknown_user_values(self):
        unknown_stack = []
        if not self.user_name:
            unknown_stack.append("user_name")
        if not self.user_location_city:
            unknown_stack.append("user_location_city")

        return unknown_stack

    def clear_tasks(self, type):
        for each_task in self.task_stack:
            if each_task['type'] == type:
                self.task_stack.remove(each_task)

    def get_all_user_input(self):
        return_stack = []
        for each in self.stack:
            if isinstance(each, user_mod.UserInput):
                return_stack.append(each)
        return return_stack

    def get_latest_user_input(self):
        temp_stack = self.stack
        for item in temp_stack[::-1]:
            if isinstance(item, user_mod.UserInput):
                return item

        return None

    def append(self, item):
        self.stack.append(item)