class HammingEncoder:
    def __init__(self):
        self.initial_code = list()
        self.encoded_code = ""
        self.bits = list()

    def encode(self, code: str):

        # Разбиваем входное сообщение на список символов
        self.initial_code = list(map(lambda s: int(s), list(code)))

        # Расставляем проверочные биты, пока что со значением 0
        self.insert_check_bits()

        # Устаналиваем для каждого проверочного бита его значение 0 или 1
        self.set_control_bits()

        # Вставляем обновленные значения в сообщение
        self.correct_control_bits()

        # Сообщение с проверочными битами
        self.encoded_code = "".join(str(i) for i in self.initial_code)

        # Запись закодироанного сообщения
        with open('encode_text.txt', 'w') as file_writer:
            file_writer.write(self.encoded_code)

    def insert_check_bits(self):
        """
        Метод вставляет контрольные биты в сообщение
        """
        i = 1
        while i < len(self.initial_code) + 1:
            self.initial_code.insert(i - 1, 0)
            self.bits.append(0)
            i *= 2

    def set_control_bits(self):
        """
        Подсчет значений контрольных битов
        """
        for i in range(len(self.initial_code)):
            binary_code = str(bin(i + 1))[2:]
            binary_code = '0' * (len(self.bits) - len(binary_code)) + binary_code
            if self.initial_code[i] != 0:
                for j in range(len(binary_code)):
                    self.bits[-j - 1] += 1 if binary_code[j] == '1' else 0
                    self.bits[-j - 1] %= 2

    def correct_control_bits(self):
        """
        Расстановка значений у контрольных битов в сообщение
        """
        i = 1
        k = 0
        while i < len(self.initial_code):
            self.initial_code[i - 1] = self.bits[k]
            k += 1
            i *= 2


class HammingDecoder:
    def __init__(self):
        self.initial_code = list()
        self.decoded_code = ""
        self.bits = list()

    def decode(self, code):
        """
        Декодирование сообщение закодироанного алгоритмом Хемминга
        """
        # Разбиваем входное сообщение на список символов
        self.initial_code = list(map(lambda s: int(s), list(code)))

        # Создаем массив битов
        self.set_bits()

        # Проверяем корректность контрольных битов, заново высчитываем все контрольные биты.
        self.check_correctness()

        # Убираем контрольные биты из входного сообщения.
        self.set_decoded_code()

        with open('decode_text.txt', 'w') as file_writer:
            file_writer.write(self.decoded_code)

    def check_correctness(self):
        for i in range(len(self.initial_code)):
            binary_code = str(bin(i + 1))[2:]
            binary_code = '0' * (len(self.bits) - len(binary_code)) + binary_code
            if self.initial_code[i] != 0:
                for j in range(len(binary_code)):
                    self.bits[-j - 1] += 1 if binary_code[j] == '1' else 0
                    self.bits[-j - 1] %= 2

        i = 1
        error_bit = 0
        for bit in self.bits:
            if bit == 1:
                error_bit += i
            i *= 2

        if error_bit != 0:
            print(f"Error found. Bit No. - {error_bit}. Fixing")

            self.initial_code[error_bit - 1] = 1 - self.initial_code[error_bit - 1]

    def set_bits(self):
        i = 1
        while i < len(self.initial_code):
            self.bits.append(0)
            i *= 2

    def set_decoded_code(self):
        offset = 0
        i = 1
        length = len(self.initial_code)
        while i < length:
            self.initial_code.pop(i - 1 - offset)
            offset += 1
            i *= 2

        self.decoded_code = "".join(str(i) for i in self.initial_code)


def get_parameters():
    print('Enter 1 if you want to encode the .txt file.')
    print('Enter 2 if you want to decode the .txt file.')
    encode_or_decode = input()

    print('Enter absolute path to file with text.')
    file_path_with_text = input(
        'C:\\Users\\Никита\\Desktop\\3.TIC\\tic\\Algorithms\\Algorithm-of-Hamming\\text.txt')
    file_path_with_text = file_path_with_text if file_path_with_text else 'C:\\Users\\Никита\\Desktop\\3.TIC\\tic\\Algorithms\\Algorithm-of-Hamming\\text.txt'

    print('Enter absolute path to file with encode text.')
    file_path_with_encode_text = input(
        'C:\\Users\\Никита\\Desktop\\3.TIC\\tic\\Algorithms\\Algorithm-of-Hamming\\encode_text.txt')
    file_path_with_encode_text = file_path_with_encode_text if file_path_with_encode_text else 'C:\\Users\\Никита\\Desktop\\3.TIC\\tic\\Algorithms\\Algorithm-of-Hamming\\encode_text.txt'

    print('Enter absolute path to file with decode text.')
    file_path_with_decode_text = input(
        'C:\\Users\\Никита\\Desktop\\3.TIC\\tic\\Algorithms\\Algorithm-of-Hamming\\decode_text.txt')
    file_path_with_decode_text = file_path_with_decode_text if file_path_with_decode_text else 'C:\\Users\\Никита\\Desktop\\3.TIC\\tic\\Algorithms\\Algorithm-of-Hamming\\decode_text.txt'

    return encode_or_decode, file_path_with_text, file_path_with_encode_text, file_path_with_decode_text


def main():

    encode_or_decode, file_path_with_text, file_path_with_encode_text, file_path_with_decode_text \
        = get_parameters()

    if encode_or_decode == '1':
        encoder = HammingEncoder()
        with open(file_path_with_text, 'r') as file:
            encoder.encode(file.read())

        print(encoder.encoded_code)

    elif encode_or_decode == '2':
        decoder = HammingDecoder()
        with open(file_path_with_encode_text, 'r') as file:
            decoder.decode(file.read())

        print(decoder.decoded_code)


if __name__ == '__main__':
    main()
