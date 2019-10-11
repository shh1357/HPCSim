'''
Created on 2015/07/28

@author: smallcat
'''

# import the wxPython GUI package
import wx
#from win32print import ScheduleJob
#import Main

xxxx = 5
yyyy = 5
schedule = "FIFO"
mode = "normal"
# topo = "grid"
topo = "3-torus"
fso_r = 1.0
speedup = "no"
backfilling = "no"
arch = "RS"
fso_cpu_ssdgpu = 0
mapping_policy = "diameter-based"
num_jobs = 0

# Create a new frame class, derived from the wxPython Frame.
class MyFrame(wx.Frame):
    
    def __init__(self, parent, id, title):
        # First, call the base class' __init__ method to create the frame
        wx.Frame.__init__(self, parent, id, title)
        
        # Associate some events with methods of this class
#         self.Bind(wx.EVT_SIZE, self.OnSize)
#         self.Bind(wx.EVT_MOVE, self.OnMove)

        # Add a panel and some controls to display the size and position
        panel = wx.Panel(self, -1)
        
#         blankline = wx.StaticText(self, -1, '')
        label7 = wx.StaticText(panel, -1, "architecture: ")
        label6 = wx.StaticText(panel, -1, "speedup: ")
        label4 = wx.StaticText(panel, -1, "topology: ")
        label1 = wx.StaticText(panel, -1, "side length of a grid: ")
        label2 = wx.StaticText(panel, -1, "scheduling: ")
        label3 = wx.StaticText(panel, -1, "Mode: ")
        self.sizeCtrl = wx.TextCtrl(panel, -1, "5")
#         self.posCtrl = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
        label5 = wx.StaticText(panel, -1, "(FSO_random) percent (%) of fso links: ")
        self.fso_ratio = wx.TextCtrl(panel, -1, "100")
        
        label8 = wx.StaticText(panel, -1, "(IRS-REPEAT) fso terminals per node (cpu-ssd/gpu): ")
        self.cpu_ssdgpu = wx.TextCtrl(panel, -1, "0")  
        
        label9 = wx.StaticText(panel, -1, "(random_contiguous_loose) mapping policy: ")      
        
        label10 = wx.StaticText(panel, -1, "(default all) number of jobs: ")   
        self.jobs = wx.TextCtrl(panel, -1, "0") 

        button_set = wx.Button(panel, 1, "Set")
        self.Bind(wx.EVT_BUTTON, self.OnSet, id=1)
        
        radio1 = wx.RadioButton(panel, -1, "FIFO", style=wx.RB_GROUP)  
        radio4 = wx.RadioButton(panel, -1, "LIFO")
        radio2 = wx.RadioButton(panel, -1, "BF")
        radio3 = wx.RadioButton(panel, -1, "SF")
        radio5 = wx.RadioButton(panel, -1, "RLF")
        radio6 = wx.RadioButton(panel, -1, "RSF")        
        for eachRadio in [radio1, radio2, radio3, radio4, radio5, radio6]: 
            self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio, eachRadio)
            
        radio01 = wx.RadioButton(panel, 1, "normal", style=wx.RB_GROUP)  
        radio02 = wx.RadioButton(panel, 1, "FSO")
        radio03 = wx.RadioButton(panel, 1, "FSO_random")
        radio04 = wx.RadioButton(panel, 1, "random_contiguous")
        radio05 = wx.RadioButton(panel, 1, "random_non_contiguous") 
        radio06 = wx.RadioButton(panel, 1, "disaggregate_contiguous")  
        radio07 = wx.RadioButton(panel, 1, "random_contiguous_loose")              
        for eachRadio in [radio01, radio02, radio03, radio04, radio05, radio06, radio07]: 
            self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio0, eachRadio)
            
#151222         radio001 = wx.RadioButton(panel, 2, "grid", style=wx.RB_GROUP)  
        radio002 = wx.RadioButton(panel, 2, "3-torus", style=wx.RB_GROUP)
#         radio003 = wx.RadioButton(panel, 2, "3-torus")
        radio004 = wx.RadioButton(panel, 2, "4-torus")
        radio005 = wx.RadioButton(panel, 2, "5-torus")
        radio006 = wx.RadioButton(panel, 2, "random")
        radio007 = wx.RadioButton(panel, 2, "random-regular")
        radio008 = wx.RadioButton(panel, 2, "edge-list")
#         for eachRadio in [radio002, radio003, radio004, radio005]: 
#             self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio00, eachRadio)
#160908         radio003 = wx.RadioButton(panel, 2, "fat-tree")
        for eachRadio in [radio002, radio004, radio005, radio006, radio007, radio008]: 
            self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio00, eachRadio)
            
        radio0001 = wx.RadioButton(panel, 3, "no", style=wx.RB_GROUP)
        radio0002 = wx.RadioButton(panel, 3, "yes")
        radio0003 = wx.RadioButton(panel, 3, "tor")
        radio0004 = wx.RadioButton(panel, 3, "tor-sub3d")
        radio0005 = wx.RadioButton(panel, 3, "sub2dmesh")
        radio0006 = wx.RadioButton(panel, 3, "sub3dmesh")
        radio0007 = wx.RadioButton(panel, 3, "sub3dtorus")
        radio0008 = wx.RadioButton(panel, 3, "subrandom")        
        for eachRadio in [radio0001,radio0002, radio0003, radio0004, radio0005, radio0006, radio0007, radio0008]: 
            self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio000, eachRadio)            

        radio00001 = wx.RadioButton(panel, 4, "RS", style=wx.RB_GROUP)
        radio00002 = wx.RadioButton(panel, 4, "IRS-REPEAT")
        radio00003 = wx.RadioButton(panel, 4, "IRS-LOOP")
        for eachRadio in [radio00001, radio00002, radio00003]: 
            self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio0000, eachRadio)  

        radio000001 = wx.RadioButton(panel, 5, "diameter-based", style=wx.RB_GROUP)
        radio000002 = wx.RadioButton(panel, 5, "aspl-based")
        for eachRadio in [radio000001, radio000002]: 
            self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio00000, eachRadio)  

        self.panel = panel

        # Use some sizers for layout of the widgets
        #sizer = wx.FlexGridSizer(2, 2, 5, 5)
        
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer7 = wx.BoxSizer(wx.HORIZONTAL)        
        sizer8 = wx.BoxSizer(wx.HORIZONTAL) 
        sizer9 = wx.BoxSizer(wx.HORIZONTAL)    
        sizer10 = wx.BoxSizer(wx.HORIZONTAL)             
        
        sizer=wx.BoxSizer(wx.VERTICAL)   

        sizer0.Add(label1, 0, wx.ALL|wx.EXPAND, 5)
        sizer0.Add(self.sizeCtrl, 0, wx.ALL|wx.EXPAND, 5)
#151222         sizer.Add(wx.StaticText(self, -1, ''), 0, wx.ALL, 5)
        
        sizer1.Add(label4, 0, wx.ALL|wx.EXPAND, 5)
#151222         sizer.Add(radio001, 0, wx.ALL|wx.EXPAND, 5)
        sizer1.Add(radio002, 0, wx.ALL|wx.EXPAND, 5)
#160908         sizer.Add(radio003, 0, wx.ALL|wx.EXPAND, 5)
        sizer1.Add(radio004, 0, wx.ALL|wx.EXPAND, 5)
        sizer1.Add(radio005, 0, wx.ALL|wx.EXPAND, 5)
        sizer1.Add(radio006, 0, wx.ALL|wx.EXPAND, 5)
        sizer1.Add(radio007, 0, wx.ALL|wx.EXPAND, 5)
        sizer1.Add(radio008, 0, wx.ALL|wx.EXPAND, 5)
        #sizer1.Add(wx.StaticText(self, -1, ''), 0, wx.ALL, 5)

        sizer2.Add(label7, 0, wx.ALL|wx.EXPAND, 5)
        sizer2.Add(radio00001, 0, wx.ALL|wx.EXPAND, 5)
        sizer2.Add(radio00002, 0, wx.ALL|wx.EXPAND, 5)
        sizer2.Add(radio00003, 0, wx.ALL|wx.EXPAND, 5)
        #sizer2.Add(wx.StaticText(self, -1, ''), 0, wx.ALL, 5)
        
        sizer3.Add(label2, 0, wx.ALL|wx.EXPAND, 5)
        sizer3.Add(radio1, 0, wx.ALL|wx.EXPAND, 5)
        sizer3.Add(radio4, 0, wx.ALL|wx.EXPAND, 5)
        sizer3.Add(radio2, 0, wx.ALL|wx.EXPAND, 5)
        sizer3.Add(radio3, 0, wx.ALL|wx.EXPAND, 5)
        sizer3.Add(radio5, 0, wx.ALL|wx.EXPAND, 5)
        sizer3.Add(radio6, 0, wx.ALL|wx.EXPAND, 5)        
        #sizer3.Add(wx.StaticText(self, -1, ''), 0, wx.ALL, 5)
        
        sizer4.Add(label6, 0, wx.ALL|wx.EXPAND, 5)
        sizer4.Add(radio0001, 0, wx.ALL|wx.EXPAND, 5)
        sizer4.Add(radio0002, 0, wx.ALL|wx.EXPAND, 5)   
        sizer4.Add(radio0003, 0, wx.ALL|wx.EXPAND, 5) 
        sizer4.Add(radio0004, 0, wx.ALL|wx.EXPAND, 5) 
        sizer4.Add(radio0005, 0, wx.ALL|wx.EXPAND, 5) 
        sizer4.Add(radio0006, 0, wx.ALL|wx.EXPAND, 5)   
        sizer4.Add(radio0007, 0, wx.ALL|wx.EXPAND, 5) 
        sizer4.Add(radio0008, 0, wx.ALL|wx.EXPAND, 5)               
        #sizer4.Add(wx.StaticText(self, -1, ''), 0, wx.ALL, 5)    
         
        sizer5.Add(label3, 0, wx.ALL|wx.EXPAND, 5)
        sizer5.Add(radio01, 0, wx.ALL|wx.EXPAND, 5)
        sizer5.Add(radio02, 0, wx.ALL|wx.EXPAND, 5)
        sizer5.Add(radio03, 0, wx.ALL|wx.EXPAND, 5)
        sizer5.Add(radio04, 0, wx.ALL|wx.EXPAND, 5)
        sizer5.Add(radio05, 0, wx.ALL|wx.EXPAND, 5)
        sizer5.Add(radio06, 0, wx.ALL|wx.EXPAND, 5)
        sizer5.Add(radio07, 0, wx.ALL|wx.EXPAND, 5)
        #sizer5.Add(wx.StaticText(self, -1, ''), 0, wx.ALL, 5)    
        
        sizer6.Add(label5, 0, wx.ALL|wx.EXPAND, 5)
        sizer6.Add(self.fso_ratio, 0, wx.ALL|wx.EXPAND, 5)
        
        sizer7.Add(label8, 0, wx.ALL|wx.EXPAND, 5)
        sizer7.Add(self.cpu_ssdgpu, 0, wx.ALL|wx.EXPAND, 5) 
        
        sizer9.Add(label9, 0, wx.ALL|wx.EXPAND, 5)
        sizer9.Add(radio000001, 0, wx.ALL|wx.EXPAND, 5)
        sizer9.Add(radio000002, 0, wx.ALL|wx.EXPAND, 5)                

        sizer10.Add(label10, 0, wx.ALL|wx.EXPAND, 5)  
        sizer10.Add(self.jobs, 0, wx.ALL|wx.EXPAND, 5) 
            
        sizer8.Add(button_set, 0, wx.ALL|wx.EXPAND, 5)    
        
        sizer.Add(sizer0, 0, wx.ALL|wx.EXPAND, 5) 
        sizer.Add(sizer1, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(sizer2, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(sizer3, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(sizer4, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(sizer5, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(sizer6, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(sizer7, 0, wx.ALL|wx.EXPAND, 5)        
        sizer.Add(sizer9, 0, wx.ALL|wx.EXPAND, 5) 
        sizer.Add(sizer10, 0, wx.ALL|wx.EXPAND, 5) 
        sizer.Add(sizer8, 0, wx.ALL|wx.EXPAND, 5) 

#         panel.SetAutoLayout(True)
        panel.SetSizerAndFit(sizer)
#         panel.SetSizer(sizer)
        self.Fit()
        


    # This method is called by the System when the window is resized,
    # because of the association above.
#     def OnSize(self, event):
#         size = event.GetSize()
#         self.sizeCtrl.SetValue("%s, %s" % (size.width, size.height))
# 
#         # tell the event system to continue looking for an event handler,
#         # so the default handler will get called.
#         event.Skip()

    # This method is called by the System when the window is moved,
    # because of the association above.
#     def OnMove(self, event):
#         pos = event.GetPosition()
#         self.posCtrl.SetValue("%s, %s" % (pos.x, pos.y))

    def OnSet(self, event):
        global xxxx, yyyy, fso_r, fso_cpu_ssdgpu, num_jobs
        xxxx = int(self.sizeCtrl.GetValue())
        yyyy = int(self.sizeCtrl.GetValue())
        fso_r = int(self.fso_ratio.GetValue())/100.0
        fso_cpu_ssdgpu = int(self.cpu_ssdgpu.GetValue())
        num_jobs = int(self.jobs.GetValue())
        self.Close()
        
        
    def OnRadio(self, event):  
        global schedule
        radioSelected = event.GetEventObject()  
        schedule = radioSelected.GetLabel()   


    def OnRadio0(self, event):  
        global mode
        radioSelected = event.GetEventObject()  
        mode = radioSelected.GetLabel() 
        
    def OnRadio00(self, event):  
        global topo
        radioSelected = event.GetEventObject()  
        topo = radioSelected.GetLabel() 
        
    def OnRadio000(self, event):  
        global speedup
        radioSelected = event.GetEventObject()  
        speedup = radioSelected.GetLabel() 

    def OnRadio0000(self, event):  
        global arch
        radioSelected = event.GetEventObject()  
        arch = radioSelected.GetLabel() 

    def OnRadio00000(self, event):  
        global mapping_policy
        radioSelected = event.GetEventObject()  
        mapping_policy = radioSelected.GetLabel() 

# Every wxWidgets application must have a class derived from wx.App
class MyApp(wx.App):

    # wxWindows calls this method to initialize the application
    def OnInit(self):

        # Create an instance of our customized Frame class
        frame = MyFrame(None, -1, "Job Scheduler")
        frame.Center()
        frame.Show(True)

        # Tell wxWindows that this is our main window
        #self.SetTopWindow(frame)

        # Return a success flag
        return True



# app = MyApp(0)     # Create an instance of the application class
# app.MainLoop()     # Tell it to start processing events
