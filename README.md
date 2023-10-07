# Minishopp - Customer Relationship Management
Python Tkinter project: a simple app to insert/update/delete SQLite database record of fictional shop customers.

## Fictional user story
Minishopp manager needs an app to keep, add, and edit digital record of their customers' name, address, and phone numbers.

## Solution
Our app is built using Python Tkinter for its graphical interface, and SQLite database for its data storage. User may insert new customer record, update, or delete it by its ID number.

The main table that stores customers data is named `ms_customers`, which has columns of:
| Column name   | Description   |
| ------------- | ------------- |
| `oid`         | automatically-generated ID number for each row data  |
| `first_name`  | customer's first name (required)  |
| `last_name`   | customer's last name |
| `address`     | customer's address |
| `phone_number`| customer's phone number (required) |
| `modified_date`| automatically-generated date timestamp of row data creation or modification |

