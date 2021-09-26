from random import choice


def display(): # fonction affichage grille
     for y in range(9):
         print (grid[y])


def hypothesis(x,y): # recherches des hypotheses ou possibilités
    test = [1,2,3,4,5,6,7,8,9]

    for i in range(9):
        if grid[y][i] in test:  #ligne
            test.remove(grid[y][i])
        if grid[i][x] in test:  #Colonne
            test.remove(grid[i][x])

    for j in range(3):#region
        for i in range(3):
            if grid[y//3*3+j][x//3*3+i] in test:
                test.remove(grid[y//3*3+j][x//3*3+i])
    return test


def create_empty_grid():
  line = [0,0,0,0,0,0,0,0,0]
  emptygrid = []
  for x in range(9):
    emptygrid.append(line)
  return emptygrid

def fill_grid(fill):
  for y in range(9):
    for x in range(9):
      c = choice(hypothesis(x,y))
      print(c)
      fill[y][x] = c
  return fill


grid = create_empty_grid()
display()
grid = fill_grid(grid)
display()