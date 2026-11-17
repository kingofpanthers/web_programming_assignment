from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from myApp.models import Student, Module
from pytz import UTC


DATETIME_FORMAT = '%m/%d/%Y'

modules = {
    "MOD002619": "Web Programming",
    "MOD002643": "Image Processing",
    "MOD002691": "Final Project",
    "MOD003212": "Introduction to Programming",
    "MOD003484": "Software Principles"
}

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the student data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


def run():
    if Student.objects.exists() or Module.objects.exists():
        print('Student data already loaded...exiting.')
        print(ALREADY_LOADED_ERROR_MESSAGE)
        return

    print("Creating module data")
    for mcode, mname in modules.items():
        mod = Module(code=mcode, name = mname)
        mod.save()

    print("Loading student data")
    for row in DictReader(open('./students.csv')):
        stu = Student()
        stu.firstName = row['fname']
        stu.lastName = row['lname']
        stu.age = row['age']
        stu.email = row['email']
        raw_enrolment_date = row['enrolment date']
        enrolment_date = UTC.localize(
            datetime.strptime(raw_enrolment_date, DATETIME_FORMAT))
        stu.enrolmentDate = enrolment_date
        stu.save()

        # Now add the module enrollments
        raw_modules = row['modules']
        module_names = [name for name in raw_modules.split('| ') if name]
        for mod_name in module_names:
            mod = Module.objects.get(code=mod_name.strip())
            stu.modules.add(mod)
        stu.save()
