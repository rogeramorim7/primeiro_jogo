import pygame
from pygame import mixer
from time import sleep
from random import randint

pygame.init()

# Inicializar a fonte para a pontuação
pygame.font.init()
fonte = pygame.font.SysFont('Arial', 30)

janela = pygame.display.set_mode([800, 600])
pygame.display.set_caption('FIRST GAME PROJECT.EXE')

imagem_fundo = pygame.image.load('D:\\workspace\\python\\pygame\\space bg game.png')
imagem_fundo = pygame.transform.scale(imagem_fundo, (800, 600))  # Redimensionar o fundo
nave_jogador = pygame.image.load('D:\\workspace\\python\\pygame\\sprite_nave_pequena.png')
nave_inimiga = pygame.image.load('D:/workspace/python\\pygame/nave_inimiga_pequena.png')

# Posição e velocidade da nave
pos_y_jogador = 350
pos_x_jogador = 420
vel_nave_jogador = 10

# Posição e velocidade da nave inimiga
pos_y_inimigo = 50
pos_x_inimigo = 430
vel_nave_inimigo = 5  # Velocidade inicial

# Controle da direção (inimigo vai apenas para a esquerda e direita)
direcao_inimigo = 1  # 1 para mover para a direita, -1 para mover para a esquerda

# Lista para disparos
disparos = []
vel_disparo = -15  # Velocidade dos disparos (movem para cima)

# Cor do disparo
cor_disparo = (255, 0, 0)  # Vermelho
tamanho_disparo = (5, 10)  # Largura e altura do disparo

# Inicializar a pontuação
pontuacao = 0

# Variável para controlar o estado da nave inimiga (viva ou destruída)
nave_inimiga_ativa = True
tempo_vida_explosao = 0  # Controla o tempo que a explosão fica visível

# Função para verificar colisão entre as naves
def verificar_colisao(x1, y1, largura1, altura1, x2, y2, largura2, altura2):
    if x1 < x2 + largura2 and x1 + largura1 > x2 and y1 < y2 + altura2 and y1 + altura1 > y2:
        return True
    return False

# Loop principal
loop = True
while loop:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            loop = False

    teclas = pygame.key.get_pressed()

    # Movimentação do jogador
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:  # Seta para cima ou W
        pos_y_jogador -= vel_nave_jogador
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:  # Seta para baixo ou S
        pos_y_jogador += vel_nave_jogador
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:  # Seta para esquerda ou A
        pos_x_jogador -= vel_nave_jogador
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:  # Seta para direita ou D
        pos_x_jogador += vel_nave_jogador

    # Limitar movimentação do jogador
    if pos_y_jogador <= -10:
        pos_y_jogador = -10
    if pos_y_jogador >= 504:
        pos_y_jogador = 504
    if pos_x_jogador <= -3:
        pos_x_jogador = -3
    if pos_x_jogador >= 711:
        pos_x_jogador = 711

    # Movimento automático da nave inimiga (somente na direção horizontal)
    if nave_inimiga_ativa:
        pos_x_inimigo += vel_nave_inimigo * direcao_inimigo

    # Inverter direção ao atingir os limites da tela
    if pos_x_inimigo <= 0:  # Limite esquerda
        direcao_inimigo = 1  # Ir para a direita
    elif pos_x_inimigo >= 710:  # Limite direita
        direcao_inimigo = -1  # Ir para a esquerda

    # Verificar colisão entre a nave do jogador e a nave inimiga
    if verificar_colisao(pos_x_jogador, pos_y_jogador, nave_jogador.get_width(), nave_jogador.get_height(),
                         pos_x_inimigo, pos_y_inimigo, nave_inimiga.get_width(), nave_inimiga.get_height()):
        pontuacao -= 10  # Perder 10 pontos quando as naves se encostam
        # Reposicionar a nave inimiga em um local aleatório
        pos_y_inimigo = randint(0, 500)
        pos_x_inimigo = randint(0, 700)

    # Criar disparo
    if teclas[pygame.K_SPACE]:  # Barra de espaço para atirar
        disparos.append([pos_x_jogador + 30, pos_y_jogador])  # Adiciona disparo no centro da nave

    # Atualizar posição dos disparos
    for disparo in disparos:
        disparo[1] += vel_disparo  # Move o disparo para cima

        # Verificar se o disparo atingiu o inimigo
        if disparo[1] < pos_y_inimigo + nave_inimiga.get_height() and disparo[0] > pos_x_inimigo and disparo[0] < pos_x_inimigo + nave_inimiga.get_width():
            disparos.remove(disparo)  # Remover disparo
            pos_y_inimigo = randint(0, 500)
            pos_x_inimigo = randint(0, 700)
            # Mantém o inimigo ativo para continuar movendo
            tempo_vida_explosao = pygame.time.get_ticks()  # Marcar o tempo da explosão
            pontuacao += 10  # Incrementar a pontuação

    # Remover disparos que saíram da tela
    disparos = [disparo for disparo in disparos if disparo[1] > 0]

    # Atualizar a tela
    janela.blit(imagem_fundo, [0, 0])  # Fundo
    janela.blit(nave_jogador, [pos_x_jogador, pos_y_jogador])  # Nave do jogador

    # Desenhar nave inimiga
    janela.blit(nave_inimiga, [pos_x_inimigo, pos_y_inimigo])  # Nave do inimigo

    # Desenhar disparos
    for disparo in disparos:
        pygame.draw.rect(janela, cor_disparo, (disparo[0], disparo[1], *tamanho_disparo))

    # Exibir a pontuação na tela
    texto_pontuacao = fonte.render(f'Pontuação: {pontuacao}', True, (255, 255, 255))
    janela.blit(texto_pontuacao, (10, 10))  # Posicionar no canto superior esquerdo

    pygame.display.update()

pygame.quit()
