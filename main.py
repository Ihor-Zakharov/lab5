from datetime import datetime
import os
import csv
from dateutil.parser import parse
from typing import Callable, TypedDict, List

class Entry(TypedDict):
  name: str
  date: str
  major: str

class Program(object):
  valid_majors = ["math", "physics", "programming"]

  @staticmethod 
  def execute_handled_input(paramName: str, handler_callback: Callable[[str], bool]) -> str:
    while True:
      value = input(f"Please, enter {paramName}: ")

      try:
        if (not handler_callback(value)):
          errorStr = f"invalid argument value {paramName} is not supposed to be {value}"
          raise Exception(errorStr)
        
        return value
      except:
        print(errorStr)

  @staticmethod
  def name_handler(name: str) -> bool:
    if len(name) > 32:
      return False
    
    return True

  @staticmethod
  def date_handler(date: str) -> bool:
    try: 
        birth_date = parse(date, fuzzy=True)
        hadNoBirthdayThisYear = (datetime.today().day, datetime.today().month) < (birth_date.day, birth_date.month)
        #bool var hadNoBirthdayThisYear is being converted to either 1 or 0
        age = datetime.today().year - birth_date.year - hadNoBirthdayThisYear

        if age > 120 or age < 10:
          return False
        
        return True

    except ValueError:
        return False
    
  @staticmethod
  def major_handler(major: str) -> bool:
    #str.strip is essentially the same as String.prototype.trim() in JS
    print(major.strip().lower())

    if major.strip().lower() in Program.valid_majors: 
      return True
    
    return False
  
  @staticmethod
  def proceed_handler(value: str) -> bool:
    if value.strip().lower() != "y" and value.strip().lower() != "n":
      False
    
    True

  @staticmethod
  def execute_dialog() -> List[Entry]:
    majorsMessage = f"major ({" / ".join(Program.valid_majors)})"
    data = []

    while True:
      name = Program.execute_handled_input("name", Program.name_handler)
      date = Program.execute_handled_input("date", Program.date_handler)
      major = Program.execute_handled_input(majorsMessage, Program.major_handler)

      entry = {
        "name": name,
        "date": parse(date).isoformat(),
        "major": major
      }

      data.append(entry)

      isProceeded = Program.execute_handled_input("Continiue? y/n", Program.name_handler)

      if isProceeded == "n": break

    return data

  @staticmethod
  def writeAsync(data: List[Entry]):
    fieldnames = ["name", "date", "major"]
    with open('university_records.csv', 'w', newline='') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerows(data)

  @staticmethod
  def execute():
    data = Program.execute_dialog()
    print(data)
    Program.writeAsync(data)

Program.execute()