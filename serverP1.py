# Clase User
class User:
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
    
    def __str__(self):
        return "User:" + self.username + " pass:" + self.password + " email:" + self.email

ListUsers = [
    User(id=1, username="usuari1", password="12345", email="prova@gmail.com"),
    User(id=2, username="usuari2", password="123", email="usuari2@gmail.com"),
    User(id=3, username="admin", password="12", email= "admin@proven.cat")
    ]

for u in ListUsers:
    print(u)

class DAOUsers:
    def __init__(self):
        self.users=ListUsers
    
    def getUserbyUsername(self,username):
        for u in self.users:
            if u.username==username:
                return u
        return None
        
daoUser = DAOUsers()

print(daoUser.getUserbyUsername("usuari1"))
u=daoUser.getUserbyUsername("usuari1")

if(u):
    print(u)
else:
    print("No trobat")
