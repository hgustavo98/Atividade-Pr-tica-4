import xmlrpc.client


def cliente_chat():
    servidor = xmlrpc.client.ServerProxy("http://localhost:8000/RPC2")

    nome = input("Digite seu nome para ingressar no sistema: ")
    usuario_id = servidor.Ingressar_no_sistema(nome)
    print(
        f"\nBem-vindo, {nome}! Seu ID é {usuario_id}. Agora você está conectado ao sistema.")

    while True:
        print("\nEscolha uma ação:")
        print("1 - Entrar na sala")
        print("2 - Sair da sala")
        print("3 - Enviar mensagem pública")
        print("4 - Listar mensagens públicas")
        print("5 - Enviar mensagem privada")
        print("6 - Listar usuários ativos")
        print("7 - Listar minhas mensagens privadas")
        print("0 - Sair")

        escolha = input("Ação: ")

        if escolha == "1":
            print(f"\n{servidor.Entrar_na_sala(usuario_id)}")

        elif escolha == "2":
            print(f"\n{servidor.Sair_da_sala(usuario_id)}")

        elif escolha == "3":
            mensagem = input("Digite sua mensagem pública: ")
            print(f"\n{servidor.Enviar_mensagem(usuario_id, mensagem)}")

        elif escolha == "4":
            mensagens = servidor.Listar_mensagens()
            print("\nMensagens públicas:")
            if mensagens:
                for mensagem, usuario, timestamp in mensagens:
                    print(f"[{timestamp}] {usuario}: {mensagem}")
            else:
                print("Nenhuma mensagem pública disponível.")

        elif escolha == "5":
            usuarios = servidor.Listar_usuarios()
            print("\nUsuários ativos:")
            for usuario in usuarios:
                print(f"- {usuario['nome']} (ID: {usuario['id']})")

            try:
                destinatario_id = int(input("\nDigite o ID do destinatário: "))
                mensagem = input("Digite a mensagem privada: ")
                print(f"\n{servidor.Enviar_mensagem_usuario(
                    usuario_id, destinatario_id, mensagem)}")
            except ValueError:
                print("ID inválido. Por favor, digite um número.")

        elif escolha == "6":
            usuarios = servidor.Listar_usuarios()
            print("\nUsuários ativos na sala:")
            if usuarios:
                for usuario in usuarios:
                    print(f"- {usuario['nome']} (ID: {usuario['id']})")
            else:
                print("Nenhum usuário ativo no momento.")

        elif escolha == "7":
            mensagens_privadas = servidor.Listar_mensagens_privadas(usuario_id)
            print("\nMinhas mensagens privadas:")
            if mensagens_privadas:
                for remetente, mensagem in mensagens_privadas:
                    print(f"De {remetente}: {mensagem}")
            else:
                print("Nenhuma mensagem privada recebida.")

        elif escolha == "0":
            print(f"\n{servidor.Sair_da_sala(usuario_id)}")
            break
        else:
            print("Escolha inválida. Tente novamente.")


cliente_chat()
