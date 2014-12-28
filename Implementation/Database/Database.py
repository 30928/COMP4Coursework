import sqlite3

#inserting data
def create_data(data, table, placeholders):
    with sqlite3.connect("PP.db") as db:
        cursor = db.cursor()
        cursor.execute("PRAGMA foreign_keys_ = ON")
        sql = "insert into {} values {}".format(table, placeholders)
        cursor.execute(sql, data)
        db.commit()

#updating data
def update_data(data, table, update, ID):
    with sqlite3.connect("PP.db") as db:
        cursor = db.cursor()
        cursor.execute("PRAGMA foreign_keys_ = ON")
        sql = "update {} set {} where {} = {}".format(table, update, ID, data)
        cursor.execute(sql)
        db.commit()

#deleting data
def delete_data(data, table, ID):
    try:
        with sqlite3.connect("PP.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys_ = ON")
            sql = "delete from {} where {} = {}".format(table, ID, data)
            cursor.execute(sql)
            db.commit()
    except:
        print("Error")


def calculate_royalties(RoyaltiesID):
    
    with sqlite3.connect("PP.db") as db:
        cursor = db.cursor()
        cursor.execute("PRAGMA foreign_keys_ = ON")

        RoyaltyTemp = 0
        i = 1
        while i != 0:
            
            try:
                sql = "select NetSales from RoyaltiesItems where RoyaltiesID = {} and RoyaltiesItems = {}".format(RoyaltiesID, i)
                cursor.execute(sql)
                NetSalesList = list(cursor.fetchone())
                NetSales = NetSalesList[0]
       
                sql = "select PrintCost from RoyaltiesItems where RoyaltiesID = {} and RoyaltiesItems = {}".format(RoyaltiesID, i)
                cursor.execute(sql)
                PrintCostList = list(cursor.fetchone())
                PrintCost = PrintCostList[0]

                sql = "select RoyaltyQuantity from RoyaltiesItems where RoyaltiesID = {} and RoyaltiesItems = {}".format(RoyaltiesID, i)
                cursor.execute(sql)
                RoyaltyQuantityList = list(cursor.fetchone())
                RoyaltyQuantity = RoyaltyQuantityList[0]
                    
                RoyaltyTemp += NetSales - (PrintCost * RoyaltyQuantity)
                        
                i += 1
                
            except:
                RoyaltiesPayment = RoyaltyTemp
                sql = "update Royalties set RoyaltyPayment = {} where RoyaltiesID = {}".format(RoyaltiesPayment, RoyaltiesID)
                cursor.execute(sql)
                db.commit()
                i = 0


def calculate_book_invoice_payment(BookInvoiceID):
    
    with sqlite3.connect("PP.db") as db:
        cursor = db.cursor()
        cursor.execute("PRAGMA foreign_keys_ = ON")

        BookInvoiceTemp = 0
        i = 1
        while i != 0:

            try:
                sql = "select BookInvoiceQuantity from BookInvoiceItems where BookInvoiceID = {} and BookInvoiceItems = {}".format(BookInvoiceID, i)
                cursor.execute(sql)
                BookInvoiceQuantityList = list(cursor.fetchone())
                BookInvoiceQuantity = BookInvoiceQuantityList[0]
           
                sql = "select BookInvoiceDiscount from BookInvoiceItems where BookInvoiceID = {} and BookInvoiceItems = {}".format(BookInvoiceID, i)
                cursor.execute(sql)
                BookInvoiceDiscountList = list(cursor.fetchone())
                BookInvoiceDiscount = BookInvoiceDiscountList[0]
                BookInvoiceDiscount /= 100

                sql = "select ShippingPrice from BookInvoiceItems where BookInvoiceID = {} and BookInvoiceItems = {}".format(BookInvoiceID, i)
                cursor.execute(sql)
                ShippingPriceList = list(cursor.fetchone())
                ShippingPrice = ShippingPriceList[0]

                sql = "select ISBN from BookInvoiceItems where BookInvoiceID = {} and BookInvoiceItems = {}".format(BookInvoiceID, i)
                cursor.execute(sql)
                ISBNList = list(cursor.fetchone())
                ISBN = ISBNList[0]

                sql = "select Price from Book where ISBN = {}".format(ISBN)
                cursor.execute(sql)
                PriceList = list(cursor.fetchone())
                Price = PriceList[0]
                    
                BookInvoiceTemp += (BookInvoiceQuantity * Price * BookInvoiceDiscount) + ShippingPrice
                        
                i += 1
                
            except:
                BookInvoicePayment = BookInvoiceTemp
                sql = "update BookInvoice set BookInvoicePayment = {} where BookInvoiceID = {}".format(BookInvoicePayment, BookInvoiceID)
                cursor.execute(sql)
                db.commit()
                i = 0


        
#placeholders and table contents for adding entries
def CustomerEntry():
    table = "Customer (FirstName, LastName, Email, PhoneNumber, Address, Postcode)"
    placeholders = "(?, ?, ?, ?, ?, ?)"
    return table, placeholders

def BookEntry():
    table = "Book (ISBN, AuthorID, BookTitle, NoOfPages, Size, Back, Cover, Paper, Font, FontSize, DatePublished, Price)"
    placeholders = "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    return table, placeholders
    
def PubInvoiceEntry():
    table = "PubInvoice (AuthorID, ISBN, PubInvoiceDate, PubInvoiceService, PubInvoicePayment)"
    placeholders = "(?, ?, ?, ?, ?)"
    return table, placeholders

def BookInvoiceEntry():
    table = "BookInvoice (AuthorID, BookInvoicePayment, BookInvoiceDate)"
    placeholders = "(?, ?, ?)"
    return table, placeholders

def BookInvoiceItemsEntry():
    table = "BookInvoiceItems (BookInvoiceID, ISBN, BookInvoiceQuantity, BookInvoiceDiscount, ShippingType, ShippingPrice)"
    placeholders = "(?, ?, ?, ?, ?, ?)"
    return table, placeholders

def RoyaltiesEntry():
    table = "Royalties (AuthorID, RoyaltyPayment, RoyaltiesDate)"
    placeholders = "(?, ?, ?)"
    return table, placeholders

def RoyaltiesItemsEntry():
    table = "RoyaltiesItems (RoyaltiesID, ISBN, Currency, RoyaltyDiscount, WholesalePrice, RoyaltyQuantity, PrintCost, NetSales, ExcRateFromGBP)"
    placeholders = "(?, ?, ?, ?, ?, ?, ?, ?, ?)"
    return table, placeholders

#retrieving input data from user
def input_customer():
    firstname = input("Enter first name: ")
    lastname = input("Enter last name: ")
    email = input("Enter Email: ")
    phonenumber = input("Enter phone number: ")
    address = input("Enter address: ")
    postcode = input("Enter postcode: ")
    input_data = (firstname, lastname, email, phonenumber, address, postcode)
    return input_data

def input_book():
    ISBN = input("Enter ISBN: ")
    AuthorID = input("Enter AuthorID: ")
    BookTitle = input("Enter book title: ")
    NoOfPages = input("Enter number of pages: ")
    Size = input("Enter size: ")
    Back = input("Enter back type: ")
    Cover = input("Enter cover type: ")
    Paper = input("Enter paper type: ")
    Font = input("Enter font: ")
    FontSize = input("Enter font size: ")
    DatePublished = input("Enter date published: ")
    Price = input("Enter price: ")
    input_data = (ISBN, AuthorID, BookTitle, NoOfPages, Size, Back, Cover, Paper, Font, FontSize, DatePublished, Price)
    return input_data

def input_pub_invoice():
    AuthorID = input("Enter AuthorID: ")
    ISBN = input("Enter ISBN: ")
    PubInvoiceDate = input("Enter publishing invoice date: ")
    PubInvoiceService = input("Enter publishing invoice service: ")
    PubInvoicePayment = input("Enter publishing invoice payment: ")
    input_data = (AuthorID, ISBN, PubInvoiceDate, PubInvoiceService, PubInvoicePayment)
    return input_data

def input_book_invoice():
    AuthorID = input("Enter AuthorID: ")
    BookInvoicePayment = None
    BookInvoiceDate = input("Enter book invoice date: ")


    input_data = (AuthorID, BookInvoicePayment, BookInvoiceDate)
    return input_data

def input_book_invoice_items():
    BookInvoiceID = input("Enter BookInvoiceID: ")
    ISBN = input("Enter ISBN: ")
    BookInvoiceQuantity = float(input("Enter quantity bought: "))
    BookInvoiceDiscount = float(input("Enter invoice discount: "))
    ShippingType = input("Enter shipping type: ")
    ShippingPrice = input("Enter shipping price: ")
    input_data = (BookInvoiceID, ISBN, BookInvoiceQuantity, BookInvoiceDiscount, ShippingType, ShippingPrice)
    return input_data, BookInvoiceID

def input_royalties():
    AuthorID = input("Enter AuthorID: ")

    RoyaltyPayment = None
    RoyaltiesDate = input("Enter royalties date: ")
    input_data = (AuthorID, RoyaltyPayment, RoyaltiesDate)
    return input_data

def input_royalties_items():
    RoyaltiesID = input("Enter RoyaltiesID: ")
    ISBN = input("Enter ISBN: ")
    Currency = input("Enter currency: ")
    RoyaltyDiscount = input("Enter royalty discount: ")
    WholesalePrice = float(input("Enter wholesale price: "))
    RoyaltyQuantity = int(input("Enter quantity bought: "))
    PrintCost = float(input("Enter print cost: "))
    ExcRateFromGBP = None
    NetSales = WholesalePrice * RoyaltyQuantity
    RoyaltiesItemPayment = NetSales - PrintCost
    if Currency != "£":
        ExcRateFromGBP = float(input("Enter current exchange rate from pounds: "))
        RoyaltiesItemPayment /= ExcRateFromGBP
        
    input_data = (RoyaltiesID, ISBN, Currency, RoyaltyDiscount, WholesalePrice, RoyaltyQuantity, PrintCost, NetSales, ExcRateFromGBP)
    
    return input_data, RoyaltiesID

#Displaying the Main Menu
def DisplayMainMenu():
    print()
    print('MAIN MENU')
    print()
    print('1. Add Data')
    print('2. Update Data')
    print('3. Remove Data')
    print()
    print('Select an option from the menu (or enter q to quit): ', end='')


#Displaying the Menu for Adding entries
def DisplayAddMenu():
    print()
    print('ADD MENU')
    print()
    print('1. Add Customer Entry')
    print('2. Add Book')
    print('3. Add Publishing Invoice')
    print('4. Add Book Invoice')
    print('5. Add Book Invoice Items')
    print('6. Add Royalties')
    print('7. Add Royalties Items')
    print()
    print('Select an option from the menu (or enter b to go back): ', end='')


#Displaying the Menu for Updating Entries
def DisplayUpdateMenu():
    print()
    print("UPDATE MENU")
    print()
    print("1. Update Customer")
    print("2. Update Book")
    print("3. Update Publishing Invoice")
    print("4. Update Book Invoice")
    print("5. Update Book Invoice Items")
    print("6. Update Royalties")
    print("7. Update Royalties Items")
    print()
    print('Select an option from the menu (or enter b to go back): ', end='')

#Displaying the Menu for Deleting Entries
def DisplayDeleteMenu():
    print()
    print("DELETE MENU")
    print()
    print("1. Delete Customer")
    print("2. Delete Book")
    print("3. Delete Publishing Invoice")
    print("4. Delete Book Invoice")
    print("5. Delete Book Invoice Item")
    print("6. Delete Royalty")
    print("7. Delete Royalties Item")
    print()
    print('Select an option from the menu (or enter b to go back): ', end='')

#Getting a choice for the main menu/add menu from the user
def GetMenuChoice():
  Choice = input()
  print()
  return Choice

#Getting a choice for the update menu from the user
def GetUpdateChoice():

    tablepick = input()

    if tablepick == "1":
        ID = "AuthorID"
        table = "Customer"
    elif tablepick == "2":
        ID = "ISBN"
        table = "Book"
    elif tablepick == "3":
        ID = "PubInvoiceID"
        table = "PubInvoice"
    elif tablepick == "4":
        ID = "BookInvoiceID"
        table = "BookInvoice"
    elif tablepick == "5":
        ID = "BookInvoiceItems"
        table = "BookInvoiceItems"
    elif tablepick == "6":
        ID = "RoyaltiesID"
        table = "Royalties"
    elif tablepick == "7":
        ID = "RoyaltiesItems"
        table = "RoyaltiesItems"
    data = input("Enter the {} for the entry you want to update: ".format(ID))

    return table, data, ID

def GetUpdateData():
    updatelist = []
    count = 0
    entry = None
    value = []
    while entry != "n":
        if count == 0:
            entry = input("Enter what you want to update: ")
            updatelist.append(entry)
            count = 1
        elif count == 1:
            entry = input("Enter what you want to update (or enter n to update): ")
            
            if entry != "n":
                updatelist.append(entry)
            
    for count in range(0, len(updatelist)):
        rawvalue = input("Enter the new value for the {}: ".format(updatelist[count]))
        rawvalue = "'" + rawvalue + "'"
        value.append(rawvalue)
        
    update = ""
    for count in range(0, len(updatelist)):
        if count == 0:
            update += "{} = {}".format(updatelist[count], value[count])
        else:
            update += ", {} = {}".format(updatelist[count], value[count])

    return update
                                   
#Getting a choice and data for the delete menu from the user
def GetDeleteChoice():

    tablepick = input()

    if tablepick == "1":
        ID = "AuthorID"
        table = "Customer"
    elif tablepick == "2":
        ID = "ISBN"
        table = "Book"
    elif tablepick == "3":
        ID = "PubInvoiceID"
        table = "PubInvoice"
    elif tablepick == "4":
        ID = "BookInvoiceID"
        table = "BookInvoice"
    elif tablepick == "5":
        ID = "BookInvoiceItems"
        table = "BookInvoiceItems"
    elif tablepick == "6":
        ID = "RoyaltiesID"
        table = "Royalties"
    elif tablepick == "7":
        ID = "RoyaltiesItems"
        table = "RoyaltiesItems"

    data = input("Enter the {}: ".format(ID))

    return data, table, ID

#main function
def main():

    Choice = '0'

    while Choice not in ['q', 'Q','Quit', 'quit']:

        DisplayMainMenu()
        Choice = GetMenuChoice()

        if Choice == '1':

            while Choice not in ['b', 'B','Back', 'back']:
                DisplayAddMenu()
                Choice = GetMenuChoice()
                
                if Choice == '1':
                    customer_data = input_customer()
                    table, placeholders = CustomerEntry()
                    create_data(customer_data, table, placeholders)
                elif Choice == '2':
                    book_data = input_book()
                    table, placeholders = BookEntry()
                    create_data(book_data, table, placeholders)
                elif Choice == '3':
                    pub_invoice_data = input_pub_invoice()
                    table, placeholders = PubInvoiceEntry()
                    create_data(pub_invoice_data, table, placeholders)
                elif Choice == '4':
                    book_invoice_data = input_book_invoice()
                    table, placeholders = BookInvoiceEntry()
                    create_data(book_invoice_data, table, placeholders)
                elif Choice == '5':
                    book_invoice_items_data, BookInvoiceID = input_book_invoice_items()
                    table, placeholders = BookInvoiceItemsEntry()
                    create_data(book_invoice_items_data, table, placeholders)
                    calculate_book_invoice_payment(BookInvoiceID)
                    
                elif Choice == '6':
                    royalties_data = input_royalties()
                    table, placeholders = RoyaltiesEntry()
                    create_data(royalties_data, table, placeholders)

                elif Choice == '7':
                    royalties_items_data, RoyaltiesID = input_royalties_items()
                    table, placeholders = RoyaltiesItemsEntry()
                    create_data(royalties_items_data, table, placeholders)
                    calculate_royalties(RoyaltiesID)
                    

        if Choice == '2':

            while Choice not in ['b', 'B', 'Back', 'back']:
                DisplayUpdateMenu()
                table, data, ID = GetUpdateChoice()
                update = GetUpdateData()
                update_data(data, table, update, ID)
        
        if Choice == '3':

            while Choice not in ['b', 'B', 'Back', 'back']:
                
                DisplayDeleteMenu()
                data, table, ID = GetDeleteChoice()
                delete_data(data, table, ID)
            
if __name__ == "__main__":
    main()
