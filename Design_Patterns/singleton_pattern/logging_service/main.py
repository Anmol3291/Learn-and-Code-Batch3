from logging_service.logger import Logger


def main():
    """Demonstrate the singleton logger implementation."""
    try:
        logger1 = Logger()
        logger2 = Logger()

        try:
            result = 10 / 0
            print(result)
        except Exception as e:
            logger1.log(f"Error processing data: {e}")

        logger2.log("This is a log message from logger2.")

        print("logger1 and logger2 are the same instance:", logger1 is logger2)

        print("Logs from logger1:")
        for log in logger1.get_logs():
            print(log)

        print("Logs from logger2:")
        for log in logger2.get_logs():
            print(log)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
