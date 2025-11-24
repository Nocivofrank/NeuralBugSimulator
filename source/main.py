import pygame, threading
from GraphFunctions import Graph
from BugFunctions import Bug

# Shared Data for Graph
shared_data = {
    "time": [],
    "energy": [],
    "bugCount": [],
    "radius_avg": [],
    "immortals": []
}

#Creates the threading lock that way i can call function on diff thread
lock = threading.Lock()

#Creating a graph class from the GraphFunctions.py file
Graph = Graph()
Graph.set_data_sources(lock, shared_data)

def Simulation():
    #initializing pygame
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    clock = pygame.time.Clock()
    running = True
    delta_Time = 1000
    world_speed = 1000
    bug_age_Counter = 0

    #setting universe Attributes
    universe_energy_max = 10000
    universe_energy = [universe_energy_max]

    #font initialization
    ui_Font = pygame.font.SysFont("arial", 50)
    bug_stat_font = pygame.font.SysFont("arial", 10)
    scroll_wheel_value = 100

    Bug.screenHeight = screen.get_height()
    Bug.screenWidth = screen.get_width()

    #this is where you will put all the code for the bug creation thing
    bugs = []
    bug_checker = []
    prev_gen_best = None
    best_bug = None

    amount_of_bugs = 150
    bugs_dead = False
    Bug.create_bug_amount(amount_of_bugs , bugs, universe_energy, True)

    generation = 0

    mouse_pos = pygame.Vector2(Bug.random_range(0 , screen.get_width()) ,Bug.random_range(0 , screen.get_height()))
    mouse_direction = pygame.Vector2(Bug.random_range(-1 , 1), Bug.random_range(-1 , 1))

    mouseR = 25
    mouseColor = ( 0 , 255 , 255)
    

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    scroll_wheel_value += 10
                elif event.y < 0:
                    scroll_wheel_value -= 10
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    world_speed *= 10
                elif event.key == pygame.K_DOWN:
                    world_speed /= 10
                elif event.key == pygame.K_SPACE:
                    world_speed = 1000
        bug_age = ui_Font.render(f"Generation : {generation}", True, (255, 255, 255))
        if prev_gen_best:
            bug_age = ui_Font.render(f"Generation : {generation}, Best Bug Time: {prev_gen_best.time_alive:.2f}, Current Best: {best_bug.time_alive}", True, (255, 255, 255))     
        
        # mouse_pos = pygame.mouse.get_pos()
        screen.fill("black")        
        
        pygame.draw.circle(screen, mouseColor, mouse_pos, mouseR)

        amount = int(300 / world_speed)
        if amount <= 0:
            amount = 1
        for i in range(amount):
            mouse_pos[1] += mouse_direction[1] * delta_Time * 2
            mouse_pos[0] += mouse_direction[0] * delta_Time * 2
            if mouse_pos[1] > screen.get_height():
                mouse_pos[1] = 10
            if mouse_pos[0] > screen.get_width():
                mouse_pos[0] = 10
            if mouse_pos[1] < 0:
                mouse_pos[1] = screen.get_height() - 10
            if mouse_pos[0] < 0:
                mouse_pos[0] = screen.get_width() - 10    
            Bug.mouse_stat_pos(mouse_pos, mouse_direction , scroll_wheel_value)
            if len(bugs) != 0:
                for b in bugs:
                    if not b.dead:
                        b._update(delta_Time, screen, universe_energy, bugs)
                        b._draw(screen, bug_stat_font)                
                    if b.dead:
                        bug_checker.append(b)
                        bugs.remove(b)
            if bugs_dead:
                best_bug = bug_checker[0]
                for b in bug_checker:
                    if b.time_alive > best_bug.time_alive:
                        best_bug = b
                if prev_gen_best == None:
                    prev_gen_best = best_bug
                if best_bug.time_alive > prev_gen_best.time_alive:
                    prev_gen_best = best_bug
                    Bug.create_bug_amount(amount_of_bugs, bugs, universe_energy, True, prev_gen_best.brain)
                else:
                    Bug.create_bug_amount(int(amount_of_bugs / 2), bugs, universe_energy, True, prev_gen_best.brain)
                    Bug.create_bug_amount(int(amount_of_bugs), bugs, universe_energy, True, best_bug.brain)

                bugs_dead = False

        if len(bugs) <= 0:
            generation += 1
            mouse_direction = pygame.Vector2(Bug.random_range(-1 , 1), Bug.random_range(-1 , 1))
            # mouse_pos = pygame.Vector2(Bug.random_range(0 , screen.get_width()) ,Bug.random_range(0 , screen.get_height()))
            bugs_dead = True

        screen.blit(bug_age, (50 , 50))

        if len(bugs) <= 0:
            bugs_dead = True

        # Flip display
        pygame.display.flip()

        # Cap FPS and get delta time
        delta_Time = clock.tick(120) / world_speed

    pygame.quit()

threading.Thread(target=Simulation, daemon=True).start()
Graph.run()