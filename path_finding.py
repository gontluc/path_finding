import pygame
from path_algorithm import * 

pygame.init()

WIDTH, HEIGHT = 630, 660
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Finding")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED   = (255, 0, 0)
GREY  = (169, 169,169)
BLUE  = (0, 0, 255)
LIGHT_BLUE = (30, 144, 255)

FPS = 60
pygame.font.init()

yes_button = pygame.image.load("images/yes_button.png").convert_alpha()
no_button = pygame.image.load("images/no_button.png").convert_alpha()

class Button:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        # Change origin rect from 0,0 to x,y
        self.rect.left = x
        self.rect.top = y

    def draw(self):
        window.blit(self.image, (self.x ,self.y))


def buttons():
    yes = Button(yes_button, 360, 10)
    yes.draw()
    no = Button(no_button, 435,10)
    no.draw()

    pygame.display.update()

    done = True
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            # Q to QUIT
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_q]:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if pygame.Rect.collidepoint(yes.rect, x, y):
                    done = False
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    return True
                if pygame.Rect.collidepoint(no.rect, x, y):
                    done = False
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    return False
            
            # Change cursor while on top of buttons
            x,y = pygame.mouse.get_pos()
            if pygame.Rect.collidepoint(yes.rect, x, y) or pygame.Rect.collidepoint(no.rect, x, y):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else: 
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

def send_text(text):
    txt = pygame.font.Font.render(pygame.font.SysFont("calibri", 20, True), text, True, BLACK)
    window.blit(txt,(15,15))
    pygame.display.update()


def get_square(x,y):
    x = x - (x % 15)
    y = y - (y % 15)
    return (x,y)


def getA():
    done = True
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            # If mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()

                # If inside window 
                if (x >= 15) and (x < 615) and (y >= 45) and (y < 645):
                    global point_A
                    point_A = get_square(x,y)   
                    done = False

            # Q to QUIT
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_q]:
                exit()


def getB(visualize):
    done = True
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            # If mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()

                # If inside window 
                if (x >= 15) and (x < 615) and (y >= 45) and (y < 645):
                    x,y = get_square(x,y) 
                    if (x,y) == point_A:
                        draw_window(visualize)
                        send_text("Please choose a different point")
                    else:
                        global point_B
                        point_B = (x,y)    
                        done = False

            # Q to QUIT
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_q]:
                exit()


def getObstacles():
    done = True
    mouse_position = ()
    global obstacles
    while done:
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                keys_pressed = pygame.key.get_pressed()

                # Hit ENTER to stop drawing obstacles       
                if keys_pressed[pygame.K_RETURN]:
                    done = False
                    obstacles.sort()

                # Q to QUIT
                if keys_pressed[pygame.K_q]:
                    exit()

            # Draw Mouse
            x,y = pygame.mouse.get_pos()
            x,y = get_square(x,y)
            if (x >= 15) and (x < 615) and (y >= 45) and (y < 645) and (x,y) != point_A and (x,y) != point_B and ((x,y) not in obstacles):

                if (x,y,15,15) != mouse_position and mouse_position != ():
                    pygame.draw.rect(window, WHITE, mouse_position)

                pygame.draw.rect(window, GREY, (x,y,15,15))
                mouse_position = (x+1,y+1,14,14)
                pygame.display.update()
                
            else:
                if mouse_position != () and ((x,y) == point_A or (x,y) == point_B):
                    pygame.draw.rect(window, WHITE, mouse_position)
                    pygame.display.update()

                if mouse_position != ():
                    pygame.draw.rect(window, WHITE, mouse_position)
                    pygame.display.update()
            

            # Draw holding Left click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x,y = pygame.mouse.get_pos()
                    if (x >= 15) and (x < 615) and (y >= 45) and (y < 645):
                        x,y = get_square(x,y)
                        done2 = True
                        while done2:
                            if (x,y) != point_A and (x,y) != point_B:
                                pygame.draw.rect(window, GREY, (x,y,15,15))
                                mouse_position = ()
                                pygame.display.update()
                                
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONUP:
                                    done2 = False

                            x,y = pygame.mouse.get_pos()
                            x,y = get_square(x,y)

                            if (x >= 15) and (x < 615) and (y >= 45) and (y < 645):
                                if (x,y) not in obstacles and (x,y) != point_A and (x,y) != point_B:
                                    obstacles.append((x,y))
        
        
def draw_point(point):
    x,y = point
    pygame.draw.rect(window, BLUE, (x+1,y+1,14,14) )


def draw_obstacles(obstacles):
    for i in obstacles:
        x,y = i
        pygame.draw.rect(window, GREY, (x+1,y+1,14,14) )


def draw_array(array, color):
    for i in array:
        if i != point_A:
            x,y = i
            pygame.draw.rect(window, color, (x+1,y+1,14,14))


def draw_path():
    x,y = point_B
    done = True
    while done:
        for p in parents:
            if p[0] == (x,y):
                x,y = p[1]
                if (x,y) != point_A:
                    pygame.draw.rect(window, BLUE, (x+1,y+1,14,14))
                else:
                    done = False


def draw_window(visualize):

    window.fill(WHITE)

    # Borders
    pygame.draw.rect(window, GREY, ((0,0),(630,15+30)))
    pygame.draw.rect(window, GREY, ((0,615+30),(630,630+30)))
    pygame.draw.rect(window, GREY, ((0,0+30),(15,630+30)))
    pygame.draw.rect(window, GREY, ((615,0+30),(630,630+30)))

    # Grid
    for i in range(15,620,15):
        pygame.draw.aaline(window, GREY, (15,i+30), (615,i+30))
        pygame.draw.aaline(window, GREY, (i,15+30), (i,615+30))

    try:
        draw_point(point_A)
        draw_point(point_B)
        draw_obstacles(obstacles)
        if visualize:
            draw_array(neighbours, GREEN)
            draw_array(nodes, RED)
    except:
        pass

    if not finding_point_B:
        draw_path()
    
    pygame.display.update()


def main():
    global finding_point_B

    run = True
    clock = pygame.time.Clock()

    have_A = False
    have_B = False
    have_obstacles = False
    have_visualize = False
    start_aux = False
    visualize = False
    ended = False
    not_possible = False

    initial_len = 0
    final_len = 0

    draw_window(visualize)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_q]:
            run = False

        while not have_A:
            send_text("Please choose the start point")

            getA() 
            have_A = True

            draw_window(visualize)
            send_text(f"Point A: {point_A}")
            pygame.time.delay(1500)

            while not have_B:
                draw_window(visualize)
                send_text("Please choose the end point")

                getB(visualize) 
                have_B = True

                draw_window(visualize)
                send_text(f"Point B: {point_B}")
                pygame.time.delay(1500)

                while not have_obstacles:
                    draw_window(visualize)
                    send_text("Please draw obstacles and hit ENTER")

                    getObstacles()
                    have_obstacles = True
        
        while have_obstacles and not have_visualize:
            draw_window(visualize)
            send_text("Do you want to visualize the algorithm?")
            visualize = buttons()
            have_visualize = True
            start_aux = True
        
        if start_aux:
            draw_window(visualize)
            send_text("Finding shortest path...")

            start = time.perf_counter()

            first_neighbours(obstacles, point_A)

            finding_point_B = found_B(point_B)

            if visualize:
                draw_window(visualize)
                send_text("Finding shortest path...")
            start_aux = False

        if finding_point_B and not not_possible:
            # Add neighbours to priority_queue
            add_neighbours(point_A, point_B)         

            # Execute priority_queue = neighbours --> nodes
            initial_len = len(nodes)

            execute()

            final_len = len(nodes)
            not_possible = final_len == initial_len

            # Go through all nodes to find new neighbours
            new_neighbours(obstacles)

            finding_point_B = found_B(point_B)

        # Draw
        if (visualize or not finding_point_B) and not not_possible:
            draw_window(visualize)
            if not finding_point_B:
                if not ended:
                    end = time.perf_counter()
                    finish_txt = f"Done in {round(end - start,1)} seconds!   Distance of path: {round(g(point_B, point_A),1)} units."
                    send_text(finish_txt)
                    pygame.time.delay(150)
                    ended = True
                else:
                    send_text(finish_txt)
                    pygame.time.delay(150)
            else:
                send_text("Finding shortest path...")
        elif not_possible:
            draw_window(visualize)
            send_text("Can't find a path. Please try again")
            pygame.time.delay(150)
        
    pygame.quit()


main()
