from functools import cmp_to_key


def puzzle_1():
    result = 0
    input_txt = open("input.txt", "r")
    lines = input_txt.read().splitlines()
    for pos in range(0, len(lines), 3):
        left = eval(lines[pos])
        right = eval(lines[pos+1])
        if right_order(left, right) < 0:
            result += (pos//3+1)

    return result

# some error in this function, used eval instead :facepalm
def parse_package(data):
    stack = []
    for char in list(data):
        if char == "[":
            stack.insert(0, [])
        elif char.isnumeric():
            if isinstance(stack[0], str):
                stack[0] = stack[0] + char
            else:
                stack.insert(0, char)
        elif char == ",":
            elem = stack.pop(0)
            if isinstance(elem, str):
                stack[0].append(int(elem))
            else:
                stack[0].append(elem)
        elif char == "]":
            elem = stack.pop(0)
            if isinstance(elem, str):
                stack[0].append(int(elem))
            elif len(elem) > 0:
                stack[0].append(elem)
            else:
                stack.insert(0, elem)
    return stack[0]

def right_order(left, right):
    for i in range(min(len(left), len(right))):
        if isinstance(left[i], int) and isinstance(right[i], int):
            if left[i] != right[i]:
                return left[i] - right[i]
        else:
            next_left = left[i]
            if isinstance(next_left, int):
                next_left = [next_left]
            next_right = right[i]
            if isinstance(next_right, int):
                next_right = [next_right]
            compare = right_order(next_left, next_right)
            if compare != 0:
                return compare
    return len(left) - len(right)

def puzzle_2():
    result = [[[2]], [[6]]]
    input_txt = open("input.txt", "r")
    lines = input_txt.read().splitlines()
    for pos in range(0, len(lines), 3):
        result.append(eval(lines[pos]))
        result.append(eval(lines[pos+1]))

    result.sort(key=cmp_to_key(right_order))

    return (result.index([[2]])+1)*(result.index([[6]])+1)


if __name__ == '__main__':
    print(f"Puzzle 1: {puzzle_1()}")
    print(f"Puzzle 2: {puzzle_2()}")
