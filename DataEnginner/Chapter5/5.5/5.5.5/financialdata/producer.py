from financialdata.tasks.task import Update
import sys


if __name__ == "__main__":
    dataset, start_date, end_date = sys.argv[1:]
    Update(dataset, start_date, end_date)
