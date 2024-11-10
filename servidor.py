from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from datetime import datetime

class ChatServer:
    def __init__(self):
        self.usuarios = {}  # Dicionário de usuários registrados {id: nome}
        self.usuarios_na_sala = {}  # Dicionário de usuários na sala {id: nome}
        self.mensagens = []  # Lista de mensagens públicas (texto, id, timestamp)
        self.mensagens_privadas = {}  # Dicionário de mensagens privadas {destinatario_id: [(remetente, mensagem)]}
        self.id_contador = 1  # Gerador de IDs incrementais

    def Ingressar_no_sistema(self, nome):
        usuario_id = self.id_contador
        self.usuarios[usuario_id] = nome
        self.id_contador += 1
        return usuario_id

    def Entrar_na_sala(self, usuario_id):
        if usuario_id in self.usuarios:
            self.usuarios_na_sala[usuario_id] = self.usuarios[usuario_id]
            return f"Usuário {self.usuarios[usuario_id]} entrou na sala."
        return "Usuário não encontrado."

    def Sair_da_sala(self, usuario_id):
        if usuario_id in self.usuarios_na_sala:
            nome = self.usuarios_na_sala.pop(usuario_id)
            return f"Usuário {nome} saiu da sala."
        return "Usuário não está na sala."

    def Enviar_mensagem(self, usuario_id, mensagem):
        if usuario_id in self.usuarios_na_sala:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.mensagens.append((mensagem, usuario_id, timestamp))
            return "Mensagem enviada."
        return "Usuário não está na sala. Entre na sala para enviar mensagens públicas."

    def Listar_mensagens(self):
        # Retorna todas as mensagens públicas
        return [(msg, self.usuarios[uid], ts) for msg, uid, ts in self.mensagens]

    def Enviar_mensagem_usuario(self, remetente_id, destinatario_id, mensagem):
        if remetente_id in self.usuarios_na_sala and destinatario_id in self.usuarios_na_sala:
            if destinatario_id not in self.mensagens_privadas:
                self.mensagens_privadas[destinatario_id] = []
            self.mensagens_privadas[destinatario_id].append(
                (self.usuarios[remetente_id], mensagem))
            return "Mensagem privada enviada."
        return "Remetente ou destinatário não está na sala. Ambos precisam estar na sala para enviar mensagens privadas."

    def Listar_mensagens_privadas(self, usuario_id):
        if usuario_id in self.usuarios_na_sala:
            return self.mensagens_privadas.get(usuario_id, [])
        return "Usuário não está na sala. Entre na sala para visualizar mensagens privadas."

    def Listar_usuarios(self):
        # Retorna apenas os usuários que estão realmente na sala
        return [{"id": uid, "nome": nome} for uid, nome in self.usuarios_na_sala.items()]

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)

with SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler) as server:
    server.register_instance(ChatServer())
    print("Servidor de Chat RPC em execução na porta 8000...")
    server.serve_forever()
