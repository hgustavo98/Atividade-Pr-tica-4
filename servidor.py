# -*- coding: utf-8 -*-
import rpyc
from datetime import datetime

class ChatServer(rpyc.Service):
    MAX_SALAS = 4

    def __init__(self):
        if not hasattr(ChatServer, 'usuarios'):
            ChatServer.usuarios = {}
            ChatServer.salas = {}
            ChatServer.id_contador = 1

    def exposed_Ingressar_no_sistema(self, nome):
        usuario_id = ChatServer.id_contador
        ChatServer.usuarios[usuario_id] = nome
        ChatServer.id_contador += 1
        return usuario_id

    def exposed_Criar_sala(self, nome_sala):
        if len(ChatServer.salas) >= self.MAX_SALAS:
            return "Limite de salas atingido. Não é possível criar mais salas."
        if nome_sala not in ChatServer.salas:
            ChatServer.salas[nome_sala] = {
                "usuarios_na_sala": {},
                "mensagens": [],
                "mensagens_privadas": {},
                "usuarios_entrada": {}
            }
            return f"Sala '{nome_sala}' criada com sucesso."
        return f"Sala '{nome_sala}' já existe."

    def exposed_Listar_salas(self):
        return list(ChatServer.salas.keys())

    def exposed_Entrar_na_sala(self, usuario_id, nome_sala):
        if usuario_id in ChatServer.usuarios and nome_sala in ChatServer.salas:
            ChatServer.salas[nome_sala]["usuarios_na_sala"][usuario_id] = ChatServer.usuarios[usuario_id]
            ChatServer.salas[nome_sala]["usuarios_entrada"][usuario_id] = datetime.now()
            return f"Usuário {ChatServer.usuarios[usuario_id]} entrou na sala '{nome_sala}'."
        return "Usuário ou sala não encontrado."

    def exposed_Sair_da_sala(self, usuario_id, nome_sala):
        if nome_sala in ChatServer.salas and usuario_id in ChatServer.salas[nome_sala]["usuarios_na_sala"]:
            nome = ChatServer.salas[nome_sala]["usuarios_na_sala"].pop(usuario_id)
            ChatServer.salas[nome_sala]["usuarios_entrada"].pop(usuario_id)
            return f"Usuário {nome} saiu da sala '{nome_sala}'."
        return "Usuário ou sala não encontrado."

    def exposed_Enviar_mensagem(self, usuario_id, nome_sala, mensagem):
        if nome_sala in ChatServer.salas and usuario_id in ChatServer.salas[nome_sala]["usuarios_na_sala"]:
            timestamp = datetime.now()
            ChatServer.salas[nome_sala]["mensagens"].append((mensagem, usuario_id, timestamp))
            return "Mensagem enviada."
        return "Usuário ou sala não encontrado."

    def exposed_Listar_mensagens(self, usuario_id, nome_sala):
        if nome_sala in ChatServer.salas:
            entrada_time = ChatServer.salas[nome_sala]["usuarios_entrada"].get(usuario_id)
            if entrada_time:
                return [(msg, ChatServer.usuarios[uid], ts.strftime("%Y-%m-%d %H:%M:%S"))
                        for msg, uid, ts in ChatServer.salas[nome_sala]["mensagens"]
                        if ts >= entrada_time]
        return "Sala não encontrada ou usuário não está na sala."

    def exposed_Listar_usuarios(self, nome_sala):
        if nome_sala in ChatServer.salas:
            usuarios = [{"id": uid, "nome": nome} for uid, nome in ChatServer.salas[nome_sala]["usuarios_na_sala"].items()]
            if len(usuarios) == 1:
                return "Você é o único na sala."
            return usuarios
        return "Sala não encontrada."

    def exposed_Enviar_mensagem_usuario(self, remetente_id, destinatario_id, nome_sala, mensagem):
        if nome_sala in ChatServer.salas and remetente_id in ChatServer.salas[nome_sala]["usuarios_na_sala"] and destinatario_id in ChatServer.salas[nome_sala]["usuarios_na_sala"]:
            if destinatario_id not in ChatServer.salas[nome_sala]["mensagens_privadas"]:
                ChatServer.salas[nome_sala]["mensagens_privadas"][destinatario_id] = []
            ChatServer.salas[nome_sala]["mensagens_privadas"][destinatario_id].append(
                (ChatServer.usuarios[remetente_id], mensagem))
            return "Mensagem privada enviada."
        return "Remetente ou destinatário não está na sala. Ambos precisam estar na sala para enviar mensagens privadas."

    def exposed_Listar_mensagens_privadas(self, usuario_id, nome_sala):
        if nome_sala in ChatServer.salas and usuario_id in ChatServer.salas[nome_sala]["usuarios_na_sala"]:
            return ChatServer.salas[nome_sala]["mensagens_privadas"].get(usuario_id, [])
        return "Usuário ou sala não encontrado."

from rpyc.utils.server import ThreadedServer
t = ThreadedServer(ChatServer, port=18861)
print("Servidor de Chat RPC em execução na porta 18861...")
t.start()