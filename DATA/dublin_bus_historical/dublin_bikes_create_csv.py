
import os
import time
import datetime

def clean_line(line, delimiter):
    months = {"JAN": "01", "FEB": "02", "MAR": "03", "APR": "04", "MAY": "05", "JUN": "06", "JUL": "07", "AUG": "08",
              "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12"}
    for month in months.keys():
        if month in line:
            line = line.replace(month, months[month])
    line = line.replace(",", "")
    line = line.split(delimiter)
    line = [cell.strip(" ") for cell in line]
    line = ["NULL" if cell=="" else cell for cell in line]
    line[1] = test_datetime(line[1])
    line[-2] = test_datetime(line[-2])
    return line

def test_datetime(val):
    datetime = val.split(" ")
    date = datetime[0].split("-")
    final = "20" + date[2] + "-" + date[1] + "-" + date[0] + " " + datetime[1]
    return final

def columns_to_string(columns):
    result = ""
    for val, col in enumerate(columns):
        if val < len(columns) - 1:
            result += col + ","
        else:
            result += col
    return result

def create_file(filein, fileout, delimiter=";"):
    fin = open(filein, "r")
    fout = open(fileout, "a")
    header = fin.readline()
    for line in fin:
        columns = clean_line(line, delimiter)
        columns = columns_to_string(columns)
        fout.write(columns)
    fin.close()
    fout.close()


if __name__=="__main__":
    start_time = time.time()
    rt_trips = "./data/rt_trips_DB_2018.txt"
    create_file(rt_trips, "trips.csv")
    rt_leavetimes = "./data/rt_leavetimes_DB_2018.txt"
    create_file(rt_leavetimes, "leavetimes.csv")
    print("--- %s seconds ---" % (time.time() - start_time))
