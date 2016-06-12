import Tkinter as tk
import time
 
class StartFrame(tk.Frame):
    ''' An example application for TkInter.  Instantiate
        and call the run method to run. '''
    def __init__(self, master):
        # Initialize window using the parent's constructor
        tk.Frame.__init__(self, master,width=400,height=400)
        # Set the title

        # This allows the size specification to take effect
        self.pack_propagate(0)
 
        # We'll use the flexible pack layout manager
        self.pack()
        

        self.name_var = tk.StringVar()
        self.name_field = tk.Entry(self,textvariable=self.name_var)
        self.name_var.set('Input Your Name')
        self.name_field.pack()

        self.label1=tk.Label(self,text="slider1:")
        self.label1.pack()

        self.slider1 = tk.Scale( self, from_=-2,to=2,orient=tk.HORIZONTAL)
        self.slider1.pack()

        self.label2=tk.Label(self,text="slider2:")
        self.label2.pack()

        self.slider2 = tk.Scale( self, from_=-2,to=2,orient=tk.HORIZONTAL)
        self.slider2.pack()

        self.label3=tk.Label(self,text="slider3:")
        self.label3.pack()

        self.slider3 = tk.Scale( self, from_=-2,to=2,orient=tk.HORIZONTAL)
        self.slider3.pack()
        
        self.label4=tk.Label(self,text="slider4:")
        self.label4.pack()

        self.slider4 = tk.Scale( self, from_=-2,to=2,orient=tk.HORIZONTAL)
        self.slider4.pack()

        self.label5=tk.Label(self,text="slider5:")
        self.label5.pack()

        self.slider5 = tk.Scale( self, from_=-2,to=2,orient=tk.HORIZONTAL)
        self.slider5.pack()

        self.button = tk.Button(self, text="Start", command=self.print_out)
        self.button.pack()

        self.button2 = tk.Button(self, text="Quit", command=self.close)
        self.button2.pack()
        
    def print_out(self):
        print self.name_var.get()
        print self.slider1.get()
        print self.slider2.get()
        print self.slider3.get()
        print self.slider4.get()
        print self.slider5.get()
        self.destroy()
        pf = PlayFrame(master)
        pf.run()

    def run(self):
        ''' Run the app '''
        self.mainloop()

    def close(self):
        master.destroy()
        
        
class PlayFrame(tk.Frame):
    ''' An example application for TkInter.  Instantiate
        and call the run method to run. '''
    def __init__(self, master):
        # Initialize window using the parent's constructor
        tk.Frame.__init__(self, master,width=400,height=400)
        # Set the title

        # This allows the size specification to take effect
        self.pack_propagate(0)
 
        # We'll use the flexible pack layout manager
        self.pack()
        

        self.label1=tk.Label(self,text="Choose a Play:")
        self.label1.pack()

        self.greeting_var = tk.StringVar()
        self.greeting = tk.OptionMenu(self,self.greeting_var,'King of Comedy')
        self.greeting.pack()

        self.button1 = tk.Button(self, text="Go", command=self.startPlay)
        self.button1.pack()


        self.labelVar = tk.StringVar()
        self.label2=tk.Label(self,textvariable=self.labelVar)
        self.label2.pack()

        self.button2 = tk.Button(self, text="Quit", command=self.close)
        self.button2.pack()
        
    def startPlay(self):
        print self.greeting_var.get()
        
        startTime=time.time()
        i=3
        while i>=0:
            if time.time()-startTime>3-i:
                self.labelVar.set("Start in "+str(i)+" second")
                i-=1
                self.update()

        self.labelVar.set("Go!")

        self.destroy()
        ef = EndFrame(master)
        ef.setScore(100)
        ef.run()

    def run(self):
        ''' Run the app '''
        self.mainloop()

    def close(self):
        master.destroy()

class EndFrame(tk.Frame):
    ''' An example application for TkInter.  Instantiate
        and call the run method to run. '''
    def __init__(self, master):
        # Initialize window using the parent's constructor
        tk.Frame.__init__(self, master,width=400,height=400)
        # Set the title

        # This allows the size specification to take effect
        self.pack_propagate(0)
 
        # We'll use the flexible pack layout manager
        self.pack()

        self.labelVar = tk.StringVar()
        self.label1=tk.Label(self,textvariable=self.labelVar)
        self.labelVar.set("Well Done! Your Score: ")
        self.label1.pack()

        self.button1 = tk.Button(self, text="Restart", command=self.restart)
        self.button1.pack()

        self.button2 = tk.Button(self, text="Quit", command=self.close)
        self.button2.pack()
    
    def setScore(self,score):
        self.labelVar.set("Well Done! Your Score: "+str(score))

    def restart(self):
        self.destroy()
        pf = PlayFrame(master)
        pf.run()

    def run(self):
        ''' Run the app '''
        self.mainloop()

    def close(self):
        master.destroy()

master=tk.Tk()
master.title("Emotionist")
sf = StartFrame(master)
sf.run()