class SuccessMessage:
    REGISTRATION_MAIL_SEND = "На почту отправлена ссылка для подтверждения регистрации"
    REGISTRATION_SUCCESS = "Вы успешно зарегистрировались"


class ErrorMessage:
    REGISTRATION_INVALID_HASH = "Ссылка не валидна"
    REGISTRATION_USER_EXISTS = "Пользователь с таким почтовым адресом уже существует"
    LOGIN_EMAIL_NULL = "Вы не указали почтовый адрес"
    LOGIN_PASSWORD_NULL = "Вы не указали пароль"
    LOGIN_NO_SUCH_USER = "Ошибка авторизации"
