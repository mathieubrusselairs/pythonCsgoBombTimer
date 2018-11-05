import server
import time
import threading
import tkinter as tk
import math



server = server.MyServer(('localhost', 3000), 'MYTOKENHERE', server.MyRequestHandler)
timerStarted = False
startTime = None
plantTime = None
app = None

print(time.asctime(), '-', 'CS:GO GSI Quick Start server starting')

try:
	t = threading.Thread(target=server.serve_forever)
	t.daemon = True
	t.start()
	# server.serve_forever()

except (KeyboardInterrupt, SystemExit):
	server.server_close()
	pass


print(time.asctime(), '-', 'CS:GO GSI Quick Start server listening!')

def check_bomb_status(server):
	if server.bomb_status != "planted":
		return False
	else:
		return True

class App():
    BOMB_TIME = 39

    def __init__(self, plantTime):
        self.root = tk.Tk()
        self.root.title("BombTimer v.1")
        # get screen width and height
        ws = self.root.winfo_screenwidth() # width of the screen
        hs = self.root.winfo_screenheight() # height of the screen
        w = 800 # width for the Tk root
        h = 650 # height for the Tk root
        self.bomb_timer_label = tk.Label(text="")
        self.bomb_timer_label.pack(side="bottom")

        self.update_clock()
        x = - (ws/2) - (w/2) + 550
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.mainloop()




    def update_clock(self):
        timeLeft = (plantTime + self.BOMB_TIME) - time.time()
        timeLeft = math.ceil(timeLeft*100)/100
        timeLeftStr = "{0:0.1f}".format(timeLeft)

        self.bomb_timer_label.configure(text=timeLeftStr, height=130, fg="cadet blue", font="Helvetica 80 bold italic")
        if timeLeft > 0:
            self.root.after(10, self.update_clock)
            if 4.9 < timeLeft < 9.9:
                self.bomb_timer_label.configure(height=130, fg="medium purple", font="Helvetica 115 bold italic")
            if 0 < timeLeft < 4.9:
                self.bomb_timer_label.configure(height=130, fg="red", font="Helvetica 150 bold italic")
           
            
        else:
            self.root.destroy()

#Check loop
while server:
	while server.bomb_status == "planted":
	# t = threading.Thread(target=check_bomb_status(server)).start()
	# while :
		if plantTime == None:
			plantTime = time.time()
			print("Starting window!")
			# threading.Thread(target=App(plantTime)).start()
			app=App(plantTime)
		print("Closing window!")
		app = None
		plantTime = None

