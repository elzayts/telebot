import re
import random


class TemplateEngine:

    def __init__(self, templates, questions):
        self.templates = templates
        self.default_answers = [answer for (template, answer) in templates if template == '*']
        self.questions=questions

    def process_question(self, question):
        """
        Process user question and find the right answer for it
        :param question: string with a question
        :return: string with an answer
        """
        # lower case the question
        question = question.lower()
        # list with sentences that could be used as answers
        answers = []
        # check each template
        for (template, answer) in self.templates:
            result = self.parse_template(template, question, answer)
            if result is not None:
                answers.append(result)
        
        if not answers:
            answers.extend(["Let's talk about something else", "Better tell me more about yourself", "Didn't quite get what you mean here"])

        # filter out answers for raw '*' operator if there are more matched answers than just default ones
        if len(answers) > len(self.default_answers):
            answers = [answer for answer in answers if answer not in self.default_answers]

        # return random answer
        # print(answers)
        return answers[random.randint(0, len(answers)-1)]

    def parse_template(self, template, question, answer):
        """
        Parse template and question to find if the template answer could be used as answer for user's question
        :param template: string template
        :param question: string user's question
        :param answer: string template answer
        :return: string processed answer if it could be used as answer for user's question or None if not
        """

        # if template contains '*' operator
        if template.find("*") != -1:
            template = template.replace("*", "")

            # template is empty
            if not template:
                return answer
            # if template contains only one char along with '*', and both answer and question has this char
            if len(template) == 1 and question.find(template) != -1 and answer.find(template) != -1:
                return answer

        # if template contains '<c>' operator
        if template.find("<c>") != -1:
            template = template.replace("<c>", "")
            # rf"((?:{template}\s))(\w+)
            # create regex to find the word that is in the question under the '<c>' operator
            pattern = re.compile(rf"((?:{template}\s))(\w+)")
            match = pattern.search(question)
            # question doesn't contain the template pattern - this template can't be used with this question
            if match is None:
                return None
            # get only matched word from the question string
            match = match.group(0).replace(template, "").strip()
            # replace '<c>' in the template answer with matched word
            return answer.replace("<c>", match)

        return answer if question.find(template) != -1 else None