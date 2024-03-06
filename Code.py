import mysql.connector

def calculate_sales(data):
    seller_sales = {}
    total_sales = {}

    for row in data:
        seller = row['seller']
        product = row['product']
        quantity = row['quantity']
        price = row['price']

        product_sales = quantity * price

        # Calculate individual product sales for each seller
        if seller not in seller_sales:
            seller_sales[seller] = {}
        if product not in seller_sales[seller]:
            seller_sales[seller][product] = 0
        seller_sales[seller][product] += product_sales

        # Calculate total sales for each seller
        if seller not in total_sales:
            total_sales[seller] = 0
        total_sales[seller] += product_sales

    return seller_sales, total_sales

db_connection = mysql.connector.connect(
    host="cis3368fall.c5nfalmzzodd.us-east-1.rds.amazonaws.com",
    user="admin",
    password="cisfall2023",
    database="cis3368falldb"
)

# Create a cursor
cursor = db_connection.cursor()

# Execute a query to fetch distinct seller names
seller_query = "SELECT DISTINCT seller FROM sales"
cursor.execute(seller_query)

# Fetch the list of distinct seller names
seller_names = [seller[0] for seller in cursor.fetchall()]

# Print the list of seller names
print("Available sellers:")
for seller_name in seller_names:
    print(seller_name)

# Ask the user to enter a seller's name
selected_seller = input("Enter a seller's name: ")

# Execute a query for the selected seller
query = f"SELECT * FROM sales WHERE seller = '{selected_seller}'"
cursor.execute(query)

# Fetch and store the data as a list of dictionaries
data = []
columns = [desc[0] for desc in cursor.description]

for row in cursor.fetchall():
    row_dict = dict(zip(columns, row))
    data.append(row_dict)

# Perform calculations for the selected seller
if data:
    print(f"Data for seller {selected_seller}:")
    for item in data:
        print(item)
    
    # Calculate sales
    seller_sales, total_sales = calculate_sales(data)

    # Print individual product sales for the seller
    print(f"Individual Product Sales for {selected_seller}:")
    for product, sales in seller_sales[selected_seller].items():
        print(f"{product}: {float(sales):.2f}")

    # Print total sales for the seller
    print(f"Total Sales for {selected_seller}: {total_sales[selected_seller]:.2f}")

else:
    print(f"No data found for seller {selected_seller}.")

# Close the cursor and connection
cursor.close()
db_connection.close()
