from database import insert_transaction

def submit_transaction(user_id, amount, category, description):
    insert_transaction(user_id, amount, category, description)
