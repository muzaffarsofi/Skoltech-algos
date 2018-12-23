class HashTable(object):

    def __init__(self, table_size=2048, hash_factor=8537):
        self.array = [list() for i in range(table_size)]
        self._hash_factor = hash_factor
        self._table_size = len(self.array)

    def _hash_function(self, a, b):
        return ((a + b) * self._hash_factor) % self._table_size

    def _find_key_index(self, a, b):
        key = self._hash_function(a,b)
        key_array = self.array[key]

        for i in range(len(key_array)):
            if key_array[i][1] == a and key_array[i][2] == b:
                return i, key_array[i]

        return None, None

    def find(self, a, b):
        index, key = self._find_key_index(a, b)
        return key

    def _find_index(self, a, b):
        index, key = self._find_key_index(a, b)
        return index

    def add(self, x):
        key = self._hash_function(x[1], x[2])
        key_idx = self._find_index(x[1], x[2])

        if key_idx is None:
            self.array[key].append(x)
        else:
            self.array[key][key_idx] = x

def solution():
    input_file = open('input.txt', 'r')
    output_file = open('output.txt', 'w')

    input_lines = input_file.readlines()

    n, diameter = (0, 0)
    ans_num = [0]
    table = HashTable()

    for line in input_lines[1:]:
        n += 1
        x,y,z = sorted(list(map(int, line.split())), reverse=True)
        suitable = table.find(x,y)

        if suitable is not None:
            if min(x,y,z + suitable[3]) > diameter:
                ans_num = [suitable[0], n]
                diameter = min(x,y,z + suitable[3])
            if z > suitable[3]:
                table.add((n,x,y,z))
        else:
            if z > diameter:
                ans_num = [n]
                diameter = z
            table.add((n,x,y,z))

    first_answer_line = '%s\n' % (len(ans_num))
    ans_num = [str(x) for x in ans_num]
    second_answer_line = '%s\n' % (' '.join(ans_num))
    third_answer_line = '%s\n' % (diameter)

    output_file.write(first_answer_line)
    output_file.write(second_answer_line)
    output_file.write(third_answer_line)

    input_file.close()
    output_file.close()

if __name__ == '__main__':
    solution()

