from models import db, Token, Persons

if __name__ == '__main__':
    db.connect()
    db.create_tables([Token])
    db.create_tables([Persons])
