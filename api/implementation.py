import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd 
from api.firestore_utils import get_collection, add_to_collection, get_object, update_collection, delete_object, fetch_firestore_id

# provide the path to the Google credentials file
cred = credentials.Certificate("./serviceAccount.json")
firebase_admin.initialize_app(cred)
# initialize a client which will be used to perform operations on the database
firestore_db = firestore.client()

"""
    Returns a list of all the users in the database
    Args:
        None
    Returns:
        List of dictionaries
"""
def get_users_list():
    print("Fetching Users Collection from Firestore")
    snapshot_list = get_collection(firestore_db)
    li = []
    for snapshot in snapshot_list:
        li.append(snapshot.to_dict())
    return li

"""
    Creates a user document in the database
    Args:
        Dictionary - request body
    Returns:
        None
"""
def create_user(data):
    print("Adding User to Firestore: {}".format(data))
    add_to_collection(firestore_db, data)

"""
    Returns the user details from the database
    Args:
        String - user ID
    Returns:
        Dictionary
"""
def get_user(id):
    print("Getting User details from Firestore: {}", id)
    docs = get_object(firestore_db, id)
    if len(docs) > 0:
        return docs[0].to_dict()
    else:
        return None

"""
    Updates specified fields for a user
    Args:
        Dictionary - updated fields
        String - user ID
    Returns:
        None
"""
def update_user(data, id):
    doc_id = get_firestore_id(id)
    print("Updating user {} in Firestore: {}".format(doc_id, data))
    update_collection(firestore_db, doc_id, data)

"""
    Deletes a user from the database
    Args:
        String - user ID
    Returns:
        None
"""
def delete_user(id):
    doc_id = get_firestore_id(id)
    print("Deleting user {} in Firestore".format(doc_id))
    delete_object(firestore_db, doc_id)

"""
    Queries database for the document ID
    Args:
        String - user ID
    Returns:
        String - document ID
"""
def get_firestore_id(user_id):
    print("Getting Firestore ID corresponding to {}".format(user_id))
    docs = fetch_firestore_id(firestore_db, user_id)
    if docs is None:
        return None
    else:
        return docs[0].id

"""
    Data normalization for CSV conversion
    Args:
        List of dictionaries
    Returns:
        List
"""
def normalize(data):
    print("Normalizing data for CSV file")
    newData = pd.json_normalize(data)
    return newData

def get_payment_details(id):
    return 0

def make_payment(data):
    return 0