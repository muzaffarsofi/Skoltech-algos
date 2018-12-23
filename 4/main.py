BIG_NUMBER = 9999999999999

def slack_table(W,L):
    n = len(W)
    S = [[BIG_NUMBER for i in range(n)] for j in range(n)]
    K = [0 for i in range(n)]
    S[0][0] = W[0]
    K[0] = n-1
    for k in range(1,n):
        S[0][k] = S[0][k-1] + W[k]
    
    for i in range(1,n):
        k = i
        S[i][k] = S[0][k] - S[0][i-1]
        while (k <= n-2) and (L - S[i][k] - (k-i) > 0):
            k += 1
            S[i][k] = S[0][k] - S[0][i-1]
        
        K[i] = k
    
    for i in range(n):
        for j in range(i, K[i]+1):
            S[i][j] = L - S[i][j] - (j-i)
            if S[i][j] < 0:
                S[i][j] = BIG_NUMBER
            else:
                S[i][j] = S[i][j]**2
    
    return S


def print_neatly(W,L):
    n = len(W)
    S = slack_table(W,L)
    C = [0]
    B = [-BIG_NUMBER for i in range(n)]
    for i in range(n):
        C.append(BIG_NUMBER)
        k = i
        T = C[k] + S[k][i]
        if T < C[i+1]:
            C[i+1] = T
            B[i] = k
        while (k>=1) and (T < BIG_NUMBER):
            k -= 1
            T = C[k] + S[k][i]
            if T < C[i+1]:
                C[i+1] = T
                B[i] = k
                
    F = [B[n-1]]
    i = B[n-1] - 1
    while i >= 0:
        F = [B[i]]+F
        i = B[i] - 1
    return F


if __name__ == '__main__':
    # based on https://alumni.media.mit.edu/~dlanman/courses/cs157/HW5.pdf
    inp = 'input.txt'
    out = 'output.txt'

    lines = []
    with open(inp, 'r') as f:
        lines = f.readlines()

    L = int(lines[0])
    words = lines[1].split(' ')

    wlens = []
    for elem in words:
        wlens.append(len(elem))
        
    res = print_neatly(wlens,L)
    ssq = 0
    for i in range(1,len(res)):
        word_sum = res[i] - res[i-1] - 1
        for x in range(res[i-1],res[i]):
            word_sum += wlens[x]

        cost = L - word_sum
        ssq += cost**2

    end_sum = len(wlens) - 1 - res[-1]
    for x in range(res[-1], len(wlens)):
        end_sum += wlens[x]

    ssq += (L-end_sum)**2

    with open(out, 'w') as f:
        f.writelines([str(ssq)+'\n', str(len(res))])