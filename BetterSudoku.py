from Sudoku import Sudoku
import math

class BetterSudoku(Sudoku):
    """Improved Sudoku Class"""

    def __init__(self,line,verbose=False):
        Sudoku.__init__(self,line,verbose)     #initialize a basic sudoku object
        self.sn=int(math.sqrt(self.n))
        self.conflict=[]               #conflict[row][col]-->cells in conflict with [row][col]
        for row in range(self.n):      #[row][cel] encoded as integer row*self.n+col
            ROW=[]
            for col in range(self.n):
                setrowcol=self.computeConflicts(row,col)
                ROW.append(setrowcol)
            self.conflict.append(ROW)

        self.forbidden=[]  #forbidden[row][col]-->digits forbidden for [row][col]
        for row in range(self.n):
            ROW=[]
            for col in range(self.n):
                ROW.append([])
            self.forbidden.append(ROW)
        #no digit is forbidden at the beginning

        #now we look at the instance and some digits are forbidden for some cells
        for row in range(self.n):
            for col in range(self.n):
                if self.instance[row][col]!=0:
                    for x in self.conflict[row][col]:
                        rx=x/self.n; cx=x%self.n
                        self.forbidden[rx][cx].append(self.instance[row][col])


    #returns the set of cells in conflict with cell [row][col]
    #Python does not allow to have a set of lists:
    #if [r][c] is in conflict with [row][col]
    #the set returned contains integer r*self.n+c
    def computeConflicts(self,row,col,verbose=False):
        setConf=set()
        for x in range(self.n):
            if verbose:
                print "Adding: "+str(row)+" "+str(x)
                print "Adding: "+str(x)+" "+str(col)
            setConf.add(row*self.n+x)
            setConf.add(x*self.n+col)
        cornerRow=(row/self.sn)*self.sn
        cornerCol=(col/self.sn)*self.sn
        if verbose:
            print "cornerRow="+str(cornerRow)
            print "cornerCol="+str(cornerCol)
        for x in range(self.sn):
            for y in range(self.sn):
                setConf.add((x+cornerRow)*self.n+y+cornerCol)
                if verbose:
                    print "Adding: "+str(x+cornerRow)+" "+str(y+cornerCol)
        setConf.remove(row*self.n+col)
        return setConf

    def setNextEmpty(self,current,newDigit):
        currentRow=current[0]
        currentCol=current[1]
        if self.verbose:
            print "Setting ",currentRow,currentCol,newDigit
        oldDigit=self.partial[currentRow][currentCol]

        if oldDigit!=0:  #if oldDigit==0 --> no forbidden digit must be removed
            for x in self.conflict[currentRow][currentCol]:
                xr=x/self.n; xc=x%self.n
                self.forbidden[xr][xc].remove(oldDigit)
                if self.verbose:
                    print "Removing ",xr,xc,oldDigit

        if newDigit!=0:  #if newDigit==0 --> no forbidden digit must be added
            for x in self.conflict[currentRow][currentCol]:
                xr=x/self.n; xc=x%self.n
                self.forbidden[xr][xc].append(newDigit)
                if self.verbose:
                    print "Adding ",xr,xc,newDigit

        self.partial[currentRow][currentCol]=newDigit

    def Gamma(self,pos):
        row=pos[0]; col=pos[1]
        if self.verbose:
            print "Forbidden for "+str(row)+" "+str(col)
            print self.forbidden[row][col]
            print "*********"
            print
        for i in range(1,self.n+1):
            if i not in self.forbidden[row][col]:
                yield i

    def isnotExtendible(self):
        for row in range(self.n):
            for col in range(self.n):
                setConf=set(self.forbidden[row][col])
                if len(setConf)==self.n:
                    return True
        return False

    def isAdmissible(self):
        return True
