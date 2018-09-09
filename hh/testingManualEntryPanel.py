from connectToDb import connectToDB

import wx
import wx.xrc
import wx.grid
import wx.adv
import re

import gLedgerFunctions as af
from validators import numOnlyValidator

conn = connectToDB()


class GetData(wx.Dialog):
    def __init__(self, parent):

        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Manual Entry", size=(650, 600))
        self.panel = wx.Panel(self, wx.ID_ANY)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.folios = self.fetchFolios()

        self.lblFolioD = wx.StaticText(self.panel, label="Folio (Debit)")
        self.folioComboD = wx.ComboBox(self.panel, choices=list(self.folios.keys()))

        self.mainSizer.Add(self.lblFolioD)
        self.mainSizer.Add(self.folioComboD)

        self.SetSizer(self.mainSizer)
        self.Layout()
        self.mainSizer.Fit(self.panel)
        self.Centre(wx.BOTH)

        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        self.Show()


    def transformHOAtoName(self, desc):
        x = re.search("(?<=Customer)[0-9]*", desc)
        if x is not None:
            q = 'SELECT name FROM customer WHERE id = %s' % (x.group(0))
            c = conn.cursor()
            c.execute(q)
            cust = c.fetchone()
            return cust['name'] + " A/C Recievable"

        x = re.search("(?<=Supplier)[0-9]*", desc)
        if x is not None:
            q = 'SELECT name FROM supplier WHERE id = %s' % (x.group(0))
            c = conn.cursor()
            c.execute(q)
            cust = c.fetchone()
            return cust['name'] + " A/C Payable"
        return None

    def fetchFolios(self):
        qry = 'SELECT id, description FROM headOfAccounts'
        curs = conn.cursor()
        curs.execute(qry)
        r = curs.fetchall()

        folios = {}
        for x in r:
            z = self.transformHOAtoName(x['description'])
            if z is not None:
                folios.update({z: x['id']})
            else:
                folios.update({x['description']: x['id']})
        return folios

    def OnQuit(self, event):
        self.result_name = None
        self.Destroy()

    def SaveConnString(self, event):
        # hoa = self.m_folioCombo.GetValue()
        hoaCredit = self.folios[self.folioComboD.GetValue()]
        hoaDebit = self.folios[self.folioComboC.GetValue()]
        tran = self.transaction.GetValue()
        cheque = self.chequeNo.GetValue()
        amount = self.amount.GetValue()

        if (hoaCredit != "" and hoaDebit != "" and amount != ""):
            af.manualEntry(hoaCredit, hoaDebit, tran, cheque, amount)

        self.Destroy()

