import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from tkinter import*
from tkinter import messagebox
from PIL import Image,ImageTk
import re




def Search():
    
    if E1.get() != "":
        
        job=E1.get()
        
        messagebox.showinfo("message","It will take a while,please wait")
        
        window.destroy()
        
        main(job)
    else:
        
        messagebox.showinfo("Alert","Enter a valid Job Role")


def create_url(job):
    
    temp="https://in.indeed.com/jobs?q={}&l=&from=searchOnHP&vjk=a32f84bf18393ed3"
    
    job=job.replace(" ","+")
    
    return temp.format(job)


def Extract_Job_Details(Detail):
    
    try:
    
        job_tag = Detail.find("h2")
    
        job_title=job_tag.text.strip()
    
    except:
    
        job_title = "Not Mentioned"

    try:
    
        company_tag = Detail.find("span",{"data-testid" : "company-name"})
    
        company = company_tag.text.strip()
    
    except:
    
        company = "Not Mentioned"

    try:
    
        location_tag = Detail.find("div",{"data-testid":"text-location"})
    
        location = location_tag.text.strip()
    
    except:
    
        location = "Not Mentioned"

    
    salary_element = Detail.find("ul")
    
    sal_tag=salary_element.find_all("li")
    
    metadata=[]
    
    salary = "Not Mentioned"
    
    job_type = "Not Mentioned"
    
    if sal_tag:
    
        for i in sal_tag:
    
            metadata.append(i.text.strip())
    
        try:
    
            salary=metadata[0] if "₹" in metadata[0] else "Not Mentioned"
    
        except:
    
            salary="Not Mentioned"
    
        try:
    
            job_type=metadata[1] if "time" in metadata[1] else "Not Mentioned"
    
        except:
    
            job_type="Not Mentioned"
        
    job_url="Not Available"
    try:
        job_link_tag=Detail.find("a",class_="jcs-JobTitle")
        job_url="https://in.indeed.com"+job_link_tag["href"]
    except:
        job_url="Not found"
    
    
    details=(job_title,company,location,salary,job_type,job_url)

    return details

def extract_salary(salary):
    Digits=[]

    if "₹" in salary:

        salary_in_digit=re.findall(r'\d+',salary.replace(",",""))

        if salary_in_digit:

            for i in salary_in_digit:

                Digits.append(int(i))
                
        return max(Digits)
        
    return 0


def export_to_excel(Job,Job_details):

    Job=Job.replace("+"," ")

    Columns=["Job Role","Company","Location","Salary","Job Type","Job Link"]

    Job_details.sort(key=lambda x:extract_salary(x[3]),reverse=True)

    df=pd.DataFrame(Job_details,columns=Columns)

    Excel_Name=f"{Job.replace(' ','_')}_details.xlsx"

    df.to_excel(Excel_Name,index=False)

    print(f"{Job} records have been stored in {Excel_Name}")
    


def main(job_name):
    
    
    
    driver=webdriver.Firefox()
    
    url=create_url(job_name)

    job_name=job_name.replace(" ","+")


    driver.get(url)

    time.sleep(15)

    Job_details=[]

    next_page_available=True

    while next_page_available:

        soup=BeautifulSoup(driver.page_source,"html.parser")

        details=soup.find_all("div",class_="job_seen_beacon")
        
        for detail in details:

            dt=Extract_Job_Details(detail)

            if dt:

                Job_details.append(dt)

        next_button=soup.find("a",{"data-testid":"pagination-page-next"})
        if next_button:
            next_page_url="https://in.indeed.com"+next_button["href"]+"&vjk=a32f84bf18393ed3"
            print(f"Navigating to {next_page_url}")
            driver.get(next_page_url)
            time.sleep(15)
            
        else:
            next_page_available=False
            print("No more pages to scrape")
            
    

    export_to_excel(job_name,Job_details)


    driver.quit()


#initializing window object
window=Tk()

window.geometry("1600x1200")  #Setting the window size

window.title("Indeed Scraper")  #setting the title for the window


#setting the bg image for the window using Image and ImageTk functions from PIL(Python Imaging Library)
img=Image.open("Dark BG.jpg")  

img=img.resize((1550,860))

pic=ImageTk.PhotoImage(img)

WBG=Label(window,image=pic)

WBG.place(x=-15,y=-2)


#creating a frame
fr=Frame(window,bg="white",highlightbackground="blue",highlightthickness="2")

fr.grid(row=0,column=0,padx=100,pady=100,ipadx=240,ipady=300)

img1=Image.open("Frame BG_2.jpg")  

img1=img1.resize((800,1100))

pic1=ImageTk.PhotoImage(img1)

FBG=Label(fr,image=pic1)

FBG.place(x=-154,y=-254)


#creating labels,Entry box and Button
L1=Label(fr,text="Enter the Job Role:",font=("helvetica",15,"bold"),bg="#eeeef0")

L1.place(x=80,y=220)

L2=Label(fr,text="Indeed Scraper",font=("verdana",16,"bold"),bg="#eeeef0",fg="midnight blue")

L2.place(x=155,y=145)


E1=Entry(fr,font=("helvetica",15),width=25,bg="white")

E1.place(x=100,y=260)


B1=Button(fr,text="Scrape",font=("helvetica",15,"bold"),padx=5,pady=2,bg="red",fg="white",command=Search)

B1.place(x=190,y=310)


E1.focus()


window.mainloop()
