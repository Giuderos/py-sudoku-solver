from BetterSudoku import BetterSudoku
import time
import sys

with open(sys.argv[1]) as myfile:
    for line in myfile:
        problem=BetterSudoku(line)
        start_time=time.time()
        if problem.BackTrack():
            print "Solution computed"
            print problem
            print "Number of recursive calls: "+str(problem.count)
            print "In ",time.time() - start_time, "seconds"
        else:
            print "No solution"
            print "In ",time.time() - start_time, "seconds"
            print problem.instance
        print
