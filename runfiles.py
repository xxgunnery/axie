import threading
import subprocess

t1 = threading.Thread(target=subprocess.run, args=(["python","axielowest.py"],))
t2 = threading.Thread(target=subprocess.run,args=(["python","axiemarket.py"],))

t1.start()
t2.start()

t1.join()
t2.join()