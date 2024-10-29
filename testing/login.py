import firebase_admin
from firebase_admin import credentials, auth, firestore

# Path to your Firebase private key file
cred = credentials.Certificate("/Users/pujitha/Downloads/to-do-list.json")
firebase_admin.initialize_app(cred)

print("Please create your account")

email = input("Enter your email: ")
password = input("Enter your password: ")

auth.create_user(email=email, password=password)


print("Please log in with the account you created.")
email = input("Enter your email: ")

try:
  user = auth.get_user_by_email(email=email)
except:
  print("There was an error logging you in.")
else:
  print(f"Logged in user {user.email} with uid {user.uid}")

