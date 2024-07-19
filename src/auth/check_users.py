from src.utils.model import PostSchema, UserSchema, UserLoginSchema
import pandas as pd
import os


base_dir = os.path.dirname(os.path.dirname(__file__))
df = pd.read_csv(base_dir + '/auth/users.csv')
users = df.to_dict(orient='records')

def check_user(data: UserLoginSchema):
    for user in users:
        if user['email'] == data.email and user['password'] == data.password:
            return True
    return False


