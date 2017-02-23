import numpy as np

'''Input:
Values (stored in array v)
Weights (stored in array w)
Number of distinct items (n)
Knapsack capacity (W) 
'''

c = 30
n = 10
w = (np.random.rand(n) * 10).astype(int)
v = (np.random.rand(n) * 10).astype(int)
#print(w)
#print(v)
m = np.zeros((n, c))
optimal_set = []



for i in range(n):
    for j in range(c):
        if w[i] > j:
            m[i, j] = m[i-1, j]
        else:
            m[i, j] = max(m[i-1, j], m[i-1, j-w[i]] + v[i])
            if(m[i-1, j-w[i]] + v[i] > m[i-1, j]):
                optimal_set.append(i)


def solve(items, capacity):

    # print optimal_value
    # 
    # for i in range(0,len(items)):
    #   print items[i]
    # for i in range(0,len(M)):
    #   print M[i]
    M, optimal_value = generate_optimal_solutions(items, len(items), capacity)
    optimal_set = []
    optimal_set_id = []
    # raise the recursion limit so that we can handle a large number of items
    #sys.setrecursionlimit(len(items)+10)
    optimal_weight = get_optimal_set(items, len(items), M, len(items)-1, capacity, optimal_set, optimal_set_id, 0)
    
    return optimal_set, optimal_weight, optimal_value, optimal_set_id


def generate_optimal_solutions(items, n, capacity):
    M = [[]]
    for w in range(0,capacity+1):
      M[0].append(0) # = 0

    for i in range(0,n):
      M.append([])
      for w in range(0,capacity+1):
        if (items[i][0] > w):
          M[i+1].append(M[i-1+1][w])
        else:
          M[i+1].append( max(M[i-1+1][w], items[i][1] + M[i-1+1][w - items[i][0]]) )

    return M, M[n][capacity]
  

def get_optimal_set(items, n, M, j, w, optimal_set, optimal_set_id, optimal_weight):

    if (j < 0):
      pass
    elif (w >= items[j][0] and items[j][1] + M[j-1+1][w - items[j][0]] > M[j-1+1][w]):
      optimal_set.append(items[j])
      optimal_set_id.append(j)
      optimal_weight += items[j][0]
      optimal_weight = get_optimal_set(items, n, M, j-1, w - items[j][0], optimal_set, optimal_set_id, optimal_weight)
    else:
      optimal_weight = get_optimal_set(items, n, M, j-1, w, optimal_set, optimal_set_id, optimal_weight)
      
    return optimal_weight


