def Evaluate(solution, qrels):
    rec = set()
    for i in solution:   
        rec.update(i)
    rel = set(qrels)
    rr = rel.intersection(rec)
    ri = rec.difference(rr)
    accuracy = len(rr) / len(rr.union(ri))
    nr = rel.difference(rr)
    recovered = len(rr) / len(rr.union(nr))
    return accuracy, recovered

def F1(accuracy, recovered):
    return (2 * accuracy * recovered) / (accuracy + recovered)

def F(accuracy, recovered, beta = 0):
    return ((1 + beta**2) * accuracy * recovered) / (beta**2 * accuracy + recovered)
    