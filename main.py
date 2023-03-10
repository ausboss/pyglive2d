from flask import Flask, request, jsonify, render_template

import json
import requests
app = Flask(__name__)

ENDPOINT = "https://clearance-les-assess-head.trycloudflare.com/"

# set up chatbot prompt
chatbot_prompt = "Let's chat! Say something to start the conversation."


class Chatbot:
    def __init__(self, char_filename):
        # read character data from JSON file
        with open(char_filename, "r") as f:
            data = json.load(f)
            self.char_name = data["char_name"]
            self.char_persona = data["char_persona"]
            self.char_greeting = data["char_greeting"]
            self.world_scenario = data["world_scenario"]
            self.example_dialogue = data["example_dialogue"]
        self.endpoint = ENDPOINT

        # initialize conversation history and character information
        self.conversation_history = f"<START>\n{self.char_name}: {self.char_greeting}\n"
        self.character_info = f"{self.char_name}'s Persona: {self.char_persona}\nScenario: {self.world_scenario}\n"
        self.num_lines_to_keep = 20



    def save_conversation(self, message):
        # add user response to conversation history
        print(f"message: {message}")
        self.conversation_history += f'You: {message}\n'
        print(f'self.conversation_history: {self.conversation_history}')
        # format prompt
        prompt = {
            "prompt": self.character_info + '\n'.join(
                self.conversation_history.split('\n')[-self.num_lines_to_keep:]) + f'{self.char_name}:',
        }
        # send a post request to the API endpoint
        response = requests.post(f"{self.endpoint}/api/v1/generate", json=prompt)
        # check if the request was successful
        if response.status_code == 200:
            # Get the results from the response
            results = response.json()['results']
            response_list = [line for line in results[0]['text'][1:].split("\n")]
            result = [response_list[0]]
            for item in response_list[1:]:
                if self.char_name in item:
                    result.append(item)
                else:
                    break
            new_list = [item.replace(self.char_name + ": ", '\n') for item in result]
            response_text = ''.join(new_list)
        self.conversation_history += f'{self.char_name}: {response_text}\n'
        return response_text




# initialize chatbot
chatbot = Chatbot('static/Tensor.json')


#Todo: fix user input not being added to chat history/prompt

# define route for the chatbot
@app.route('/chatbot', methods=['POST'])
def chatbot():
    print(request.form)  # Debugging statement
    user_input = request.form['input']
    # Process the user's input and generate a chatbot response
    chatbot_response = chatbot.save_conversation(user_input)
    # Return the chatbot response as JSON
    return jsonify({'output': chatbot_response})


# initialize chatbot before first request
@app.before_first_request
def init_chatbot():
    global chatbot
    chatbot = Chatbot('static/Tensor.json')

# define route for the homepage 
# Todo: make chatbot_prompt show up as first message
@app.route('/')
def home():
    return render_template('home.html', chatbot_prompt=chatbot_prompt)

@app.route('/hd', methods=['GET', 'POST'])
def hd():
    if request.method == 'GET':
        openai_key = request.args.get('openai')
        engine = request.args.get('engine')
        model = request.args.get('model')
        return render_template('index.html', openai_key=openai_key, engine=engine, model=model)
    elif request.method == 'POST':
        print(request.form)  # Debugging statement
        user_input = request.form['input']
        # Process the user's input and generate a chatbot response
        chatbot_response = chatbot.save_conversation(user_input)
        # Return the chatbot response as JSON
        return jsonify({'output': chatbot_response})



if __name__ == '__main__':
    app.run(debug=True)