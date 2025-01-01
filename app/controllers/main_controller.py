import pandas as pd
from flask import session


def get_security_systems_data(page, per_page, query=None):
    try:
        # Read the Excel file
        df = pd.read_excel(
            "C://DEV\Py_Selenium_Script 1//app//models//saviynt_data.xlsx"
        )

        # Select specific columns and remove duplicates
        df = df[
            [
                "SECURITY_SYSTEM_KEY",
                "SECURITY_SYSTEM_NAME",
                "SECURITY_SYSTEM_DISPLAYNAME",
                "CONNECTION_KEY",
                "CONNECTION_NAME",
            ]
        ].drop_duplicates()

        # Filter the data based on the search query
        if query:
            df = df[
                df["SECURITY_SYSTEM_NAME"].str.contains(query, case=False, na=False)
                | df["SECURITY_SYSTEM_DISPLAYNAME"].str.contains(
                    query, case=False, na=False
                )
            ]

        # Calculate pagination
        total_items = len(df)
        total_pages = (total_items + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page
        paginated_df = df[start:end]

        # Convert the DataFrame to a dictionary
        data = paginated_df.to_dict(orient="records")

        return data, total_pages, total_items
    except FileNotFoundError:
        print("Error: The specified Excel file was not found.")
        return [], 0, 0
    except pd.errors.EmptyDataError:
        print("Error: The Excel file is empty.")
        return [], 0, 0
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return [], 0, 0


def get_endpoints_data(page, per_page, query=None):
    try:
        # Read the Excel file
        df = pd.read_excel(
            "C://DEV\Py_Selenium_Script 1//app//models//saviynt_data.xlsx"
        )

        # Select specific columns and remove duplicates
        df = df[
            ["ENDPOINT_KEY", "ENDPOINT_NAME", "ENDPOINT_DISPLAYNAME"]
        ].drop_duplicates()

        # Filter the data based on the search query
        if query:
            df = df[
                df["ENDPOINT_NAME"].str.contains(query, case=False, na=False)
                | df["ENDPOINT_DISPLAYNAME"].str.contains(query, case=False, na=False)
            ]

        # Calculate pagination
        total_items = len(df)
        total_pages = (total_items + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page
        paginated_df = df[start:end]

        # Convert the DataFrame to a dictionary
        data = paginated_df.to_dict(orient="records")

        return data, total_pages, total_items
    except FileNotFoundError:
        print("Error: The specified Excel file was not found.")
        return [], 0, 0
    except pd.errors.EmptyDataError:
        print("Error: The Excel file is empty.")
        return [], 0, 0
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return [], 0, 0


def get_cart():
    try:
        if 'cart' not in session:
            session['cart'] = []
        return session['cart']
    except Exception as e:
        print(f"Error retrieving the cart from session: {e}")
        raise

def add_to_cart(item_id, category, displayname, name, connectionkey, connectionname):
    try:
        cart = get_cart()
        # Check if the item with the same id and category already exists in the cart
        if not any(item['id'] == item_id and item['category'] == category for item in cart):
            cart.append({'id': item_id, 'category': category, 'displayname': displayname, 'name': name, 'connectionkey': connectionkey, 'connectionname': connectionname})
            session['cart'] = cart
            print(f"Item with key {item_id}, category {category}, and name {name} added to the cart.")
            print(cart)
        else:
            print(f"Item with key {item_id}, category {category}, and name {name} is already in the cart.")
            print(cart)
    except Exception as e:
        print(f"Error adding item with key {item_id}, category {category}, and name {name} to the cart: {e}")
        raise

def remove_from_cart(item_id, category, name):
    try:
        cart = get_cart()
        # Remove the item with the specified id and category from the cart
        cart = [item for item in cart if not (item['id'] == item_id and item['category'] == category)]
        session['cart'] = cart
        print(f"Item {name} with key {item_id} and category {category} removed from the cart.")
    except Exception as e:
        print(f"Error removing item {name} with key {item_id} and category {category} from the cart: {e}")
        raise

def clear_cart():
    try:
        cart = session.get('cart', [])
        if not cart:
            return {'message': 'Cart is already empty'}, 400
        
        session['cart'] = []
        print("Cart cleared.")
        return {'message': 'Cart cleared successfully'}, 200
    except Exception as e:
        print(f"Error clearing cart: {e}")
        return {'message': f'Error clearing cart: {e}'}, 500
    
def validate_cart(cart):
    if not cart.get('security_systems') or not cart.get('endpoints'):
        return False, 'Both security systems and endpoints must be present in the cart.'
    return True, 'Cart is valid.'