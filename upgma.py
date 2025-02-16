from copy import deepcopy

def readMatrix():
    matrix = []
    with open('input.txt') as f:
        lines = f.readlines()
        matrix = [[float(x) for x in ln.strip().split(",")] for ln in lines[1:]]
    labels = [title for title in lines[0].strip().split(",")]

    return matrix, labels


def matrixMinimum(matrix):
    min_i = 0
    min_j = 0
    minimum = float('inf')

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            value = abs(float(matrix[i][j]))
            if value < minimum and value != 0:
                minimum = value
                min_i = i
                min_j = j

    return min_i, min_j


def join_labels(labels, a, b):
    # Join the labels in the first index
    labels[a] = labels[a] + "," + labels[b]

    # Remove the (now redundant) label in the second index
    del labels[b]

def split_labels(labels, separator=","):
    return labels.split(separator)


def upgma(matrix, labels):

    o_matrix = deepcopy(matrix)
    o_labels = deepcopy(labels)

    while len(matrix) > 1:

        min_i, min_j = matrixMinimum(matrix)
        minimum_value = matrix[min_i][min_j]
        distance = minimum_value / 2

        # Getting min max index
        min_ij = min(min_i, min_j)
        max_ij = max(min_i, min_j)

        # Printing
        print("----------------------")
        print(labels)
        for row in matrix:
            print(row)
        print("Minimum value is:", minimum_value)
        print("Merging:", labels[min_ij], "and" ,labels[max_ij])
        print(f"Distance between {labels[min_ij]} and {labels[max_ij]}:", distance)

        # Getting associated labels of matrix minimum value
        label1 = labels[min_ij]
        label2 = labels[max_ij]

        # Merging labels
        new_labels = label1 + "," + label2
        labels[min_ij] = new_labels
        del labels[max_ij]

        # --- Removing max row and column

        # Row
        del matrix[max_ij]
        # column
        for i in range(len(matrix)):
            del matrix[i][max_ij]

        # new row,column labels
        merged_row_labels = new_labels.split(",")

        # Update merged row
        for col in range(min_ij):
            col_labels = labels[col].split(",")
            total = []
            for row_label in merged_row_labels:
                for col_label in col_labels:
                    # Because this is a lower triangle matrix
                    # using max idx as row and min idx as column
                    row_idx = o_labels.index(row_label)
                    col_idx = o_labels.index(col_label)
                    total.append(o_matrix[max(row_idx, col_idx)][min(row_idx, col_idx)])
            matrix[min_ij][col] = sum(total) / len(total)

        # Update merged column
        for row in range(min_ij + 1, len(matrix)):
            row_labels = labels[row].split(",")
            total = []
            for row_label in row_labels:
                for col_label in merged_row_labels:
                    # Because this is a lower triangle matrix
                    # using max idx as row and min idx as column
                    row_idx = o_labels.index(row_label)
                    col_idx = o_labels.index(col_label)
                    total.append(o_matrix[max(row_idx, col_idx)][min(row_idx, col_idx)])
            matrix[row][min_ij] = sum(total) / len(total)


if __name__ == "__main__":
    matrix, labels = readMatrix()
    upgma(matrix, labels)
