import re
import csv
from pprint import pprint


def read_book(filename):
    with open(filename, encoding="utf8") as f:
        rows = csv.reader(f, delimiter=",")
        contact_list = list(rows)
    return contact_list


def write_book(filename, list):
    with open(filename, "w") as f:
        datawriter = csv.writer(f, delimiter=",")
        datawriter.writerows(list)


# Удаление сдублирующихся записей по Фамилия + Имя
def delete_double(source_list):
    k = 1
    while k < len(source_list) - 1:
        source_list.sort(key=lambda item: item[0] + " " + item[1])
        result = []
        new_list = list(zip(source_list[k], source_list[k + 1]))
        if new_list[0][0] == new_list[0][1] and new_list[1][0] == new_list[1][1]:
            for elem in new_list:
                if elem[0] == "":
                    result.append(elem[1])
                elif elem[1] == "":
                    result.append(elem[0])
                else:
                    result.append(elem[0])
            source_list.remove(source_list[k + 1])
            source_list.remove(source_list[k])
            source_list.append(result)
        else:
            k += 1

    return source_list


# Замена номеров согласно шаблону
def replace_phone(source_list):
    result_list = []
    for elem in source_list:
        pattern_phone = r"(\+7|8)?\s*\(*(\d{3})\)*\s*\-*(\d{3})\-*(\d{2})\-*(\d{2})"
        pattern_add = r"\s*\(*доб.\)*\s*(\d{4})\)*"
        sub_phone = r"+7(\2)\3-\4-\5"
        sub_add = r" доб.\1"
        res = re.sub(pattern_phone, sub_phone, "&&".join(elem))
        res = re.sub(pattern_add, sub_add, res)
        result_list.append(res.split("&&"))
    return result_list


if __name__ == '__main__':
    list_contact = read_book("phonebook_raw.csv")
    for elem in list_contact:
        # print(item)
        fio = elem[0] + " " + elem[1] + " " + elem[2]
        fio = re.split(r"\s", fio)
        elem[0], elem[1], elem[2] = fio[0], fio[1], fio[2]

    clear_list = delete_double(list_contact)
    out_list = replace_phone(clear_list)
    write_book("phonebook.csv", out_list)
