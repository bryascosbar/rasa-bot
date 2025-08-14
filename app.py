from flask import Flask, request, jsonify, render_template  # Importa render_template para renderizar HTML.
import requests  # Importa la biblioteca 'requests' para realizar solicitudes HTTP a otros servidores (en este caso, el servidor de Rasa).

app = Flask(__name__)  # Crea una instancia de la aplicación Flask. Esto inicializa la aplicación web.

# Ruta para servir el archivo HTML (index.html).
@app.route("/")
def index():
    return render_template("index.html")  # Renderiza el archivo index.html cuando el usuario accede a la raíz del sitio.

# Ruta para manejar las interacciones con el chatbot.
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")  # Obtiene el mensaje del usuario desde la solicitud JSON.

    # Envía el mensaje del usuario al servidor de Rasa a través de una solicitud POST.
    rasa_response = requests.post(
        "http://localhost:5005/webhooks/rest/webhook",  # URL del servidor de Rasa (que debe estar ejecutándose localmente).
        json={"message": user_message}  # Envía el mensaje del usuario en formato JSON.
    )
    
    bot_response = rasa_response.json()  # Obtiene la respuesta del servidor de Rasa en formato JSON.
    if bot_response:  # Verifica si Rasa ha devuelto una respuesta.
        # Si hay respuesta, obtiene el texto de la primera respuesta que envía Rasa. Si no hay texto, muestra un mensaje predeterminado.
        bot_message = bot_response[0].get("text", "Lo siento, no puedo responder eso en este momento.")
    else:  # Si no hay respuesta de Rasa.
        bot_message = "Lo siento, no entendí tu mensaje."  # Mensaje predeterminado si el bot no puede procesar el mensaje.

    return jsonify({"bot_response": bot_message})  # Devuelve la respuesta del bot en formato JSON.

if __name__ == "__main__":  # Comprueba si este archivo se está ejecutando directamente (no importado como módulo).
    app.run(port=8000, debug=True)  # Inicia el servidor Flask en el puerto 8000 y activa el modo de depuración.
