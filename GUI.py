from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
import OnlineBookstore
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.mycursor = OnlineBookstore.mydb.cursor()
        #self.mycursor.execute("USE Online_Bookstore_Project_Seden_Canpolat")

        self.window = uic.loadUi("BookstoreProject.ui")
        self.window.searchButton.clicked.connect(self.search_books)
        self.window.addButton.clicked.connect(self.add_cart)
        self.window.deleteButton.clicked.connect(self.delete_from_cart)
        self.window.allButton.clicked.connect(self.all_books)
        self.window.historyButton.clicked.connect(self.cart_refresh)
        self.window.deleteButton_2.clicked.connect(self.clear_cart)

        self.cart_refresh()
  

    def all_books(self):
        self.mycursor.execute("""
            SELECT Books.Title, Authors.First_Name, Authors.Last_Name, Publishers.Name, Books.Genre, Books.Price
            FROM Books
            JOIN Authors ON Books.Author_ID = Authors.Author_ID
            JOIN Publishers ON Books.Publisher_ID = Publishers.Publisher_ID
        """)
        results = self.mycursor.fetchall()
        self.window.table.setRowCount(len(results))
        self.window.table.setColumnCount(len(results[0]))
        self.window.table.setHorizontalHeaderLabels(["Title", "First Name", "Last Name", "Publisher", "Genre", "Price"])
        for row_num, result_data in enumerate(results):
            for col_num, row_data in enumerate(result_data):
                item = QTableWidgetItem(str(row_data))
                self.window.table.setItem(row_num, col_num, item)

        self.agg_books()
        


    def search_books(self):
        title = self.window.searchLineEdit.text()    
        self.mycursor.execute("""
            SELECT Books.Title, Authors.First_Name, Authors.Last_Name, Publishers.Name, Books.Genre, Books.Price
            FROM Books
            JOIN Authors ON Books.Author_ID = Authors.Author_ID
            JOIN Publishers ON Books.Publisher_ID = Publishers.Publisher_ID
            WHERE Books.Title = %s or Authors.First_Name = %s or Authors.Last_Name = %s or Publishers.Name = %s or Books.Genre = %s or Books.Price = %s
        """, (title, title, title, title, title, title))
        results = self.mycursor.fetchall()

        if len(results) == 0:
            results = "No books found"
            self.window.table.setRowCount(1)
            self.window.table.setColumnCount(1)
            self.window.table.setHorizontalHeaderLabels(["Error"])
            item = QTableWidgetItem(str(results))
            self.window.table.setItem(0, 0, item)
            self.window.countLabel.setText(f"Count of books: 0")   

        else:
            self.window.table.setRowCount(len(results))
            self.window.table.setColumnCount(len(results[0]))
            self.window.table.setHorizontalHeaderLabels(["Title", "First Name", "Last Name", "Publisher", "Genre", "Price"])
            for row_num, result_data in enumerate(results):
                for col_num, row_data in enumerate(result_data):
                    item = QTableWidgetItem(str(row_data))
                    self.window.table.setItem(row_num, col_num, item)

            self.mycursor.execute("""
                SELECT COUNT(*) FROM Books
                JOIN Authors ON Books.Author_ID = Authors.Author_ID
                JOIN Publishers ON Books.Publisher_ID = Publishers.Publisher_ID
                WHERE Books.Title = %s or Authors.First_Name = %s or Authors.Last_Name = %s or Publishers.Name = %s or Books.Genre = %s or Books.Price = %s
                """, (title, title, title, title, title, title))
            count = self.mycursor.fetchone()[0]
            self.window.countLabel.setText(f"Count of books: {count}") 



    total = 0.0
    count = 0
    
    def add_cart(self):

        self.window.cart.setRowCount(self.window.cart.rowCount() + 1)
        self.window.cart.setColumnCount(3)
        self.window.cart.setHorizontalHeaderLabels(["Title", "Price", "Quantity"])

        self.cart_refresh()
        title = self.window.cartLineEdit.text()
        self.mycursor.execute("""
            SELECT Books.Book_ID, Books.Title, Books.Price
            FROM Books
            WHERE Books.Title = %s;    
        """, (title, ))
        result = self.mycursor.fetchone()
        self.mycursor.fetchall()

        if result is not None: #if the book is available
            book_id, book_title, book_price = result
            self.mycursor.execute("""
            SELECT Carts.Book_ID
            FROM Carts
            WHERE Carts.Book_ID = %s;    
            """, (book_id, ))
            result = self.mycursor.fetchone()

            if result is not None: #if the book is already in the cart
                self.mycursor.execute(""" 
                    UPDATE Carts
                    SET Quantity = Quantity + 1
                    WHERE Book_ID IN (
                    SELECT Book_ID FROM Books
                    WHERE Books.Title = %s
                    );    
                """, (title, ))
                OnlineBookstore.mydb.commit()
                self.cart_refresh()

            else: #if the book is not in the cart
                self.mycursor.execute("""
                    INSERT INTO Carts (Customer_ID, Book_ID, Price, Quantity, Shopping_Date, Shipping_Date)
                    SELECT 1, Books.Book_ID, Books.Price, 1, CURRENT_DATE, NULL
                    FROM Books
                    WHERE Books.Title = %s;   
                """, (title, ))
                OnlineBookstore.mydb.commit()
                self.cart_refresh()

        else:
            self.window.cart.setRowCount(1)
            self.window.cart.setColumnCount(1)
            self.window.cart.setHorizontalHeaderLabels(["Error"])
            item = QTableWidgetItem("Book not found")
            self.window.cart.setItem(0, 0, item)
            self.window.countLabel2.setText(f"Count of books: 0")
       

    def agg_books(self):
        self.mycursor.execute("SELECT COUNT(*) FROM Books")
        count = self.mycursor.fetchone()[0]
        self.window.countLabel.setText(f"Count of books: {count}")

        self.mycursor.execute("SELECT MIN(Price) FROM Books")
        min_price = self.mycursor.fetchone()[0]
        self.window.minPriceLabel.setText(f"Min price of books: {min_price:.2f}")

        self.mycursor.execute("SELECT MAX(Price) FROM Books")
        min_price = self.mycursor.fetchone()[0]
        self.window.maxPriceLabel.setText(f"Max price of books: {min_price:.2f}")

        self.mycursor.execute("SELECT AVG(Price) FROM Books")
        avg_price = self.mycursor.fetchone()[0]
        self.window.avgPriceLabel_2.setText(f"Average price of books: {avg_price:.2f}")

        self.mycursor.execute("SELECT COUNT(*) FROM Authors")
        author_count = self.mycursor.fetchone()[0]
        self.window.authorLabel.setText(f"Author count: {author_count: }")

        self.mycursor.execute("SELECT COUNT(*) FROM Publishers")
        publisher_count = self.mycursor.fetchone()[0]
        self.window.authorLabel_2.setText(f"Publisher count: {publisher_count: }")

        self.mycursor.execute("SELECT COUNT(DISTINCT Genre) FROM Books")
        genre_count = self.mycursor.fetchone()[0]
        self.window.authorLabel_3.setText(f"Genre count: {genre_count: }")


    def refresh_agg_cart(self):
        self.mycursor.execute("SELECT AVG(Price) FROM Carts")
        avg_price_result = self.mycursor.fetchone()
        if avg_price_result[0] is not None:
            avg_price = avg_price_result[0]
            self.window.avgPriceLabel.setText(f"Average Price: {avg_price:.2f}")
        else:
            self.window.avgPriceLabel.setText(f"Average Price: 0")

        self.mycursor.execute("SELECT MIN(Price) FROM Carts")
        min_price_result = self.mycursor.fetchone()
        if min_price_result[0] is not None:
            min_price = min_price_result[0]
            self.window.minPriceLabel_2.setText(f"Min priced book from cart: {min_price:.2f}")
        else:
            self.window.minPriceLabel_2.setText(f"Min priced book from cart: 0")

        self.mycursor.execute("SELECT MAX(Price) FROM Carts")
        max_price_result = self.mycursor.fetchone()
        if max_price_result[0] is not None:
            max_price = max_price_result[0]
            self.window.maxPriceLabel_2.setText(f"Max priced book from cart: {max_price:.2f}")
        else:
            self.window.maxPriceLabel_2.setText(f"Max priced book from cart: 0")


    def refresh_total(self):
        self.window.totalBox.setText('Total: ' + str(self.total))

    def refresh_count(self):
        self.window.countLabel2.setText(f"Count of books: {self.count}")


    def delete_from_cart(self):
        title_item = self.window.cart.item(self.window.cart.currentRow(), 0)
        quantity_item = self.window.cart.item(self.window.cart.currentRow(), 2)

        if title_item is not None and quantity_item is not None:
            title = title_item.text()
            quantity = int(quantity_item.text())

            deleted_book_price_item = self.window.cart.item(self.window.cart.currentRow(), 1)
            deleted_book_price = float(deleted_book_price_item.text()) if deleted_book_price_item is not None else 0.0

            self.mycursor.execute("""
                DELETE FROM Carts
                WHERE Book_ID IN (
                    SELECT Book_ID FROM Books
                    WHERE Title = %s
                )
            """, (title,))
            OnlineBookstore.mydb.commit()

            self.mycursor.execute("""
                SELECT COUNT(*) FROM Books
                WHERE Books.Title = %s
            """, (title,))
            
            count = self.mycursor.fetchone()[0]

            self.total -= deleted_book_price * quantity
            self.refresh_total()

            self.count -= quantity

            if self.count == 0:
                self.window.countLabel2.setText(f"Count of books: 0")
            else:
                self.refresh_count()
                
            self.refresh_agg_cart()         

            self.window.cart.removeRow(self.window.cart.currentRow())


    def clear_cart(self):
        self.mycursor.execute("DELETE FROM Carts")
        OnlineBookstore.mydb.commit()
        self.window.cart.setRowCount(0)
        self.window.countLabel2.setText(f"Count of books: 0")
        self.refresh_agg_cart()
        self.window.totalBox.setText('Total: 0.0')

        
          
    def cart_refresh(self):
        self.mycursor.execute("""
            SELECT Books.Title, Books.Price, Carts.Quantity
            FROM Books 
            JOIN Carts ON Books.Book_ID = Carts.Book_ID  
        """)
        result = self.mycursor.fetchall()

        total = 0.0
        count = 0

        self.window.cart.setRowCount(len(result))
        self.window.cart.setColumnCount(3) 
        self.window.cart.setHorizontalHeaderLabels(["Title", "Price", "Quantity"])

        for row_num, (book_title, book_price, quantity) in enumerate(result):

            item_title = QTableWidgetItem(str(book_title))
            item_price = QTableWidgetItem(str(book_price))
            item_quantity = QTableWidgetItem(str(quantity))
            self.window.cart.setItem(row_num, 0, item_title)
            self.window.cart.setItem(row_num, 1, item_price)
            self.window.cart.setItem(row_num, 2, item_quantity)

            total += book_price * quantity
            count += quantity
            

        self.total = total
        self.refresh_total()

        self.count = count
        self.refresh_count()

        self.refresh_agg_cart()


    def show(self):
        self.window.show()

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()