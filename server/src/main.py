import sys
from utils.permissions import check_permissions, restore_permissions 
from aiohttp import web
from routes import setup_routes, MessageSingleton

# GUI
import subprocess
import os
import signal
import threading
import asyncio
import tkinter as tk
from tkinter import simpledialog
import queue
import time
import random
from utils.message_singleton import MessageSingleton

# Called on clicking the GUI "Start Server" button. It initializes a 
# ThreadedServer.
def start_server():
    admin_key = tk.simpledialog.askstring("Password", "Permissions must be set, please enter administrator password:", show='*')
    try:
        check_permissions(admin_key)
        new_server.server_init()
    except:
        msg = MessageSingleton('Wrong password, try again.')
    

# Called on clicking the GUI "Quit" button. Kills program via OS call when server is running to guarantee it does not hang. 
def quit_system():
    if new_server.is_running:
        admin_key = tk.simpledialog.askstring("Password", "Permissions must be returned to normal, please enter administrator password:", show='*')
        restore_permissions(admin_key)
        os.kill(os.getpid(),signal.SIGKILL)
    else:
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
routes_message = MessageSingleton('')

# Tkinter GUI setup. The "master" argument is required by Tkinter. The "queue"
# argument is for passing messages from the server (error messages, print
# statements) to be rendered in the GUI. The commented-out code in Gui and
# ThreadedServer classes implements this message passing, but is commented out 
# because it's not yet implemented throughout the server code.
class Gui:
    def __init__(self, master, queue):
        self.queue = queue

        # Logo widget
        T = tk.Text(window, height=20, width=60)
        T.grid(row=0, column=0, columnspan=6)
        T.configure(background="blue", foreground="yellow")
        T.insert(tk.END,logo)
        # Buttons
        b1=tk.Button(window, text="Start Server", width=12, command=start_server)
        b1.grid(row=2, column=0)
        b2=tk.Button(window, text="Quit", width=12, command=quit_system)
        b2.grid(row=1, column=0)
        # Info display
        Info = tk.Text(window, width = 30, height=2)
        Info.grid(row = 1, column =3)
        Info.configure(background="white", foreground="red")
        Info.insert(tk.END,routes_message.val)

    def process_incoming(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                Info = tk.Text(window, width = 30, height=2)
                Info.grid(row = 1, column =3)
                Info.configure(background="white", foreground="red")
                Info.insert(tk.END,msg)
            except queue.Empty:
                pass

# ThreadedServer class that runs AIOHTTP's async server in its own thread.
# More info: https://aiohttp.readthedocs.io/en/stable/web_advanced.html#aiohttp-web-app-runners
class ThreadedServer:
    def __init__(self, runner, master):
        self.runner = runner
        self.master = master
        self.is_running = False
        self.queue = queue.Queue()
        # self.queue_thread = threading.Thread(target=self.worker_thread)
        # self.queue_thread.start()
        self.gui = Gui(self.master, self.queue)
        self.check_queue()

    def check_queue(self):
        self.gui.process_incoming()
        msg = routes_message.val
        self.queue.put(msg)
        self.master.after(300, self.check_queue)

    # def worker_thread(self):
    #     while self.is_running:
    #         time.sleep(10)
    #         msg = routes_message.val
    #         print(msg)
    #         self.queue.put(msg)

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()


    def server_init(self):
        self.is_running = not self.is_running
        new_loop = asyncio.new_event_loop()
        asyncio.run_coroutine_threadsafe(self.async_server(), new_loop)
        threading.Thread(target=self.start_loop, args=(new_loop,)).start()

    async def async_server(self):
        await self.runner.setup()
        print("Runner is set up")
        site = web.TCPSite(self.runner, 'localhost', 8080)
        await site.start()
        print("Site is set up")
        msg = MessageSingleton("server is started, waiting for connection from client")
        self.queue.put(msg.val)


# Main function that sets up the server with either a GUI or CLI. All
# of the functions above are for the GUI.
if __name__ == '__main__':
    try:
        if sys.argv[1] == '--gui':
            app = web.Application()
            setup_routes(app)
            runner = web.AppRunner(app)
            window = tk.Tk()
            window.title("Sea Lion")
            new_server = ThreadedServer(runner, window)
            window.mainloop()
        elif sys.argv[1] == '--cli':
            check_permissions()
            app = web.Application()
            setup_routes(app)
            web.run_app(app)
            restore_permissions()
        else:
            print('Try again with either the "--gui" or "--cli" flag')
    except IndexError as e:
        print('Try again with either the "--gui" or "--cli" flag')
