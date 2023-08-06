# A simple task tracking system
import os
import io
import re
import argparse
import datetime
import calendar
from subprocess import call
from colors import Colors

DID_HOME = os.path.expanduser("~/.did")
DID_DATA = f"{DID_HOME}/data"
EDITOR = os.environ.get('EDITOR', 'vim')

def get_copied_file_location(day: datetime.date) -> str:
    return f"{DID_DATA}/{day.year}/{day.isocalendar()[1]}/copied-{day.weekday()}.md"

def get_file_location(day: datetime.date) -> str:
    return f"{DID_DATA}/{day.year}/{day.isocalendar()[1]}/{day.weekday()}.md"

def colorise(line: str) -> str:
    string = ""
    if re.search("^# ", line):
        string += f"{Colors.BOLD}{Colors.BLUE}"
    elif re.search("^- \[ \]", line):
        string += f"{Colors.RED}"
    elif re.search("^- \[X\]", line):
        string += f"{Colors.GREEN}"
    elif re.search("^\s+-", line):
        string += f"{Colors.YELLOW}"

    return string + f"{line[:-1]}{Colors.END}"

def show_day(date: datetime.date):
    file_location = get_file_location(date)
    copied_file_location = get_copied_file_location(date)
    if (os.path.exists(copied_file_location)):
        file_location = copied_file_location

    if (not os.path.exists(file_location)):
        print(f"You did nothing on {date}")
    else:
        with open(file_location) as file:
            for line in file:
                print(colorise(line))

def show_week(date: datetime.date):
    week_path = f"{DID_DATA}/{date.year}/{date.isocalendar()[1]}"
    if (not os.path.exists(week_path)):
        print(f"You did nothing in week {date.isocalendar()[1]}")
    else:
        for weekday in range(1,8):
            day = datetime.date.fromisocalendar(date.year, date.isocalendar()[1], weekday)
            show_day(day)

def get_last_weekday(weekday: int) -> datetime.date:
    one_day = datetime.timedelta(days=1)
    date = datetime.date.today() - one_day
    while (date.weekday() != weekday):
        date = date - one_day
    return date

def handle_date(date: str) -> None:
    today = datetime.date.today()
    if (date == 'today'):
        show_day(today)
    elif (date == 'yesterday' or date == 'yes'):
        show_day(today - datetime.timedelta(days=1))
    elif (date == 'monday' or date == 'mon'):
        show_day(get_last_weekday(0))
    elif (date == 'tueday' or date == 'tue'):
        show_day(get_last_weekday(1))
    elif (date == 'wednesday' or date == 'wed'):
        show_day(get_last_weekday(2))
    elif (date == 'thursday' or date == 'thu'):
        show_day(get_last_weekday(3))
    elif (date == 'friday' or date == 'fri'):
        show_day(get_last_weekday(4))
    elif (date == 'saturday' or date == 'sat'):
        show_day(get_last_weekday(5))
    elif (date == 'sunday' or date == 'sun'):
        show_day(get_last_weekday(6))
    elif (date == 'thisweek' or date == 'week' or date == 'w'):
        show_week(today)
    elif (date == 'lastweek' or date == 'lw'):
        show_week(today - datetime.timedelta(days=7))
    else:
        try:
            day = datetime.date.fromisoformat(date)
            show_day(day)
        except ValueError:
            print(f'Invalid date format: {date}')

def handle_search(search: str) -> None:
    call(['grep', '--color=auto', '-rni', search, DID_DATA])

# Copy recent unfinished tasks to todays file if they aren't already present
# If today is the first entry in this week, look at the previous week
# Otherwise look through the previous files from this week
def copy_unfinished_tasks_to_file(file: io.TextIOWrapper, today: datetime.date) -> None:
    copy_week = f"{DID_DATA}/{today.year}/{today.isocalendar()[1]}"
    if (len(os.listdir(copy_week)) == 1): # if we are making the first file of the week
        last_week = today - datetime.timedelta(days=7)
        copy_week = f"{DID_DATA}/{today.year}/{last_week.isocalendar()[1]}"
    for filename in os.scandir(copy_week):
        if filename.is_file() and str(today.weekday()) not in filename.name and re.search("^[0-6].md", filename.name):
            with open(filename.path, 'r') as copy_file:
                copy_notes = False
                for line in copy_file:
                    if copy_notes and re.search("^\s+-", line):
                        file.write(line)
                    elif re.search("^- \[ \]", line):
                        copy_notes = True
                        file.write(line)
                    else:
                        copy_notes = False
            os.rename(filename.path, f"{copy_week}/copied-{filename.name}")

def did() -> None:
    today = datetime.date.today()
    week = today.isocalendar()[1]
    today_file = f"{DID_DATA}/{today.year}/{week}/{today.weekday()}.md"
    today_header = f"# {calendar.day_name[today.weekday()]} {today.day} {calendar.month_name[today.month]} {today.year} - Week {week}" 

    if (not os.path.exists(today_file)):
        os.makedirs(f"{DID_DATA}/{today.year}/{week}", exist_ok=True) # make the dirs if they don't exist
        with open(today_file, 'w') as file:
            file.write(f"{today_header}\n")
            copy_unfinished_tasks_to_file(file, today)

    # Open the editor
    call([EDITOR, "+ normal GA", today_file])

def handle_args(args: argparse.Namespace) -> None:
    if (args.date):
        handle_date(args.date)
    elif (args.search):
        handle_search(args.search)
    else:
        did()

def initialise() -> None:
    if (not os.path.exists(DID_HOME)):
        print("did home directory does not exist. creating {DID_HOME}")
        os.makedirs(DID_HOME)

def main() -> None:
    initialise()
    parser = argparse.ArgumentParser(
                    prog = 'did',
                    description = 'what did i do?')
    parser.add_argument('date', nargs='?', help='open the did file for this date (try "monday", "thisweek", "lastweek" or "yesterday"!)')
    parser.add_argument('-s', '--search', required=False, help='search for text in did files')
    args = parser.parse_args()
    handle_args(args)

if __name__ == '__main__':
    main()
