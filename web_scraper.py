import customtkinter as ctk
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import messagebox

# =====================================
# SETTINGS
# =====================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# =====================================
# WINDOW
# =====================================
app = ctk.CTk()
app.geometry("950x700")
app.title("🕸 Ultra Fancy Web Scraper")

# =====================================
# TITLE
# =====================================
title = ctk.CTkLabel(
    app,
    text="🕸 WEB SCRAPER DASHBOARD",
    font=("Arial", 34, "bold"),
    text_color="cyan"
)

title.pack(pady=20)

# =====================================
# FRAME
# =====================================
frame = ctk.CTkFrame(app)
frame.pack(pady=10, padx=20, fill="both", expand=True)

# =====================================
# TEXTBOX
# =====================================
textbox = ctk.CTkTextbox(
    frame,
    width=850,
    height=450,
    font=("Consolas", 16)
)

textbox.pack(pady=20)

# =====================================
# SCRAPE FUNCTION
# =====================================
def scrape_data():

    try:

        url = "https://books.toscrape.com/"

        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.find_all("article", class_="product_pod")

        data = []

        textbox.delete("1.0", "end")

        for book in books:

            name = book.h3.a["title"]

            price = book.find("p", class_="price_color").text

            rating = book.p["class"][1]

            data.append([name, price, rating])

            textbox.insert(
                "end",
                f"📖 {name}\n💲 {price}\n⭐ {rating}\n\n"
            )

        # Save CSV
        df = pd.DataFrame(
            data,
            columns=["Book Name", "Price", "Rating"]
        )

        df.to_csv("products.csv", index=False)

        messagebox.showinfo(
            "Success",
            "Data scraped and saved to products.csv"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

# =====================================
# CLEAR FUNCTION
# =====================================
def clear_data():

    textbox.delete("1.0", "end")

# =====================================
# BUTTON FRAME
# =====================================
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=20)

# =====================================
# SCRAPE BUTTON
# =====================================
scrape_button = ctk.CTkButton(
    button_frame,
    text="🚀 Start Scraping",
    command=scrape_data,
    width=220,
    height=50,
    font=("Arial", 20, "bold"),
    fg_color="green"
)

scrape_button.grid(row=0, column=0, padx=15)

# =====================================
# CLEAR BUTTON
# =====================================
clear_button = ctk.CTkButton(
    button_frame,
    text="🗑 Clear",
    command=clear_data,
    width=180,
    height=50,
    font=("Arial", 20, "bold"),
    fg_color="red"
)

clear_button.grid(row=0, column=1, padx=15)

# =====================================
# FOOTER
# =====================================
footer = ctk.CTkLabel(
    app,
    text="💻 Built with Python + BeautifulSoup + Pandas",
    font=("Arial", 15),
    text_color="gray"
)

footer.pack(pady=10)

# =====================================
# RUN APP
# =====================================
app.mainloop()