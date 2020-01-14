import server
import time
import threading
import tkinter as tk
import math



server = server.MyServer(('localhost', 3033), 'MYTOKENHERE', server.MyRequestHandler)
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

        self.bomb_timer_label = tk.Label(text="", bg="white")
        self.bomb_timer_label.pack(side="bottom")

        self.update_clock()
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-disabled", True)
        self.root.wm_attributes("-transparentcolor", "white")
        
        
        self.root.geometry("100x100+1200+-30")
        self.root.lift()
        self.root.mainloop()




    def update_clock(self):
        timeLeft = (plantTime + self.BOMB_TIME) - time.time()
        timeLeft = math.ceil(timeLeft*100)/100
        timeLeftStr = "{0:0.1f}".format(timeLeft)

        self.bomb_timer_label.configure(text=timeLeftStr, height=100, fg="cadet blue", font="Helvetica 45 bold italic")
        if timeLeft > 0:
            self.root.after(10, self.update_clock)
            if 4.9 < timeLeft < 9.9:
                self.bomb_timer_label.configure(height=100, fg="medium purple", font="Helvetica 45 bold italic")
            if 0 < timeLeft < 4.9:
                self.bomb_timer_label.configure(height=100, fg="red", font="Helvetica 45 bold italic")
           
            
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

