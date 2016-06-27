class SuccessMessage:
    REGISTRATION_MAIL_SENT = "На почту отправлена ссылка для подтверждения регистрации"
    REGISTRATION_SUCCESS = "Вы успешно зарегистрировались"
    PASSWORD_RECOVERY_MAIL_SENT = "Новый пароль отправлен на почту"


class ErrorMessage:
    REGISTRATION_INVALID_HASH = "Срок действия ссылки истек"
    REGISTRATION_USER_EXISTS = "Пользователь с таким почтовым адресом уже существует"
    REGISTRATION_PASSWORD_NOT_MATCH = "Введенные пароли не совпадают"
    REGISTRATION_BLANK_CREDENTIALS = "Все поля должны быть заполнены"
    LOGIN_BLANK_CREDENTIALS = "Все поля должны быть заполнены"
    LOGIN_EMAIL_BLANK = "Почтовый адрес не может быть пустым"
    LOGIN_PASSWORD_BLANK = "Пароль не может быть пустым"
    LOGIN_AUTHENTICATION_ERROR = "Не верно введена пара логин\пароль"
    LOGIN_USER_IS_NOT_ACTIVE = "Пользователь не активен"
    RECOVERY_NO_SUCH_USER = "Такого пользователя не существует"
