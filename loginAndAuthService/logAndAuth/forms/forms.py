from logAndAuth.model.models import User
from logAndAuth.exceptions import UserNameValidationError,EmailDoesNotExist,EmailAndPasswordDoNotMatch,EmailValidationError


from logAndAuth import bcrypt

class Validations:
    def validate_username_email(self,username,email):
        return self.validate_username(username) and self.validate_email(email)
    
    def validate_username(self, username):
        username = User.query.filter_by(username=username).first()
        if username:
            raise UserNameValidationError('That username has already been taken. Please choose another username')
        return True
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email).first()

        if email:
            raise EmailValidationError('That email has already been taken. Please choose another email')
        return False

    def validate_email_password(self,email,password):
        user = User.query.filter_by(email=email).first()
        if not user:
            raise EmailDoesNotExist('That email does not exist')
        match = bcrypt.check_password_hash(user.password, password)
        if not match:
            raise EmailAndPasswordDoNotMatch('The email ID and password did not match')
    