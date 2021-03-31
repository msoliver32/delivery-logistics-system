from copy import deepcopy
from decimal import Decimal
from typing import List

mapa = {}

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

cidades_distancia = []


def carrega_mapa():
    for rota in malha:
        if rota[0] not in mapa:
            mapa[rota[0]] = {rota[1]: rota[2]}

        else:
            mapa[rota[0]].update({rota[1]: rota[2]})

        if rota[1] not in mapa:
            mapa[rota[1]] = {rota[0]: rota[2]}

        else:
            mapa[rota[1]].update({rota[0]: rota[2]})


def itera_percurso(origem: str, destino: str, rotas: List = []) -> int:
    print(f"Origem: {origem} - Cidades Anteriores: {rotas}")
    malha_rotas = deepcopy(mapa[origem])

    if origem not in malha_rotas:
        rotas.append(origem)

    menor_rota = busca_menor_rota(origem, destino, rotas)
    menor_km = malha_rotas.get(menor_rota, 0)

    if destino == origem:
        print("Caminho mais curto")
        print("\oooo/")
        return rotas

    elif menor_rota is None:
        origem = rotas[rotas.index(origem) - 1]
        return itera_percurso(origem, destino, rotas)
    else:
        print(f"Próxima menor rota: {menor_rota} / {menor_km} KM")
        rotas = rotas[: rotas.index(origem) + 1]
        return itera_percurso(menor_rota, destino, rotas)


def busca_menor_rota(origem: str, destino: str, cidades_anteriores: List[str]) -> str:
    rotas = deepcopy(mapa[origem])
    [rotas.pop(cd, None) for cd in cidades_anteriores]

    if rotas.get(destino, {}):
        return destino

    if rotas:
        menor_rota = min(rotas.keys(), key=lambda k: rotas[k])
        return menor_rota
    else:
        return None


def calcula_km(percurso: List[str]):
    total_km = 0

    for cidade in range(len(percurso)):
        if cidade == len(percurso) - 1:
            break
        total_km += mapa.get(percurso[cidade]).get(percurso[cidade + 1])
    return total_km


def calcula_frete(total_km: int, autonomia: Decimal, valor_combustivel: Decimal):
    return Decimal(total_km / autonomia) * valor_combustivel


def busca_vizinhos(nome_cidade: str) -> List[str]:
    for cidade_vizinha, rotas in mapa.items():
        if nome_cidade == cidade_vizinha:
            return [rota for rota, km in rotas.items()]

    return []


carrega_mapa()
print(mapa)

percurso_AD = itera_percurso("A", "D", [])
print(percurso_AD)

total_km_AD = calcula_km(percurso_AD)
print(total_km_AD)

total_frete_AD = calcula_frete(total_km_AD, 10, Decimal("2.50"))
print(round(total_frete_AD, 2))


percurso_AC = itera_percurso("A", "C", [])
print(percurso_AC)

total_km_AC = calcula_km(percurso_AC)
print(total_km_AC)

total_frete_AC = calcula_frete(total_km_AC, 10, Decimal("2.50"))
print(round(total_frete_AC, 2))


print(f"Cidade A: {busca_vizinhos('A')}")
print(f"Cidade B: {busca_vizinhos('B')}")
print(f"Cidade C: {busca_vizinhos('C')}")
print(f"Cidade D: {busca_vizinhos('D')}")
print(f"Cidade E: {busca_vizinhos('E')}")
