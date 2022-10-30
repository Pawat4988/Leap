n = 10
count = 0
for t in range(n):
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            qubit_a = t * n + i
            qubit_b = (t + 1)%n * n + j
            count += 1
            print(f"A: {qubit_a}, B: {qubit_b}")
print(count)