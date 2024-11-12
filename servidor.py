# -*- coding: utf-8 -*-
import rpyc
from datetime import datetime

class ChatServer(rpyc.Service):
    MAX_SALAS = 4

    def __init__(self):
        self.usuarios = {} 
        self.salas = {}  
        self.id_contador = 1

    def exposed_Ingressar_no_sistema(self, nome):
        usuario_id = self.id_contador
        self.usuarios[usuario_id] = nome
        self.id_contador += 1
        return usuario_id

    def exposed_Criar_sala(self, nome_sala):
        if len(self.salas) >= self.MAX_SALAS:
            return "Limite de salas atingido. Não é possível criar mais salas."
        if nome_sala not in self.salas:
            self.salas[nome_sala] = {
                "usuarios_na_sala": {},
                "mensagens": [],
                "mensagens_privadas": {}
            }
            return f"Sala '{nome_sala}' criada com sucesso."
        return f"Sala '{nome_sala}' já existe."

    def exposed_Listar_salas(self):
        return list(self.salas.keys())

    def exposed_Entrar_na_sala(self, usuario_id, nome_sala):
        if usuario_id in self.usuarios and nome_sala in self.salas:
            self.salas[nome_sala]["usuarios_na_sala"][usuario_id] = self.usuarios[usuario_id]
            return f"Usuário {self.usuarios[usuario_id]} entrou na sala '{nome_sala}'."
        return "Usuário ou sala não encontrado."

    def exposed_Sair_da_sala(self, usuario_id, nome_sala):
        if nome_sala in self.salas and usuario_id in self.salas[nome_sala]["usuarios_na_sala"]:
            nome = self.salas[nome_sala]["usuarios_na_sala"].pop(usuario_id)
            return f"Usuário {nome} saiu da sala '{nome_sala}'."
        return "Usuário ou sala não encontrado."

    def exposed_Enviar_mensagem(self, usuario_id, nome_sala, mensagem):
        if nome_sala in self.salas and usuario_id in self.salas[nome_sala]["usuarios_na_sala"]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.salas[nome_sala]["mensagens"].append((mensagem, usuario_id, timestamp))
            return "Mensagem enviada."
        return "Usuário ou sala não encontrado."

    def exposed_Listar_mensagens(self, nome_sala):
        if nome_sala in self.salas:
            return [(msg, self.usuarios[uid], ts) for msg, uid, ts in self.salas[nome_sala]["mensagens"]]
        return "Sala não encontrada."

    def exposed_Listar_usuarios(self, nome_sala):
        if nome_sala in self.salas:
            return [{"id": uid, "nome": nome} for uid, nome in self.salas[nome_sala]["usuarios_na_sala"].items()]
        return "Sala não encontrada."

    def exposed_Enviar_mensagem_usuario(self, remetente_id, destinatario_id, nome_sala, mensagem):
        if nome_sala in self.salas and remetente_id in self.salas[nome_sala]["usuarios_na_sala"] and destinatario_id in self.salas[nome_sala]["usuarios_na_sala"]:
            if destinatario_id not in self.salas[nome_sala]["mensagens_privadas"]:
                self.salas[nome_sala]["mensagens_privadas"][destinatario_id] = []
            self.salas[nome_sala]["mensagens_privadas"][destinatario_id].append(
                (self.usuarios[remetente_id], mensagem))
            return "Mensagem privada enviada."
        return "Remetente ou destinatário não está na sala. Ambos precisam estar na sala para enviar mensagens privadas."

    def exposed_Listar_mensagens_privadas(self, usuario_id, nome_sala):
        if nome_sala in self.salas and usuario_id in self.salas[nome_sala]["usuarios_na_sala"]:
            return self.salas[nome_sala]["mensagens_privadas"].get(usuario_id, [])
        return "Usuário ou sala não encontrado."

from rpyc.utils.server import ThreadedServer
t = ThreadedServer(ChatServer, port=18861)
print("Servidor de Chat RPC em execução na porta 18861...")
t.start()