import rpyc

def cliente_chat():
    servidor = rpyc.connect('localhost', 18861, config={'allow_public_attrs': True}).root
    nome = input("Digite seu nome para ingressar no sistema: ")
    usuario_id = servidor.Ingressar_no_sistema(nome)
    print(f"\nBem-vindo, {nome}! Seu ID é {usuario_id}. Agora você está conectado ao sistema.")
    sala_atual = None
    while True:
        print("\nEscolha uma ação:")
        print("1 - Criar sala")
        print("2 - Entrar na sala")
        print("3 - Sair da sala")
        print("4 - Enviar mensagem pública")
        print("5 - Listar mensagens públicas")
        print("6 - Enviar mensagem privada")
        print("7 - Listar usuários ativos")
        print("8 - Listar minhas mensagens privadas")
        print("0 - Sair")
        escolha = input("Ação: ")
        try:
            if escolha == "1":
                nome_sala = input("Digite o nome da sala: ")
                print(f"\n{servidor.Criar_sala(nome_sala)}")
            elif escolha == "2":
                salas = servidor.Listar_salas()
                if salas:
                    print("\nSalas disponíveis:")
                    for sala in salas:
                        print(f"- {sala}")
                    nome_sala = input("Digite o nome da sala: ")
                    print(f"\n{servidor.Entrar_na_sala(usuario_id, nome_sala)}")
                    sala_atual = nome_sala
                else:
                    print("Nenhuma sala disponível.")
            elif escolha == "3":
                if sala_atual:
                    print(f"\n{servidor.Sair_da_sala(usuario_id, sala_atual)}")
                    sala_atual = None
                else:
                    print("Você não está em nenhuma sala.")
            elif escolha == "4":
                if sala_atual:
                    mensagem = input("Digite sua mensagem pública: ")
                    print(f"\n{servidor.Enviar_mensagem(usuario_id, sala_atual, mensagem)}")
                else:
                    print("Você precisa entrar em uma sala primeiro.")
            elif escolha == "5":
                if sala_atual:
                    mensagens = servidor.Listar_mensagens(sala_atual)
                    print("\nMensagens públicas:")
                    if mensagens:
                        for mensagem, usuario, timestamp in mensagens:
                            print(f"[{timestamp}] {usuario}: {mensagem}")
                    else:
                        print("Nenhuma mensagem pública disponível.")
                else:
                    print("Você precisa entrar em uma sala primeiro.")
            elif escolha == "6":
                if sala_atual:
                    usuarios = servidor.Listar_usuarios(sala_atual)
                    print("\nUsuários ativos:")
                    for usuario in usuarios:
                        print(f"- {usuario['nome']} (ID: {usuario['id']})")
                    try:
                        destinatario_id = int(input("\nDigite o ID do destinatário: "))
                        mensagem = input("Digite a mensagem privada: ")
                        print(f"\n{servidor.Enviar_mensagem_usuario(usuario_id, destinatario_id, sala_atual, mensagem)}")
                    except ValueError:
                        print("ID inválido. Por favor, digite um número.")
                else:
                    print("Você precisa entrar em uma sala primeiro.")
            elif escolha == "7":
                if sala_atual:
                    usuarios = servidor.Listar_usuarios(sala_atual)
                    print("\nUsuários ativos na sala:")
                    if usuarios:
                        for usuario in usuarios:
                            print(f"- {usuario['nome']} (ID: {usuario['id']})")
                    else:
                        print("Nenhum usuário ativo no momento.")
                else:
                    print("Você precisa entrar em uma sala primeiro.")
            elif escolha == "8":
                if sala_atual:
                    mensagens_privadas = servidor.Listar_mensagens_privadas(usuario_id, sala_atual)
                    print("\nMinhas mensagens privadas:")
                    if mensagens_privadas:
                        for remetente, mensagem in mensagens_privadas:
                            print(f"De {remetente}: {mensagem}")
                    else:
                        print("Nenhuma mensagem privada recebida.")
                else:
                    print("Você precisa entrar em uma sala primeiro.")
            elif escolha == "0":
                if sala_atual:
                    print(f"\n{servidor.Sair_da_sala(usuario_id, sala_atual)}")
                break
            else:
                print("Escolha inválida. Tente novamente.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    cliente_chat()