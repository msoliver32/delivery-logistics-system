from decimal import Decimal
from math import ceil

import networkx as nx

import matplotlib.pyplot as plt

malha = [
    ["A", "B", 10],
    ["B", "D", 15],
    ["A", "C", 20],
    ["C", "D", 30],
    ["B", "E", 50],
    ["D", "E", 30],
    ["E", "A", 12],
    ["B", "C", 3],
]

origem = "A"
destino = "D"
autonomia = Decimal("10.0")
valor_combustivel = Decimal("2.50")

neighbors = {}


def round_up(n: Decimal, decimals: int = 0) -> float:
    multiplier = 10 ** decimals
    return ceil(n * multiplier) / multiplier


def calcula_frete(
    total_km: int, autonomia: Decimal, valor_combustivel: Decimal
) -> float:
    return round_up((total_km / autonomia) * valor_combustivel, 2)


Gr = nx.Graph()
for r in malha:
    Gr.add_node(r[0])

for r in malha:
    Gr.add_edge(r[0], r[1], weight=r[2])

for node in list(Gr.nodes()):
    neighbors[node] = list(Gr.adj[node])

shortest_distance = nx.single_source_dijkstra(Gr, source=origem, target=destino)
total_frete = calcula_frete(shortest_distance[0], autonomia, valor_combustivel)

print(f"Mapa: {malha}")

print(
    f"\nOrigem: {origem}, Destino: {destino}, Autonomia Veículo: {autonomia}, Valor combustível: {valor_combustivel}"
)
print(
    f"Menor valor de entrega {total_frete} - Km {shortest_distance[0]} - Rota: {shortest_distance[1]}"
)

destino = "C"

shortest_distance = nx.single_source_dijkstra(Gr, source=origem, target=destino)
total_frete = calcula_frete(shortest_distance[0], autonomia, valor_combustivel)

print(
    f"\nOrigem: {origem}, Destino: {destino}, Autonomia Veículo: {autonomia}, Valor combustível: {valor_combustivel}"
)
print(
    f"Menor valor de entrega {total_frete} - Km {shortest_distance[0]} - Rota: {shortest_distance[1]}"
)

print("\nCidades Vizinhas: ")
for k, v in neighbors.items():
    print(f"Cidade {k}: {v}")

labels = nx.get_edge_attributes(Gr, "weight")
pos = nx.spring_layout(Gr, k=10)

nx.draw(Gr, pos, with_labels=True)
nx.draw_networkx_edge_labels(Gr, pos, edge_labels=labels)

plt.show()
