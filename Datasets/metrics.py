def Evaluate(solution, qrels):
    rec = set()
    for i in solution:   
        rec.update(i)
    rel = set(qrels)
    rr = rel.intersection(rec)
    ri = rec.difference(rr)
    accuracy = len(rr) / len(rr.union(ri)) if len(rr.union(ri)) > 0 else 0
    nr = rel.difference(rr)
    recovered = len(rr) / len(rr.union(nr)) if len(rr.union(nr)) > 0 else 0
    return accuracy, recovered

def F1(accuracy, recovered):
    return (2 * accuracy * recovered) / (accuracy + recovered) if accuracy + recovered > 0 else 0

def F(accuracy, recovered, beta = 0):
    return ((1 + beta**2) * accuracy * recovered) / (beta**2 * accuracy + recovered) if beta**2 * accuracy + recovered > 0 else 0
    