import sqlite3

def create_table(db_name, table_name, sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("PRAGMA foreign_keys_ = ON")
        cursor.execute("select name from sqlite_master where name=?", (table_name,))
        result = cursor.fetchall()
        keep_table = True
        if len(result) == 1:
            response = input("The table {0} already exists, do you wish to recreate it (y/n): ".format(table_name))
            if response == "y":
                keep_table = False
                print("The {0} table will be recreated - all existing data will be lost".format(table_name))
                cursor.execute("drop table if exists {0}".format(table_name))
                db.commit()
            else:
                print("The existing table was kept")
        else:
            keep_table = False
        if not keep_table:
            cursor.execute(sql)
            db.commit()

def customer_table(db_name):
    sql = """create table Customer 
             (AuthorID integer,
             FirstName text,
             LastName text,
             Email text,
             PhoneNumber text,
             Address text,
             Postcode text,
             primary key(AuthorID))"""
    create_table(db_name, "Customer", sql)
        
def book_table(db_name):
    sql = """create table Book 
             (ISBN text,
             AuthorID integer,
             BookTitle text,
             NoOfPages integer,
             Size text,
             Back text,
             Cover text,
             Paper text,
             Font text,
             FontSize real,
             DatePublished date,
             Price real,
             primary key(ISBN),
             foreign key(AuthorID) references Customer(AuthorID))"""
    create_table(db_name, "Book", sql)

def pub_invoice_table(db_name):
    sql = """create table PubInvoice 
             (PubInvoiceID integer,
             ISBN text,
             AuthorID integer,
             PubInvoiceDate date,
             PubInvoiceService text,
             PubInvoicePayment real,
             primary key(PubInvoiceID),
             foreign key(AuthorID) references Customer(AuthorID),
             foreign key(ISBN) references Book(ISBN))"""
    create_table(db_name, "PubInvoice", sql)

def book_invoice_table(db_name):
    sql = """create table BookInvoice
             (BookInvoiceID integer,
             AuthorID integer,
             BookInvoiceDate date,
             BookInvoicePayment real,
             primary key(BookInvoiceID),
             foreign key(AuthorID) references Customer(AuthorID))"""
    create_table(db_name, "BookInvoice", sql)

def book_invoice_items_table(db_name):
    sql = """create table BookInvoiceItems
             (BookInvoiceItemsID integer,
             BookInvoiceID integer,
             ISBN text,
             BookInvoiceQuantity integer,
             BookInvoiceDiscount real,
             ShippingType text,
             ShippingPrice real,
             primary key(BookInvoiceItemsID),
             foreign key(BookInvoiceID) references BookInvoice(BookInvoiceID),
             foreign key(ISBN) references Book(ISBN))"""
    create_table(db_name, "BookInvoiceItems", sql)

def royalties_table(db_name):
    sql = """create table Royalties
             (RoyaltiesID integer,
             AuthorID integer,
             RoyaltiesDate date,
             RoyaltyPayment real,
             primary key(RoyaltiesID),
             foreign key(AuthorID) references Customer(AuthorID))"""
    create_table(db_name, "Royalties", sql)

def royalty_items_table(db_name):
    sql = """create table RoyaltyItems
             (RoyaltyItemsID integer,
             RoyaltiesID integer,
             ISBN text,
             Currency text,
             RoyaltyDiscount real,
             WholesalePrice real,
             RoyaltyQuantity integer,
             NetSales real,
             PrintCost real,
             ExcRateFromGBP real,
             primary key(RoyaltyItemsID),
             foreign key(RoyaltiesID) references Royalties(RoyaltiesID),
             foreign key(ISBN) references Book(ISBN))"""
    create_table(db_name, "RoyaltyItems", sql)

def main():
    db_name = "PP.db"
    customer_table(db_name)
    book_table(db_name)
    pub_invoice_table(db_name)
    book_invoice_table(db_name)
    book_invoice_items_table(db_name)
    royalties_table(db_name)
    royalty_items_table(db_name)

    

if __name__ == "__main__":
    main()
    
