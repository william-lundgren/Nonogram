import pygame as pg
import random as rand
import time

'''
Doomsdays:
3/1 (4/1 leap year)
28/2 (29/2 leap year)
14/3
4/4 6/6 8/8 10/10 12/12
5/9 9/5

Side notes:
4/6 (USA Nationaldag)
31/10 (Halloween)
26/12 (Annandag jul)

Memorize:
osv
Doomsday 1700: Sunday
Doomsday 1800: Friday
Doomsday 1900: Wednesday
Doomsday 2000: Tuesday  
osv

Tips:
Think of days as numbers
Key years to make high years easier:
0 28 56 84 
'''


def find_cent_doom(year):
    """
    Find what the doomsday is for that century
    :param year: int: Which year (century to check)
    :return: String: Weekday for doomsday
    """
    doomsday_cents = ["Sunday", "Friday", "Wednesday", "Tuesday"]
    return doomsday_cents[(int(str(year)[:2]) - 17) % 4]


def is_leap_year(year):
    """
    Find out if a year is a leap year
    :param year: int
    :return: bool
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def find_doomsday(year):
    """
    Find doomsday for a certain year
    Number of years after century + number of leap year = Days after century dooms day
    :param year: int: year to find doomsday for
    :return: String: weekday for doomsday
    """
    week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    base_doom = find_cent_doom(year)
    base_doom_num = week.index(base_doom)

    century = int(str(year)[:2] + "00")

    leaps = (year - century) // 4

    dooms_day_final_num = (year - century + leaps + base_doom_num) % 7

    dooms_day_final = week[dooms_day_final_num]

    return dooms_day_final


def find_week_day(date, year):
    """
    Find weekday of a certain date
    :param date: String what date to find weekday for
    :param year: int year of the date
    :param leap: bool if leap year or not
    :return: String: weekday for date
    """

    # (4/1 leap year)
    # (29/2 leap year)
    leap = is_leap_year(year)

    week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    doomsdays = ["4/1" if leap else "3/1", "29/2" if leap else "28/2", "14/3", "4/4", "9/5", "6/6", "11/7", "8/8", "5/9", "10/10", "7/11", "12/12"]

    # Weekday for doomsday
    doomsday = find_doomsday(year)

    day, month = date.split("/")
    day = int(day)
    month = int(month)

    # Find doomsday for that month
    closest_doom = doomsdays[month - 1]

    # Number of days from date to doomsday
    diff = day - int(closest_doom.split("/")[0])

    # Return weekday from doomsday to date
    return week[(week.index(doomsday) + diff) % 7]


def take_inp():
    while True:
        print("Write date (d/m yyyy)")
        inp = input()
        if inp == "q":
            break
        else:
            print(find_week_day(inp.split()[0], int(inp.split()[1])))


def print_stats():
    txt = open("results.txt", "r")
    lines = txt.readlines()
    txt.close()
    plays = lines[0]
    wins = 0
    total_time = 0

    for i in lines[1:]:
        wins += int(i[0])
        total_time += float(i[2:-1])

    avg_time = total_time / int(plays)
    win_perc = wins / int(plays) * 100

    print(f"Wins: {wins} Win %: {win_perc:.3f} Average time: {avg_time:.3f}")


def practice():
    override = None
    keep_playing = True

    while keep_playing:
        normal_years = range(1900, 2050)
        weird_years = [i for i in range(1400, 2300) if not (i >= 1900 and i < 2050)]

        year_type = rand.randrange(100)

        if year_type < 0.25:
            year = rand.choice(weird_years)
        else:
            year = rand.choice(normal_years)

        month = rand.randint(1, 12)

        leap = is_leap_year(year)
        valid_days = [31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        day = rand.choice(valid_days)

        while True:
            print("Ready? (Enter to start)")
            inp = input()
            if inp == "q":
                keep_playing = False
                break
            elif inp == "override":
                pass # remove last line of txt (wrong attempt) and add to list anyway
            elif inp == "stats":
                print_stats()
            else:
                break

        if not keep_playing:
            break

        date = str(day) + "/" + str(month)
        print(date, year)
        start = time.time()

        inp = input("Answer: ")
        if inp.lower() == "q":
            break

        res = time.time() - start
        print(res)
        correct = find_week_day(date, year)
        print("Answer was " + correct)

        # Text handle
        txt = open("results.txt", "r+")
        lines = txt.readlines()
        tries = str(int(lines[0]) + 1)
        if len(lines[0]) <= len(str(tries)):
            tries += "\n"
        txt.seek(0)
        txt.write(tries)
        txt.close()

        txt = open("results.txt", "a+")
        if inp.capitalize() == correct:
            txt.write("1 " + str(round(res, 2)) + "\n")
        if inp.capitalize() != correct:
            txt.write("0 " + str(round(res, 2)) + "\n")

        # If answer was correct add to file other wise add wrong
        # Print stats, correct % and avg time


def main():
    print("Enter option: (q, write, practice)")
    while True:
        inp = input()
        if inp.lower() == "q":
            break
        elif inp.lower() == "write":
            take_inp()
            break
        elif inp.lower() == "practice":
            practice()
            break
        else:
            print("Invalid input")


if __name__ == "__main__":
    main()
