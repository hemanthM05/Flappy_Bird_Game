import pygame, sys, random 


def game_floor():
    screen.blit(floor_base,(floor_x_pos,900))
    screen.blit(floor_base,(floor_x_pos+576,900))


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
        if bird_rect.top <= -100 or bird_rect.bottom >=900:
            return False
    return True

  
def create_pipe():
    random_pipe_pos=random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe=pipe_surface.get_rect(midbottom = (700,random_pipe_pos-300))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 5
	return pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 900:
		    screen.blit(pipe_surface,pipe)
		else: 
		    flip_pipe = pygame.transform.flip(pipe_surface,False,True)
		    screen.blit(flip_pipe,pipe)





#display
def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(f'score: {str(int(score))}',True,(0,0,0))
		score_rect = score_surface.get_rect(center = (430,50))
		screen.blit(score_surface,score_rect)
	if game_state == 'game_over':
		score_surface = game_font.render(f'Score : {int(score)}' ,True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,680))
		screen.blit(score_surface,score_rect)
		
		dis_game_over = game_font.render(f'GAME OVER' ,True,(255,255,0))
		dis_game_over_rect = dis_game_over.get_rect(center = (288,360))
		screen.blit(dis_game_over,dis_game_over_rect)

		display_message = game_font.render(f'TAP TO PLAY' ,True,(255,0,0))
		display_message_rect = dis_game_over.get_rect(center = (265,430))
		screen.blit(display_message,display_message_rect)


		high_score_surface = game_font.render(f'High score : {int(high_score)}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (288,750))
		screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score
	
	
	
def pipe_score_check():
	global score, can_score 
	if pipe_list:
		for pipe in pipe_list:
			if 95 < pipe.centerx < 101 and can_score:
				score += 1
				#score_sound.play()
				can_score = False
			if pipe.centerx < 0:
				can_score = True

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)

pygame.init()
screen = pygame.display.set_mode((576,850))
clock = pygame.time.Clock()

game_font = pygame.font.Font('fontBold.otf',40)


# Game Variables
gravity = 0.15
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

bg_surface = pygame.image.load('background.jpg').convert()
bg_surface = pygame.transform.scale2x(bg_surface)


bird = pygame.image.load("bird.png").convert_alpha()
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100,512))

floor_base=pygame.image.load("base.png").convert()
floor_base = pygame.transform.scale2x(floor_base)

floor_x_pos =0 

message=pygame.image.load("message.jpg").convert_alpha()
message = pygame.transform.scale2x(message)
game_over_rect = message.get_rect(center=(288,512))


pipe_surface = pygame.image.load('pipe.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
#pipe_height = 300
pipe_height = [400,600,800]

game_active = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()    
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
                #flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                # game_active = True
				# pipe_list.clear()
                bird_rect.center = (100,512)
                bird_movement = 0
                pipe_list.clear()
                game_active=True
                score=0
                
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())
    screen.blit(bg_surface,(0,0))
	
    if game_active:
        bird_movement +=gravity
        bird_rect.centery += bird_movement
        screen.blit(bird,bird_rect)
        pipe_list=move_pipes(pipe_list)
        draw_pipes(pipe_list)
        game_active=check_collision(pipe_list)
        
        #score
        pipe_score_check()
        score_display("main_game")
    else:
        screen.blit(message,game_over_rect)
        high_score = update_score(score,high_score)
        score_display("game_over")
        #return "Game Over"
    '''
    #base
    floor_x_pos -=1
    game_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0
    '''
    pygame.display.update()
    clock.tick(120)