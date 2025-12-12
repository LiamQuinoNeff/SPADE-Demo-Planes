"""
TorreAgent (agent) - controla la pista

Este módulo implementa la lógica de la Torre de control.
La Torre recibe mensajes de los aviones y responde según el estado
de la pista (`pista_ocupada`). Su comportamiento principal es leer
mensajes y responder con performatives y bodies sencillos.
"""

import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class TorreAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):
            # Cada iteración intenta recibir un mensaje con timeout corto
            # print("[Torre] Escuchando mensajes...")  # Comentado para reducir ruido
            msg = await self.receive(timeout=1)
            if msg is None:
                return
            sender_full = str(msg.sender)
            sender_name = sender_full.split('@')[0]
            body = msg.body
            # Mostrar resumen del mensaje recibido (depuración)
            # print(f"[Torre] Mensaje de {sender_name}: {body}")  # Comentado para reducir ruido

            # Preparar respuesta básica
            reply = Message(to=sender_full)

            # Lógica de la torre según el contenido (body) del mensaje
            if body == "volando":
                # Acknowledge inform
                reply.set_metadata("performative", "inform")
                reply.body = "recibido"
            elif body == "aterrizar":
                # Petición para aterrizar
                if self.agent.pista_ocupada:
                    # Pista ocupada: rechazo
                    print(f"[Torre] Solicitud rechazada para {sender_name} - pista ocupada")
                    reply.set_metadata("performative", "reject-proposal")
                    reply.body = "rechazo"
                else:
                    # Pista libre: aceptar y marcarla ocupada
                    print(f"[Torre] Permiso concedido a {sender_name}")
                    reply.set_metadata("performative", "accept-proposal")
                    reply.body = "aceptar"
                    self.agent.pista_ocupada = True
            elif body in ("liberar", "fin"):
                # El avión notifica que liberó la pista
                print(f"[Torre] Pista liberada por {sender_name}")
                self.agent.pista_ocupada = False
                reply.set_metadata("performative", "inform")
                reply.body = "liberado"
            else:
                # Mensaje no entendido
                reply.set_metadata("performative", "not-understood")
                reply.body = "desconocido"

            # Enviar la respuesta al remitente
            await self.send(reply)

    async def setup(self):
        # Mensaje de inicio del agente Torre
        print(f"[Sistema] Torre de control iniciada")
        # Bandera que indica si la pista está ocupada
        self.pista_ocupada = False
        # Añadir comportamiento receptor de mensajes
        self.add_behaviour(self.RecvBehav())