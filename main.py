import time
from datetime import datetime
from sudoku_connections import SudokuConnections
from PIL import Image, ImageDraw,ImageFont
from math import sqrt




class SBoard :
    def __init__(self,board,n=9) :

        self.board = self.getBoard(board)
        self.n=n
        self.sudokuGraph = SudokuConnections(n)
        self.mappedGrid = self.__getMappedMatrix() # Maps all the ids to the position in the matrix
        self.frames=[]
        self.dots=[j for j in  range(n**2)]
    def __getMappedMatrix(self) :
        matrix = [[0 for cols in range(self.n)]
        for rows in range(self.n)]

        count = 1
        for rows in range(self.n) :
            for cols in range(self.n):
                matrix[rows][cols] = count
                count+=1
        return matrix

    def getFrames(self):
        return self.frames
    def getBoard(self,board) :

        self.board=board
        return board

    def getCons(self, n):
        cons=self.sudokuGraph.graph.getNode(n).getConnections()
        return cons

    def retBoard(self):
        return self.board

    def printBoard(self) :
        for i in range(len(self.board)) :
            if i%int(sqrt(self.n)) == 0  :#and i != 0:
                print(" ==============================="*(1*self.n//10+1))

            for j in range(len(self.board[i])) :
                if j %int(sqrt(self.n)) == 0 :#and j != 0 :
                    print(" |  ", end = "")
                if j == self.n-1 :
                    print(self.board[i][j]," | ")
                else :
                    print(f"{ self.board[i][j] } ", end="")
                    if(self.n>10 and self.board[i][j] // 10 ==0):
                        print((" "),end="")
        print(" ==============================="*(1*self.n//10+1))

    def is_Blank(self) :

        for row in range(len(self.board)) :
            for col in range(len(self.board[row])) :
                if self.board[row][col] == 0 :
                    return (row, col)
        return None

    def graphColoringInitializeColor(self):
        color = [0] * (self.sudokuGraph.graph.totalV+1)
        given = []
        for row in range(len(self.board)) :
            for col in range(len(self.board[row])) :
                if self.board[row][col] != 0 :

                    idx = self.mappedGrid[row][col]

                    color[idx] = self.board[row][col]

                    given.append(idx)

        return color, given

    def solveGraphColoring(self,img, m =9,) :

        color, given = self.graphColoringInitializeColor()
        if self.__graphColorUtility(img=img,m =m, color=color, v =1, given=given) is None :
            print("unsolvable or the program cannot solve this due to lack of code")
            return False
        count = 1
        for row in range(m) :
            for col in range(m) :
                self.board[row][col] = color[count]
                count += 1
        return color
    def Draw_Base(self,img,status=-1):
        colors = ['gray', 'brown', 'blue', 'green', 'yellow', 'pink', 'aquamarine', 'red', 'orange', 'olive',
                  'chartreuse', 'lightblue', 'crimson', 'golden', 'sienna', 'violet', 'green']

        draw=ImageDraw.Draw(img)
        draw.line([(self.n*2 + 1) * 40, 0, (self.n*2 + 1) * 40, (self.n*2 + 1) * 40], width=1, fill='black')
        for i in range(0,self.n+1):
            draw.ellipse([(self.n*2 + 1) * 40 + 10, int(i) * 40 + 10, (self.n*2 + 1) * 40 + 50, int(i) * 40 + 50], width=40, fill=colors[i])
            font = ImageFont.truetype("arial.ttf", 20)
            draw.text(((self.n*2 + 1) * 40 + 25,int(i) * 40 + 20),str(i),fill='black',font=font)
        if status==(-1):
            temp = self.board
            for i in range(0, self.n**2):

                draw.ellipse([int(i % self.n)*80+40,int(i // self.n)*80+40,int(i % self.n)*80+80,int(i // self.n)*80+80],width=40,fill=colors[temp[i // self.n ][i % self.n ]])
        elif status ==0:
            x = []
            y = []
            for i in range(0, self.n**2):
                x.append((int(i % self.n)*80+60))
                y.append(int(i // self.n)*80+60)
            for i in range(0, self.n**2):
                cons = list(self.getCons(i + 1))
                for c in cons:
                    draw.line([x[i],y[i],x[c - 1],y[c - 1]],width=1,fill='black')

            temp = self.board
            for i in range(0, self.n**2):
                draw.ellipse([int(i % self.n) * 80 + 40, int(i // self.n) * 80 + 40, int(i % self.n) * 80 + 80,int(i // self.n) * 80 + 80], width=40, fill=colors[temp[i // self.n][i % self.n]])

    def Draw(self,img,v=-1,num=-1,n=9):
        colors = ['gray', 'brown', 'blue', 'green', 'yellow', 'pink', 'aquamarine', 'red', 'orange', 'olive',
                  'chartreuse', 'lightblue', 'crimson', 'golden', 'sienna', 'violet', 'green']
        temp = self.board
        if num!=self.board[(v-1) // self.n][(v-1) % self.n]:

            if(self.frames==[]):
                im_n=img.copy()
            else:
                im_n=self.frames[-1].copy()
            draw1=ImageDraw.Draw(im_n)
            draw1.ellipse([int((v-1) % self.n) * 80 + 40, int((v-1) // self.n) * 80 + 40, int((v-1) % self.n) * 80 + 80,
                              int((v-1) // self.n) * 80 + 80], width=40, fill=colors[num])
            self.frames.append(im_n)

    def __graphColorUtility(self,img, m, color, v, given) :
        if v == self.sudokuGraph.graph.totalV+1  :
            return True
        for c in range(1,m+1) :
            if self.__isSafe2Color(v, color, c, given) == True :
                color[v] = c
                self.Draw(img,v, c)
                if self.__graphColorUtility(img,m, color, v+1, given) :
                    return True
            if v not in given :
                color[v] = 0

    def __isSafe2Color(self, v, color, c, given) :

        if v in given and color[v] == c:
            return True
        elif v in given :
            return False
        #print(self.sudokuGraph.graph.totalV+1)
        for n in self.getCons(v) :

            if color[n] == c:

                return False

        return True





def main() :

    print("Type in sudoku size(n)")
    n=int(input())
    print("Type in sudoku(0 - empty cell, type without separators, rows separation by enter)")
    b=[]
    img = Image.new('RGB', ((n*2 + 1) * 40 + 70, (n*2 + 1) * 40), color='white')
    for i in range(n):
        temp=str(input())
        chars=[]
        #print(len(temp))
        if(len(temp)!=n):
            print('You didnt entered n values')
            return False
        for j in range(n):
            if (int(temp[j]) > n or int(temp[j]) <0):
                print('One of the values is bigger than N or less than 0')
                return False
            chars.append(int(temp[j]))
        b.append(chars)
    t1=datetime.now()
    s = SBoard(b,n)
    print("Sudoku ...")
    print("\n\n")
    s.printBoard()
    print("\nSolving ...")
    print("\n\n\nSolved Sudoku ...")
    print("\n\n")
    s.Draw_Base(img)
    s.Draw_Base(img,0)
    if(s.solveGraphColoring(img,m=n)):
        s.printBoard()
        t2=datetime.now()
        res=t2-t1
        frames=s.getFrames()
        frames[-1].show()
        frames[0].save('pillow_imagedraw.gif',save_all=True, append_images=frames[1:], optimize=True, loop=0)
        return res.microseconds
    return 0


if __name__ == "__main__" :
    main()

