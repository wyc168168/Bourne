# /usr/bin/env python
# _*_ coding:UTF-8 _*_
# file name:copyinorder.py

import sys,os,shutil,time,datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

global sorname,desname

class copyinorder(QWidget):
    def __init__(self,parent =  None):
        super(copyinorder,self).__init__(parent)
        self.location()
        self.initUI()
        self.show()
        
        
    def location(self):
        self.setWindowTitle('Copy In Order')
        self.resize(800,400)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2 , (screen.height() - size.height())/2)
        self.setFixedSize(self.width(), self.height())
        
    def initUI(self):
        self.total_size = 0

        
        self.headername = ['文件名','大小','创建时间','完整路径']
        self.target_label = QLabel('目标路径：')
        self.target_line = QLineEdit()
        self.target_btn = QPushButton('……')
        self.target_btn.clicked.connect(self.opendir)
        
        self.add_btn = QPushButton('添加文件')
        self.add_btn.clicked.connect(self.addfile)
        self.del_btn = QPushButton('删除文件')
        self.del_btn.clicked.connect(self.delfile)
        self.up_btn = QPushButton('上    移')
        self.up_btn.clicked.connect(self.upfile)
        self.down_btn = QPushButton('下    移')
        self.down_btn.clicked.connect(self.downfile)
        self.clear_btn = QPushButton('清    除')
        self.clear_btn.clicked.connect(self.clear)
        
        
        self.cover_check = QCheckBox('覆盖')
        self.cover_check.setChecked(True)
        self.confirm_btn = QPushButton('开始复制')
        self.confirm_btn.clicked.connect(self.confirm)
        self.cancel_btn = QPushButton('退    出')
        self.cancel_btn.clicked.connect(self.close)
        
        self.tableWidget = QTableWidget()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.setColumnCount(len(self.headername))
 
        self.tableWidget.setHorizontalHeaderLabels(self.headername)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.sortItems(0,Qt.AscendingOrder)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnWidth(0,400)
        self.tableWidget.setColumnWidth(1,60)
        self.tableWidget.setColumnWidth(2,140)  
        self.tableWidget.setColumnWidth(3,500)      
        
        tarlayout = QHBoxLayout()
        tarlayout.addWidget(self.target_label)
        tarlayout.addWidget(self.target_line)
        tarlayout.addWidget(self.target_btn)
        
        grid = QGridLayout()
        grid.addWidget(self.tableWidget,0,1,15,5)
        grid.addWidget(self.add_btn,0,6)
        grid.addWidget(self.del_btn,2,6)
        grid.addWidget(self.up_btn,4,6)
        grid.addWidget(self.down_btn,6,6)
        grid.addWidget(self.clear_btn,8,6)
        grid.addWidget(self.cover_check,10,6)
        
        confirmlayout = QHBoxLayout()
        confirmlayout.addWidget(self.confirm_btn)
        confirmlayout.addWidget(self.cancel_btn)
        
        table = QWidget()
        table.setLayout(grid)
             
        
        target = QWidget()
        target.setLayout(tarlayout)
        
        confirm = QWidget()
        confirm.setLayout(confirmlayout)
        
        
        layout = QVBoxLayout()
        
        layout.addWidget(target)
        layout.addWidget(table)
        layout.addWidget(confirm)

        
        self.setLayout(layout)
        
    def opendir(self):
        dirname = QFileDialog.getExistingDirectory(self,"选取文件夹","/")
        self.target_line.setText(dirname)
        
    def addfile(self):
        files, ok1 = QFileDialog.getOpenFileNames(self,"多文件选择","/","All Files (*)")
        filecount = len(files)
        print (filecount)
        row = self.tableWidget.rowCount()
        print ('行数为：'+str(row))

        for i in range(0,len(files)):
            self.tableWidget.insertRow(row+i)
            comnameItem = QTableWidgetItem(str(files[i]))
            nameItem = QTableWidgetItem(str(files[i].split("/")[-1]))
            file_size = self.get_FileSize(files[i])
            sizeItem = QTableWidgetItem(str(file_size))    
            sizeItem.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            timeItem = QTableWidgetItem(str(self.get_FileCreateTime(files[i])))
            self.tableWidget.setItem(row+i,0,nameItem)
            self.tableWidget.setItem(row+i,1,sizeItem)
            self.tableWidget.setItem(row+i,2,timeItem)
            self.tableWidget.setItem(row+i,3,comnameItem)  
            self.total_size = round(self.total_size + self.del_last(file_size),2)
        print (self.total_size)
            
    def delfile(self):
        try:
            row1 = self.tableWidget.currentItem().row()
            self.tableWidget.removeRow(row1)
        except AttributeError:
            pass
        
    def upfile(self):
        try:
            uprow = self.tableWidget.currentItem().row()
            if uprow >0:       
                upnameItem = QTableWidgetItem(self.tableWidget.item(uprow,0).text())
                upsizeItem = QTableWidgetItem(self.tableWidget.item(uprow,1).text())
                upsizeItem.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                uptimeItem = QTableWidgetItem(self.tableWidget.item(uprow,2).text())
                upcomnameItem = QTableWidgetItem(self.tableWidget.item(uprow,3).text())
                renameItem = QTableWidgetItem(self.tableWidget.item(uprow-1,0).text())
                resizeItem = QTableWidgetItem(self.tableWidget.item(uprow-1,1).text())
                resizeItem.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                retimeItem = QTableWidgetItem(self.tableWidget.item(uprow-1,2).text())
                recomnameItem = QTableWidgetItem(self.tableWidget.item(uprow-1,3).text())
            
                self.tableWidget.setItem(uprow,0,renameItem)
                self.tableWidget.setItem(uprow,1,resizeItem)
                self.tableWidget.setItem(uprow,2,retimeItem)
                self.tableWidget.setItem(uprow,3,recomnameItem)
                self.tableWidget.setItem(uprow-1,0,upnameItem)
                self.tableWidget.setItem(uprow-1,1,upsizeItem)
                self.tableWidget.setItem(uprow-1,2,uptimeItem)
                self.tableWidget.setItem(uprow-1,3,upcomnameItem)
                self.tableWidget.setCurrentCell(uprow-1,0)
        except AttributeError:
            pass
                
    def downfile(self):
        try:
            downrow = self.tableWidget.currentItem().row()
            countrow = self.tableWidget.rowCount()
            if downrow < countrow:       
                downnameItem = QTableWidgetItem(self.tableWidget.item(downrow,0).text())
                downsizeItem = QTableWidgetItem(self.tableWidget.item(downrow,1).text())
                downsizeItem.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                downtimeItem = QTableWidgetItem(self.tableWidget.item(downrow,2).text())
                downcomnameItem = QTableWidgetItem(self.tableWidget.item(downrow,3).text())
                renameItem = QTableWidgetItem(self.tableWidget.item(downrow+1,0).text())
                resizeItem = QTableWidgetItem(self.tableWidget.item(downrow+1,1).text())
                resizeItem.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                retimeItem = QTableWidgetItem(self.tableWidget.item(downrow+1,2).text())
                recomnameItem = QTableWidgetItem(self.tableWidget.item(downrow+1,3).text())
            
                self.tableWidget.setItem(downrow,0,renameItem)
                self.tableWidget.setItem(downrow,1,resizeItem)
                self.tableWidget.setItem(downrow,2,retimeItem)
                self.tableWidget.setItem(downrow,3,recomnameItem)
                self.tableWidget.setItem(downrow+1,0,downnameItem)
                self.tableWidget.setItem(downrow+1,1,downsizeItem)
                self.tableWidget.setItem(downrow+1,2,downtimeItem)
                self.tableWidget.setItem(downrow+1,3,downcomnameItem)
                self.tableWidget.setCurrentCell(downrow+1,0)
        except AttributeError:
            pass
            
    def clear(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        
    def confirm(self):
        self.filepath = self.target_line.text()
        selerow = self.tableWidget.rowCount()
        cover = 0
        if self.cover_check.isChecked():
            cover = 1
        if len(self.filepath):
            if selerow == 0 :
                warn = QMessageBox.about(self,'复制文件','请添加需要复制的文件！')  
            else:
                if os.path.isdir(self.filepath):
                    print ('文件夹存在')

                    print ('cover:',cover)
                    copy_name,copy_size,dec_name,total_size = self.get_copyname()
                    copy_work = copy_file(copy_name,dec_name,cover)
                    copy_work.start()
                    copy_status = copy_pro(copy_size,dec_name,total_size)
                    copy_work.trigger.connect(copy_status.test_tirgger)

                    if copy_status.exec_():
                        print ("复制完成")

                else:
                    mess = message_box()
                    if mess.exec_():
                        if mess.confirm == 1:
                            self.mk_dir(self.filepath)
                            copy_name,copy_size,dec_name,total_size = self.get_copyname()
                            copy_work = copy_file(copy_name,dec_name,cover)
                            copy_work.start()
                            copy_status = copy_pro(copy_size,dec_name,total_size)
                            copy_work.trigger.connect(copy_status.test_tirgger)
                            if copy_status.exec_():
                                print ("复制完成")
                    
                    else:
                        warn = QMessageBox.about(self,'复制文件','操作完成！')  
        else:
            warn = QMessageBox.about(self,'复制文件','请添加目标路径！') 

            
    def get_FileSize(self,filePath): 
        fsize = os.path.getsize(filePath)
        fsize = fsize/float(1024*1024)
        if fsize >= 1024:
            fsize =fsize / 1024 
            fsize_out = str(round(fsize,2))+'G'
        elif fsize <= 0.01:
            fsize = 0.01 * 1024
            fsize_out = str(round(fsize,0)) + 'B'
        else:fsize_out = str(round(fsize,2)) + 'M'
        return fsize_out
        
        
    def get_FileCreateTime(self,filePath):
        t = os.path.getctime(filePath)
        return self.TimeStampToTime(t) 
        
    def TimeStampToTime(self,timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)
    
    def copy_status(self):
        reply = self.get_FileSize(self.desname)
        print (reply)     
       
    def mk_dir(self,filepath):
        path = filepath
        print (path)
        #split_path = path.split('/')
        #mmpath = ""
        #for i in range(1,len(split_path)):
        #    mmpath = mmpath + split_path[i] # linux(mmpath = mmpath + '/' + split_path[i]),windows(mmpath = mmpath + split_path[i])
        #    print (mmpath)
        while os.path.isdir(path) == False:
            os.mkdir(path)
        print ('新建' + path + '文件夹')
                
    def del_last(self,str):
        str_list=list(str)
        if str_list[-1] =='G':
            str_list.pop()
            add_size = round((float("".join(str_list)) *1024),0)
        elif str_list[-1] == 'B':
            str_list.pop()
            add_size = round((float("".join(str_list)) /1024),2)
        else:
            str_list.pop()
            add_size = round(float("".join(str_list)) ,2)
        return add_size

                
    def get_copyname(self):
        copyname = []
        copysize = []
        decname = []
        total_size = 0
        print (self.tableWidget.rowCount())
        for i in range(0,self.tableWidget.rowCount()):
            copyname.append(self.tableWidget.item(i,3).text())
            copysize.append(self.del_last(self.tableWidget.item(i,1).text()))
            decname.append(self.filepath + '/' + self.tableWidget.item(i,0).text())
            total_size = round(total_size + self.del_last(self.tableWidget.item(i,1).text()),2)
        return copyname,copysize,decname,total_size
            
       
class message_box(QDialog):
    def __init__(self,parent =  None):
        super(message_box,self).__init__(parent)
        self.location()
        self.initUI()

        
        
    def location(self):
        self.setWindowTitle('新建文件夹')
        self.resize(200,100)                    
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2 , (screen.height() - size.height())/2)
        self.setFixedSize(self.width(), self.height())

        
    def initUI(self):
        self.confirm = 0
        self.time = QTimer(self)
        self.count = 5
        self.time.timeout.connect(self.timecount)
        self.time.start(1000)
        self.info_label = QLabel("文件夹不存在，是否新建文件夹再复制？")
        self.accept_btn = QPushButton("确认")
        self.cancel_btn = QPushButton("取消" + "(" + str(self.count)+ ")" )
        self.accept_btn.clicked.connect(self.agree)
        self.cancel_btn.clicked.connect(self.reject)
        Hlayout = QHBoxLayout()
        Hlayout.addWidget(self.accept_btn)
        Hlayout.addWidget(self.cancel_btn)
        
        hh = QWidget()
        hh.setLayout(Hlayout)
        
        Vlayout = QVBoxLayout()
        Vlayout.addWidget(self.info_label)
        Vlayout.addWidget(hh)
        
        self.setLayout(Vlayout)
        
    def timecount(self):
        if self.count ==1:
            self.close()
        else:
            self.count = self.count -1
            self.cancel_btn.setText("取消" + "(" + str(self.count) + ")")    
            
    def agree(self):
        self.confirm = 1
        self.accept()


class filetest_box(QDialog):
    def __init__(self,parent =  None):
        super(filetest_box,self).__init__(parent)
        self.location()
        self.initUI()

        
        
    def location(self):
        self.setWindowTitle('文件复制')
        self.resize(200,100)                    
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2 , (screen.height() - size.height())/2)
        self.setFixedSize(self.width(), self.height())

        
    def initUI(self):
        self.confirm = 0
        self.time = QTimer(self)
        self.count = 5
        self.time.timeout.connect(self.timecount)
        self.time.start(1000)
        self.info_label = QLabel("文件已存在，是否覆盖？")
        self.accept_btn = QPushButton("确认")
        self.cancel_btn = QPushButton("取消" + "(" + str(self.count)+ ")" )
        self.accept_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        Hlayout = QHBoxLayout()
        Hlayout.addWidget(self.accept_btn)
        Hlayout.addWidget(self.cancel_btn)
        
        hh = QWidget()
        hh.setLayout(Hlayout)
        
        Vlayout = QVBoxLayout()
        Vlayout.addWidget(self.info_label)
        Vlayout.addWidget(hh)
        
        self.setLayout(Vlayout)
        
    def timecount(self):
        if self.count ==1:
            self.reject()
        else:
            self.count = self.count -1
            self.cancel_btn.setText("取消" + "(" + str(self.count) + ")")    
            
class copy_file(QThread):
    trigger = pyqtSignal()

    def __init__(self,source_name,target_name,cover):

        super(copy_file,self).__init__()
        self.source_n = source_name
        self.target_n = target_name
        self.cover = cover

    def run(self):
        print ("开始复制")
   
        for no in range(0,len(self.source_n)):
            if self.cover:
                shutil.copyfile(self.source_n[no],self.target_n[no])
            else:
                if os.path.exists(self.target_n[no]):
                    filetest = filetest_box()
                    if filetest.exec_():
                        shutil.copyfile(self.source_n[no],self.target_n[no])
                else:
                    shutil.copyfile(self.source_n[no],self.target_n[no])   
            self.trigger.emit()
        print ("复制完成")    


        
class copy_pro(QDialog):
    mm = 5
    dd = 0
    def __init__(self,filesize,filename,totalsize):
        super(copy_pro,self).__init__()
        self.file_size = filesize
        self.file_Path = filename
        self.file_name = []
        self.all_size = 0
        self.curren_size = 0
        for i in range(0,len(filename)):
            self.file_name.append(filename[i].split('/')[-1])
        print (self.file_name)
        self.copysize = float(self.file_size[0])
        self.total_size = totalsize
        self.location()
        self.initUI()
        
        
    def location(self):
        
        self.setWindowTitle('复制进度')
        self.resize(300,150)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2 , (screen.height() - size.height())/2)
        self.setFixedSize(self.width(), self.height())

        
    def initUI(self):
        self.time = QTimer(self)
        self.count = 0
        self.time.timeout.connect(self.timecount)
        self.time.start(200)
        self.copy_label = QLabel('正在复制'+ '"'+ self.file_name[0] + '"')
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.single_copy = QLabel()
        self.pbar2 = QProgressBar(self)
        self.pbar2.setGeometry(30, 40, 200, 25)
        self.all_copy = QLabel()
        self.status_label = QLabel("0")
        
        layout = QVBoxLayout()
        layout.addSpacing(30)
        layout.addWidget(self.copy_label)
        layout.addWidget(self.pbar)
        layout.addWidget(self.single_copy)
        layout.addWidget(self.pbar2)
        layout.addWidget(self.all_copy)
        self.setLayout(layout)
        
    def paintEvent(self,event):


        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.blue)
        painter.drawLine(20,15,280,15)
        #painter.begin(self)
        self.draw(painter)
        #painter.end()
        
        
    def draw(self,qp):
        qp.setPen(Qt.red)

        qp.drawRect(self.mm,10,10,10)
        
    def get_FileSize(self,filePath): 
        fsize = os.path.getsize(filePath)
        fsize = fsize/float(1024*1024)
        return round(fsize,2)
        
    def timecount(self):
        if self.mm < 275 and self.dd == 0 :
            self.mm = self.mm + 10
            
        elif self.mm >15 and self.dd == 10:
            self.mm = self.mm - 10
        elif self.mm >= 275 and self.dd == 0:
            self.mm = self.mm -10
            self.dd = 10
        else:
            self.mm =self.mm + 10
            self.dd = 0
        self.update()


        if self.copysize > 0:
            print ('count:',self.count,self.file_Path[self.count])
            if self.count == 0:
                self.curren_size = float(self.get_FileSize(self.file_Path[self.count]))
            else:
                self.curren_size = float(self.get_FileSize(self.file_Path[self.count-1]))
            stepint = self.curren_size/float(self.copysize)*100
            step = int(stepint)
            self.pbar.setValue(step)
            self.single_copy.setText('共' + str(round(self.copysize,2)) + 'M,' + '已复制;' + str(round(self.curren_size,2)) + 'M')
            self.cureen_all = self.all_size + self.curren_size
            stepall = self.cureen_all/float(self.total_size)*100
            self.pbar2.setValue(stepall)
            self.all_copy.setText('总计' + str(self.total_size) + 'M,' + '已复制:' + str(round(self.cureen_all,2)) + 'M')
        else:
            self.pbar.setValue(100)

    def test_tirgger(self):
        
        if self.count == (len(self.file_name)-1):
            print ("全部复制完成")
            self.pbar.setValue(100)
            self.single_copy.setText('共' + str(round(self.copysize,2)) + 'M,' + '已复制;' + str(round(self.copysize,2)) + 'M')
            self.pbar2.setValue(100)
            self.all_copy.setText('总计' + str(self.total_size) + 'M,' + '已复制:' + str(self.total_size) + 'M')
            self.copy_label.setText('文件复制完成')
            self.time.stop()

            warn = QMessageBox.about(self,'复制文件','操作完成')

            self.accept()
        else:

            self.copy_label.setText('正在复制'+ '"'+ self.file_name[self.count+1] + '"')
            self.pbar.setValue(0)
            self.copysize = self.get_FileSize(self.file_Path[self.count])
            self.all_size = self.all_size + self.curren_size
            self.count = self.count +1

def main():
    app = QApplication(sys.argv)
    wyc = copyinorder()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
