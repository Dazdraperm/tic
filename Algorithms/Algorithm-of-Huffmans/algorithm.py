import copy


class AlgorithmHuffman:
    """ Данный класс описывает работу алгоритма Хаффмана """

    def __init__(self, *, file_path_with_text: str,
                 file_path_with_encode_text: str,
                 file_path_with_codecs: str,
                 file_path_with_decode_text: str):

        self.__file_path_with_text = file_path_with_text if file_path_with_encode_text else 'C:\\Users\\Никита\\Desktop\\3.TIC\\tic\\Algorithms\\Algorithm-of-Huffmans\\Folder-with-Text\\text_1.txt'
        self.__file_path_with_encode_text = file_path_with_encode_text if file_path_with_encode_text else 'C:\\Users\\Никита\\Desktop\\3.TIC\\tic\\Algorithms\\Algorithm-of-Huffmans\\Folder-with-Text\\encoded_text.txt'
        self.__file_path_with_codecs = file_path_with_codecs if file_path_with_codecs else 'C:\\Users\\Никита\\Desktop\\3.TIC\\tic\\Algorithms\\Algorithm-of-Huffmans\\Folder-with-Text\\codec.txt'
        self.__file_path_with_decode_text = file_path_with_decode_text if file_path_with_decode_text else 'C:\\Users\\Никита\\Desktop\\3.TIC\\tic\\Algorithms\\Algorithm-of-Huffmans\\Folder-with-Text\\decoded_text.txt'

        self.frequency_list = []
        self.buffer = list(range(10))

    def decoding_huffman(self):
        """
        Декодировании текста, закодированного алгоритмом Хаффмана

        :return:
        """
        codecs = self.get_codecs(self.get_lines_from_file(self.__file_path_with_codecs), encode=False)
        encode_text = self.get_lines_from_file(self.__file_path_with_encode_text)

        with open(self.__file_path_with_decode_text, 'w') as file_writer:
            char = ''

            for line in encode_text:
                for bit_num in line:
                    char += bit_num

                    if char in codecs:
                        file_writer.write(codecs[char])

                        char = ''

    def encoding_huffman(self):
        """
        Алгоритм Хаффмана

        :return:
        """
        # Стираем данные о кодировке из файла
        with open(self.__file_path_with_codecs, 'w') as file_writer:
            file_writer.write('')

        # Стираем закодированный текст из файла
        with open(self.__file_path_with_encode_text, 'w') as file_writer:
            file_writer.write('')

        # Получаем строки из файла
        lines = self.get_lines_from_file(self.__file_path_with_text)

        # Получаем лист частоты появлений символов в тексте
        frequency_list = self.get_the_char_frequency(lines=lines)

        # Создание дерева
        root = self.create_the_tree_huffman(frequency_list=frequency_list)

        # Расстановка значений по дереву
        self.set_code_for_char(node=root, code=0)

        # Кодирование текста
        codecs = self.get_codecs(self.get_lines_from_file(self.__file_path_with_codecs))
        self.encoding_text(codecs, lines)

    @staticmethod
    def get_codecs(lines: list, encode: bool = True) -> dict:
        """
        Возвращает кодировку символ-битовое значение и обратно.

        :param lines:
        :param encode:
        :return:
        """

        codecs = dict()

        for line in lines:
            line = line.replace('\n', '').split(' is: ')
            if encode:
                codecs[line[0]] = line[1]
            else:
                codecs[line[1]] = line[0]
        return codecs

    def encoding_text(self, codecs: dict, lines: list):
        with open(self.__file_path_with_encode_text, 'a') as file_writer:
            for line in lines:
                for char in line:
                    file_writer.write(codecs[char])

    def set_code_for_char(self, node, code):
        """
        Проходим по дереву, чтобы подсчитать кодировку, каждого значения
        :param code:
        :param node:
        :return:
        """
        # print(node.name if node.name else node.sub_name, node.value, node.left_child, node.right_child)
        # print(self.buffer)
        if node.name:
            symbol_value = ''
            for i in range(code):
                symbol_value += str(self.buffer[i])

            with open(self.__file_path_with_codecs, 'a', newline='') as file_writer:
                file_writer.write(f'{node.name} is: {symbol_value}\n')

        elif node.sub_name:
            # Происходит разбиение на то в какую сторону идет дерево, если 0, то влево, если 1, то вправо
            self.buffer[code] = 0
            self.set_code_for_char(node.left_child, code + 1)
            self.buffer[code] = 1
            self.set_code_for_char(node.right_child, code + 1)

        else:

            return

    @staticmethod
    def create_the_tree_huffman(frequency_list: list):
        """
        Создание дерева элементов

        :param frequency_list:
        :return:
        """
        tree = copy.deepcopy(frequency_list)

        while len(tree) != 1:
            tree.sort(key=lambda node: node.value, reverse=True)

            first_element = tree.pop(-1)
            second_element = tree.pop(-1)
            name_first_element = first_element.name if first_element.name else first_element.sub_name
            name_second_element = second_element.name if second_element.name else second_element.sub_name

            n = Node(sub_name=name_first_element + ' ' + name_second_element,
                     value=(first_element.value + second_element.value))

            n.left_child = first_element
            n.right_child = second_element

            tree.append(n)

        return tree[0]

    @staticmethod
    def get_lines_from_file(file_name) -> list:
        lines = []

        with open(file_name, 'r') as file:
            for line in file.readlines():
                line = line.lower()
                lines.append(line)

        return lines

    @staticmethod
    def get_the_char_frequency(lines: list) -> list:
        """
        Подсчет частосты символов встречающихся в тексте

        :return: Возвращает лист состоящий из некоторого количества Node (буква и количество ее встреч)
        """
        frequency_dict = dict()
        for line in lines:
            for char in line:
                if char.isalpha():
                    if char in frequency_dict:
                        frequency_dict[char] += 1
                    else:
                        frequency_dict.update({char: 1})

        return [Node(k, v) for k, v in frequency_dict.items()]

    @staticmethod
    def sort_frequency_list(frequency_list):
        frequency_list.sort(key=lambda node: node.value, reverse=True)


# Создать класс узла
class Node:
    def __init__(self, name=None, value=None, sub_name=None):
        self.name = name
        self.value = value
        self.left_child = None
        self.right_child = None
        self.sub_name = sub_name

    def __str__(self):
        return f'{self.name, self.value}'

    def __repr__(self):
        return f'{self.name, self.value}'


def get_parameters():
    print('Enter 1 if you want to encode the .txt file.')
    print('Enter 2 if you want to decode the .txt file.')
    encode_or_decode = input()

    print('Enter absolute path to file with text.')
    file_path_with_text = input(
        'C:\\Users\\Никита\\Desktop\\3.TIC\\tic\\Algorithms\\Algorithm-of-Huffmans\\Folder-with-Text\\text_1.txt')

    print('Enter absolute path to file with encode text.')
    file_path_with_encode_text = input(
        'C:\\Users\\Никита\\Desktop\\3.TIC\\tic\\Algorithms\\Algorithm-of-Huffmans\\Folder-with-Text\\encoded_text.txt')

    print('Enter the absolute path to the file where the codecs will be saved.')
    file_path_with_codecs = input(
        'C:\\Users\\Никита\\Desktop\\3.TIC\\tic\\Algorithms\\Algorithm-of-Huffmans\\Folder-with-Text\\codec.txt')

    print('Enter absolute path to file with decode text.')
    file_path_with_decode_text = input(
        'C:\\Users\\Никита\\Desktop\\3.TIC\\tic\\Algorithms\\Algorithm-of-Huffmans\\Folder-with-Text\\decoded_text.txt')

    return encode_or_decode, file_path_with_text, file_path_with_encode_text, file_path_with_codecs, file_path_with_decode_text


def main():
    encode_or_decode, file_path_with_text, file_path_with_encode_text, file_path_with_codecs, file_path_with_decode_text\
        = get_parameters()

    algorithm = AlgorithmHuffman(file_path_with_text=file_path_with_text,
                                 file_path_with_encode_text=file_path_with_encode_text,
                                 file_path_with_codecs=file_path_with_codecs,
                                 file_path_with_decode_text=file_path_with_decode_text)

    if encode_or_decode == '1':
        algorithm.encoding_huffman()

    elif encode_or_decode == '2':
        algorithm.decoding_huffman()


if __name__ == '__main__':
    main()
