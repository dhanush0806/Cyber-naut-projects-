import mysql.connector
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
from tkinter import*
from tkinter import messagebox
from PIL import Image,ImageTk
import time
import threading
import re


# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="ProductComparison"
)
cursor = db.cursor()
cursor.execute("TRUNCATE TABLE products")
# Function to insert data into MySQL
def insert_product(name, price, rating, rating_count, link, platform):
    
    cursor.execute("""
        INSERT INTO products (name, price, rating, rating_count, link, platform)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, price, rating, rating_count, link, platform))
    db.commit()

def search():
    if E1.get()!="":
        product=E1.get()
        print(product)
        messagebox.showinfo("message","Please wait for a while")
        w.destroy()
        main(product)
        
    else:
        messagebox.showinfo("Alert","Enter a valid product name")

# Scraping Amazon
def scrape_amazon(product_name):
    search_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    
    driver.get(search_url)
    time.sleep(10)

    
    next_page_available=True
    while next_page_available:
        soup = BeautifulSoup(driver.page_source,"html.parser")
        products = soup.find_all("div", {"data-component-type": "s-search-result"})
        for product in products:  # Limit to 5 products
            try:
                title = product.find("h2")
            except:
                title = "Not available"
            try:
                price = product.find("span", class_="a-price-whole")
            except:
                price = "Not Available"
            try:
                rating_tag = product.find("i")
                rating = float(rating_tag.text.strip().split()[0]) if rating_tag else 0.0
            except:
                rating = 0.0
            try:
                rating_count = product.find("span", class_="a-size-base s-underline-text")
            except:
                rating_count = "Not available"
            try:
                link = product.find("a", class_="a-link-normal")
            except:
                link = "Not Available"
    
            if title:
                insert_product(
                    title.text.strip(),
                    float(price.text.replace(",", "")) if price else None,
                    rating,
                    rating_count.text.strip() if rating_count else "No rating count",
                    "https://www.amazon.in" + link["href"] if link else "No link",
                    "Amazon"
                )
        next_page=soup.find("a",class_="s-pagination-next")
        if next_page and not "s-pagination-disabled" in next_page.get("class", []):
            next_page_url = "https://www.amazon.in" + next_page["href"]
            print(f"Moving to the next page in amazon: {next_page_url}")
            driver.get(next_page_url)
            time.sleep(10)  # Add a delay to allow the page to load
            
        else:
             
            print("No more pages to scrape in Amazon.")
            next_page_available = False

    driver.quit()

# Scraping Flipkart
def scrape_flipkart(product_name):
    search_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '+')}"
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    
    driver.get(search_url)
    time.sleep(15)  # Allow page to load

    soup = BeautifulSoup(driver.page_source,"html.parser")
    
    # Check if product cards exist
    
    next_page_available = True
    while next_page_available:
        products = soup.find_all("div", class_="tUxRFH")  # Updated class for product cards
        if not products:
            print("⚠ No products found on Flipkart. HTML structure might have changed.")
            print("We can't scrape vertical product cards in this model")
            driver.quit()
            return
        for product in products:  # Limit to 5 products
            try:
                title = product.find("div", class_="KzDlHZ")  # Product title
                title = title.text.strip()
            except:
                title="No Title Available"
    
            try:
                price = product.find("div", class_="Nx9bqj _4b5DiR")  # Price
                price = price.text.replace("₹", "").replace(",","").strip()
            except:
                price = "No price Available"
            
            try:
                rating_tag = product.find("div", class_="XQDdHH")
                rating = float(rating_tag.text.strip().split()[0]) if rating_tag else 0.0
            except:
                rating = 0.0
            
            try:
                rating_count = product.find("span", class_="Wphh3N")  # Rating count
                rating_count = rating_count.text.strip()
            except:
                rating_count = 0
            
                
            
            link = product.find("a", class_="CGtC98") # Product link
    
           #print(title,price,rating,rating_count,"https://www.flipkart.com" + link["href"] if link else "No link","Flipkart")
            
    
    
            if title and price:
                if price.isnumeric():
                    pass
                else:
                    price = None
                try:
                    insert_product(
                        title,
                        float(price),  # Convert price to float
                        rating,
                        rating_count,
                        "https://www.flipkart.com" + link["href"] if link else "No link",
                        "Flipkart"
                    )
                    #print(f"✅ Stored Flipkart product: {title}")
                except Exception as e:
                    print(f"⚠ Error inserting Flipkart product: {e}")
        
        
        next_button_list=soup.find_all("a",class_="_9QVEpD")
        next=next_button_list[-1].find("span").text
        if next=="Next":
            next_button="https://www.flipkart.com"+next_button_list[-1]["href"]
            print(f"Moving to next page in Flipkart:{next_button}")
            driver.get(next_button)
            time.sleep(15)
            soup=BeautifulSoup(driver.page_source,"html.parser")
        
        else:
            print("No more pages to scrape in Flipkart")
            next_page_available=False

    driver.quit()


def product_comparison():
    cursor.execute("SELECT name, price, rating, rating_count, link, platform FROM products")
    products = cursor.fetchall()

    # Filter out products with missing price
    filtered_products = [p for p in products if p[2] is not None]

    # Find the best deal (lowest price)
    if filtered_products:
        best_product = max(filtered_products, key=lambda x: x[2])
        print("\n💰 **Best Product Suggestion:**")
        print(f"🛒 **Name:** {best_product[0]}")
        print(f"💲 **Price:** ₹{best_product[1]}")
        print(f"⭐ **Rating:** {best_product[2]} ({best_product[3]} reviews)")
        print(f"🔗 **Link:** {best_product[4]}")
        print(f"🏬 **Platform:** {best_product[5]}")
    else:
        print("No valid product data available.")






w=Tk()
w.geometry("1600x1200")
w.title("E-Commerce comparison tool")

img = Image.open("E-commerce_2.jpg")
img = img.resize((1550, 1000))
pic = ImageTk.PhotoImage(img)
WBG = Label(w, image=pic)
WBG.place(x=-3, y=-2)


fr=Frame(w,bg="lavender",highlightbackground="blue",highlightthickness="2")
fr.grid(row=0,column=0,padx=950,pady=100,ipadx=240,ipady=300)

L1=Label(fr,text="E-Commerce comparing tool",font=("helvetica",15,"bold"),fg="blue2",bg="lavender")
L1.place(x=100,y=25)

L2=Label(fr,text="Enter the product:",font=("helvetica",15,"bold"),fg="dodger blue",bg="lavender")
L2.place(x=30,y=220)

E1=Entry(fr,font=("helvetica",15,"bold"),width=25,bg="white")
E1.place(x=100,y=260)

B1=Button(fr,text="Find the best",font=("helvetica",15,"bold"),bg="maroon1",fg="white",command=search)
B1.place(x=160,y=320)


def main(product):
    p1 =threading.Thread(target=scrape_amazon, args=(product,))
    p2 = threading.Thread(target=scrape_flipkart, args=(product,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    product_comparison()
    

w.mainloop()
# Close MySQL connection
cursor.close()
db.close()
