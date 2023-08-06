from dataclasses import dataclass


@dataclass
class Credentials:
    username: str
    password: str


config_for_beta_user = {
    "app_key": "PPE_DESKTOP_APP_KEY",
    "username": "PPE_USERNAME",
    "password": "PPE_PASSWORD",
}

config_for_prod_user = {
    "app_key": "DESKTOP_APP_KEY",
    "username": "EDP_USERNAME",
    "password": "EDP_PASSWORD",
    "username_second": "EDP_USERNAME_2",
    "password_second": "EDP_PASSWORD_2",
    "username_third": "EDP_USERNAME_3",
    "password_third": "EDP_PASSWORD_3",
    "rdp_username": "RDP_USERNAME",
    "rdp_password": "RDP_PASSWORD",
    "rdp_username_second": "RDP_USERNAME_2",
    "rdp_password_second": "RDP_PASSWORD_2",
    "eikon_username": "EIKON_USERNAME",
    "eikon_password": "EIKON_PASSWORD",
}
