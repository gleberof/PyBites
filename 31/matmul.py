class Matrix(object):

    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return f'<Matrix values="{self.values}">'

    def __matmul__(self, other):
        result = []
        for i, l in enumerate(self.values):
            line = []
            for j in range(len(other.values[0])):
                line.append(sum([e * other.values[k][j] for k, e in enumerate(l)]))
            result.append(line)
        return Matrix(result)

    def __rmatmul__(self, other):
        return other.__matmul__(self.values)

    def __imatmul__(self, other):
        return self.__matmul__(other)
