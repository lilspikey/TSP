import sys
from math import sqrt

results={}

def sd(scores):
    avg=sum(scores)/len(scores)
    var=sum((s-avg)*(s-avg) for s in scores)/len(scores)
    return sqrt(var)

def best_score(results, index):
    best,best_name=max((scores[index],name) for name, scores in results.items())
    return best,best_name

for arg in sys.argv[1:]:
    lines=open(arg).readlines()
    lines=[line.strip() for line in lines if line.strip() != '']
    scores=[float(line.split()[1]) for line in lines]
    if len(scores) > 0:
        avg=sum(scores)/len(scores)                
        results[arg]=(min(scores),avg,max(scores),sd(scores))

best,best_name=best_score(results,2)
print "best best: %f in %s" % (best,best_name)
best,best_name=best_score(results,1)
print "best avg: %f in %s" % (best,best_name)
best,best_name=best_score(results,0)
print "best worst: %f in %s" % (best,best_name)


avgs=results.keys()
avgs.sort(key=lambda arg: -results[arg][1])

for arg in avgs:
    print arg, results[arg]
