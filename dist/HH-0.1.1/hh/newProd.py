from connectToDb import connectToDB
from validators import numOnlyValidator

conn = connectToDB()

import wx
import wx.xrc

class GetData(wx.Dialog):
    def __init__(self, parent, bc):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "New Product", size= (650,360))
        self.panel = wx.Panel(self,wx.ID_ANY)

        self.lblName = wx.StaticText(self.panel, label="Name", pos=(20,20))
        self.name = wx.TextCtrl(self.panel, value="", pos=(110,20), size=(500,-1))
        
        self.lblBarcode = wx.StaticText(self.panel, label="Barcode", pos=(20,60))
        self.barcode = wx.TextCtrl(self.panel, value="", pos=(110,60), size=(500,-1))
        self.barcode.SetValue(str(bc))
        
        self.lblCP = wx.StaticText(self.panel, label="Cost Price", pos=(20,100))
        self.costPrice = wx.TextCtrl(self.panel, value="", pos=(110,100), size=(500,-1), validator=numOnlyValidator())
        
        self.lblSP = wx.StaticText(self.panel, label="Selling Price", pos=(20,140))
        self.sellingPrice = wx.TextCtrl(self.panel, value="", pos=(110,140), size=(500,-1), validator=numOnlyValidator())
        
        self.lblQty = wx.StaticText(self.panel, label="Quantity", pos=(20,180))
        self.qty = wx.TextCtrl(self.panel, value="", pos=(110,180), size=(500,-1), validator=numOnlyValidator())
        
        self.lblmlvl = wx.StaticText(self.panel, label="Minimum Level", pos=(20,220))
        self.minLvl = wx.TextCtrl(self.panel, value="", pos=(110,220), size=(500,-1), validator=numOnlyValidator())
        
        self.lblcdn = wx.StaticText(self.panel, label="Codename", pos=(20,260))
        self.cdn = wx.TextCtrl(self.panel, value="", pos=(110,260), size=(500,-1))
        
        self.saveButton =wx.Button(self.panel, label="Save", pos=(110,300))
        self.closeButton =wx.Button(self.panel, label="Cancel", pos=(250,300))
        
        self.saveButton.Bind(wx.EVT_BUTTON, self.SaveConnString)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
        
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        
        self.Show()	

    def OnQuit(self, event):
        self.result_name = None
        self.Destroy()

    def SaveConnString(self, event):
        name = self.name.GetValue()
        bc = self.barcode.GetValue()
        cp = self.costPrice.GetValue()
        sp = self.sellingPrice.GetValue()
        qty = self.qty.GetValue()
        minLvl = self.minLvl.GetValue()
        cdn = self.cdn.GetValue()
        
        if (name == "" or bc == "" or cp == "" or sp == "" or qty == "" or minLvl == "" or cdn == ""):
                return
        
        
        qry = "INSERT INTO `products` (name, type, costPrice, sellingPrice, minLevel, barcode, codeName) VALUES ('%s', '3', '%s', '%s', '%s', '%s', '%s')" % (name, cp, sp, minLvl, bc, cdn)
        
        conn.cursor().execute(qry)
        
        i = conn.insert_id()
        
        qry = "INSERT INTO `currentinventory` (productId, quantity) VALUES ('%s', '%s')" % (i, qty)
        
        conn.cursor().execute(qry)
        
        conn.commit()
        
        self.Destroy()

