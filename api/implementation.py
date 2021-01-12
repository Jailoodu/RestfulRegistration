import firebase_admin
from firebase_admin import credentials, firestore

# provide the path to the Google credentials file
cred = credentials.Certificate("./RestfulRegistration/serviceAccount.json")
firebase_admin.initialize_app(cred)
# initialize a client which will be used to perform operations on the database
firestore_db = firestore.client()

# returns a list of all the users in the database
def get_users_list():
    snapshots = list(firestore_db.collection(u'users').get())
    li = []
    for snapshot in snapshots:
        li.append(snapshot.to_dict())
    return li

# creates user document in the database
def create_user(data):
    firestore_db.collection(u'users').add(data)

# fetches user details from the database given id
def get_user(id):
    users_ref = firestore_db.collection(u'users')
    # create a custom query which uses the id provided
    query = users_ref.where(u'id', u'==', id)
    docs = query.get()
    if len(docs) > 0:
        return docs[0].to_dict()
    else:
        return None

# updates specified fields for a user in the database
def update_user(data, id):
    doc_id = get_firestore_id(id)
    user_ref = firestore_db.collection(u'users').document(doc_id)
    user_ref.update(data)

# deletes user document from the database
def delete_user(id):
    doc_id = get_firestore_id(id)
    user_ref = firestore_db.collection(u'users').document(doc_id)
    user_ref.delete()

# queries database for the document id corresponding to the user id
def get_firestore_id(user_id):
    users_ref = firestore_db.collection(u'users')
    query = users_ref.where(u'id', u'==', user_id)
    docs = query.get()
    return docs[0].id