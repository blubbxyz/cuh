# https://roadmap.sh/python?fl=1
# nice hotkeys : - cntrl + slash dine in comment setzteb/raussetzen

# typecasting

q_basedmg = 100
try:
    item_ad = int(input("how much ad does Riven get through items? "))
    rivenq_dmg = q_basedmg + item_ad
    print("Value:", rivenq_dmg)
    print("Data Type:", type(rivenq_dmg))
except ValueError:
    print("Please enter a valid number for AD.")

# functions

def glaze(name):
    print(f"du geiler hangst{name}")

name = input("Wie heißt du? ")
glaze(name)

# sets,dictionarys and lists,tuples

coolnum_set = {1,2,2,3,4,4,5,}
print("cool numbers:", coolnum_set)
coolchamp_set = {"Kaisa", "Riven", "Akali","Akali", "Riven"}
print("cool champs:", coolchamp_set)
# sets cannot contain duplicates

fruit_list = ['🍎', '🍓', '🍐']
fruit_list[1]
# '🍓'

animal_tuple = ('🐶', '🐱', '🐮')
animal_tuple[2]
# '🐮'

vehicle_set = {'🚐', '🏍', '🚗'}
vehicle_set[0]
# TypeError: 'set' object is not subscriptable

my_set = {"apple", "apple", "banana"}
print(my_set)  # {'apple', 'banana'}
if "banana" in my_set:
    print("Found!")

my_dict = {
    "apple": 3,
    "banana": 5,
    "cherry": 2
}
print(my_dict["banana"])  # 5
# | Feature     | **Set**                    | **Dictionary**              |
# | ----------- | -------------------------- | --------------------------- |
# | Stores      | Just keys                  | Keys and values             |
# | Duplicates? | No duplicates              | No duplicate keys           |
# | Lookup      | Check if element exists    | Get value by key            |
# | Syntax      | `{a, b, c}`                | `{key: value}`              |
# | Example     | `{"red", "blue"}`          | `{"red": 255, "blue": 0}`   |
# | Use case    | Unique collection of items | Mapping from keys to values |
