# Разработаем программу, в которой есть два вида задач - генерация чисел и проверка на простоту. Производитель
# генерирует числа, а потребитель проверяет их на простоту.

import threading
from queue import Queue
import math


class Producer(threading.Thread):
    def __init__(self, number_queue, max_numbers):
        threading.Thread.__init__(self)
        self.number_queue = number_queue
        self.max_numbers = max_numbers

    def run(self):
        for num in range(2, self.max_numbers + 1):
            self.number_queue.put(num)

        self.number_queue.put(None)  # Сигнал конца генерации чисел


class Consumer(threading.Thread):
    def __init__(self, input_queue, output_queue):
        threading.Thread.__init__(self)
        self.input_queue = input_queue
        self.output_queue = output_queue

    def is_prime(self, num):
        if num < 2:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True

    def run(self):
        while True:
            num = self.input_queue.get()

            if num is None:
                break

            if self.is_prime(num):
                self.output_queue.put((num, True))
            else:
                self.output_queue.put((num, False))


if __name__ == '__main__':
    max_number = 20  # Максимальное число для проверки

    input_queue = Queue()  # Очередь для входных чисел
    output_queue = Queue()  # Очередь для результатов проверки

    producer = Producer(input_queue, max_number)
    prime_checker = Consumer(input_queue, output_queue)

    # Запуск производителя и потребителя
    producer.start()
    prime_checker.start()

    # Ожидание завершения работы потребителя
    prime_checker.join()

    # Вывод результатов
    while not output_queue.empty():
        num, is_prime = output_queue.get()
        status = "простое" if is_prime else "составное"
        print(f"Число {num} - {status}")