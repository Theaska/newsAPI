REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# SETTINGS FOR JWT
ACCESS_TOKEN_LIFETIME = 60*60*3  # in seconds
REFRESH_TOKEN_LIFETIME = 60*60*24  # in seconds