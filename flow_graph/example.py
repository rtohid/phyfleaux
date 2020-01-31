class DFSResult:
    def __init__(self):
        self.parent={}
        self.discovery_time = {}
        self.finish_time = {}
        self.edges = {}
        self.order = []
        self.t = 0

def dfs(g):
    results = DFSResult()
    for vertex in g.intervertices():
        if vertex not in results.parents:
            dfs_visit(g, vertex, results)
    return results

def dfs_visit(g, v, results, parent = None):
    results.parent[v] = parent
    results.t += 1
    results.discovery_time[v] = results.t
    if parent:
        results.edges[(parent,v)] = 'tree'

    for n in g.neighbors(v):
        if n not in results.parent:
            dfs_visit(g, n, results, v)
        else:
            results.edges[(v, n)] = 'back'
        
    results.t += 1
    results.finish_time[v] = results.t
    results.order.append(v)
