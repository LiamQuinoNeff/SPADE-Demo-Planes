"""
HostAgent - lanzador de la simulación

Este script crea y arranca la Torre y varios agentes Avión. Se usa como
entrypoint para poner en marcha la simulación localmente (necesita XMPP).
"""

import spade
from spade.agent import Agent
from torreAgent import TorreAgent
from avionAgent import AvionAgent


class HostAgent(Agent):
    """Agente host que crea la Torre y múltiples Aviones."""

    numAviones = 10

    async def setup(self):
        # Crear y arrancar la Torre
        torre = TorreAgent("torre@localhost", "123456abcd.")
        await torre.start(auto_register=True)
        print("Torre started")

        # Crear y arrancar N aviones
        for i in range(self.numAviones):
            avion = AvionAgent(f"avion{i}@localhost", "123456abcd.")
            await avion.start(auto_register=True)
            print(f"avion{i} started")

        # Esperar que la Torre termine (en esta demo normalmente se interrumpe manualmente)
        await spade.wait_until_finished(torre)
        print("Agents finished")


async def main():
    # Crear el host y arrancarlo
    host = HostAgent('host@localhost', '123456abcd.')
    await host.start()
    print("Host agent started")
    await spade.wait_until_finished(host)


if __name__ == "__main__":
    spade.run(main())
