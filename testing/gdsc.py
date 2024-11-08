import firebase_admin
from firebase_admin import credentials, firestore, auth

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "gdsc-demo-939da",
  "private_key_id": "58d64bbbd2a3cbfdd17d5068fce286563cd23ca2",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCGurBMnaD2RoIS\niC3y1HxUCcuzdDEcTmSDampvYqOP+r86HT96cKbJfKvhWMjDTgXyVCbdmzuI1jSc\n7tXgCTz79YK5RupRB5yGXICEgD+3gb35OZa5V34Yo5jhvKDyo/SqTdMPZPh/X+8P\nisn5Kk93z3U9x/3YGozDUnbLJnbi8g7sdw6FSMl2RpLm8Yf618EeiXsl7/w6ViRO\nvSwOIkyd4J5e7nbZs9j1dIxJGITrMXQT4XKzYitWiAqM25zkqwAB3Yv9QbCp4ORS\nPOoaClEZW525jDRjSao84lKguGm6KlZgU28v3boWgz4hfCkxkQlJeznn0PuvhvAY\nFXk4Nr/9AgMBAAECggEAHoNqGdQKaDSEUYOnmmtO5C6axKAgXkeP4qaHiAYIQrvY\nsuX8YjPgxlnWyLD1uSvy01UFP2PgqidPX6qE5FpbRjoumt0phOQLKnAJSFkOdTZs\nauVE0mGzJIvqvFdfAU0qRKbfEgm9cQWubC/z+dtAB8PDyxQAFQFAV51V28EwpEm3\nf4lJipUoaHPTldM9ndn9im1Bd3Nq41M9jyobylsNgPK6R+oEQSmN68KzzElGKL9q\nReOPi7pAvASH+ij2luUlh/UmgDaYykLyheyIiGZdzBzVlzOoOWSQrjTGF7SpFfLb\ng0TNZSRLlgEo34eeYrcyuXkA9u9qqNiFI0vKNfmAwQKBgQC8Q0CPoqBbrldaI8ie\n0WtyV1+tvtU7pHWuaLUCv0sSpq06QqUS8fr249nnUoqbwkGdzJ7VAcMT8c4Si/Xi\n3sSYqkKfz/rIF3foQgscjlztKAZcwIJZ32cvY2ByQEO4Foh5SQja2jBrQQsZZbER\n7zFt0btfNG2qzv6tehIBQSA9PQKBgQC3NIHYHyvse752Y6enpmV+Fb3zjynsmeSr\nwWU1PVHrNZXPUYDBjTO9X6aunzQH4std65NToevM2Xlu38dn1SeR+wEwGYtP2i1U\nTbcfUkVUIsDeyERYaYr0z3zB57gYqSpW2yKj274ezHzd+hHeChA1pg4SnAc+MYt9\ndukTVr45wQKBgQCTpk8RF6Oao94gdOYYIPia4YnJk1xa/X3KPpaQRAUV6KD9i105\nwYxpa4Pvl13cEPszTlLXjh04HDHZe+lpd/tKHGZKPmxZ14YUIw/h4olg+j4bKmRR\nJhQgJ1lx4ZL64rlAHhaSxgKpa4bP8WBxR15F2fKRFWZZSySUW6OZVkF5pQKBgH+v\nTL/AGfDb3cbNdc/WnO3fYWAa63FHYKSESXFtp2ZzFlJDz6UWMHVP8O/LbYwBeROg\nWDH1rE49U/D+bg/j84w+kHlhlEK3INicwYBG6qLVBe8/TMMB7CLraVwLj7dAT43x\ndJcXU85LXsumukUyZlG9xhkaPcIO7dUnxxH/Zt0BAoGADTNtjUwSfCNHb9xhII5y\nJKnHLypRY59dJkWDupAjabi/nUraFz6/GtZCz3BPNr3UOmnN1B/K/HJxHQO0iKTs\n4HZ6NQQNSxkXlGAXZnT7CrkQnyFLUEztrpDj72zpMgxhwba9VL4Z1sgB3aTVgps9\nL+PDeXTzTCMahNqsh2tnp9w=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-rvjr6@gdsc-demo-939da.iam.gserviceaccount.com",
  "client_id": "107208204304874725343",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-rvjr6%40gdsc-demo-939da.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
)
firebase_admin.initialize_app(cred)

#print("Please create your account")

#email = input("Enter your email: ")
#password = input("Enter your password: ")

#auth.create_user(email=email, password=password)

email = input("Please enter your email")

try:
  user = auth.get_user_by_email(email=email)

except:
  print("ERROR")

else:
  print(f"Logged in user {user.email} with uid {user.uid}")
