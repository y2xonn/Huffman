import os

os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Graphviz\bin"

from collections import Counter
import heapq
import math
from graphviz import Digraph

# 허프만 트리 노드
class Node:
    count = 0

    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

        self.id = str(Node.count)
        Node.count += 1

    def __lt__(self, other):
        return self.freq < other.freq


# 허프만 트리 생성
def build_tree(text):

    frequency = Counter(text)

    heap = []

    for char, freq in frequency.items():
        heapq.heappush(heap, Node(char, freq))

    while len(heap) > 1:

        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        parent = Node(None, left.freq + right.freq)
        parent.left = left
        parent.right = right

        heapq.heappush(heap, parent)

    return heap[0], frequency


# 허프만 코드 생성
def make_codes(node, code="", codes=None):

    if codes is None:
        codes = {}

    if node is None:
        return codes

    if node.char is not None:
        codes[node.char] = code if code else "0"

    make_codes(node.left, code + "0", codes)
    make_codes(node.right, code + "1", codes)

    return codes


# 압축
def compress(text, codes):

    return "".join(codes[ch] for ch in text)


# 엔트로피
def entropy(freq):

    total = sum(freq.values())

    H = 0

    for f in freq.values():

        p = f / total

        H -= p * math.log2(p)

    return H


# 허프만 트리 그림 생성
def draw_tree(root):

    dot = Digraph(
        "HuffmanTree",
        format="png"
    )

    dot.attr(rankdir="TB")

    dot.attr(
        "node",
        shape="circle",
        style="filled",
        fillcolor="lightblue",
        fontname="Malgun Gothic",
        fontsize="12"
    )

    def dfs(node):

        if node is None:
            return

        if node.char is None:
            label = f"{node.freq}"
        else:
            label = f"{node.char}\n({node.freq})"

        dot.node(node.id, label)

        if node.left:

            dfs(node.left)

            dot.edge(
                node.id,
                node.left.id,
                label="0"
            )

        if node.right:

            dfs(node.right)

            dot.edge(
                node.id,
                node.right.id,
                label="1"
            )

    dfs(root)

    # tree.png 생성
    from datetime import datetime
    filename = datetime.now().strftime("tree_%Y%m%d_%H%M%S")
    dot.render(filename, cleanup=True)
    print("\n허프만 트리 이미지 저장 완료")
    print("파일명 :", filename)


# 메인

print("=" * 45)
print("Huffman Coding 압축 프로그램")
print("=" * 45)

text = input("\n텍스트 입력 : ")
count_without_whitespace = len("".join(text.split()))
print(f"글자 수(공백 포함) : {len(text)}")
print(f"글자 수(공백 제외) : {count_without_whitespace}")

tree, frequency = build_tree(text)

codes = make_codes(tree)

compressed = compress(text, codes)

before_bits = len(text) * 8

after_bits = len(compressed)

ratio = (before_bits - after_bits) / before_bits * 100

H = entropy(frequency)

print("\n")
print("=" * 45)
print("문자 빈도")
print("=" * 45)

for char, freq in sorted(frequency.items()):
    print(f"{repr(char):>5} : {freq}")

print("\n")
print("=" * 45)
print("허프만 코드")
print("=" * 45)

for char, code in sorted(codes.items()):
    print(f"{repr(char):>5} : {code}")

print("\n")
print("=" * 45)
print("압축 결과")
print("=" * 45)

print(f"원본 크기      : {before_bits} bit")
print(f"압축 후 크기   : {after_bits} bit")
print(f"압축률         : {ratio:.2f}%")
print(f"엔트로피       : {H:.4f} bit/symbol")




draw_tree(tree)

print("\n프로그램 종료")