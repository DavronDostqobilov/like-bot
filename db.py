import json

class LikeDB:
    def __init__(self, file_path):
        # Initialize the database
        self.file_path = file_path
        # Open the database file if it exists, otherwise create a new one
        try:
            with open(self.file_path, 'r') as f:
                self.db = json.load(f)
        except:
            self.db = {}
            with open(self.file_path, 'w') as f:
                json.dump(self.db, f)

    def save(self):
        """
        Save the database to the file
        """
        with open(self.file_path, 'w') as f:
            json.dump(self.db, f, indent=4)
         
    def add_student(self,user_id):
         
         if self.db.get(user_id)==None:
             self.db[user_id]={'like':0 , 'dislike':0}
             self.save()

    def all_likes(self, user_id):
        """
        Count all users likes
        """
        likes = self.db.get(user_id)
        return likes['like']

    def all_dislikes(self, user_id):
        """
        Count all users dislikes
        """
        likes = self.db.get(user_id)
        return likes['dislike']

    def add_like(self, user_id:str):
        """
        Add like to the database
        
        Args:
            user_id (str): telegram user id

        Returns:
            The number of likes and dislikes for the post
        """
        user = self.db.get(user_id)
        if user['like']==1:
                user['like']=0
        elif user['like']==0:
            user['like']+=1
            user['dislike']=0
        
        self.save()
        
        return user

    def add_dislike(self, user_id:str):
        """
        Add dislike to the database
        
        Args:
            user_id (str): telegram user id

        Returns:
            The number of likes and dislikes for the post
        """
        user = self.db.get(user_id)
        if user['dislike']==1:
                user['dislike']=0
        elif user['dislike']==0:
            user['dislike']+=1
            user['like']=0
        self.save()
    
   
        return user