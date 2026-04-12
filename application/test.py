import emailgetter

emailgetter.init()

otp = emailgetter.getLatestOTP()
if otp:
    print(otp)
else:
    print("a stinky error happened")