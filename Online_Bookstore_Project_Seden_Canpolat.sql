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
  Shopping_Date varchar(10),
  Shipping_Date varchar(10),
  PRIMARY KEY (Cart_ID)
);

DROP TABLE Customers, Authors, Publishers, Books, Carts;

INSERT INTO Authors (First_Name, Last_Name, Date_of_Birth) VALUES ("JK", "Rowling", "12");
INSERT INTO Publishers (Address, Name, Telephone_Number) VALUES ("Izmir", "Can", "2183648123");
INSERT INTO Books (Author_ID, Publisher_ID, Title, Genre, Number_of_Pages, Price) VALUES ("1", "1", "Harry Potter", "Fantasy", "300", "50");