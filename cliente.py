import socket
import json

def cliente_mcp(filtros):
    """Envia filtros para o servidor MCP e exibe a resposta."""
    host = "127.0.0.1"
    porta = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, porta))

    # Converte filtros para JSON e envia
    filtros_json = json.dumps(filtros)
    client_socket.sendall(filtros_json.encode())

    # Recebe resposta MCP
    resposta_mcp = client_socket.recv(4096).decode()
    print("\nResposta do Servidor MCP:\n")
    print(resposta_mcp)

    client_socket.close()

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