from django.utils.dateparse import parse_duration

from project import env

JWT_SECRET = env.get('JWT_SECRET')
JWT_EXPIRATION_DELTA = env.get('JWT_EXPIRATION_DELTA', parse_duration)
JWT_ALGORITHM = env.get('JWT_ALGORITHM', default='HS256')
