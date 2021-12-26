import json
from collections import defaultdict, Counter


class ArithmeticEncoder:
    def __init__(self, precision):
        self.initial_text = ''
        self.total = 0
        self.code = ''
        self.codes = list()
        self.probabilities = {}
        self.left = 0
        self.right = 10 ** precision
        self.denominator = 10 ** precision
        self.precision = precision
        self.sums = defaultdict(list)

    def encode(self, source, destination, probabilities=""):
        # Считываем файл и добавляем ограничивающий символ в конец
        self.read_file(source)

        #
        self.set_probabilities(probabilities)
        self.fill_sums()
        for char in self.initial_text:
            self.count_intervals(char)
        self.build_code()
        self.write_code(destination)
        self.save_probabilities(probabilities)

    def read_file(self, source):
        with open(source, 'r', encoding="utf8") as f:
            self.initial_text = f.read()
        if "\0" in self.initial_text:
            raise Exception("\0 is used as escape character, but found in text. Returning")

        self.initial_text += "\0"

    def set_probabilities(self, probabilities=""):
        if probabilities == "":
            self.probabilities = Counter(self.initial_text)
            for char, count in self.probabilities.items():
                string = str(count / len(self.initial_text))[2:self.precision + 2]
                self.probabilities[char] = int(string)
            if self.probabilities['\0'] == 0:
                raise Exception("Not enough precision")
        else:
            with open(probabilities, "r", encoding="utf8") as f:
                self.probabilities = json.loads(f.read())

    def fill_sums(self):
        sum = 0
        for char, count in self.probabilities.items():
            self.sums[char] = [sum, sum + count]
            sum += count

    def count_intervals(self, char):
        right = self.left * 10 ** self.precision + (self.right - self.left) * self.sums[char][1]
        left = self.left * 10 ** self.precision + (self.right - self.left) * self.sums[char][0]
        self.left = left
        self.right = right
        self.denominator *= 10 ** self.precision

    def build_code(self):
        left = f"0.{'0' * (len(str(self.denominator)) - len(str(self.left)) - 1)}{self.left}"
        right = f"0.{'0' * (len(str(self.denominator)) - len(str(self.right)) - 1)}{self.right}"
        total = 0
        power = 0
        next_ = 5
        while True:
            current = total + next_
            power += 1
            string = f"0.{'0' * (power - len(str(current)))}{current}"
            if string < left:
                self.code += "1"
                total += next_
            if left <= string < right:
                self.code += "1"
                break
            if string >= right:
                self.code += "0"
            total *= 10
            next_ *= 5

        self.code += "0" * (8 - len(self.code) % 8)

    def write_code(self, destination):
        for i in range(0, len(self.code), 8):
            self.codes.append(int(self.code[i: i + 8], 2))
        with open(destination, 'wb') as f:
            f.write(bytes(self.codes))

    def save_probabilities(self, probabilities):
        if probabilities == "":
            probabilities = "probabilities.json"
        string = json.dumps(self.probabilities)
        with open(probabilities, "w", encoding="utf8") as f:
            f.write(string)


class ArithmeticDecoder:
    def __init__(self, probabilities, precision=0):

        with open(probabilities, 'r', encoding='utf8') as f:
            self.probabilities: dict = json.loads(f.read())
        if precision == 0:
            max_precision = 0

            for char, value in self.probabilities.items():
                max_precision = max(max_precision, len(str(value)))
            self.precision = max_precision
        else:
            self.precision = precision
        self.denominator = 10 ** self.precision
        self.text = ''
        self.left = 0
        self.right = 10 ** self.precision
        self.number = 0
        self.bytes = list()
        self.sums = defaultdict(list)
        self.power = 0

    def decode(self, source, destination):
        self.read_file(source)
        self.build_number()
        self.fill_sums()
        self.build_text()
        self.write_text(destination)

    def read_file(self, source):
        with open(source, 'rb') as f:
            self.bytes = list(map(lambda s: str(bin(s))[2:], list(f.read())))

    def build_number(self):
        total = 0
        next_ = 5
        power = 1
        for byte in self.bytes:
            byte = '0' * (8 - len(byte)) + byte
            for char in byte:
                if char == '1':
                    total += next_
                next_ *= 5
                power += 1
                total *= 10
        self.number = total
        self.power = power

    def fill_sums(self):
        sum = 0
        for char, count in self.probabilities.items():
            self.sums[char] = [sum, sum + count]
            sum += count

    def count_intervals(self, char):
        right = self.left * 10 ** self.precision + (self.right - self.left) * self.sums[char][1]
        left = self.left * 10 ** self.precision + (self.right - self.left) * self.sums[char][0]
        return left, right

    def build_text(self):
        string = f"0.{'0' * (self.power - len(str(self.number)))}{self.number}"
        finish = False
        while not finish:
            for char, value in self.probabilities.items():
                denominator = self.denominator * 10 ** self.precision
                left, right = self.count_intervals(char)
                left_ = f"0.{'0' * (len(str(denominator)) - len(str(left)) - 1)}{left}"
                right_ = f"0.{'0' * (len(str(denominator)) - len(str(right)) - 1)}{right}"
                if left_ <= string < right_:
                    if char == '\0':
                        finish = True
                        break
                    self.text += char
                    self.left = left
                    self.right = right
                    self.denominator *= 10 ** self.precision

    def write_text(self, destination):
        with open(destination, "w", encoding="utf8") as f:
            f.write(self.text)


if __name__ == '__main__':
    encoder = ArithmeticEncoder(precision=5)
    encoder.encode("text_arithmetic.txt", "arithmetic.binary")

    decoder = ArithmeticDecoder("probabilities.json", precision=5)
    decoder.decode("arithmetic.binary", "arithmetic_decode.txt")

    with open("text_arithmetic.txt", "r", encoding="utf8") as inp:
        with open("arithmetic_decode.txt", 'r', encoding="utf8") as out:
            assert inp.read() == out.read()