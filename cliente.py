import requests
import json


# Para garantir que o cliente não use proxy
proxies = {
    "http": None,
    "https": None,
}

def calcular_proximidade(veiculo, filtros):
    """Calcula a proximidade do veículo com base nos filtros fornecidos."""
    peso_marca = 3
    peso_ano = 2
    peso_combustivel = 1
    
    score = 0
    if "marca" in filtros and filtros["marca"].lower() == veiculo.get("marca", "").lower():
        score += peso_marca
    if "ano" in filtros and filtros["ano"] == str(veiculo.get("ano", "")):
        score += peso_ano
    if "combustivel" in filtros and filtros["combustivel"].lower() == veiculo.get("combustivel", "").lower():
        score += peso_combustivel
    
    return score

def cliente_mcp(filtros):
    """Envia filtros para o servidor Django e exibe a resposta ordenada."""
    url = "http://127.0.0.1:5000/api/filtrar-veiculos/"  # Ajuste para a URL da sua API
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=filtros, headers=headers)
        
        print(f"Status da resposta: {response.status_code}")
        print(f"Conteúdo da resposta: {response.text}")
        
        if response.status_code == 200:
            resposta_mcp = response.json()
            
            # Ordena os veículos pela proximidade com os filtros
            veiculos_ordenados = sorted(resposta_mcp, key=lambda v: calcular_proximidade(v, filtros), reverse=True)
            
            print("\nResposta do Servidor MCP (Ordenada):\n")
            print(json.dumps(veiculos_ordenados, indent=4, ensure_ascii=False))
        else:
            print(f"Erro ao obter dados da API: {response.status_code}")
    except Exception as e:
        print(f"Erro ao conectar à API: {str(e)}")


if __name__ == "__main__":
    print("Bem-vindo ao Cliente MCP!")
    marca = input("Digite a marca do carro (ou deixe em branco): ").strip()
    ano = input("Digite o ano do carro (ou deixe em branco): ").strip()
    combustivel = input("Digite o tipo de combustível (ou deixe em branco): ").strip()

    filtros = {}
    if marca:
        filtros["marca"] = marca
    if ano:
        filtros["ano"] = ano
    if combustivel:
        filtros["combustivel"] = combustivel

    cliente_mcp(filtros)
