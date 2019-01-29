import requests
from bs4 import BeautifulSoup
import lxml.html as lh
import pandas as pd

username = input("Enter Roll Number : ")
password = input("Enter OAS Password : ")
url = "http://oas.iitmandi.ac.in/student/"
login_data = {"txtUserName": username, "txtPassword": password, "Login": "Login"}

result_page_url = "http://oas.iitmandi.ac.in/student/ProvisionalSemesterResultCard.aspx"
result_data = {
    "ctl00$MainContent$ddlPeriod": "2018-2019 ODD",
    "__EVENTTARGET": "ctl00$MainContent$ddlPeriod",
    "__SCROLLPOSITIONX": "0",
    "__SCROLLPOSITIONY": "0",
}
# creating session
with requests.Session() as s:
    # loging-in
    login_page = s.get(url)
    login_soup = BeautifulSoup(login_page.content, "html5lib")
    login_data["ScriptManager1_HiddenField"] = login_soup.find(
        "input", attrs={"name": "ScriptManager1_HiddenField"}
    )["value"]
    login_data["__VIEWSTATE"] = login_soup.find("input", attrs={"name": "__VIEWSTATE"})[
        "value"
    ]
    main_page = s.post(url, data=login_data)

    # getting result
    result_page = s.get(result_page_url)
    result_soup = BeautifulSoup(result_page.content, "html5lib")
    result_data["__VIEWSTATE"] = result_soup.find(
        "input", attrs={"name": "__VIEWSTATE"}
    )["value"]
    result_page = s.post(result_page_url, result_data)

    # scraping data
    table = lh.fromstring(result_page.content)


def Get_Grade_Score(x):
    if x == "O":
        return 10
    elif x == "A":
        return 9
    elif x == "B":
        return 8
    elif x == "C":
        return 7
    elif x == "D":
        return 6
    elif x == "E":
        return 4
    elif x == "F":
        return 0
    elif x == "I":
        return -1


data = []
tr_elements1 = table.xpath("//tr")
for tr in tr_elements1:
    name = str(tr.text_content())
    name = name.replace("\n", "").replace("\t", "").replace("\r", "").replace("   ", "")
    data.append(name)

Student_Name = data[8][8:]
Student_Roll = data[7][12:]
Student_Course = data[9][30:]
Semester = data[10][-2:]

col_Grades = []
col_Course_No = []
col_Course_name = []
col_Course_Credit = []
for i in range(12, len(data)):
    col_Grades.append(data[i][-3])
    if data[i][9].isupper():
        col_Course_No.append(data[i][2:9])
        col_Course_name.append(data[i][9:-3])
    else:
        col_Course_No.append(data[i][2:8])
        col_Course_name.append(data[i][8:-3])
    col_Course_Credit.append(data[i][-1])
df = pd.DataFrame()
df["Course No"] = col_Course_No
df["Course Name"] = col_Course_name
df["Grade"] = col_Grades
df["Credits"] = col_Course_Credit
print("Name : %s\nRoll : %s\nCourse : %s" % (Student_Name, Student_Roll, Student_Course))
print(df)
sumation = 0
total_credits = 0
for index, row in df.iterrows():
    sumation += Get_Grade_Score(row["Grade"]) * int(row["Credits"])
    total_credits += int(row["Credits"])
print(
    "\nYour SGPA for %s is %f"
    % (result_data["ctl00$MainContent$ddlPeriod"], sumation / total_credits)
)
