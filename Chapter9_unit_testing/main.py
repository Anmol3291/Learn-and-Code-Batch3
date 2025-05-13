from divisor_app.divisor_checker import DivisorChecker


def main():
    test_cases = int(input("Enter number of test cases: "))
    divisor_checker = DivisorChecker()
    save_results = []

    for _ in range(test_cases):
        k = int(input("Enter k: "))
        result = divisor_checker.count_valid_n(k)
        save_results.append(result)

    for result in save_results:
        print(result)


if __name__ == "__main__":
    main()
