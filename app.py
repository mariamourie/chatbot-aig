import os
from flask import Flask, render_template, request, session
from openai import OpenAI

# Carrega a chave da API do OpenAI a partir das variáveis de ambiente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inicializa a aplicação Flask
app = Flask(__name__)
# Define uma chave secreta para a sessão - substitua com uma chave segura
app.secret_key = "SUA_CHAVE_SECRETA_AQUI"

# Cria o cliente OpenAI com a chave da API
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def chatgpt_send_message(question):
    """
    Envia uma mensagem para o ChatGPT e retorna a resposta.
    """
    context = "Você é um atendente de SAC"
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": question},
        ],
    )
    return {"role": "assistant", "content": completion.choices[0].message.content}

@app.route("/", methods=["GET", "POST"])
def send_messages():
    """
    Rota principal que trata as mensagens enviadas pelo usuário.
    """
    if request.method == "POST":
        pergunta = request.form["pergunta"]
        user_message = {"role": "user", "content": pergunta}
        historico_chat = session.get("historico_chat", [])
        historico_chat.append(user_message)
        historico_chat.append(chatgpt_send_message(pergunta))
        session["historico_chat"] = historico_chat
        return render_template("index.html", historico_chat=historico_chat)
    return render_template("index.html")

@app.route("/delete-chat", methods=["POST"])
def delete_chat():
    """
    Endpoint para limpar o histórico do chat.
    """
    session.pop("historico_chat", None)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)