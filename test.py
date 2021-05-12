import jwt
from os import listdir
private_key = open('.ssh/is_rsa').read()
token = jwt.encode({'some': 'pyload'}, private_key, algorithm='RS256').decode('utf-8')
print(token)