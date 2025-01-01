from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify
import subprocess
import json
from controllers.main_controller import get_security_systems_data
from controllers.main_controller import get_endpoints_data
from controllers.main_controller import get_cart
from controllers.main_controller import add_to_cart
from controllers.main_controller import remove_from_cart
from controllers.main_controller import clear_cart
from controllers.main_controller import validate_cart


views = Blueprint("views", __name__, template_folder="templates")


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/security_systems")
def security_systems():
    # Get the current page number and search query from the query string
    page = request.args.get("page", 1, type=int)
    query = request.args.get("query", "")
    per_page = 10  # Number of items per page

    # Get the data from the controller
    data, total_pages, total_items = get_security_systems_data(page, per_page, query)

    return render_template(
        "security_systems.html",
        data=data,
        page=page,
        total_pages=total_pages,
        total_items=total_items,
    )


@views.route("/endpoints")
def endpoints():
    # Get the current page number and search query from the query string
    page = request.args.get("page", 1, type=int)
    query = request.args.get("query", "")
    per_page = 10  # Number of items per page

    # Get the data from the controller
    data, total_pages, total_items = get_endpoints_data(page, per_page, query)
    return render_template(
        "endpoints.html",
        data=data,
        page=page,
        total_pages=total_pages,
        total_items=total_items,
    )


@views.route("/about")
def about():
    return render_template("about.html")


@views.route("/cart")
def cart():
    cart = get_cart()  # Use the controller's logic to get the cart
    categorized_cart = {
        "security_systems": [
            {"id": item["id"], "displayname": item["displayname"], "name": item["name"]}
            for item in cart
            if item["category"] == "security_systems"
        ],
        "endpoints": [
            {"id": item["id"], "displayname": item["displayname"], "name": item["name"]}
            for item in cart
            if item["category"] == "endpoints"
        ],
    }
    return render_template(
        "cart.html", cart=categorized_cart
    )  # Render the template with the categorized cart data


@views.route("/add_to_cart", methods=["POST"])
def add_to_cart_route():
    item_id = request.json.get("key")
    category = request.json.get("category")
    displayname = request.json.get("displayname")
    name = request.json.get("name")
    connectionkey = request.json.get("connectionkey")
    connectionname = request.json.get("connectionname")
    add_to_cart(item_id, category, displayname, name, connectionkey, connectionname)
    return jsonify({"status": "success", "message": f"{name} added to cart"})


@views.route("/remove_from_cart", methods=["POST"])
def remove_from_cart_route():
    item_id = request.json.get("key")
    name = request.json.get("name")
    category = request.json.get("category")
    remove_from_cart(item_id, category, name)
    return jsonify({"status": "success", "message": f"{name} removed from cart"})


@views.route("/get_cart", methods=["GET"])
def get_cart_route():
    cart = get_cart()
    categorized_cart = {
        "security_systems": [
            {
                "id": item["id"],
                "displayname": item["displayname"],
                "name": item["name"],
                "category": item["category"],
                "connectionkey": item["connectionkey"],
                "connectionname": item["connectionname"],
            }
            for item in cart
            if item["category"] == "security_systems"
        ],
        "endpoints": [
            {
                "id": item["id"],
                "displayname": item["displayname"],
                "name": item["name"],
                "category": item["category"],
            }
            for item in cart
            if item["category"] == "endpoints"
        ],
    }
    print(categorized_cart)
    return jsonify(categorized_cart)


@views.route("/submit_cart", methods=["POST"])
def submit_cart_route():
    data = request.json
    # Serialize the lists to dictionaries with 'id' and 'name'
    security_systems = [
        {"id": item["id"], "name": item["name"]} for item in data.get("security_systems", [])
    ]
    endpoints = [
        {"id": item["id"], "name": item["name"]} for item in data.get("endpoints", [])
    ]
    # Get unique connection keys
    connection_keys = list(
        set(item["connectionkey"] for item in data.get("security_systems", []))
    )

    # Validate the cart
    is_valid, message = validate_cart(
        {
            "security_systems": [item["id"] for item in security_systems],
            "endpoints": [item["id"] for item in endpoints],
        }
    )
    if not is_valid:
        return jsonify({"message": message}), 400

    # Process the submitted cart data as needed
    print(f"Security Systems: {security_systems}")
    print(f"Endpoints: {endpoints}")
    print(f"Unique Connection keys: {connection_keys}")

    # Serialize the data to JSON for safe passing as arguments
    security_systems_json = json.dumps(security_systems)
    endpoints_json = json.dumps(endpoints)
    connection_keys_json = json.dumps(connection_keys)

    # Call the external script with the keys as arguments
    try:
        result = subprocess.run(
            [
                "python",
                "C:\\DEV\\Py_Selenium_Script 1\\scripts\\src\\run.py",
                "--security_systems", security_systems_json,
                "--endpoints", endpoints_json,
                "--connection_keys", connection_keys_json,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        print(result.stdout)
        return jsonify(
            {"message": "Cart submitted successfully", "script_output": result.stdout}
        )

    except subprocess.CalledProcessError as e:
        print(e.stderr)
        return jsonify({"message": "Error running script", "error": e.stderr}), 500


@views.route("/clear_cart", methods=["POST"])
def clear_cart_route():
    response, status_code = clear_cart()
    return jsonify(response), status_code


@views.route("/profile/<username>")
def profile(username):
    return render_template("index.html", name=username)
