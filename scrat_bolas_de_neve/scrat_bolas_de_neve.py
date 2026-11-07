import os
import random
import sys

import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()

LARGURA = 1280
ALTURA = 720
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("SCRAT E A NOZ PERDIDA")

clock = pygame.time.Clock()


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


ESTADO_CAPA = 0
ESTADO_MENU = 1
ESTADO_HISTORIA_INICIAL = 2
ESTADO_FASE1 = 3
ESTADO_HISTORIA_FINAL = 4

estado_jogo = ESTADO_CAPA

tempo_capa = pygame.time.get_ticks()
DURACAO_CAPA = 5000

historia_atual = 1
TOTAL_HISTORIAS_INICIAL = 7

fase1_fase = 1
fase1_velocidade_obstaculo = 5
fase1_velocidade_scrat = 7
fase1_em_pausa = True
fase1_tempo_inicio_fase = pygame.time.get_ticks()
DURACAO_PAUSA = 3000
fase1_mostrando_fase = False
fase1_tempo_mostrando_fase = 0
DURACAO_FASE_TELA = 3000
fase1_mostrando_atingido = False
fase1_tempo_atingido = 0
fase1_tempo_inicio = pygame.time.get_ticks()
fase1_duracao_fases = {1: 18, 2: 12, 3: 10, 4: 10, 5: 5}

fonte_contador = pygame.font.SysFont(None, 50)

capa = pygame.transform.scale(
    pygame.image.load(resource_path("assets/capa.png")).convert_alpha(), (LARGURA, ALTURA))

hist1 = pygame.image.load(resource_path("assets/história1.png")).convert_alpha()
hist2 = pygame.image.load(resource_path("assets/história2.png")).convert_alpha()
hist3 = pygame.image.load(resource_path("assets/história3.png")).convert_alpha()
hist4 = pygame.image.load(resource_path("assets/história4.png")).convert_alpha()
hist5 = pygame.image.load(resource_path("assets/história5.png")).convert_alpha()
hist6 = pygame.image.load(resource_path("assets/história6.png")).convert_alpha()
hist7 = pygame.image.load(resource_path("assets/história7.png")).convert_alpha()
hist8 = pygame.image.load(resource_path("assets/história8.png")).convert_alpha()
hist9 = pygame.image.load(resource_path("assets/história9.png")).convert_alpha()
hist10 = pygame.image.load(resource_path("assets/história10.png")).convert_alpha()

fase1_img = pygame.transform.scale(
    pygame.image.load(resource_path("assets/fase1.png")).convert_alpha(), (LARGURA, ALTURA))
fase2_img = pygame.transform.scale(
    pygame.image.load(resource_path("assets/fase2.png")).convert_alpha(), (LARGURA, ALTURA))
fase3_img = pygame.transform.scale(
    pygame.image.load(resource_path("assets/fase3.png")).convert_alpha(), (LARGURA, ALTURA))
fase4_img = pygame.transform.scale(
    pygame.image.load(resource_path("assets/fase4.png")).convert_alpha(), (LARGURA, ALTURA))
fase5_img = pygame.transform.scale(
    pygame.image.load(resource_path("assets/fase5.png")).convert_alpha(), (LARGURA, ALTURA))

atingido_img = pygame.transform.scale(
    pygame.image.load(resource_path("assets/derrota.png")).convert_alpha(), (LARGURA, ALTURA))
vitoria_img = pygame.transform.scale(
    pygame.image.load(resource_path("assets/vitória.png")).convert_alpha(), (LARGURA, ALTURA))

fundo_fase1 = pygame.transform.scale(
    pygame.image.load(resource_path("assets/fundo10.jpg")).convert_alpha(), (LARGURA, ALTURA))

esquilo_sheet = pygame.image.load(resource_path("artes/esquilos_corre.png")).convert_alpha()
TAM_SCRAT = (127, 94)
fase1_frames_direita = []
for _x, _y in [(0, 0), (318, 0), (0, 237), (318, 237)]:
    quadro = esquilo_sheet.subsurface((_x, _y, 318, 237))
    fase1_frames_direita.append(pygame.transform.scale(quadro, TAM_SCRAT))
fase1_frames_esquerda = [pygame.transform.flip(q, True, False) for q in fase1_frames_direita]
fase1_frame_idx = 0
scrat_virado_direita = True
scrat_img = fase1_frames_direita[0]
scrat_rect = scrat_img.get_rect(midbottom=(LARGURA // 2, ALTURA - 100))

fonte_decisao = pygame.font.SysFont(None, 60)
sombra_decisao = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
sombra_decisao.fill((0, 0, 0, 150))
txt_jogar = fonte_decisao.render("Aperte J para jogar novamente", True, (255, 255, 255))
txt_menu = fonte_decisao.render("Aperte M para voltar ao menu", True, (255, 255, 255))

obstaculo_img = pygame.transform.scale(
    pygame.image.load(resource_path("assets/neve11.png")).convert_alpha(), (60, 60))
fase1_obstaculos = []

menu_img = pygame.transform.scale(
    pygame.image.load(resource_path("artes/escolha.png")).convert_alpha(), (LARGURA, ALTURA))

musica_loop = pygame.mixer.Sound(resource_path('efeitos sonoros/music_loop.ogg'))
musica_loop.set_volume(0.8)
music_menu = pygame.mixer.Sound(resource_path('efeitos sonoros/music_menu.ogg'))
music_menu.set_volume(0.7)
som_colisao = pygame.mixer.Sound(resource_path('efeitos sonoros/som_morte.wav'))
som_colisao.set_volume(1)

CRIAR_OBSTACULO = pygame.USEREVENT
pygame.time.set_timer(CRIAR_OBSTACULO, 1000)


def resetar_fase1():
    global fase1_fase, fase1_velocidade_obstaculo, fase1_em_pausa, fase1_obstaculos
    global fase1_mostrando_fase, fase1_mostrando_atingido, scrat_rect
    fase1_fase = 1
    fase1_velocidade_obstaculo = 5
    fase1_em_pausa = True
    fase1_mostrando_fase = False
    fase1_mostrando_atingido = False
    fase1_obstaculos.clear()
    scrat_rect.midbottom = (LARGURA // 2, ALTURA - 100)
    pygame.time.set_timer(CRIAR_OBSTACULO, 1000)


music_menu.play(-1)

rodando = True
while rodando:
    clock.tick(45)
    tempo_atual = pygame.time.get_ticks()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN and estado_jogo == ESTADO_FASE1 and fase1_mostrando_atingido:
            if evento.key == pygame.K_j:
                fase1_mostrando_atingido = False
                resetar_fase1()
                fase1_tempo_inicio_fase = tempo_atual
                fase1_tempo_inicio = tempo_atual
            elif evento.key == pygame.K_m:
                fase1_mostrando_atingido = False
                resetar_fase1()
                estado_jogo = ESTADO_MENU
                historia_atual = 0
                musica_loop.stop()
                music_menu.play(-1)
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if estado_jogo == ESTADO_HISTORIA_INICIAL:
                    historia_atual += 1
                    if historia_atual > TOTAL_HISTORIAS_INICIAL:
                        estado_jogo = ESTADO_FASE1
                        resetar_fase1()
                        fase1_tempo_inicio_fase = tempo_atual
                        fase1_tempo_inicio = tempo_atual
                elif estado_jogo == ESTADO_HISTORIA_FINAL:
                    historia_atual += 1
                    if historia_atual > 10:
                        historia_atual = 0
                        estado_jogo = ESTADO_MENU
                        musica_loop.stop()
                        music_menu.play(-1)

            if estado_jogo == ESTADO_MENU:
                if evento.key == pygame.K_j:
                    music_menu.stop()
                    musica_loop.play(-1)
                    estado_jogo = ESTADO_HISTORIA_INICIAL
                    historia_atual = 1

        if evento.type == CRIAR_OBSTACULO and estado_jogo == ESTADO_FASE1:
            if not fase1_em_pausa and not fase1_mostrando_fase and not fase1_mostrando_atingido:
                x = random.randint(0, LARGURA - 60)
                rect = obstaculo_img.get_rect(topleft=(x, -60))
                fase1_obstaculos.append(rect)

    tela.fill((0, 0, 0))

    if estado_jogo == ESTADO_CAPA:
        tela.blit(capa, (0, 0))
        if tempo_atual - tempo_capa >= DURACAO_CAPA:
            estado_jogo = ESTADO_MENU

    elif estado_jogo == ESTADO_MENU:
        tela.blit(menu_img, (0, 0))

    elif estado_jogo == ESTADO_HISTORIA_INICIAL:
        historias = [None, hist1, hist2, hist3, hist4, hist5, hist6, hist7]
        if historia_atual < len(historias):
            tela.blit(historias[historia_atual], (0, 0))

    elif estado_jogo == ESTADO_FASE1:
        tempo_passado = (tempo_atual - fase1_tempo_inicio) // 1000
        tempo_restante = max(0, fase1_duracao_fases.get(fase1_fase, 30) - tempo_passado)

        if fase1_mostrando_atingido:
            tela.blit(atingido_img, (0, 0))
            tela.blit(sombra_decisao, (0, 0))
            tela.blit(txt_jogar, txt_jogar.get_rect(center=(LARGURA // 2, ALTURA // 2 + 250)))
            tela.blit(txt_menu, txt_menu.get_rect(center=(LARGURA // 2, ALTURA // 2 + 300)))

        elif fase1_mostrando_fase:
            fases_imgs = [None, fase1_img, fase2_img, fase3_img, fase4_img, fase5_img]
            if fase1_fase < len(fases_imgs):
                tela.blit(fases_imgs[fase1_fase], (0, 0))

            if tempo_atual - fase1_tempo_mostrando_fase >= DURACAO_FASE_TELA:
                fase1_mostrando_fase = False
                fase1_em_pausa = False
                fase1_tempo_inicio = tempo_atual

        else:
            if fase1_em_pausa:
                if tempo_atual - fase1_tempo_inicio_fase >= DURACAO_PAUSA:
                    fase1_mostrando_fase = True
                    fase1_tempo_mostrando_fase = tempo_atual

            if not fase1_em_pausa and not fase1_mostrando_fase:
                if tempo_restante == 0:
                    fase1_mostrando_fase = True
                    fase1_tempo_mostrando_fase = tempo_atual
                    fase1_em_pausa = True
                    fase1_obstaculos.clear()
                    fase1_fase += 1

                    if fase1_fase > 5:
                        tela.blit(vitoria_img, (0, 0))
                        pygame.display.flip()
                        pygame.time.wait(3000)
                        historia_atual = 8
                        estado_jogo = ESTADO_HISTORIA_FINAL
                        continue
                    else:
                        velocidades = {2: (9, 500), 3: (13, 400), 4: (15, 350), 5: (17, 300)}
                        if fase1_fase in velocidades:
                            fase1_velocidade_obstaculo, timer = velocidades[fase1_fase]
                            pygame.time.set_timer(CRIAR_OBSTACULO, timer)

                    fase1_tempo_inicio = tempo_atual

            teclas = pygame.key.get_pressed()
            movendo = False
            if not fase1_em_pausa and not fase1_mostrando_fase and not fase1_mostrando_atingido:
                if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                    scrat_rect.x -= fase1_velocidade_scrat
                    scrat_virado_direita = False
                    movendo = True
                elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                    scrat_rect.x += fase1_velocidade_scrat
                    scrat_virado_direita = True
                    movendo = True

            if movendo:
                fase1_frame_idx = (fase1_frame_idx + 0.35) % len(fase1_frames_direita)
            else:
                fase1_frame_idx = 0
            quadros = fase1_frames_direita if scrat_virado_direita else fase1_frames_esquerda
            scrat_img = quadros[int(fase1_frame_idx)]

            scrat_rect.clamp_ip(tela.get_rect())

            if not fase1_em_pausa and not fase1_mostrando_fase and not fase1_mostrando_atingido:
                for obstaculo in fase1_obstaculos:
                    obstaculo.y += fase1_velocidade_obstaculo

            fase1_obstaculos = [o for o in fase1_obstaculos if o.top < ALTURA]

            for obstaculo in fase1_obstaculos:
                if scrat_rect.colliderect(obstaculo) and not fase1_mostrando_atingido:
                    som_colisao.play()
                    fase1_mostrando_atingido = True
                    fase1_tempo_atingido = tempo_atual

            if fase1_mostrando_atingido:
                tela.blit(atingido_img, (0, 0))

            elif fase1_mostrando_fase:
                fases_imgs = [None, fase1_img, fase2_img, fase3_img, fase4_img, fase5_img]
                tela.blit(fases_imgs[fase1_fase], (0, 0))

            else:
                tela.blit(fundo_fase1, (0, 0))
                tela.blit(scrat_img, scrat_rect)

                for obstaculo in fase1_obstaculos:
                    tela.blit(obstaculo_img, obstaculo)

                texto_contador = fonte_contador.render(str(tempo_restante), True, (0, 0, 0))
                tela.blit(texto_contador, (10, 10))

    elif estado_jogo == ESTADO_HISTORIA_FINAL:
        historias = [None, None, None, None, None, None, None, None, hist8, hist9, hist10]
        if historia_atual < len(historias):
            tela.blit(historias[historia_atual], (0, 0))

    pygame.display.flip()

pygame.quit()
