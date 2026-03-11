import collections

# Compatibilidade experta Python 3.10+
if not hasattr(collections, "Mapping"):
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping
    collections.Sequence = collections.abc.Sequence
    collections.Iterable = collections.abc.Iterable

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from experta import *
from PIL import Image, ImageTk


# -----------------------
# APP SETUP
# -----------------------

root = tk.Tk()

recommended_car = ""

manufacturer_var = StringVar()
car_type_var = StringVar()
fuel_var = StringVar()
budget_var = StringVar()


# -----------------------
# IMAGE LOADER
# -----------------------

def load_image(path, size=None):
    try:
        img = Image.open(path)

        if size:
            img = img.resize(size, Image.Resampling.LANCZOS)

        return ImageTk.PhotoImage(img)

    except Exception as e:
        print("Image error:", e)
        return None


# -----------------------
# EXPERT SYSTEM
# -----------------------

class CarExpert(KnowledgeEngine):

    @DefFacts()
    def initial_facts(self):

        yield Fact(action="find_car")
        yield Fact(car_type=car_type_var.get())
        yield Fact(manufacturer=manufacturer_var.get())
        yield Fact(fuel=fuel_var.get())
        yield Fact(price_range=budget_var.get())


# -----------------------
# BRAND RULES
# -----------------------

    @Rule(Fact(car_type="popular"),
          Fact(manufacturer="france"),
          salience=10)
    def peugeot_brand(self):

        self.declare(Fact(brand="peugeot"))


    @Rule(Fact(car_type="high-end"),
          Fact(manufacturer="germany"),
          salience=10)
    def mercedes_brand(self):

        self.declare(Fact(brand="mercedes"))


    @Rule(Fact(car_type="high-end"),
          Fact(manufacturer="USA"),
          salience=10)
    def tesla_brand(self):

        self.declare(Fact(brand="tesla"))


    @Rule(Fact(car_type="sport"),
          Fact(manufacturer="germany"),
          salience=10)
    def audi_brand(self):

        self.declare(Fact(brand="audi"))


    @Rule(Fact(car_type="commercial"),
          Fact(manufacturer="japan"),
          salience=10)
    def toyota_brand(self):

        self.declare(Fact(brand="toyota"))


# -----------------------
# CAR SELECTION RULES
# -----------------------

    @Rule(Fact(brand="peugeot"),
            Fact(price_range="[30000-70000]"),
          salience=20)
    def peugeot_model(self):

        self.declare(Fact(final_car="peugeot_e_208"))


        @Rule(Fact(brand="peugeot"),
            Fact(price_range="[70000-180000]"),
            salience=20)
        def peugeot_model_mid(self):

          self.declare(Fact(final_car="peugeot_e_208"))


        @Rule(Fact(brand="peugeot"),
            Fact(price_range="[180000-600000]"),
            salience=20)
        def peugeot_model_high(self):

          self.declare(Fact(final_car="peugeot_e_208"))


    @Rule(Fact(brand="mercedes"),
            Fact(price_range="[70000-180000]"),
          salience=20)
    def mercedes_model(self):

        self.declare(Fact(final_car="mercedes_class_a"))


        @Rule(Fact(brand="mercedes"),
            Fact(price_range="[180000-600000]"),
            salience=20)
        def mercedes_model_high(self):

          self.declare(Fact(final_car="mercedes_class_a"))


    @Rule(Fact(brand="tesla"),
            Fact(price_range="[70000-180000]"),
          salience=20)
    def tesla_model(self):

        self.declare(Fact(final_car="tesla_model_3"))


        @Rule(Fact(brand="tesla"),
            Fact(price_range="[180000-600000]"),
            salience=20)
        def tesla_model_high(self):

          self.declare(Fact(final_car="tesla_model_3"))


    @Rule(Fact(brand="audi"),
            Fact(price_range="[180000-600000]"),
          salience=20)
    def audi_rs3(self):

        self.declare(Fact(final_car="audi_rs3"))


    @Rule(Fact(brand="audi"),
            Fact(price_range="[70000-180000]"),
          salience=20)
    def audi_a4(self):

        self.declare(Fact(final_car="audi_a4"))


        @Rule(Fact(brand="audi"),
            Fact(price_range="[30000-70000]"),
            salience=20)
        def audi_a4_low(self):

          self.declare(Fact(final_car="audi_a4"))


    @Rule(Fact(brand="toyota"),
            Fact(price_range="[70000-180000]"),
          salience=20)
    def toyota_hilux(self):

        self.declare(Fact(final_car="toyota_hylux"))


    @Rule(Fact(brand="toyota"),
            Fact(price_range="[180000-600000]"),
          salience=20)
    def toyota_prado(self):

        self.declare(Fact(final_car="toyota_prado"))


        @Rule(Fact(brand="toyota"),
            Fact(price_range="[30000-70000]"),
            salience=20)
        def toyota_hilux_low(self):

          self.declare(Fact(final_car="toyota_hylux"))


# -----------------------
# RESULT RULE
# -----------------------

    @Rule(Fact(final_car=MATCH.car), salience=30)
    def show_result(self, car):

        global recommended_car
        recommended_car = car


# -----------------------
# FALLBACK
# -----------------------

    @Rule(Fact(action="find_car"),
          NOT(Fact(final_car=W())),
          salience=-10)
    def no_match(self):

        global recommended_car
        recommended_car = "no_match"


# -----------------------
# RESULT WINDOW
# -----------------------

def open_result_window():

    global recommended_car

    recommended_car = ""

    engine = CarExpert()
    engine.reset()

    # DEBUG (ative se quiser ver regras)
    # engine.watch('RULES','FACTS')

    engine.run()

    if recommended_car == "":
        recommended_car = "no_match"

    win = Toplevel(root)
    win.title("Recommendation Result")
    win.geometry("760x560")
    win.resizable(False, False)
    win.config(bg="#F6F5F5")

    frame = Frame(win, bg="#F6F5F5")
    frame.pack(pady=30, padx=20)

    if recommended_car == "no_match":

        Label(frame,
              text="No match found",
              font=("Arial",18,"bold"),
              fg="red",
              bg="#F6F5F5").pack()

        Label(frame,
              text="Try another combination",
              font=("Arial",12),
              bg="#F6F5F5").pack()

    else:

        car_name = recommended_car.replace("_"," ").title()

        Label(frame,
              text="Recommended Car",
              font=("Arial",22,"bold"),
              bg="#F6F5F5").pack()

        Label(frame,
              text=car_name,
              font=("Arial",15),
              bg="#F6F5F5").pack(pady=10)

        img = load_image(f"./images/{recommended_car}.jpg",(420,260))

        if img:

            lbl = Label(frame,image=img,bg="#F6F5F5")
            lbl.image = img
            lbl.pack()

        else:

            Label(frame,
                  text="Image not found",
                  bg="#F6F5F5").pack()

    Button(win,
           text="Close",
            command=win.destroy,
            width=12,
            font=("Arial",11)).pack(pady=20)


# -----------------------
# BUTTON FUNCTIONS
# -----------------------

def submit_request():

    if any(v.get()=="None" for v in
           [manufacturer_var,car_type_var,fuel_var,budget_var]):

        messagebox.showwarning("Warning",
                               "Please select all options")

    else:

        open_result_window()


def reset_selections():

    manufacturer_var.set("None")
    car_type_var.set("None")
    fuel_var.set("None")
    budget_var.set("None")


# -----------------------
# MAIN UI
# -----------------------

root.title("CarMatch Car Expert System")
root.geometry("1020x700")
root.resizable(False, False)
root.config(bg="#F6F5F5")


header = Frame(root,bg="#F6F5F5")
header.pack(pady=16)

Label(header,
      text="CarMatch Advisor",
    font=("Arial",28,"bold"),
      bg="#F6F5F5",
      fg="#276678").pack()

Label(header,
      text="Expert system to find your ideal car",
    font=("Arial",12),
      bg="#F6F5F5").pack()


body = Frame(root,bg="#F6F5F5")
body.pack(pady=24)

left = Frame(body,bg="#D3E0EA",padx=28,pady=24)
left.pack(side="left",padx=18)

right = Frame(body,bg="#D3E0EA",padx=28,pady=24)
right.pack(side="right",padx=18)


# Manufacturer

Label(left,text="Manufacturer",font=("Arial",12,"bold"),bg="#D3E0EA").pack(anchor="w")

manufacturer_var.set("None")

for t,v in [("France","france"),
            ("Germany","germany"),
            ("USA","USA"),
            ("Japan","japan")]:

    Radiobutton(left,
                text=t,
                variable=manufacturer_var,
                value=v,
                font=("Arial",11),
                bg="#D3E0EA").pack(anchor="w")


# Category

Label(left,text="\nCategory",font=("Arial",12,"bold"),bg="#D3E0EA").pack(anchor="w")

car_type_var.set("None")

for t,v in [("Sport","sport"),
            ("Commercial","commercial"),
            ("Popular","popular"),
            ("High-end","high-end")]:

    Radiobutton(left,
                text=t,
                variable=car_type_var,
                value=v,
                font=("Arial",11),
                bg="#D3E0EA").pack(anchor="w")


# Fuel

Label(right,text="Fuel Type",font=("Arial",12,"bold"),bg="#D3E0EA").pack(anchor="w")

fuel_var.set("None")

for t,v in [("Diesel","diesel"),
            ("Gasoline","gasoline"),
            ("Electric","electric")]:

    Radiobutton(right,
                text=t,
                variable=fuel_var,
                value=v,
                font=("Arial",11),
                bg="#D3E0EA").pack(anchor="w")


# Budget

Label(right,text="\nBudget",font=("Arial",12,"bold"),bg="#D3E0EA").pack(anchor="w")

budget_var.set("None")

for t,v in [("R$ 30.000 - R$ 70.000","[30000-70000]"),
            ("R$ 70.000 - R$ 180.000","[70000-180000]"),
            ("R$ 180.000 - R$ 600.000","[180000-600000]")]:

    Radiobutton(right,
                text=t,
                variable=budget_var,
                value=v,
                font=("Arial",11),
                bg="#D3E0EA").pack(anchor="w")


footer = Frame(root,bg="#F6F5F5")
footer.pack(pady=28)

Button(footer,
       text="Reset",
       command=reset_selections,
    width=14,
    font=("Arial",11)).pack(side="left",padx=12)

Button(footer,
       text="Search",
       command=submit_request,
    width=14,
    font=("Arial",11)).pack(side="left",padx=12)


root.mainloop()