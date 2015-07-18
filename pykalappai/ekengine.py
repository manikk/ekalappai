# -*- coding: utf-8 -*-
__author__ = 'manikk'
import pythoncom
import pyHook
import winpipe
from parse_scim_table import ScimTableParser

class EKEngine:
    charPressed = ""
    charsToSend = ""
    prevCharToDelete = ""
    prevUnicodeCharLength = 0
    scimMapping = {}
    scimMappingReversed = {}
    validChars = []

    def onKeyboardEvent(self,event):
        char =  chr(event.Ascii)
        if char in self.validChars:
            self.charPressed += char
        elif char == " ":
            self.charPressed += char
        elif char == 8:
            pass
        else:
            return True

        try:
            if char == 8:
                self.charPressed = self.charPressed[:-1]

            if len(self.charPressed) > 20 :
                self.charPressed = self.charPressed[-20:]

            for i in range(-5,0):
                chars = self.charPressed[i:]
                if chars in self.scimMapping:
                    self.charsToSend = self.scimMapping[chars]
                    if chars[:-1] in self.scimMapping :
                        self.prevCharToDelete = self.scimMapping[chars[:-1]]
                    else:
                        self.prevCharToDelete = ""
                    self.prevUnicodeCharLength = len(self.prevCharToDelete)
                    break
                elif i == -1:
                    return True

            if self.prevUnicodeCharLength > 0 and len(self.charsToSend) > 0 :
                for i in range(0, self.prevUnicodeCharLength):
                    winpipe.SendBackSpace()

            if self.charsToSend :
                for i in self.charsToSend:
                    winpipe.SendKeyPress(i)
                self.charsToSend = ""

            return False

        except KeyError as e:
            return True
            # print ('MessageName:',event.MessageName)
            # print ('Message:',event.Message)
            # print ('Time:',event.Time)
            # print ('Window:',event.Window)
            # print ('WindowName:',event.WindowName)
            # print ('Ascii:', event.Ascii, chr(event.Ascii))
            # print ('Key:', event.Key)
            # print ('KeyID:', event.KeyID)
            # print ('ScanCode:', event.ScanCode)
            # print ('Extended:', event.Extended)
            # print ('Injected:', event.Injected)
            # print ('Alt', event.Alt)
            # print ('Transition', event.Transition)
            # print ('---')
        return True

    def setValidChars(self):
        keysList = list(self.scimMapping.keys())
        self.validChars = list(set("".join(keysList)))
        return True

    def reverseScimMap(self):
        self.scimMappingReversed = {}
        for k, v in self.scimMapping.items():
            self.scimMappingReversed[v] = k

    def initialize(self):
        tableParser = ScimTableParser()
        self.scimMapping = tableParser.parse()
        self.setValidChars()
        self.reverseScimMap()

    def __init__(self):
        self.initialize()
        hm = pyHook.HookManager()
        hm.KeyDown = self.onKeyboardEvent
        hm.HookKeyboard()
        pythoncom.PumpMessages()

ekEngine = EKEngine()