from testPY import db, Token


if __name__ == '__main__':
    db.connect()
    db.create_tables([Token])
