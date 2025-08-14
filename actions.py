# actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionConsultarMultas(Action):

    def name(self) -> Text:
        return "action_consultar_multas"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Slot donde capturamos la cédula
        cedula = tracker.get_slot("cedula")
        if not cedula:
            dispatcher.utter_message(text="❗ Por favor, proporciona tu número de cédula para consultar multas.")
            return []

        url = f"https://api.verifik.co/v2/co/simit/consultar?numero_identificacion={cedula}"
        headers = {
            "Accept": "application/json",
            "Authorization": "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRJZCI6IjY4OWQyOGEzMWZlZDRjYzg4YmIxYmFjMyIsInAiOiJ2ayIsIkpXVFBocmFzZSI6IjY4OWQyM2JmOTllNjhlNTllYzMzZDNmYSIsImV4cGlyZXNBdCI6MTc1NzgwOTQ5NCwiaWF0IjoxNzU1MTMxMDk0fQ.8xqud8VUEQl_HZhZ7JrB6X-Hu4-ckDlKjUqXRlGrYxU"
        }

        try:
            response = requests.get(url, headers=headers)
            data = response.json()

            if "error" in data:
                dispatcher.utter_message(text=f"❌ No se encontraron multas: {data['error']}")
            elif not data.get("multas"):
                dispatcher.utter_message(text="✅ No se encontraron multas para esta cédula.")
            else:
                mensajes = []
                for multa in data["multas"]:
                    mensaje = (
                        f"🚨 *Infractor:* {multa.get('nombre_infractor')}\n"
                        f"📄 *Resolución:* {multa.get('numero_resolucion')}\n"
                        f"🏛️ *Secretaría:* {multa.get('secretaria_emisora')}\n"
                        f"💰 *Valor total:* {multa.get('valor_total')}\n"
                        f"📌 *Estado:* {multa.get('estado')}\n"
                        "------------------------"
                    )
                    mensajes.append(mensaje)
                dispatcher.utter_message(text="\n".join(mensajes))

        except Exception as e:
            dispatcher.utter_message(text=f"⚠️ Error al consultar multas: {str(e)}")

        return []
