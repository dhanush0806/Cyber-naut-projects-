from tkinter import *
from PIL import Image,ImageTk
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

def Search():
    product = E1.get()
    window.destroy()
    main(product)

def get_url(search_term):
    template = "https://www.amazon.in/s?k={}&crid=3L52JK4Z4U3W6&sprefix=ultrawide+monitor%2Caps%2C340&ref=nb_sb_noss_1"
    search_term = search_term.replace(" ", "+")
    return template.format(search_term)

def extract_record(item):
    title_tag = item.find("h2")
    title = title_tag.text.strip()
    
    try:
        price_tag = item.find("span", class_="a-price-whole")
        price = price_tag.text.strip()
    except:
        price = "Not Available"
    
    link_tag = item.find("a", class_="a-link-normal")
    link = "https://www.amazon.in" + link_tag.get("href", " ") if link_tag else "No link found"
    
    try:
        rating_tag = item.find("i")
        rating = rating_tag.text.strip()
    except:
        rating = "No Ratings available"
    
    try:
        rating_count_tag = item.find("span", class_="a-size-base s-underline-text")
        rating_count = rating_count_tag.text.strip()
    except:
        rating_count = "No ratings available"
    
    rec = (title, price, link, rating, rating_count)
    return rec

def extract_to_excel(product, records):
    columns = ["title", "price", "link", "rating", "rating_count"]
    df = pd.DataFrame(records, columns=columns)
    excel_name = f"{product.replace(' ', '_')}_record.xlsx"
    df.to_excel(excel_name, index=False)
    print(f"{product} records have been stored in {excel_name}")

# --- Graph Generating Mechanism Only ---
def plot_rating_distribution(records):
    ratings = []
    for rec in records:
        try:
            # Assume the rating text starts with a number (e.g., "4.5 out of 5 stars")
            rating_value = float(rec[3].split()[0])
            ratings.append(round(rating_value))
        except:
            continue
    if not ratings:
        print("No valid ratings found for graph generation.")
        return
    # Count the frequency for each rating from 1 to 5
    counts = {star: ratings.count(star) for star in range(1, 6)}
    plt.bar(counts.keys(), counts.values(), color=['red','orange','yellow','green','blue'])
    plt.xlabel("Star Ratings")
    plt.ylabel("Number of Products")
    plt.title("Distribution of Product Ratings")
    plt.xticks(np.arange(1, 6))
    plt.show()

def main(product):
   
    driver = webdriver.Firefox()
    
    url = get_url(product)
    driver.get(url)
    time.sleep(10)
    
    records = []
    next_page_available = True
    
    while next_page_available:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.find_all("div", {"data-component-type": "s-search-result"})
        
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
        
        next_button = soup.find("a", class_="s-pagination-next")
        
        if next_button and not "s-pagination-disabled" in next_button.get("class", []):
            next_page_url = "https://www.amazon.in" + next_button["href"]
            print(f"Moving to the next page: {next_page_url}")
            driver.get(next_page_url)
            time.sleep(10)
        else:
            print("No more pages to scrape.")
            next_page_available = False
    
    extract_to_excel(product, records)
    plot_rating_distribution(records)  # Call the graph function
    driver.quit()

# Initialize Tkinter window
window = Tk()
window.geometry("1600x1200")
window.title("Amazon Web Scraper")
window.config(bg="lavender")

# Load and set background image
img = Image.open("Scrapper BG_1.jpg")
img = img.resize((1600, 800))
pic = ImageTk.PhotoImage(img)
WBG = Label(window, image=pic)
WBG.place(x=-15, y=-2)

# Create frame
fr = Frame(window, bg="white", highlightbackground="black", highlightthickness=2)
fr.grid(row=0, column=0, padx=920, pady=100, ipadx=240, ipady=300)

# Create labels, entry box, and button
L1 = Label(fr, text="Enter the product:", font=("helvetica", 15, "bold"), bg="white")
L1.place(x=80, y=220)

E1 = Entry(fr, font=("helvetica", 15), width=30, bg="lavender")
E1.place(x=80, y=260)

B1 = Button(fr, text="Search", font=("helvetica", 15, "bold"), padx=5, pady=2, bg="red", fg="white", command=Search)
B1.place(x=200, y=310)

E1.focus()
window.mainloop()
