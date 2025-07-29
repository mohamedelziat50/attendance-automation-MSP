# 3rd Party Packages
...

# Our own package related, Syntax: from package.module import class/function
from attendance_tool.processor import Processor


def main():
    proccesor = Processor("input.csv")
    print(proccesor)


if __name__ == "__main__":
    main()
