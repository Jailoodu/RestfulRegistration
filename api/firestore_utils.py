import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd 

def get_collection(firestore_db):
    return list(firestore_db.collection(u'users').get())

def add_to_collection(firestore_db, data):
    firestore_db.collection(u'users').add(data)

def get_object(firestore_db, id):
    users_ref = firestore_db.collection(u'users')
    # create a custom query which uses the id provided
    query = users_ref.where(u'id', u'==', id)
    return query.get()

def update_collection(firestore_db, id, data):
    user_ref = firestore_db.collection(u'users').document(id)
    user_ref.update(data)

def delete_object(firestore_db, id):
    user_ref = firestore_db.collection(u'users').document(id)
    user_ref.delete()

def fetch_firestore_id(firestore_db, user_id):
    users_ref = firestore_db.collection(u'users')
    query = users_ref.where(u'id', u'==', user_id)
    docs = query.get()
    return docs