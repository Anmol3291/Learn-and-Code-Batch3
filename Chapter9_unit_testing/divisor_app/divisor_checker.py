class DivisorChecker:
    def __init__(self):
        self.divisor_cache = {}

    def count_divisors(self, number):
        if number in self.divisor_cache:
            return self.divisor_cache[number]

        if number == 1:
            self.divisor_cache[number] = 1
            return 1

        count = 0
        for i in range(1, int(number**0.5) + 1):
            if number % i == 0:
                count += 1 if i * i == number else 2

        self.divisor_cache[number] = count
        return count

    def count_valid_n(self, k):
        count = 0
        for n in range(2, k):
            if self.count_divisors(n) == self.count_divisors(n + 1):
                count += 1
        return count
