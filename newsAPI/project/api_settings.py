REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api_auth.authentication.TokenAuthentication',
    ],
}

# SETTINGS FOR JWT
ACCESS_TOKEN_LIFETIME = 60*60*3  # in seconds
REFRESH_TOKEN_LIFETIME = 60*60*24  # in seconds