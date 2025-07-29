# 3rd Party Packages
...

# Our own package related, Syntax: from package.module import class/function
from attendance_tool.processor import Processor


def main():
    proccesor = Processor("input.csv")
    valid_rows, invalid_rows = proccesor.validate()

    print("=========Successful=============")
    for row in valid_rows:
        print(row, end="\n\n")
        
    print("=========Not successful=============")
    for row in invalid_rows:
        print(row, end="\n\n")


if __name__ == "__main__":
    main()
