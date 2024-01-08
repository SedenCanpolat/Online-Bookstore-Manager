CREATE DATABASE Online_Bookstore_Project_Seden_Canpolat;
USE Online_Bookstore_Project_Seden_Canpolat;

CREATE TABLE Customers (
  Customer_ID int NOT NULL AUTO_INCREMENT,
  First_Name varchar(50),
  Last_Name varchar(50),
  Email varchar(50),
  Address varchar(70),
  Telephone_Number varchar(10),
  PRIMARY KEY (Customer_ID)
);

CREATE TABLE Publishers (
  Publisher_ID int NOT NULL AUTO_INCREMENT,
  Address varchar(70),
  Name varchar(50),
  Telephone_Number varchar(10),
  PRIMARY KEY (Publisher_ID)
);

CREATE TABLE Authors (
  Author_ID int NOT NULL AUTO_INCREMENT,
  First_Name varchar(50),
  Last_Name varchar(50),
  Date_of_Birth varchar(10),
  PRIMARY KEY (Author_ID) 
);

CREATE TABLE Books (
  Book_ID int NOT NULL AUTO_INCREMENT,
  Author_ID int,
  Publisher_ID int,
  Title varchar(50),
  Genre varchar(50),
  Number_of_Pages int,
  Price int,
  PRIMARY KEY (Book_ID),
  FOREIGN KEY (Publisher_ID) REFERENCES Publishers (Publisher_ID),
  FOREIGN KEY (Author_ID) REFERENCES Authors (Author_ID)
);

CREATE TABLE Carts (
  Cart_ID int NOT NULL AUTO_INCREMENT,
  Customer_ID int,
  Book_ID int,
  Price int,
  Quantity int,
  Shopping_Date varchar(10),
  Shipping_Date varchar(10),
  PRIMARY KEY (Cart_ID)
);

DROP TABLE Customers, Authors, Publishers, Books, Carts;
DROP TABLE Carts;

INSERT INTO Customers (First_Name, Last_Name, Email, Address, Telephone_Number) VALUES ("Elsa", "Snow", "elsasnowemail", "Finland", "5364562141");
INSERT INTO Customers (First_Name, Last_Name, Email, Address, Telephone_Number) VALUES ("Elmas", "Snow", "elmassnowemail", "Finland", "5364564558");
INSERT INTO Customers (First_Name, Last_Name, Email, Address, Telephone_Number) VALUES ("Adrea", "Sun", "adreasunemail", "Sweden", "5556898437");

INSERT INTO Authors (First_Name, Last_Name, Date_of_Birth) VALUES ("J.K.", "Rowling", "1965");
INSERT INTO Publishers (Address, Name, Telephone_Number) VALUES ("Izmir", "YKY", "2183648123");
INSERT INTO Books (Author_ID, Publisher_ID, Title, Genre, Number_of_Pages, Price) VALUES ("1", "1", "Harry Potter", "Fantasy", "300", "50");

INSERT INTO Authors (First_Name, Last_Name, Date_of_Birth) VALUES ("William", "Shakespeare", "1564");
INSERT INTO Publishers (Address, Name, Telephone_Number) VALUES ("Istanbul", "Turkiye Is Bankasi", "2362542112");
INSERT INTO Books (Author_ID, Publisher_ID, Title, Genre, Number_of_Pages, Price) VALUES ("2", "2", "Romeo ve Juliet", "Drama", "150", "30");

INSERT INTO Authors (First_Name, Last_Name, Date_of_Birth) VALUES ("George", "Orwell", "1903");
INSERT INTO Publishers (Address, Name, Telephone_Number) VALUES ("Izmir", "Can", "2562451221");
INSERT INTO Books (Author_ID, Publisher_ID, Title, Genre, Number_of_Pages, Price) VALUES ("3", "3", "1984", "Science Fiction", "350", "40");

INSERT INTO Books (Author_ID, Publisher_ID, Title, Genre, Number_of_Pages, Price) VALUES ("3", "3", "Hayvan Ciftligi", "Fable", "150", "20");
  
select * from Customers;
select * from Publishers;
select * from Books;
select * from Authors;
select * from Publishers;
select * from Carts;
