import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./RestfulRegistration/serviceAccount.json")
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()

def get_users_list():
    snapshots = list(firestore_db.collection(u'users').get())
    li = []
    for snapshot in snapshots:
        li.append(snapshot.to_dict())
    return li

def create_user(data):
    firestore_db.collection(u'users').add(data)

def get_user(id):
    users_ref = firestore_db.collection(u'users')
    query = users_ref.where(u'id', u'==', id)
    docs = query.get()
    if len(docs) > 0:
        for doc in docs:
            return doc.to_dict()
    else:
        return None

def update_user(data, id):
    users_ref = firestore_db.collection(u'users')
    query = users_ref.where(u'id', u'==', id)
    docs = query.get()
    doc_id = docs[0].id

    user_ref = firestore_db.collection(u'users').document(doc_id)
    user_ref.update(data)

def delete_user(id):
    users_ref = firestore_db.collection(u'users')
    query = users_ref.where(u'id', u'==', id)
    docs = query.get()
    doc_id = docs[0].id

    user_ref = firestore_db.collection(u'users').document(doc_id)
    user_ref.delete()