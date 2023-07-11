import pygame
import os
import keyboard
import time
import random


class Board():
    def __init__(self, board, father, level, f_value, i, j):
        self.board = board
        self.father = father
        self.level = level
        self.f_value = f_value
        self.i = i
        self.j = j

    def shuffle(self):
        for _ in range(40):
            while True:
                number = random.randint(1, 4)
                if  number == 1 and self.j != 3:
                    self.board[self.i][self.j] = self.board[self.i][self.j+1]
                    self.board[self.i][self.j+1] = 0
                    self.j += 1
                    break

                if number == 2 and self.j != 0:
                    self.board[self.i][self.j] = self.board[self.i][self.j-1]
                    self.board[self.i][self.j-1] = 0
                    self.j -= 1
                    break
                
                if number == 3 and self.i != 3:
                    self.board[self.i][self.j] = self.board[self.i+1][self.j]
                    self.board[self.i+1][self.j] = 0
                    self.i += 1
                    break
                    
                if number == 4 and self.i != 0:
                    self.board[self.i][self.j] = self.board[self.i-1][self.j]
                    self.board[self.i-1][self.j] = 0
                    self.i -= 1
                    break
                    

    def copy(self, board):
        aux = []
        for i in board:
            a = []
            for j in i:
                a.append(j)
            aux.append(a)
        return aux

    def generateChild(self):
        children = []

        if self.j != 3:
            aux = self.copy(self.board)
            aux[self.i][self.j] = aux[self.i][self.j+1]
            aux[self.i][self.j+1] = 0
            children.append(Board(aux, self, self.level+1, 0, self.i, self.j+1))

        if self.j != 0:
            aux = self.copy(self.board)
            aux[self.i][self.j] = aux[self.i][self.j-1]
            aux[self.i][self.j-1] = 0
            children.append(Board(aux, self, self.level+1, 0, self.i, self.j-1))
        
        if self.i != 3:
            aux = self.copy(self.board)
            aux[self.i][self.j] = aux[self.i+1][self.j]
            aux[self.i+1][self.j] = 0
            children.append(Board(aux, self, self.level+1, 0, self.i+1, self.j))

        if self.i != 0:
            aux = self.copy(self.board)
            aux[self.i][self.j] = aux[self.i-1][self.j]
            aux[self.i-1][self.j] = 0
            children.append(Board(aux, self, self.level+1, 0, self.i-1, self.j))

        return children

class Numpuz():
    def __init__(self):
        pygame.font.init()

        self.BOARD_WIDTH, self.BOARD_HEIGHT = 800, 800
        self.NUMBER_WIDTH, self.NUMBER_HEIGHT = 224, 224
        self.screen = pygame.display.set_mode((self.BOARD_WIDTH, self.BOARD_HEIGHT))
        pygame.display.set_caption("Numpuz Game")
        self.number_list = []

        # Load images
        self.BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")), (self.BOARD_WIDTH, self.BOARD_HEIGHT))
        self.clock_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "clock.png")), (96, 96))
        self.mouse = pygame.transform.scale(pygame.image.load(os.path.join("assets", "mouse.png")), (96, 96))
        self.title = pygame.transform.scale(pygame.image.load(os.path.join("assets", "title.png")), (750, 160))
        self.trophy = pygame.transform.scale(pygame.image.load(os.path.join("assets", "trophy.png")), (768, 768))
        for i in range(16):
            self.number_list.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", f"number_{i}.png")), (self.NUMBER_WIDTH, self.NUMBER_HEIGHT)))

        # Clock
        self.clock = pygame.time.Clock()
        # Set the font of text
        self.my_font = pygame.font.SysFont('Comic Sans MS', 64)
        # Set a default position
        self.DEFAULT_BOARD_POSITION = (0, 0)
        # Set the completed time
        self.finished = None

    def printBoard(self, board):
        # Background Color
        self.screen.fill((255, 255, 255))

        self.screen.blit(self.BG, self.DEFAULT_BOARD_POSITION)
        self.screen.blit(self.clock_image, (85, 707))
        self.screen.blit(self.mouse, (385, 712))
        self.screen.blit(self.title, (23, -35))

        text_surface = self.my_font.render(str(self.movimentos), False, (0, 127, 227))
        self.screen.blit(text_surface, (465, 740))
        if self.finished == None:
            clock_surface = self.my_font.render(str(int(round(pygame.time.get_ticks()/1000))) + 's', False, (0, 127, 227))
        else:
            clock_surface = self.my_font.render(str(self.finished) + 's', False, (0, 127, 227))
        self.screen.blit(clock_surface, (178, 740))

        board_image = [[self.number_list[0], self.number_list[0], self.number_list[0], self.number_list[0]],
                       [self.number_list[0], self.number_list[0], self.number_list[0], self.number_list[0]],
                       [self.number_list[0], self.number_list[0], self.number_list[0], self.number_list[0]],
                       [self.number_list[0], self.number_list[0], self.number_list[0], self.number_list[0]]]
        for i in range(4):
            for j in range(4):
                board_image[i][j] = self.number_list[board[i][j]]
        
        self.NUMBER_IMAGE_POSITION = [63, 63]
        for i in range(4):
            self.NUMBER_IMAGE_POSITION[0] = 63
            for j in range(4):
                if board_image[i][j] != self.number_list[0]:
                    self.screen.blit(board_image[i][j], self.NUMBER_IMAGE_POSITION)
                self.NUMBER_IMAGE_POSITION[0] += 150
            self.NUMBER_IMAGE_POSITION[1] += 150

    def checkWin(self, board):
        goal = [[1, 2, 3, 4], 
                [5, 6, 7, 8], 
                [9, 10, 11, 12],
                [13, 14, 15, 0]]
        return board == goal
                
        
    def printWin(self):
        # Background Color
        self.screen.fill((255, 255, 255))

        self.screen.blit(self.clock_image, (85, 707))
        self.screen.blit(self.mouse, (385, 712))
        self.screen.blit(self.title, (23, -35))
        self.screen.blit(self.trophy, (16, 50))

        text_surface = self.my_font.render(str(self.movimentos), False, (0, 127, 227))
        self.screen.blit(text_surface, (465, 740))

        clock_surface = self.my_font.render(str(self.finished) + 's', False, (0, 127, 227))
        self.screen.blit(clock_surface, (178, 740))


    def manhattanHeuristic(self, board):
        finded = False
        heuristic = 0
        goal = [[1, 2, 3, 4], 
                [5, 6, 7, 8], 
                [9, 10, 11, 12],
                [13, 14, 15, 0]]

        for i in range(4):
            for j in range(4):
                finded = False
                if board[i][j] != 0:
                    for x in range(4):
                        for y in range(4):
                            if board[i][j] == goal[x][y]:
                                heuristic += int(abs(i-x) + abs(j-y))
                                finded == True
                                break
                        if finded == True:
                            break
        
        return heuristic
    
    def totalHeuristic(self, node):
        return self.manhattanHeuristic(node.board) + node.level

    def playerStart(self):
        # Prepare loop condition
        running = False
        win = False
        self.movimentos = 0
        goal = [[1, 2, 3, 4], 
                [5, 6, 7, 8], 
                [9, 10, 11, 12],
                [13, 14, 15, 0]]
        
        main_board = Board(goal, None, 0, 0, 3, 3)
        main_board.shuffle()

        # Event loop
        while not running and not win:
            # Close window event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = True

            if keyboard.is_pressed('left') and main_board.j != 3:
                main_board.board[main_board.i][main_board.j] = main_board.board[main_board.i][main_board.j+1]
                main_board.board[main_board.i][main_board.j+1] = 0
                main_board.j += 1
                self.movimentos += 1
                time.sleep(0.1)

            if keyboard.is_pressed('right') and main_board.j != 0:
                main_board.board[main_board.i][main_board.j] = main_board.board[main_board.i][main_board.j-1]
                main_board.board[main_board.i][main_board.j-1] = 0
                main_board.j -= 1
                self.movimentos += 1
                time.sleep(0.1)

            if keyboard.is_pressed('up') and main_board.i != 3:
                main_board.board[main_board.i][main_board.j] = main_board.board[main_board.i+1][main_board.j]
                main_board.board[main_board.i+1][main_board.j] = 0
                main_board.i += 1
                self.movimentos += 1
                time.sleep(0.1)

            if keyboard.is_pressed('down') and main_board.i != 0:
                main_board.board[main_board.i][main_board.j] = main_board.board[main_board.i-1][main_board.j]
                main_board.board[main_board.i-1][main_board.j] = 0
                main_board.i -= 1
                self.movimentos += 1
                time.sleep(0.1)

            # Show the image
            self.printBoard(main_board.board)

            # Check the victory
            win = self.checkWin(main_board.board)
        
            # Part of event loop
            pygame.display.flip()
            self.clock.tick(30)
        self.finished = str(int(round(pygame.time.get_ticks()/1000)))
        time.sleep(3)

        if win == True:
            running = False

            while not running:
                # Close window event
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = True

                # Show the win image
                self.printWin()
                
                # Part of event loop
                pygame.display.flip()
                self.clock.tick(30)
    
    def starStart(self):
        # Prepare loop condition
        running = False
        win = False
        self.movimentos = -1
        goal = [[1, 2, 3, 4], 
                [5, 6, 7, 8], 
                [9, 10, 11, 12],
                [13, 14, 15, 0]]
        
        main_board = Board(goal, None, 0, 0, 3, 3)
        main_board.shuffle()
        main_board.f_value = self.totalHeuristic(main_board)

        open = []
        open.append(main_board)
        closed = []
        
        # Solving the Numpuz
        while not running and not win:
            # Close window event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = True

            current = open[0]

            # Show the image
            self.movimentos += 1
            self.printBoard(current.board)

            # Check the victory
            if self.manhattanHeuristic(current.board) == 0:
                win = True
            
            for i in current.generateChild():
                i.f_value = self.totalHeuristic(i)
                open.append(i)

            closed.append(current)
            del open[0]

            open.sort(key = lambda x:x.f_value, reverse=False)

            # Part of event loop
            pygame.display.flip()
            self.clock.tick(30)
        self.finished = str(int(round(pygame.time.get_ticks()/1000)))

        solution = []
        while current != None:
            solution.append(current.board)
            current = current.father
        solution.reverse()

        i = 0
        while not running and i != len(solution):
            # Close window event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = True

            # Show the image
            self.printBoard(solution[i])
            i += 1
            time.sleep(0.5)

            # Part of event loop
            pygame.display.flip()
            self.clock.tick(30)
        
        time.sleep(3)

        if win == True:
            running = False

            while not running:
                # Close window event
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = True

                # Show the win image
                self.printWin()
                
                # Part of event loop
                pygame.display.flip()
                self.clock.tick(30)


if __name__ == '__main__':
    numpuz = Numpuz()
    numpuz.starStart()
