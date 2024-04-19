from openai import *

API_KEY = open("ai.env", "r").read().strip()
client = OpenAI(api_key = API_KEY)

def get_ai_questions(search_topic, level):
    prompt_query = (
        f"I Would like to generate a set of 15 questions on the topic of {search_topic} that most would quantify as an {level} question.\n"
        f"Also generate 4 possible multiple choice answers with 1 of them being the correct answer.\n"
        f"Randomize the position of the correct answer.\n"
        f"Provide your response for each generated question in this format: ['The Question', ['Answer 1', 'Answer 2', 'Answer 3', 'Answer 4'], 'correct answer', {{'difficulty': '{level}'}}],\n"
        f"The format is a list. Inside the list is a string with the question, then a list with each multiple choice question as a string, then the correct answer as a string, then a dictionary with a key of 'difficulty' and a value of {level}\n"
    )


    response = client.completions.create(
        prompt = prompt_query,
        model = 'gpt-3.5-turbo-instruct',
        temperature = 0.4,
        max_tokens = 500,
        n=15,
        stop = None
    )
    
    return response.choices[0].text


print(get_ai_questions('sewing','easy'))
