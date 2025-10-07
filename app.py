from flask import Flask, render_template, request, jsonify
from transformers import pipeline, Conversation

app = Flask(__name__)

#Load the AI model
print("Loading AI model..")

chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")

print("Model Loaded")

def chatbot_response(user_input):
    try:
        conv = Conversation(user_input)
        result = chatbot(conv)
        # The pipeline returns a list of Conversation(s)
        reply = result.generated_responses[-1]
        return reply
    except Exception as e:
        print("ERROR:", e)
        return "Sorry, something went wrong!"


@app.route('/')

def home():
  return render_template("index.html")

@app.route('/chat', methods = ['POST'])
def chat():
  data = request.get_json()
  user_message = data.get('message',"")
  response = chatbot_response(user_message)
  return jsonify({"response": response})

if __name__ == '__main__':
  app.run(debug=True)

