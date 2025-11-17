"""
AvionAgent (agent) - comportamiento del avión

Este módulo define el agente Avión para la simulación.
Cada avión tiene varios comportamientos periódicos:
	- StatusTick: muestra estado periódicamente (para depuración).
	- SendVolando: informa a la Torre que "está volando".
	- RequestLanding: solicita permiso para aterrizar.
	- RecvBehav: procesa las respuestas de la Torre.
	- LandingBehav: simula el aterrizaje y libera la pista.
Notas:
- Los mensajes se envían usando `Message` con `body` y `performative` en metadata.
- Este archivo se ejecuta como módulo de la simulación; el arranque real lo hace `hostAgent.py`.
"""

import asyncio
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour, CyclicBehaviour, OneShotBehaviour
from spade.message import Message



class AvionAgent(Agent):
	# Muestra un pequeño ticker con el nombre del agente (depuración)
	class StatusTick(PeriodicBehaviour):
		async def run(self):
			print(f"({self.agent.name})")


	# Envía periódicamente un informe de estado "volando" a la torre
	class SendVolando(PeriodicBehaviour):
		async def run(self):
			msg = Message(to="torre@localhost")
			msg.set_metadata("performative", "inform")
			msg.body = "volando"
			await self.send(msg)


	# Solicita permiso para aterrizar (periodicamente)
	class RequestLanding(PeriodicBehaviour):
		async def run(self):
			msg = Message(to="torre@localhost")
			msg.set_metadata("performative", "propose")
			msg.body = "aterrizar"
			await self.send(msg)


	# Recibe respuestas de la Torre y decide la acción a tomar
	class RecvBehav(CyclicBehaviour):
		async def run(self):
			msg = await self.receive(timeout=1)
			if msg is None:
				return
			body = msg.body
			# La Torre responde con cadenas simples en el body
			if body == "recibido":
				print(f"->{self.agent.name} confirmación de la Torre")
			elif body == "aceptar":
				# Inicia el comportamiento de aterrizaje (se ejecutará una vez)
				print(f"=>\t{self.agent.name} (inicio aterrizaje)")
				# add_behaviour no es awaitable, se invoca directamente
				self.agent.add_behaviour(self.agent.LandingBehav())
			elif body == "rechazo":
				# Rechazo: el avión intentará de nuevo en el siguiente RequestLanding
				print(f"{self.agent.name}: rechazo de aterrizaje")


	# Comportamiento que simula el aterrizaje (una sola ejecución)
	class LandingBehav(OneShotBehaviour):
		async def run(self):
			# Simula tiempo de aterrizaje
			await asyncio.sleep(2)
			print(f"=>\t{self.agent.name} (fin aterrizaje)")
			# Notifica a la Torre que libera la pista
			msg = Message(to="torre@localhost")
			msg.set_metadata("performative", "inform")
			msg.body = "liberar"
			await self.send(msg)
			# El avión finaliza su ciclo (se borra a sí mismo)
			await self.agent.stop()


	async def setup(self):
		# Mensaje de arranque del agente
		print(f"Avion {str(self.jid)} started")
		# Añadir comportamientos periódicos y el receptor
		self.add_behaviour(self.StatusTick(period=1))
		self.add_behaviour(self.SendVolando(period=5))
		self.add_behaviour(self.RequestLanding(period=10))
		self.add_behaviour(self.RecvBehav())


if __name__ == "__main__":
	print("Este archivo define el agente AvionAgent; ejecútalo desde hostAgent.py")
 