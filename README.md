# Web programming — week by week

Open **index.html** for the seven-week project collection. Runnable files are directly inside their matching named tutorial folders under `tutorial-source/MOD002619-WebProgramming-main/`. Weeks 01–02 work directly in a browser; weeks 03–07 are independent Django projects with their own databases.

## Setup (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$projectPython = (Resolve-Path .\.venv\Scripts\python.exe).Path
cd tutorial-source/MOD002619-WebProgramming-main/Week03-Django-Introduction
& $projectPython manage.py migrate
& $projectPython manage.py seed_demo
& $projectPython manage.py runserver
```

Visit http://127.0.0.1:8000/. Choose the corresponding Week04 through Week07 tutorial folder to explore later weeks. Use the virtual-environment Python in each week's commands. Choose your own admin password with `manage.py createsuperuser`. These are local learning configurations.

## Demo admin login

These local demonstration accounts have been created in the five existing Django databases. The same credentials work for weeks 3 through 7:

- Username: `demo_admin`
- Password: `j-RZjeQVJ-cPvcLS7nw`

| Project | Admin page when running on its assigned port |
| --- | --- |
| Week 3 | http://127.0.0.1:8003/admin/ |
| Week 4 | http://127.0.0.1:8004/admin/ |
| Week 5 | http://127.0.0.1:8005/admin/ |
| Week 6 | http://127.0.0.1:8006/admin/ |
| Week 7 | http://127.0.0.1:8007/admin/ |

If you start a week with the default `runserver` command, use http://127.0.0.1:8000/admin/ instead. Weeks 1 and 2 have no Django admin.

These accounts belong to the existing local databases. After creating a fresh database, run `python manage.py createsuperuser` from that week folder and choose your credentials. Demo credentials are for local use only.

## Folder layout

```text
tutorial-source/MOD002619-WebProgramming-main/
  Week01-HTML-CSS/
  Week02-JavaScript/
  Week03-Django-Introduction/
  Week04-Django-Templates/
  Week05-Django-statics/
  Week06-Django-Forms/
  Week07-Django-TDD/
```

Each named tutorial folder contains its runnable project and supplied resources. Open `index.html` in Week01 or Week02 for browser exercises; run `manage.py` directly from each Django week folder.

## Organisation

- week01: two-page responsive HTML/CSS site, without JavaScript or frameworks.
- week02: basic bill splitter, menu-item splitter and non-persistent to-do list.
- week03: rugby players/positions, specialist flags, CSV import and admin.
- week04: student/module models, inherited templates, detail pages and 404 handling.
- week05: student images, static files and pagination.
- week06: validated student editing, image uploads, module and name/age filtering, retained pagination filters.
- week07: SHA-256 form, saved hashes, asynchronous preview and tests.
- tutorial-source: supplied images/code, with runnable files directly in each matching tutorial folder.

## Tests and dependencies

Run `python manage.py test` from each Django week. Week 07 includes optional Selenium browser tests: install Selenium, ensure Chrome is available, and run `python manage.py test school.browser_tests`. These require browser/driver availability and are separate from the default test suite.

Student CSVs contain synthetic example records because students.csv was not included in the supplied archive. The projects use original responsive CSS, native Django forms and ORM filters. Python 3.11 uses Django 5.2.


The optional browser test requires `python -m pip install selenium` and Chrome. The regular Django tests do not need Selenium.

The original standalone Selenium demonstration in Week07 is named `selenium_example.py` so it is not imported by the regular Django test discovery. Its code is unchanged and uses the original Linux Chrome path.
