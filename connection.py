import csv


def read_from_file(filename):
    with open(filename, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        data = []
        for row in reader:
            data.append(row)
    csv_file.close()
    return data


def append_to_file(filename, dict_to_append):
    with open(filename, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file)
        writer.writerow(dict_to_append)
    csv_file.close()

def write_to_file(filename, list_of_dicts_to_write):
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file)

        writer.writeheader()
        for row in list_of_dicts_to_write:
            writer.writerow(row)
    csv_file.close()