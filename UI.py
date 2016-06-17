import Tkinter as tk
import time
import numpy as np
import cv2
import pickle
import EmotionPredictor
import EmotionPlotter

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

        self.label1=tk.Label(self,text="Cautious vs. Curious")
        self.label1.pack()

        self.slider1 = tk.Scale( self, from_=-2,to=2,orient=tk.HORIZONTAL)
        self.slider1.pack()

        self.label2=tk.Label(self,text="Organized vs. Careless")
        self.label2.pack()

        self.slider2 = tk.Scale( self, from_=-2,to=2,orient=tk.HORIZONTAL)
        self.slider2.pack()

        self.label3=tk.Label(self,text="Reserved vs. Outgoing")
        self.label3.pack()

        self.slider3 = tk.Scale( self, from_=-2,to=2,orient=tk.HORIZONTAL)
        self.slider3.pack()
        
        self.label4=tk.Label(self,text="Analytical vs. Compassionate")
        self.label4.pack()

        self.slider4 = tk.Scale( self, from_=-2,to=2,orient=tk.HORIZONTAL)
        self.slider4.pack()

        self.label5=tk.Label(self,text="Confident vs. Nervous")
        self.label5.pack()

        self.slider5 = tk.Scale( self, from_=-2,to=2,orient=tk.HORIZONTAL)
        self.slider5.pack()

        self.button = tk.Button(self, text="Start", command=self.start)
        self.button.pack()

        self.button2 = tk.Button(self, text="Quit", command=self.close)
        self.button2.pack()
        
    def start(self):
        print self.name_var.get()
        print self.slider1.get()
        print self.slider2.get()
        print self.slider3.get()
        print self.slider4.get()
        print self.slider5.get()
        personalityMetric=self.personalityConversion(self.slider1.get(),self.slider2.get(),self.slider3.get(),self.slider4.get(),self.slider5.get())
        print personalityMetric
        self.destroy()
        pf = PlayFrame(master,personalityMetric)
        pf.run()

    def run(self):
        ''' Run the app '''
        self.mainloop()

    def close(self):
        master.destroy()

        
        '''
        {0.0:'Neutral',1.0:'Anger',2.0:'Contempt',3.0:'Disgust',4.0:'Fear',5.0:'Happy',6.0:'Sadness',7.0:'Surprise'}
        Big Five Theory:
        Openess:          Cautious vs. Curious             Neutral+ Surprise- Anger- vs. Contempt- Disgust- Surprise+
        Conscientiouness: Organized vs. Careless           Neutral+ vs. Neutral- Happy+ Sadness+
        Extraversion:     Reserved vs. Outgoing            Neutral+ vs. Neutral- Happy+ Surprise+
        Agreeableness:    Analytical vs. Compassionate     Neutral+ Anger+ Contempt+ vs. Neutral- Sadness+ Fear+
        Neuroticism:      Confident vs. Nervous            Happy+ vs. Fear+ Surprise+ Sadness+ Anger+
        '''
    def personalityConversion(self,openess,conscientiouness,extraversion,agreeableness,neuroticism):
        personalityMetric=[0.02,0.07,0.07,0.07,0.07,0.07,0.07,-0.44]
        #openess
        if openess>0:
            #Contempt-
            personalityMetric[2]+=0.07*openess
            for i in range(8):
                if i!=2:
                    personalityMetric[i]-=0.01*openess
            #Disgust-
            personalityMetric[3]+=0.07*openess
            for i in range(8):
                if i!=3:
                    personalityMetric[i]-=0.01*openess
            #Surprise+
            personalityMetric[7]-=0.07*openess
            for i in range(8):
                if i!=7:
                    personalityMetric[i]+=0.01*openess
        else:
            #Neutral+
            personalityMetric[0]-=0.07*(-openess)
            for i in range(8):
                if i!=0:
                    personalityMetric[i]+=0.01*(-openess)
            #Surprise-
            personalityMetric[7]+=0.07*(-openess)
            for i in range(8):
                if i!=7:
                    personalityMetric[i]-=0.01*(-openess)   
            #Anger-
            personalityMetric[1]+=0.07*(-openess)
            for i in range(8):
                if i!=1:
                    personalityMetric[i]-=0.01*(-openess)      

        #conscientiouness    
        if conscientiouness>0:
            #Neutral-
            personalityMetric[0]+=0.07*conscientiouness
            for i in range(8):
                if i!=0:
                    personalityMetric[i]-=0.01*conscientiouness
            #Happy+
            personalityMetric[5]-=0.07*conscientiouness
            for i in range(8):
                if i!=5:
                    personalityMetric[i]+=0.01*conscientiouness
            #Sadness+
            personalityMetric[6]-=0.07*conscientiouness
            for i in range(8):
                if i!=6:
                    personalityMetric[i]+=0.01*conscientiouness
        else:
            #Neutral+
            personalityMetric[0]-=0.07*(-conscientiouness)
            for i in range(8):
                if i!=0:
                    personalityMetric[i]+=0.01*(-conscientiouness)

        #extraversion
        if extraversion>0:
            #Neutral-
            personalityMetric[0]+=0.07*extraversion
            for i in range(8):
                if i!=0:
                    personalityMetric[i]-=0.01*extraversion
            #Happy+
            personalityMetric[5]-=0.07*extraversion
            for i in range(8):
                if i!=5:
                    personalityMetric[i]+=0.01*extraversion
            #Surprise+
            personalityMetric[7]-=0.07*extraversion
            for i in range(8):
                if i!=7:
                    personalityMetric[i]+=0.01*extraversion
        else:
            #Neutral+
            personalityMetric[0]-=0.07*(-extraversion)
            for i in range(8):
                if i!=0:
                    personalityMetric[i]+=0.01*(-extraversion)

        #agreeableness
        if agreeableness>0:
            #Neutral-
            personalityMetric[0]+=0.07*agreeableness
            for i in range(8):
                if i!=0:
                    personalityMetric[i]-=0.01*agreeableness
            #Fear+
            personalityMetric[4]-=0.07*agreeableness
            for i in range(8):
                if i!=4:
                    personalityMetric[i]+=0.01*agreeableness
            #Sadness+
            personalityMetric[6]-=0.07*agreeableness
            for i in range(8):
                if i!=6:
                    personalityMetric[i]+=0.01*agreeableness
        else:
            #Neutral+
            personalityMetric[0]-=0.07*(-agreeableness)
            for i in range(8):
                if i!=0:
                    personalityMetric[i]+=0.01*(-agreeableness)           
            #Anger+
            personalityMetric[1]-=0.07*(-agreeableness)
            for i in range(8):
                if i!=1:
                    personalityMetric[i]+=0.01*(-agreeableness)
            #Contemt+
            personalityMetric[2]-=0.07*(-agreeableness)
            for i in range(8):
                if i!=2:
                    personalityMetric[i]+=0.01*(-agreeableness)  

        #neuroticism
        if neuroticism>0:
            #Fear+
            personalityMetric[4]-=0.07*neuroticism
            for i in range(8):
                if i!=4:
                    personalityMetric[i]+=0.01*neuroticism 
            #Surprise+
            personalityMetric[7]-=0.07*neuroticism
            for i in range(8):
                if i!=7:
                    personalityMetric[i]+=0.01*neuroticism 
            #Sadness+
            personalityMetric[6]-=0.07*neuroticism
            for i in range(8):
                if i!=6:
                    personalityMetric[i]+=0.01*neuroticism 
            #Anger+
            personalityMetric[1]-=0.07*neuroticism
            for i in range(8):
                if i!=1:
                    personalityMetric[i]+=0.01*neuroticism 
        else:
            #Happy+
            personalityMetric[5]-=0.07*(-neuroticism)
            for i in range(8):
                if i!=5:
                    personalityMetric[i]+=0.01*(-neuroticism) 

        return personalityMetric


class PlayFrame(tk.Frame):
    ''' An example application for TkInter.  Instantiate
        and call the run method to run. '''
    def __init__(self, master,personalityMetric):
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
    
        self.button3 = tk.Button(self, text="Free Try", command=self.freeTry)
        self.button3.pack()
        
        with open('classifier/trainingDataCK.pkl', 'rb') as input:
            self.data = pickle.load(input)
            self.label = pickle.load(input)
            self.featureMeans = pickle.load(input)
            self.featureVariance = pickle.load(input)

        with open('classifier/svmCK.pkl', 'rb') as input:
            self.clf = pickle.load(input)

        self.emotionPredictor=EmotionPredictor.EmotionPredictor()
        self.emotionPlotter=EmotionPlotter.EmotionPlotter()
        #self.standardMetric=[0.04,0.06,0.06,0.06,0.06,0.06,0.06,-0.40]
        self.personalityMetric=personalityMetric

        self.captions=[{1.0:"Your wife is in her labour"},
        {4.0:"You son was born"},
        {7.0:"Your wife is dead"},
        {10.0:"Got a genuis son calling papa at birth"},
        {13:"Win lottery"},
        {16:"The first prize"},
        {19:"Your genuis son is dead"},
        {22:"End"}]

    def startPlay(self):
        print self.greeting_var.get()
        
        startTime_=time.time()
        i=3
        while i>=0:
            if time.time()-startTime_>3-i:
                self.labelVar.set("Start in "+str(i)+" second")
                i-=1
                self.update()

        self.labelVar.set("Go!")
        
        self.plotBuffer=self.emotionPredictor.startPredictionFromCamera(self.clf,self.featureMeans,self.featureVariance,self.personalityMetric,24,self.captions)
        
        '''size=50
        standard=[]
        for i in range(8):
        	temp=[0.25]*size
        	standard.append(temp)'''

        standard=[
        [0.125,0.125,0.125,0.05,0.05,0.05,0.05,0.05,0.05,0.10,0.10,0.10,0.10,0.10,0.10 ,0.00,0.00,0.00,0.00,0.00,0.00, 0.00,0.00,0.00,0.00,0.00,0.00,0.20,0.20,0.20,0.20,0.20,0.20,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.125,0.125,0.125,0.125,0.125],
        [0.125,0.125,0.125,0.30,0.30,0.30,0.30,0.30,0.30,0.00,0.00,0.00,0.00,0.00,0.00 ,0.10,0.10,0.10,0.10,0.10,0.10, 0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.10,0.10,0.10,0.10,0.10,0.10,0.125,0.125,0.125,0.125,0.125],
        [0.125,0.125,0.125,0.05,0.05,0.05,0.05,0.05,0.05,0.00,0.00,0.00,0.00,0.00,0.00 ,0.00,0.00,0.00,0.00,0.00,0.00, 0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.125,0.125,0.125,0.125,0.125],
        [0.125,0.125,0.125,0.05,0.05,0.05,0.05,0.05,0.05,0.00,0.00,0.00,0.00,0.00,0.00 ,0.00,0.00,0.00,0.00,0.00,0.00, 0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.125,0.125,0.125,0.125,0.125],
        [0.125,0.125,0.125,0.05,0.05,0.05,0.05,0.05,0.05,0.00,0.00,0.00,0.00,0.00,0.00 ,0.50,0.50,0.50,0.50,0.50,0.50, 0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.50,0.50,0.50,0.50,0.50,0.50,0.125,0.125,0.125,0.125,0.125],
        [0.125,0.125,0.125,0.40,0.40,0.40,0.40,0.40,0.40,0.50,0.50,0.50,0.50,0.50,0.50 ,0.00,0.00,0.00,0.00,0.00,0.00, 0.20,0.20,0.20,0.20,0.20,0.20,0.40,0.40,0.40,0.40,0.40,0.40,0.50,0.50,0.50,0.50,0.50,0.50,0.00,0.00,0.00,0.00,0.00,0.00,0.125,0.125,0.125,0.125,0.125],
        [0.125,0.125,0.125,0.05,0.05,0.05,0.05,0.05,0.05,0.00,0.00,0.00,0.00,0.00,0.00 ,0.40,0.40,0.40,0.40,0.40,0.40, 0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.40,0.40,0.40,0.40,0.40,0.40,0.125,0.125,0.125,0.125,0.125],
        [0.125,0.125,0.125,0.05,0.05,0.05,0.05,0.05,0.05,0.40,0.40,0.40,0.40,0.40,0.40 ,0.00,0.00,0.00,0.00,0.00,0.00, 0.80,0.80,0.80,0.80,0.80,0.80,0.40,0.40,0.40,0.40,0.40,0.40,0.50,0.50,0.50,0.50,0.50,0.50,0.00,0.00,0.00,0.00,0.00,0.00,0.125,0.125,0.125,0.125,0.125]]

        print len(self.plotBuffer[0])
        #self.emotionPlotter.plotEmotions(self.plotBuffer)
        score,_=self.emotionPredictor.computeSimilarityToStandardEmotion(self.plotBuffer,standard)

        self.destroy()
        ef = EndFrame(master,self.personalityMetric)
        ef.setScore(score)
        ef.run()
        
        

    def freeTry(self):
        self.plotBuffer=self.emotionPredictor.startPredictionFromCamera(self.clf,self.featureMeans,self.featureVariance,self.personalityMetric,1000,[])
        
        self.emotionPlotter.plotEmotions(self.plotBuffer)

    def run(self):
        ''' Run the app '''
        self.mainloop()

    def close(self):
        master.destroy()

class EndFrame(tk.Frame):
    ''' An example application for TkInter.  Instantiate
        and call the run method to run. '''
    def __init__(self, master,personalityMetric):
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
        self.personalityMetric=personalityMetric
    
    def setScore(self,score):
        self.labelVar.set("Well Done! Your Score: "+str(score))

    def restart(self):
        self.destroy()
        pf = PlayFrame(master,self.personalityMetric)
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