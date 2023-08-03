
def sum_digits(num):
    return sum([int(n) for n in str(num)])

def createMatrix(date = ''):
    result = []

    sequence = [int(s) for s in date]
    sequence = sequence + sequence[::-1]

    while len(sequence) != 0:
        result.append(sequence)

        newSequence = []
        for i in range(len(sequence)-1):
            summ = sequence[i] + sequence[i+1]
            while len(str(summ)) != 1:                
                summ = sum_digits(summ)                            
            newSequence.append(summ)

        sequence = newSequence

    result.reverse()

    return {'matrix': result, 'center': result[0][0]}

if __name__ == '__main__':
    matrix = createMatrix('26031969')['matrix']
    matrix.reverse()
    for i in range(len(matrix)):
        for elem in matrix[i]:

            print(elem, end=' ')

        print()