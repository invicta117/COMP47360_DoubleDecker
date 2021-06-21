
import os
import time

def clean_line(line, delimiter):
    months = {"JAN": "01", "FEB": "02", "MAR": "03", "APR": "04", "MAY": "05", "JUN": "06", "JUL": "07", "AUG": "08",
              "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12"}
    for month in months.keys():
        if month.lower() in line:
            line = line.replace(month.lower(), months[month])
    line = line.split(delimiter)
    line = ["NULL" if cell=="" else cell for cell in line]
    line = ["NULL" if cell == " " else cell for cell in line]
    line = [cell.strip(" ") for cell in line]
    line = ["NULL\n" if cell == "\n" else cell for cell in line]
    #print("Line", line)
    return line

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
    for i in range(16):
        header = fin.readline()
    for num, line in enumerate(fin):
        columns = clean_line(line, delimiter)
        columns = columns_to_string(columns)
        #print(num, columns)
        fout.write(columns)
    fin.close()
    fout.close()


if __name__=="__main__":
    start_time = time.time()
    rt_trips = "./hly175/hly175.csv"
    create_file(rt_trips, "weather.csv", delimiter=",")
    print("--- %s seconds ---" % (time.time() - start_time))
