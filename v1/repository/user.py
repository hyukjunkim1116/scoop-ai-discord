from . import get_collection

class UserRepository:
    def __init__(self):
        self.collection = get_collection("users", "users")

    def initialize_user(self, user_id):
        return self.collection.insert_one({"user_id": user_id})

    def get_user_by_id(self, user_id):
        return self.collection.find_one({"user_id": user_id})

    def update_user(self, user_id, updated_data):
        return self.collection.update_one({"user_id": user_id}, {"$set": updated_data})

    def delete_user(self, user_id):
        return self.collection.delete_one({"user_id": user_id})
