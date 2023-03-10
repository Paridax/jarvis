import datetime


def get_timezone_offset(timezone):
    timezone_dict = {
        'EST': -5,
        'CST': -6,
        'MST': -7,
        'PST': -8,
        'AKT': -9,
        'HST': -10,
        'AST': -4,
        'GMT': 0,
        'BST': 1,
        'CET': 1,
        'EET': 2,
        'MSK': 3,
        'IST': 5.5,
        'WIB': 7,
        'CHST': 8,
        'JST': 9,
        'AET': 10,
        'NZT': 12,
        'NST': -3.5,
        'CAT': 2
    }
    return timezone_dict.get(timezone, 0)


def get_time(dictionary):
    # dictionary has timeZone as string
    # get time
    if dictionary.get("timeZone") is None:
        # print("No timezone found")
        # default to local timezone
        # get the time
        time = datetime.datetime.now()
        # convert to format "HH:MM AM/PM"
        time = time.strftime("It is %I:%M %p")
        print(time)
        return
    # get timezone offset, as an integer
    timezone_offset = dictionary.get("timeZone")

    try:
        timezone_offset = int(timezone_offset)
    except ValueError:
        print("I couldn't find this for you. Please try again. The timezone offset was invalid.")
        return

    # get the time as UTC
    time = datetime.datetime.utcnow()
    # add the timezone offset
    time = time + datetime.timedelta(hours=timezone_offset)
    # convert to format "HH:MM AM/PM"
    time = time.strftime("%I:%M %p")
    print("It is " + time + " in " + dictionary.get("location"))