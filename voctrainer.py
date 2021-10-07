from colorama import Fore
import os
import random

def get_categories():
    categories = []
    for current in os.listdir("."):
        if os.path.isdir(current):
             categories.append(current)
    return  categories

def get_sub_categories(category):
    path = ".\\" + get_categories()[category - 1] +"\\"
    sub_categories = []
    for current in os.listdir(path):
        if not os.path.isdir(current) and not current == "performance.txt":
            sub_categories.append(current)
    return sub_categories

def get_percent(category, sub_category=0):
    if sub_category == 0:
        with open("performance.txt", "r", encoding="utf-8") as fi:
            lines = fi.readlines()
            category_lines = 0
            category = get_categories()[category - 1]
            all_percent = 0
            for line in lines:
                category_name, percent = line.split("=")
                if category_name.split("/")[0] == category:
                    all_percent += int(percent)
                    category_lines += 1
            if category_lines != 0:
                all_percent /= category_lines
                return int(all_percent)
            else: 
                return 0
    else:
        with open("performance.txt", "r", encoding="utf-8") as fi:
            lines = fi.readlines()
            category_name = get_categories()[category - 1]
            sub_category_name = get_sub_categories(category)[sub_category - 1]
            for line in lines:
                current_category, percent = line.split("=")
                if current_category == category_name + "/" + sub_category_name:
                    return percent

def get_percent_string(percent):
    done = f"{Fore.LIGHTGREEN_EX}" + ("-" * int(int(percent) / 5))
    failed = f"{Fore.LIGHTBLACK_EX}" + ("-" * int(20 - (int(percent) / 5)))
    if (len(failed) + len(done) - 10) == 19:
        failed += "-"
    string =  done + failed + f"{Fore.WHITE}"
    return string

def get_word_lines(category, sub_category):
    with open(get_categories()[category - 1] + "/" + get_sub_categories(category)[sub_category - 1], "r", encoding="utf-8") as fi:
        lines = fi.readlines()
    while len(lines) > 0:
        r = random.randint(0, len(lines) - 1)
        line = lines[r]
        lines.remove(line)
        yield line

def choose_category():
    print("Choose a category:")
    category = 0
    categories = get_categories()
    while category > len(categories) or category < 1:
        i = 0
        for current_category in categories:
            i += 1
            percent_string = get_percent_string(get_percent(i, 0))
            print(f"{i}: {current_category} {percent_string}")
        category = int(input(">"))
        if category > len(categories) or category < 1:
            print("Invalid category!")
    return category

def choose_sub_category(category):
    sub_categories = get_sub_categories(category)
    sub_category = 0
    while sub_category < 1 or sub_category > len(sub_categories):
        i = 0
        for current_sub_category in sub_categories:
            i += 1
            percent_string = get_percent_string(get_percent(category, i))
            print(f"{i}: {current_sub_category} {percent_string}") 
        sub_category = int(input(">"))
        if sub_category < 1 or sub_category > len(sub_categories):
            print("Invalid sub category!")
    return sub_category

def check_for_update():
    pass

def update():
    pass

while True:
    category = choose_category()
    sub_category = choose_sub_category(category)
    done = 0
    failed = 0
    leng = 0

    for line in get_word_lines(category, sub_category):
        one, two = line.replace("\n","").split("=")
        r = random.randint(1, 2)
        leng += 1

        if r == 1:
            print(one)
            answer = input(">")
            if answer == two:
                done += 1
                print(f"{Fore.LIGHTGREEN_EX}Correct!{Fore.WHITE}")
            else:
                failed += 1
                print(f"{Fore.RED}False!{Fore.WHITE} Solution: {two}")
        elif r == 2:
            print(two)
            answer = input(">")
            if answer == one:
                done += 1
                print(f"{Fore.LIGHTGREEN_EX}Correct!{Fore.WHITE}")
            else:
                failed += 1
                print(f"{Fore.RED}False!{Fore.WHITE} Solution: {one}")

    percent = done / leng * 100
    sub_category_name = get_sub_categories(category)[sub_category - 1]
    final = ""

    with open("performance.txt", "r", encoding="utf-8") as fi:
        category_name = get_categories()[category - 1]
        lines = fi.readlines()
        for line in lines:
            line = line.replace("\n", "")
            if not line.split("=")[0] == category_name + "/" + sub_category_name:
                final += line + "\n"

    final += str(get_categories()[category - 1]) + "/" + str(sub_category_name) + "=" + str(int(percent))

    with open("performance.txt", "w", encoding="utf-8") as fi:
        fi.writelines(final)    
        print("\n")