list = []
N = int(input())
for i in range(N):
    cmd = input().split()
    if cmd[0] == 'insert':
      i = int(cmd[1])
      e = int(cmd[2])
      list.insert(i,e)
    
    elif cmd[0] == "print":
       print(list)
    
