from random import choice
import requests
import pygame

class Sudoku:
    def __init__(self):

        self.background_color = (8, 32, 50)
        self.accent_color = (255, 76, 41)
        self.clear_color = (51, 71, 86)
        self.dark_color = (44, 57, 75)
        self.box_size = 50
        self.buffer = 5
        self.title = "Sudoku Solver"
        
        self.solved = False
        self.running = True
        self.start()

    def start(self): # On instancie pygame et on crée la fenetre et on dessine puis telecharge et remplit la grille initiale
        pygame.init()
        self.window = pygame.display.set_mode((self.box_size * 11,self.box_size * 11))
        pygame.display.set_caption(self.title)
        self.window.fill(self.background_color)
        self.myfont = pygame.font.SysFont('Comic Sans MS', self.box_size - 15)
        for i in range(0,10):
                if(i%3 == 0):
                    line_colour = self.clear_color
                    line_thickness = 3
                else:
                    line_colour = self.dark_color
                    line_thickness = 1

                pygame.draw.line(self.window, (line_colour), (self.box_size + self.box_size*i, self.box_size), (self.box_size + self.box_size*i ,self.box_size * 10 ), line_thickness )
                pygame.draw.line(self.window, (line_colour), (self.box_size, self.box_size + self.box_size*i), (self.box_size * 10, self.box_size + self.box_size*i), line_thickness )

        response = requests.get("https://sugoku.herokuapp.com/board?difficulty=hard") 
        self.grid = response.json()['board']
        self.grid_original = [[self.grid[x][y] for y in range(len(self.grid[0]))] for x in range(len(self.grid))] #conservation de la grille d'origine, inutile pour le moment

        self.fill_grid()
        self.run()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.manage_events(event)

        self.quit()

    def manage_events(self,event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if self.solved == False:
                self.solve()
                self.solved = True
            else:
                self.solved = False
                self.start()

    def update(sefl):
        pygame.display.update()

    def quit(self):
        pygame.quit()


    def fill_grid(self,color = None): # fonction remplissage grille
        if color == None:
            color = self.accent_color
        for i in range(0, len(self.grid[0])):
            for j in range(0, len(self.grid[0])):
                self.erase_box(i,j)
                if(0<self.grid[i][j]<10):
                    self.fill_box(self.grid[i][j],i,j,color)

        self.update

    def erase_box(self,x,y): # effacer une case
        pygame.draw.rect(self.window, self.background_color, ((y+1) * self.box_size + self.buffer, (x+1) * self.box_size+ self.buffer, self.box_size -2*self.buffer ,  self.box_size - 2*self.buffer))
        self.update()

    def fill_box(self,i ,x ,y,color = None): # remplir une case
        if color == None:
            color = self.dark_color
        self.erase_box(x,y)
        value = self.myfont.render(str(i), True, color)
        self.window.blit(value, ((y+1)*self.box_size + 15, (x+1)*self.box_size ))
        self.update()
       
    def solve(self): #solution avec backtracking
        find = self.find_empty()
        if not find :
            return True
        else :
            y,x = find
        h=self.hypothesis(x,y)
        for i in h:
            self.grid[y][x] = i
            self.fill_box(i,y,x)
            if self.solve():
                return True
            self.grid[y][x] = 0
            self.erase_box(y,x)
        return False

    def find_empty(self): 
        for y in range(9):
            for x in range(9):
                if self.grid[y][x] == 0:
                    return y,x
        return None

    def hypothesis(self,x,y): # recherches des hypotheses ou possibilités
        test = [1,2,3,4,5,6,7,8,9]

        for i in range(9):
            if self.grid[y][i] in test:  #ligne
                test.remove(self.grid[y][i])
            if self.grid[i][x] in test:  #Colonne
                test.remove(self.grid[i][x])

        for j in range(3):#region
            for i in range(3):
                if self.grid[y//3*3+j][x//3*3+i] in test:
                    test.remove(self.grid[y//3*3+j][x//3*3+i])
        return test

if __name__ == "__main__":
    Sudoku_1 = Sudoku()