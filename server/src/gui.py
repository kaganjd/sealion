import time
import threading
import random
import queue
from tkinter import *
import tkinter.simpledialog
from permissions import *
import asyncio

def server_start():
    client.has_server_started = 1
    admin_key = tkinter.simpledialog.askstring("Password", "Permissions must be set, please enter administrator password:", show='*')
    check_permissions(admin_key)
    client.running = 1
    client.thread1.start()

def quit_system():
    if client.has_server_started:
        admin_key = tkinter.simpledialog.askstring("Password", "Permissions must be returned to normal, please enter administrator password:", show='*')
        restore_permissions(admin_key)
        os.kill(os.getpid(),signal.SIGKILL)
    else:
        import sys
        sys.exit(1)
    

logo='''
                 ___________                 oo
                / __/ __/ _ |             = "  $==
               _\ \/ _// __ |             " o   $
              /___/___/_/_|_|_  _  __    "      $
                / /  /  _/ __ \/ |/ /   $      $$ 
               / /___/ // /_/ /    /    o"     "$o 
   $oo        /____/___/\____/_/|_/     $     "$$$
   $"$oo  the friendly packet sniffer  "      "o$$ 
  "$$o$"o"o        "ARP ARP"         o"      $"$$$
     """o"$o"""""""" """ oo ooooooo"""     o""o$$$
          "$$ o                            o""$$$
    oooo$$$$$$$$oo"o o                 o "o "o ""oo
   "$$$$$$"         ""$$o$o$ $ "ooo$o$o$$$$$$"$o$o$
   "$""                 """"$$$$$o$$$$$$$$$     "$o$$o
   "                           " "" "  "$$$$       " $o
                                         "$$$         ""
                                           ""$
'''    

class GuiPart:
    def __init__(self, master, queue, endCommand):
        self.queue = queue
        # Set up the GUI

        #logo widget
        T = Text(window, height=20, width=60)
        T.grid(row=0, column=0, columnspan=6)
        T.configure(background="blue", foreground="yellow")
        T.insert(END,logo)

        b1=Button(window,text="Start Server", width=12, command=server_start)
        b1.grid(row=2, column=0)
        b2=Button(window,text="Quit", width=12, command=quit_system)
        b2.grid(row=1, column=0)

        # window.mainloop()


        # Add more GUI stuff here depending on your specific needs

    def processIncoming(self):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize(  ):
            try:
                msg = self.queue.get(0)
                # Check contents of message and do whatever is needed. As a
                # simple test, print it (in real life, you would
                # suitably update the GUI's display in a richer fashion).
                print(msg)
            except queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master

        # Create the queue
        self.queue = queue.Queue(  )

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 0
        self.has_server_started = 0
        self.thread1 = threading.Thread(target=self.workerThread1)
        # self.thread1.start(  )

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall(  )

    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.processIncoming(  )
        # if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            # import sys
            # sys.exit(1)
        self.master.after(200, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        app = web.Application()
        # web.run_app(app)
        setup_routes(app)
        handler = app.make_handler()
        print("handler is set up")
        server = loop.create_server(handler, host='localhost', port=8080)
        print("server is running")
        loop.run_until_complete(server)
        loop.run_forever()

    def endApplication(self):
        quit_system()


window = Tk(  )
window.title("SeaLion Sniffer Server")
client = ThreadedClient(window)
window.mainloop(  )