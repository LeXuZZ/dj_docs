from dj_docs.settings import BASE_URL, SENDGRID_API_KEY


class BaseTemplate:

    def __init__(self, to, text, url, registration_hash, subject):
        self.to = to
        self.text = text
        self.url = url
        self.registration_hash = registration_hash
        self.subject = subject
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer %s" % SENDGRID_API_KEY
        }

    def __str__(self):
        return {
            "personalizations": [
                {
                    "to": [
                        {
                            "email": self.to
                        }
                    ],
                    "subject": self.subject
                }
            ],
            "from": {
                "email": "porovozls@gmail.com"
            },
            "content": [
                {
                    "type": "text",
                    "value": "%s %s" % (self.text, self.url)
                }
            ]
        }


class RegistrationConfirmationTemplate(BaseTemplate):
    def __init__(self, to, registration_hash):
        self.text = "Для подтверждения регистрации перейдите по следующей ссылке: "
        self.subject = "Подтверждение регистрации"
        self.url = BASE_URL + "auth/registration_confirmation/" + registration_hash
        super().__init__(to, self.text, self.url, registration_hash, self.subject)


class PasswordRecoveryTemplate(BaseTemplate):
    def __init__(self, to, registration_hash):
        self.text = "Для сброса пароля перейдите по следующей ссылке: "
        self.subject = "Восстановление пароля"
        self.url = BASE_URL + "auth/password_recovery/" + registration_hash
        super().__init__(to, self.text, self.url, registration_hash, self.subject)
