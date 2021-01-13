import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd 

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
    snapshots = list(firestore_db.collection(u'users').get())
    li = []
    for snapshot in snapshots:
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
    firestore_db.collection(u'users').add(data)

"""
    Returns the user details from the database
    Args:
        String - user ID
    Returns:
        Dictionary
"""
def get_user(id):
    users_ref = firestore_db.collection(u'users')
    # create a custom query which uses the id provided
    query = users_ref.where(u'id', u'==', id)
    docs = query.get()
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
    user_ref = firestore_db.collection(u'users').document(doc_id)
    user_ref.update(data)

"""
    Deletes a user from the database
    Args:
        String - user ID
    Returns:
        None
"""
def delete_user(id):
    doc_id = get_firestore_id(id)
    user_ref = firestore_db.collection(u'users').document(doc_id)
    user_ref.delete()

"""
    Queries database for the document ID
    Args:
        String - user ID
    Returns:
        String - document ID
"""
def get_firestore_id(user_id):
    users_ref = firestore_db.collection(u'users')
    query = users_ref.where(u'id', u'==', user_id)
    docs = query.get()
    return docs[0].id

"""
    Data normalization for CSV conversion
    Args:
        List of dictionaries
    Returns:
        List
"""
def normalize(data):
    newData = pd.json_normalize(data)
    return newData