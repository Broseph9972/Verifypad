import emailgetter

emailgetter.init()

success, email = emailgetter.getLatestEmailBody()
if success:
    print(email)
else:
    print("a stinky error happened")