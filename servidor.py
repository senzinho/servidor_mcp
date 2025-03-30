import socket
import json

# Banco de dados simulado (lista de dicionários)
DADOS = [
    {
        "id": 20, "marca": "Rios-Riley", "modelo": "stop", "ano": 2000,
        "cor": "Aqua", "quilometragem": 142110, "motorizacao": "3.9L 16V",
        "combustivel": "Flex", "preco": "14340.00"
    },
    {
        "id": 21, "marca": "Ford", "modelo": "Focus", "ano": 2015,
        "cor": "Preto", "quilometragem": 65000, "motorizacao": "2.0L 16V",
        "combustivel": "Gasolina", "preco": "45000.00"
    }
]

def filtrar_dados(filtros):
    """Filtra os dados com base nos critérios enviados pelo cliente."""
    resultado = []
    
    for item in DADOS:
        match = True
        for chave, valor in filtros.items():
            if str(item.get(chave, "")).lower() != str(valor).lower():
                match = False
                break
        if match:
            resultado.append(item)
    
    return resultado

def json_para_mcp(resultado):
    """Converte JSON para formato MCP."""
    mcp = "MCP/1.0\nSTATUS: sucesso\nMENSAGEM: Resultados encontrados\nDADOS:\n"
    for item in resultado:
        mcp += f"  - ID: {item['id']}\n"
        mcp += f"    MARCA: {item['marca']}\n"
        mcp += f"    MODELO: {item['modelo']}\n"
        mcp += f"    ANO: {item['ano']}\n"
        mcp += f"    COR: {item['cor']}\n"
        mcp += f"    QUILOMETRAGEM: {item['quilometragem']}\n"
        mcp += f"    MOTORIZACAO: {item['motorizacao']}\n"
        mcp += f"    COMBUSTIVEL: {item['combustivel']}\n"
        mcp += f"    PRECO: {item['preco']}\n"

    return mcp if resultado else "MCP/1.0\nSTATUS: erro\nMENSAGEM: Nenhum resultado encontrado\n"

def servidor_mcp():
    """Cria o servidor TCP para receber requisições MCP."""
    host = "127.0.0.1"
    porta = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, porta))
    server_socket.listen(5)

    print(f"Servidor MCP rodando em {host}:{porta}...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Conexão recebida de {addr}")

        dados_recebidos = conn.recv(1024).decode()
        print(f"Dados recebidos:\n{dados_recebidos}")

        try:
            filtros = json.loads(dados_recebidos)
            resultados = filtrar_dados(filtros)
            resposta_mcp = json_para_mcp(resultados)
        except Exception as e:
            resposta_mcp = f"MCP/1.0\nSTATUS: erro\nMENSAGEM: Erro ao processar requisição\nERRO: {str(e)}\n"

        conn.sendall(resposta_mcp.encode())
        conn.close()

if __name__ == "__main__":
    servidor_mcp()
