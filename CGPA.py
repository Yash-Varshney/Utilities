import requests
from bs4 import BeautifulSoup
import lxml.html as lh
import pandas as pd

username = input("Enter UserName : ")
password = input("Enter Password : ")
url = "http://oas.iitmandi.ac.in/student/"
login_data = {'txtUserName' : username, 
              'txtPassword' : password,
              'Login' : 'Login',
              }

result_page_url = 'http://oas.iitmandi.ac.in/student/ProvisionalSemesterResultCard.aspx'
result_data = {'ctl00$MainContent$ddlPeriod' : '2018-2019 ODD',
            '__EVENTTARGET' : 'ctl00$MainContent$ddlPeriod',
            '__SCROLLPOSITIONX' : '0',
            '__SCROLLPOSITIONY' : '0'
            }
#creating session
with requests.Session() as s:
    #loging-in
    login_page = s.get(url)
    login_soup = BeautifulSoup(login_page.content, 'html5lib')
    login_data['ScriptManager1_HiddenField'] = login_soup.find('input',attrs={'name' : 'ScriptManager1_HiddenField'})['value'] 
    login_data['__VIEWSTATE'] = login_soup.find('input',attrs={'name' : '__VIEWSTATE'})['value']   
    main_page = s.post(url,data = login_data)
    
    #getting result
    result_page = s.get(result_page_url)
    result_soup = BeautifulSoup(result_page.content, 'html5lib')
    result_data['__VIEWSTATE'] = result_soup.find('input',attrs={'name' : '__VIEWSTATE'})['value']
    result_page = s.post(result_page_url,result_data)
    
    #scraping data
    table = lh.fromstring(result_page.content)

def Get_Grade_Score(x):
    if (x == 'O'):
        return 10
    elif (x == 'A'):
        return 9
    elif (x == 'B'):
        return 8
    elif (x =='C'):
        return 7
    elif (x == 'D'):
        return 6
    elif (x == 'E'):
        return 4
    elif (x == 'F'):
        return 0
    elif (x == 'I'):
        return -1
    
tr_elements = table.xpath("//tr[@class = '%s']" %("sp_grid_row"))
col_Grades = []
col_Course_No = []
col_Course_name = []
col_Course_Credit = []
for t in tr_elements:
    name = t.text_content()
    name = str(name.strip().replace("\r\n                                               ",""))
    col_Grades.append(name[-6])
    if(name[9].isupper()):
        col_Course_No.append(name[2:9])
        col_Course_name.append(name[9:-6])
    else:
        col_Course_No.append(name[2:8])
        col_Course_name.append(name[8:-6])
    col_Course_Credit.append(name[-1])
df = pd.DataFrame()
df["Course No"] = col_Course_No
df["Course Name"] = col_Course_name
df["Grade"] = col_Grades
df["Credits"] = col_Course_Credit
print(df)
sumation = 0
total_credits = 0
for index,row in df.iterrows():
    sumation += Get_Grade_Score(row["Grade"])*int(row["Credits"])
    total_credits += int(row["Credits"])
print("Your CGPA for %s is %f" %(result_data['ctl00$MainContent$ddlPeriod'],sumation/total_credits))