import csv
import time

class CSVAppender:
    def __init__(self, filename='data.csv'):
        self.filename = filename
        self.file = open(filename, 'a', newline='')
        self.writer = csv.writer(self.file)

        # Check if the file already has content
        # If not, write headers
        if self.file.tell() == 0:
            self.writer.writerow(["timestamp", "num1", "operator", "num2", "timetaken"])

    def append(self, timestamp, num1, operator, num2, timetaken):
        self.writer.writerow([timestamp, num1, operator, num2, timetaken])
        # If you want to ensure data is written immediately (not buffered), uncomment next line:
        # self.file.flush()

    def close(self):
        self.file.close()

# Sample usage:
appender = CSVAppender()
appender.append(time.time(), 5, '+', 3, 2.3)
time.sleep(5)
appender.append(time.time(), 7, '*', 4, 1.8)
appender.close()