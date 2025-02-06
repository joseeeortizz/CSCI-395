"""
Name: Jose Miguel Ortiz
Email: jose.ortiz60@lagcc.cuny.edu
Pod: 1st right
Date: 02/06/2025

"""

# complete the lambda function
cube = lambda x: x ** 3

def fibonacci(n):

    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i - 1] + fib[i - 2])
    return fib[:n+1]

if __name__ == '__main__':
    print("Enter the number of terms you want in the fibonacci series: ")
    n = int(input())
    print(list(map(cube, fibonacci(n))))
