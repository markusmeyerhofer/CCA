import ftplib
import time
import importmodulepd as inp

server = ftplib.FTP()
server.connect('host35.ssl-net.net', 21)
server.login('darksz_top_invest', '29gHl9vZxte8jXwo')

diraddr = "CAINS_PI1"
alist = inp.getlist()

server.cwd(diraddr)

print(alist)

while True:
    x = 0

    while x != len(alist):
        localfile = "D:\\PythonLibary\\pythonProject\\getter\\CAINS\\" + alist[x] + ""
        remotefile = "" + alist[x] + ""

        print("Uploading...")

        with open(localfile, "rb") as file:
            server.storbinary('STOR %s' % remotefile, file)

        file.close()
        print("...Complete")
        x = x + 1
    print("All data online!")
    time.sleep(43200)
