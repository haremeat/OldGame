import random
import pygame

# 하늘에서 내려오는 적 피하기 게임
################################################
# 기본 초기화 (반드시 해야 하는 것들)

pygame.init()

# 화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Fall Game")

# FPS
clock = pygame.time.Clock()
################################################

# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 폰트 등)

# 배경 이미지 불러오기
background = pygame.image.load("D:/pygameProject/Assets/background.png")

# sprite(캐릭터) 불러오기
character = pygame.image.load("D:/pygameProject/Assets/character.png")
character_size = character.get_rect().size # 이미지 크기를 구해 옴
character_width = character_size[0]
character_height = character_size[1]
# character_x_pos = (screen_width / 2) - (character_width / 2) # 화면 중앙에 위치
character_x_pos = (screen_width)
character_y_pos = (screen_height - character_height) # 가장 아래 위치

# 이동할 좌표
to_x = 0
to_y = 0

enemy_to_x = 0
enemy_to_y = 0

# 이동 속도
character_speed = 0.6

# 적 enemy 캐릭터
# enemies = []
enemy = pygame.image.load("D:/pygameProject/Assets/enemy.png")
enemy_size = enemy.get_rect().size  # 이미지 크기를 구해 옴
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = random.randrange(0, (screen_width - enemy_width))
enemy_y_pos = 0
enemy_speed = 10

# random.shuffle(enemies)
# for i in range(5):
#     enemies.append(enemy)

# 폰트 정의
game_font = pygame.font.Font(None, 40) # 폰트 객체 생성 (폰트, 크기)

# 총 시간
total_time = 20

# 시간 계산
start_ticks = pygame.time.get_ticks() # 현재 tick을 받아 옴


# 이벤트 루프
running = True # 게임 진행중인가?
while running:
    dt = clock.tick(60) # 게임 화면의 초당 프레임 수를 설정

    # fps check
    # print("fps : " + str(clock.get_fps()))

    for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가?
            running = False # 게임이 진행중이 아님

        if event.type == pygame.KEYDOWN: # 키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
            elif event.key == pygame.K_UP:
                to_y -= character_speed
            elif event.key == pygame.K_DOWN:
                to_y += character_speed

        if event.type == pygame.KEYUP: # 방향키를 떼면 멈춤
            if event.type == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.type == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0

    # 캐릭터 좌표값 이동
    character_x_pos += to_x * dt
    character_y_pos += to_y * dt

    # 적 좌표값 이동
    enemy_y_pos += enemy_speed

    # 적이 화면 밖으로 나가면 재생성
    if enemy_y_pos > screen_height:
        enemy_y_pos = 0
        enemy_x_pos = random.randrange(0, (screen_width - enemy_width))

    # 가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > (screen_width - character_width):
        character_x_pos = (screen_width - character_width)

    # 세로 경계값 처리
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > (screen_height - character_height):
        character_y_pos = (screen_height - character_height)


    # 충돌 처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    # 충돌 체크
    if character_rect.colliderect(enemy_rect):
        print("collide")
        running = False

    #screen.fill((0,0,255))
    screen.blit(background, (0, 0)) # 배경 그리기
    # 캐릭터 그리기
    screen.blit(character, (character_x_pos, character_y_pos))
    # screen.blit(character, (random.randrange(0, screen_width), random.randrange(0, screen_height)))
    # 적 캐릭터 그리기
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

    # 타이머 집어 넣기
    # 경과 시간(ms) 계산 (1000으로 나누어서 초(s)로 환산)
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000

    # 출력할 글자, True, 글자 색상
    timer = game_font.render(str(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    if (total_time - elapsed_time) <= 0:
        print("Time out")
        running = False

    pygame.display.update() # 게임 화면 다시 그리기 (필수)

# 게임 종료 전 잠시 대기 (2초 대기)
pygame.time.delay(2000)

# pygame 종료
pygame.quit()
