import wx.grid
import numpy as np
import csv
from os import path
import random
import math

class MyApp(wx.App):
    def OnInit(self):
        
        if not path.exists('tmp.csv'):
            with open('tmp.csv', 'x') as self.f:
                self.f.write('')
        else:
            f = open("tmp.csv", "w+")
            f.close()
       
        frame = wx.Frame(None, -1, title = "Juego de Mesa", style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX), size=(525,515))
        self.grid = wx.grid.Grid(frame)
        row = 5
        column = 10
        self.array = np.zeros( (row, column) )
        cRow = 0
        
        res = random.sample(range(1,67), 25)
        res.extend(res)
        random.shuffle(res)
        
        self.grid.CreateGrid(row,column)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self._OnSelectedCell)

        for i in range(0,len(res)):
            img = wx.Bitmap("../cards/back.png", wx.BITMAP_TYPE_ANY)
            img = self.scale_bitmap(img, 50, 100)
            imageRenderer = MyImageRenderer(img)
            if cRow < row:
                self.grid.SetCellRenderer(cRow,i%10,imageRenderer)
                self.array[cRow,i%10] = res[i]
                self.grid.SetColSize(i%10,img.GetWidth()+2)
                self.grid.SetRowSize(cRow,img.GetHeight()+2)
                if i%10 == 9:
                    cRow+=1
       
        self.grid.SetRowLabelSize(0)
        self.grid.SetColLabelSize(0)
        frame.Show(True)
        print(self.array)
        return True
    
    def scale_bitmap(self, bitmap, width, height):
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result

    def _OnSelectedCell(self, event):
        with open('tmp.csv', mode='a') as tmpFile:
            fileWriter = csv.writer(tmpFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            fileWriter.writerow([event.GetRow(), event.GetCol(), self.array[event.GetRow(),event.GetCol()]])
        
        nLines = self.getFileNumberLine()
        if nLines == 2:
            self.first = 0
            self.second = 0
            self.r1 = 0
            self.c1 = 0
            self.r2 = 0
            self.c2 = 0
            with open('tmp.csv') as tmpFile:
                fileReader = csv.reader(tmpFile, delimiter=',')
                line_count = 0
                for row in fileReader:
                    if line_count == 0:
                        self.r1 = row[0]
                        self.c1 = row[1]
                        self.first = row[2]
                        line_count += 1
                    else:
                        self.r2 = row[0]
                        self.c2 = row[1]
                        self.second = row[2]
                        line_count += 1
                        
            if self.first == self.second:
                print("iguales!")
                self.grid.ClearGrid()
                img = wx.Bitmap("../cards/" + str(math.trunc(float(self.first))) +".png", wx.BITMAP_TYPE_ANY)
                img = self.scale_bitmap(img, 50, 100)
                imageRenderer = MyImageRenderer(img)
                self.grid.SetCellRenderer(int(self.r1),int(self.c1),imageRenderer)
                self.array[int(self.r1),int(self.c1)] = 0
                
                img = wx.Bitmap("../cards/" + str(math.trunc(float(self.second))) +".png", wx.BITMAP_TYPE_ANY)
                img = self.scale_bitmap(img, 50, 100)
                imageRenderer = MyImageRenderer(img)
                self.grid.SetCellRenderer(int(self.r2),int(self.c2),imageRenderer)
                self.array[int(self.r2),int(self.c2)] = 0
                f = open("tmp.csv", "w+")
                f.close()
                
            else:
                f = open("tmp.csv", "w+")
                f.close()
        
            print(self.array)

    def getFileNumberLine(self):
        file = open('tmp.csv')
        numline = len(file.readlines())
        return numline


class MyImageRenderer(wx.grid.GridCellRenderer):
    def __init__(self, img):
        wx.grid.GridCellRenderer.__init__(self)
        self.img = img
    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        image = wx.MemoryDC()
        image.SelectObject(self.img)
        dc.SetBackgroundMode(wx.SOLID)
        if isSelected:
            dc.SetBrush(wx.Brush(wx.BLUE, wx.SOLID))
            dc.SetPen(wx.Pen(wx.BLUE, 1, wx.SOLID))
        else:
            dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
            dc.SetPen(wx.Pen(wx.WHITE, 1, wx.SOLID))
        dc.DrawRectangle(rect)
        width, height = self.img.GetWidth(), self.img.GetHeight()
        if width > rect.width-2:
            width = rect.width-2
        if height > rect.height-2:
            height = rect.height-2
        dc.Blit(rect.x+1, rect.y+1, width, height, image, 0, 0, wx.COPY, True)

app = MyApp(0)
app.MainLoop()