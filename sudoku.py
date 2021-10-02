from random import choice
import requests
import pygame


background_color = (8, 32, 50)
red = (255, 76, 41)
blue_clear = (51, 71, 86)
blue_dark = (44, 57, 75)
box_size = 50
buffer = 5



class Sudoku:
    def __init__(self):
        
        response = requests.get("https://sugoku.herokuapp.com/board?difficulty=hard") 
        self.grid = response.json()['board']
        self.grid_original = [[self.grid[x][y] for y in range(len(self.grid[0]))] for x in range(len(self.grid))]

    def display(self): # fonction remplissage grille
        # for y in range(9):
        #     print (self.grid[y])
        # print("\n")
        for i in range(0, len(self.grid[0])):
            for j in range(0, len(self.grid[0])):
                self.erase_box(i,j)
                if(0<self.grid[i][j]<10):
                    self.fill_box(self.grid[i][j],i,j,red)

        pygame.display.update()

    def erase_box(self,x,y): # effacer une case
        pygame.draw.rect(window, background_color, ((y+1) * box_size + buffer, (x+1) * box_size+ buffer, box_size -2*buffer ,  box_size - 2*buffer))
        pygame.display.update()

    def fill_box(self,i ,x ,y,color = blue_clear): # remplir une case
        self.erase_box(x,y)
        value = myfont.render(str(i), True, color)
        window.blit(value, ((y+1)*box_size + 15, (x+1)*box_size ))
        pygame.display.update()
       
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

pygame.init()
window = pygame.display.set_mode((box_size * 11,box_size * 11))
pygame.display.set_caption("Sudoku Solver")
window.fill(background_color)
myfont = pygame.font.SysFont('Comic Sans MS', box_size - 15)
for i in range(0,10):
        if(i%3 == 0):
            line_colour = blue_clear
            line_thickness = 3
        else:
            line_colour = blue_dark
            line_thickness = 1

        pygame.draw.line(window, (line_colour), (box_size + box_size*i, box_size), (box_size + box_size*i ,box_size * 10 ), line_thickness )
        pygame.draw.line(window, (line_colour), (box_size, box_size + box_size*i), (box_size * 10, box_size + box_size*i), line_thickness )
pygame.display.update()

Sudoku_1 = Sudoku()
solved = 0
Sudoku_1.display()


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if solved == 0:
                Sudoku_1.solve()
                solved = 1
            else:
                Sudoku_1 = Sudoku()
                solved = 0
                Sudoku_1.display()

pygame.quit()