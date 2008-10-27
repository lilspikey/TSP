import sys
from math import sqrt

results={}

def sd(scores):
    avg=sum(scores)/len(scores)
    var=sum((s-avg)*(s-avg) for s in scores)/len(scores)
    return sqrt(var)

best_score=None
best_score_file=None

for arg in sys.argv[1:]:
    lines=open(arg).readlines()
    lines=[line.strip() for line in lines if line.strip() != '']
    scores=[float(line.split()[1]) for line in lines]
    if len(scores) > 0:
        avg=sum(scores)/len(scores)
        best=max(scores)
        
        if best_score_file is None or best_score < best:
            best_score=best
            best_score_file=arg
                
        results[arg]=(min(scores),avg,max(scores),sd(scores))
        #results[arg]=avg

print "best found: %d in %s" % (best_score,best_score_file)

avgs=results.keys()
avgs.sort(key=lambda arg: -results[arg][1])

for arg in avgs:
    print arg, results[arg]
