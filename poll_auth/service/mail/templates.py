from dj_docs.settings import BASE_URL


class BaseTemplate:

    def __init__(self, to, hash):
        self.to = to
        self.hash = hash
        self.subject = None
        self.message = None

    def sendgrid_dump(self):
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
                    "value": self.message
                }
            ]
        }


class RegistrationConfirmationTemplate(BaseTemplate):
    def __init__(self, to, hash):
        super().__init__(to, hash)
        self.subject = "Подтверждение регистрации"
        self.message = self._construct_message()

    def _construct_message(self):
        return "Для подтверждения регистрации пройдите по следующей ссылке: %s" % (
            BASE_URL + "auth/register/" + self.hash
        )


class PasswordRecoveryTemplate(BaseTemplate):
    def __init__(self, to, hash, new_password):
        super().__init__(to, hash)
        self.subject = "Восстановление пароля"
        self.new_password = new_password
        self.message = self._construct_message()

    def _construct_message(self):
        return "Ваш новый пароль: %s .Для сброса перейдите по следующей ссылке: %s" % (
            self.new_password,
            BASE_URL + "auth/password_recovery/" + self.hash
        )
