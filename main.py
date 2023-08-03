from textblob import TextBlob
from textblob import Word
from textblob.wordnet import ADJ
import random
import convo
import user_mod

class ChatBot:

    def __init__(self, name):
        self.name = name
        self.conversation_stack = convo.Conversation()
        self.printResponse("Hello, my name is %s." % name)

        while(True):
            self.communicate()

    def communicate(self):
        text = user_mod.UserInput(raw_input("You: "), self.conversation_stack)
        self.conversation_stack.append(text)
        self.respond()

    def respond(self):
        user_input = self.conversation_stack.get_latest_user_input()
        response = None
        if self.conversation_stack.task_stack:
            task = self.conversation_stack.task_stack[-1]
            response = self.mapTask(task, sentence=user_input.parsed)

        if not response:
            response = self.respond_to_input(user_input)

        self.conversation_stack.append(response)
        self.printResponse(response)

    def respond_to_input(self, sentence):
        response = None

        if not response:
            subject = sentence.subject
            noun = sentence.noun
            if subject:
                if "?" in sentence.sentence:
                    response = "Are you sure I can even answer questions about %s?" % random.choice(subject.pluralize())
                else:
                    if noun:
                        current_noun = random.choice(noun)
                        response = "Listen, I don't want to hear about %s okay?" % current_noun.pluralize()
            else:
                if "?" in sentence.sentence:
                    if self.conversation_stack.user_name:
                        response = "I'm not even sure what you are asking, %s." % self.conversation_stack.user_name
                    else:
                        response = "Dude what are you even saying?"
                else:
                    if self.conversation_stack.task_stack == []:
                        response = self.conversation_stack.learn_user()

            if not response:
                response = self.conversation_stack.talk_about_interests()

            if not response:
                verb = sentence.verb
                noun = sentence.noun
                if verb and noun:
                    current_verb = Word(random.choice(verb))
                    response = "%s a %s you say..?" % (current_verb, random.choice(noun).singularize())
                elif verb:
                    current_verb = Word(random.choice(verb))
                    current_syn = random.choice(current_verb.synsets).lemma_names()
                    if current_syn:
                        response = "%s is sort of like %sing right?" % (current_verb,
                                                                        random.choice(current_syn)
                                                                        )
                elif noun:
                    current_noun = Word(random.choice(noun))
                    if current_noun.synsets:
                        current_syn = random.choice(current_noun.synsets).lemma_names()
                        if current_syn:
                            response = "Tell me more about the %s. Would you say it is similar to a %s?" % (current_noun,
                                                                                                            random.choice(current_syn))
                else:
                    response = "I'll be right back, pizza is here."

        return response

    def printResponse(self, response):
        print "%s: %s" % (self.name, response)

    def mapTask(self, task, **kwargs):
        mapper = [
            {"type": "Name Enquiry", "action": lambda f: self.update_name(kwargs)},
            {"type": "City Enquiry", "action": lambda f: self.set_city(kwargs)}
        ]
        for eachMap in mapper:
            if eachMap['type'] == task['type']:
                return eachMap['action'](kwargs)

    def set_city(self, sentence):
        CITY_WITH_NAME = [
            "{name} grew up in {city}... It all makes sense now",
            "{city}? I recently spoke with someone from there. {name} what is the weather like right now?",
            "Okay {name} from {city}, so I bet you think you're pretty cool huh?"
        ]
        CITY_WITH_NO_NAME = [
            "{city}? I recently spoke with someone from there. What is the weather like right now?",
            "I bet {city} has got some funny looking people.",
            "I was stationed in {city} for three years, its a nice place."
        ]
        CITY_ERROR = [
            "So where did you say you are from again?",
            "Still waiting to hear where you're from...",
            "I'm from California, what about yourself?"
        ]
        sentence = sentence['sentence']
        city_found = False
        response = ""
        for thing in sentence.tags:
            if thing[1] == u'NNP':
                city_found = True
                self.conversation_stack.user_location_city = thing[0]
                if self.conversation_stack.user_name:
                    response = random.choice(CITY_WITH_NAME).format(**{"name": self.conversation_stack.user_name, "city": thing[0].capitalize()})
                else:
                    response = random.choice(CITY_WITH_NO_NAME).format(**{"city": thing[0].capitalize()})
                self.conversation_stack.clear_tasks("City Enquiry")
        if city_found == False:
            response = "%s\n%s: %s" % (self.respond_to_input(self.conversation_stack.get_latest_user_input()),
                                       self.name,
                                       random.choice(CITY_ERROR)
                                       )
        return response

    def update_name(self, input_data):
        greetings_with_name = [
            "Delighted to meet you, {name}.",
            "Interesting, I once knew a {name}.",
            "{name}? That's a unique name..."
        ]
        name_error_messages = [
            "I'm sorry, could you tell me your name again?",
            "I didn't quite catch that... What's your name?",
            "I'm still not sure of your name... Could you say 'My name is %s'?" % self.name
        ]
        input_sentence = input_data['sentence']
        is_name_identified = False
        reply = ""
        for item in input_sentence.tags:
            if item[1] == u'NNP':
                is_name_identified = True
                self.conversation_stack.user_name = item[0]
                reply = random.choice(greetings_with_name).format(**{"name": item[0].capitalize()})
                self.conversation_stack.clear_tasks("Name Enquiry")
        if not is_name_identified:
            reply = "%s\n%s: %s" % (self.respond_to_input(self.conversation_stack.get_latest_user_input()),
                                    self.name,
                                    random.choice(name_error_messages)
                                    )
        return reply

c = ChatBot("Bob")