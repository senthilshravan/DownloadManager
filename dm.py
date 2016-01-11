import threading
import urllib.request
import threading

parts = [" " for i in range(1, 9, 1)]

class downloader(threading.Thread):
    def __init__(self, num, start, end, link):
        threading.Thread.__init__(self)
        self.num = num
        self.start_bytes = start
        self.end = end
        self.link = link
        self.req = urllib.request.Request(self.link)
        self.req.headers['Range']="bytes=%s-%s"%(self.start_bytes, self.end)


    def run(self):
        global parts
        print("Running ", self.num," thread")
        try:
            sendurl = urllib.request.urlopen(self.req)
            parts[self.num] = sendurl.read()
            # print(parts[self.num])
        except Exception as e:
            print(e)


def threadDownload(link, fileName, filePath, fileSize):
    global parts
    nofchunks = 8
    chunkSize = int(int(fileSize)/nofchunks)
    thread = [None for i in range(0, 8, 1)]

    start = 0
    for i in range(0, 8, 1):
        if(i is 7):
            thread[7] = downloader(7, start, fileSize, link)
            thread[7].start()
            # print(e)
        else:
            thread[i] = downloader(i, start, start+chunkSize, link)
            start = start+chunkSize+1
            thread[i].start()
    for i in range(0, 8, 1):
        thread[i].join()
    for i in range(1, 8, 1):
        # print(parts[i])
        parts[0] += parts[i]
    print("Going to Write")
    f = open("/home/shravan/"+fileName, "wb")
    f.write(parts[0])
    print("Completed")
    f.close()


def Download(conn, fileName, filePath):
    result = conn.read()
    print(fileName)
    f = open("/home/shravan/"+fileName, "wb")
    f.write(result)
    f.close()



def Main():
    link = input("Download Link:")
    fileName = input("FileName with Extension:")
    filePath = ""
    connection = None
    try:
        connection = urllib.request.urlopen(link)
    except Exception as e:
        print(e)
        print("Please Verify the link")
        exit

    headers = connection.headers
    fileSize = headers['Content-Length']
    resumeCap = headers['Accept-Ranges']
    print("Size of the file is" + fileSize)
    if resumeCap == "bytes":
        print("Resume Capability:YES")
        resume = True
    else:
        print("No resume Capability")
        resume = False
    if resume is False:
        Download(connection, fileName, filePath)
    else:
        threadDownload(link, fileName, filePath, fileSize)

if __name__ == '__main__':
    Main()
