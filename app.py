from flask import Flask,render_template, request, Response
import os
from openai import OpenAI
import dotenv
from time import sleep

app = Flask(__name__)
app.secret_key = 'alura'
    
dotenv.load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=openai_key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods = ['POST'])
def chat():
    prompt = request.json['msg']
    return Response(trata_resposta(prompt), mimetype='text/event-stream')
    
def trata_resposta(prompt):
    resposta_parcial = ''
    for resposta in bot(prompt):
        pedaco_resposta = resposta.choices[0].delta.content
        print(pedaco_resposta)
        if len(pedaco_resposta):
            resposta_parcial += pedaco_resposta
            yield pedaco_resposta 


def bot(prompt):
    maxima_repeticao = 1
    repeticao = 0
    while True:
        try:
            model='gpt-3.5-turbo'
            prompt_do_sistema = f"""
            Você é um chatbot de atendimento a clientes de um e-commerce.
            Você não deve responder perguntas que não sejam dados do ecommerce informado!
            """
            response = openai.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt_do_sistema
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                stream = True,
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                model = model)
            
            return response
        except Exception as erro:
            repeticao += 1
            if repeticao >= maxima_repeticao:
                return "Erro no GPT3: %s" % erro
            print('Erro de comunicação com OpenAI:', erro)
            sleep(1)

if __name__ == "__main__":
    app.run(debug = True)
