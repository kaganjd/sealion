import sys
from aiohttp import web
from routes import setup_routes
from permissions import *

# GUI
import threading
from tkinter import *
import tkinter.simpledialog
from permissions import *
import asyncio

def server_start():
    admin_key = tkinter.simpledialog.askstring("Password", "Permissions must be set, please enter administrator password:", show='*')
    check_permissions(admin_key)
    new_server.server_init()

def quit_system():
    if _Server.has_started:
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

class GUI:
    def __init__(self, master):
        # Logo widget
        T = Text(window, height=20, width=60)
        T.grid(row=0, column=0, columnspan=6)
        T.configure(background="blue", foreground="yellow")
        T.insert(END,logo)

        b1=Button(window,text="Start Server", width=12, command=server_start)
        b1.grid(row=2, column=0)
        b2=Button(window,text="Quit", width=12, command=quit_system)
        b2.grid(row=1, column=0)

class _Server:
    def __init__(self, runner):
        self.has_started = False
        self.runner = runner

    def toggle(self):
        type(self).has_started = True

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def server_init(self):
        self.toggle()
        new_loop = asyncio.new_event_loop()
        asyncio.run_coroutine_threadsafe(self.async_server(), new_loop)
        threading.Thread(target=self.start_loop, args=(new_loop,)).start()

    async def async_server(self):
        await self.runner.setup()
        print("Runner is set up")
        site = web.TCPSite(self.runner, 'localhost', 8080)
        await site.start()
        print("Site is set up")

if __name__ == '__main__':
    if sys.argv[1] == '--gui':
      app = web.Application()
      setup_routes(app)
      runner = web.AppRunner(app)
      new_server = _Server(runner)

      window = Tk()
      window.title("SeaLion Sniffer Server")
      main_ui = GUI(window)
      window.mainloop()
    elif sys.argv[1] == '--cli':
      check_permissions()
      app = web.Application()
      setup_routes(app)
      web.run_app(app)
      restore_permissions()
    else: 
      echo('Set the --gui or --cli flag')
