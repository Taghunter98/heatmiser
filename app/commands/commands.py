import json
import ssl
import websocket

class Command():
    def __init__(self, NEOHUB_URL, TOKEN):
        self.NEOHUB_URL = NEOHUB_URL
        self.TOKEN = TOKEN

    def runRecipe(self, recipe_name):
        try:
            # Connect to NeoHub
            ws = websocket.create_connection(self.NEOHUB_URL, sslopt = {"cert_reqs": ssl.CERT_NONE})

            # Construct the message in the correct format
            command_payload = {
                "message_type": "hm_get_command_queue",
                "message": json.dumps({
                    "token": self.TOKEN,
                    "COMMANDS": [
                        {"COMMAND": f"{{'RUN_RECIPE':['{recipe_name}']}}", "COMMANDID": 1}
                    ]
                })
            }

            # Convert to JSON and send over WebSocket
            ws.send(json.dumps(command_payload))

            # Receive response
            response = ws.recv()
            print("Response from NeoHub:", response)

            # Close WebSocket connection
            ws.close()

        except Exception as e:
            print("Error:", e)