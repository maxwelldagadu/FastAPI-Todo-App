from passlib.context import CryptContext


class Hash():

    # hash user pasword
    def hash_passwd(password:str):
        passwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
        hash_passwd = passwd_context.hash(password)
        return hash_passwd
    
    # verify user password

    def verify(user_input:str,password:str):        
        passwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
        verify_passwd = passwd_context.verify(user_input,password)
        return verify_passwd
    
    



    


