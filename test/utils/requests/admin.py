"""Admin json requests
"""
# valid requests
admin = {
    "name": "Test",
    "email": "testadmin@plotlabs.com",
    "password": "plotlabs"
}

# invalid email values
admin_invalid_email_format = {
    "name": "Test",
    "email": "testadminplotlabs.com",
    "password": "plotlabs"
}

admin_email_none = {
    "name": "Test",
    "email": None,
    "password": "plotlabs"
}

# invalid password values
admin_password_short = {
    "name": "Test",
    "email": "testadmin@plotlabs.com",
    "password": "plot"
}

admin_password_long = {
    "name": "Test",
    "email": "testadmin@plotlabs.com",
    "password": "plotlabsplotlabsplotlabsplotlabsplotlabsplotlabsplotlabs"
                "plotlabs"
}

admin_password_none = {
    "name": "Test",
    "email": "testadmin@plotlabs.com",
    "password": None
}

# invalid name values
admin_name_short = {
    "name": "Tes",
    "email": "testadmin@plotlabs.com",
    "password": "plotlabs"
}

admin_name_long = {
    "name": "testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttest",
    "email": "testadmin@plotlabs.com",
    "password": "plotlabs"
}
