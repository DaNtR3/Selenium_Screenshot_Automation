import os
import re
import pandas as pd
from flask import session
from azure.storage.blob import BlobServiceClient
from io import BytesIO
from datetime import datetime


def get_blob_saviynt_data():
    try:
        # 1. Retrieve the connection string from the environment variables
        connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        if not connection_string:
            raise ValueError("Connection string not found in environment variables!")

        # 2. Retrieve the container name and blob file name from environment variables
        container_name = os.getenv('AZURE_BLOB_CONTAINER_NAME')
        blob_name = os.getenv('AZURE_BLOB_FILE_NAME_TEST_DATA')

        if not container_name or not blob_name:
            raise ValueError("Container name or Blob file name not found in environment variables!")
        # Get the current date and time
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        #print(f"Using container: {container_name}, blob: {blob_name}")
        print(f"Using container: {container_name}, blob: {blob_name}, at {current_datetime}")

        # 3. Initialize BlobServiceClient using the connection string
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        # 4. Download the Excel file from Azure Blob Storage
        blob_client = container_client.get_blob_client(blob_name)
        blob_data = blob_client.download_blob()

        # 5. Read the downloaded data into a pandas DataFrame
        file_bytes = blob_data.readall()  # Read the file content into bytes
        excel_data = BytesIO(file_bytes)  # Convert byte content to a BytesIO object (in-memory file)

        # 6. Use pandas to read the Excel file into a DataFrame
        df = pd.read_excel(excel_data)

        # Return the DataFrame
        return df

    except ValueError as ve:
        print(f"ValueError occurred: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_security_systems_data(page, per_page, query=None):

    try:
        df=get_blob_saviynt_data()

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
            # Escape special characters in the query
            escaped_query = re.escape(query)
            df = df[
                df["SECURITY_SYSTEM_NAME"].str.contains(escaped_query, case=False, na=False, regex=True)
                | df["SECURITY_SYSTEM_DISPLAYNAME"].str.contains(
                    escaped_query, case=False, na=False, regex=True
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
        df=get_blob_saviynt_data()

        # Select specific columns and remove duplicates
        df = df[
            ["ENDPOINT_KEY", "ENDPOINT_NAME", "ENDPOINT_DISPLAYNAME"]
        ].drop_duplicates()

        # Filter the data based on the search query
        if query:
            # Escape special characters in the query
            escaped_query = re.escape(query)
            df = df[
                df["ENDPOINT_NAME"].str.contains(escaped_query, case=False, na=False, regex=True)
                | df["ENDPOINT_DISPLAYNAME"].str.contains(escaped_query, case=False, na=False, regex=True)
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