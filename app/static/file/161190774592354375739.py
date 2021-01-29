n = int(input())
a = list(map(int, input().split()))
q = int(input())
lr = [list(map(int, input().split())) for _ in range(q)]

sm = [0] * (n+1)
for i in range(n):
    sm[i+1] = sm[i] + a[i]

for i in range(q):
    l, r = lr[i]
    print(sm[r] - sm[l-1])