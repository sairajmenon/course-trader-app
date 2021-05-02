from logAndAuth.model.models import User
from logAndAuth.exceptions import UserNameValidationError,EmailDoesNotExist,EmailAndPasswordDoNotMatch,EmailValidationError


from logAndAuth import bcrypt

class Validations:
    def validate_username_email(self,username,email):
        return self.validate_username(username) and self.validate_email(email)
    
    def validate_username(self, username):
        print (username)
        user = User.query.filter_by(username=username).first()
        print (user)
        if user:
            raise UserNameValidationError('That username has already been taken. Please choose another username')
        return True
    
    def validate_email(self, email):
        print (email)
        emailUser = User.query.filter_by(email=email).first()
        print (emailUser)
        if emailUser:
            raise EmailValidationError('That email has already been taken. Please choose another email')
        return True

    def verify_email_exists(self, email):
        emailUser = User.query.filter_by(email=email).first()
        if not emailUser:
            raise EmailDoesNotExist('That email does not exist')
        return True

    def validate_email_password(self,email,password):
        user = User.query.filter_by(email=email).first()
        print (email,user)
        if not user:
            raise EmailDoesNotExist('That email does not exist')
        match = bcrypt.check_password_hash(user.password, password)
        if not match:
            raise EmailAndPasswordDoNotMatch('The email ID and password did not match')
    