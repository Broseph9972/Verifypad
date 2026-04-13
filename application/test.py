import sys

blue = "\033[34m"
reset = "\033[0m"

if len(sys.argv) > 1:
    test = sys.argv[1]
else:
    print("Please specify a test to run:" + blue + "\npython test.py <test name>" + reset)
    sys.exit()
print(f'Attempting to run test: "{test}"')

if test == "otp":
    print("Running test")
    import emailgetter

    emailgetter.init()

    otp = emailgetter.getLatestOTP()
    if otp:
        print(otp)
    else:
        print("a stinky error happened")

elif test == "link":
    print("Running test")
    import emailgetter

    emailgetter.init()

    link = emailgetter.getLatestLink()
    if link:
        print(link)
    else:
        print("a stinky error happened")

elif test == "paste":
    print("Running test")
    from paste import pasteText
    import time
    time.sleep(3)
    pasteText("yay it works :D")

elif test == "config":
    import config
    print("Config File Check: " + config.checkForConfig)
    print("New config:\n" + config.setConfig())
else:
    print("No such test found")