#coding=utf-8

from PyQt5 import QtWidgets,QtGui,QtCore
from ui import Ui_MainWindow
import hashlib  
import os

class Mywindow(QtWidgets.QMainWindow):
	def __init__(self):
		super(Mywindow,self).__init__()		
		self.new=Ui_MainWindow()
		self.new.setupUi(self)
		
	
		self.dirtree = QtWidgets.QFileSystemModel()    #左上目录树形图
		dir='::{20D04FE0-3AEA-1069-A2D8-08002B30309D}'
		self.dirtree.setRootPath(dir)                    #设置根目录
		self.new.treeView.setModel(self.dirtree)           #view跟mode绑定
		self.new.treeView.setRootIndex(self.dirtree.index(dir))     #设置显示目录
		self.new.treeView.resizeColumnToContents(0)
		
		self.new.treeView.clicked.connect(self.treeView_double_click)		#doubleClicked双击信号，clicked单击
		
		
		self.new.comboBox_2.activated.connect(self.continueActivated)         #combobox信号触发，右上目录树显示
	
	
		self.dirtree2 = QtWidgets.QFileSystemModel()    #左下目录树形图
		self.new.treeView.customContextMenuRequested[QtCore.QPoint].connect(self.myListWidgetContext)
		
		
		self.new.comboBox_3.activated.connect(self.handleActivated)         #combobox信号触发，右上目录树显示					
		self.dirtree3 = QtWidgets.QFileSystemModel()       #右上目录树，回显示
		self.new.treeView_2.clicked.connect(self.treeView_2_double_click)
		
		
		self.dirtree4 = QtWidgets.QFileSystemModel()         #右下目录树
	
	
	def transmission(self):	             #右键上传点击动作
		        
		ALLfile = self.getfile(self.file_path)

		
		if ALLfile:                               #如果是单个文件此值为空			
			ALLdir = self.getdir(self.file_path)
			
			filenameone = self.dirtree.fileName(self.dirtree.index(self.file_path))   #获取当前选择的名字
			selectdir = self.targetpath + '\\' + filenameone
			try:
				os.mkdir(selectdir)
				self.new.plainTextEdit.appendPlainText("[创建目录] %s" %selectdir)
			except FileExistsError:
				self.new.plainTextEdit.appendPlainText("[目录已存在] %s" %selectdir)
			#print ('[当前选择的名字为：%s]' %filenameone)
			
			for filedir in ALLdir:                 #选择的是目录路径
				
				dirindex = self.dirtree.index(filedir)           #索引
				
				if self.dirtree.isDir(dirindex):      #如果索引是目录
					
					target = selectdir + filedir.replace(self.file_path,'')
					# print ('#####%s   %s' %(target,target2))
					try:
						os.mkdir(target)
						self.new.plainTextEdit.appendPlainText('[创建目录]: %s' %target)
					except FileExistsError:
						self.new.plainTextEdit.appendPlainText('[目录已存在]: %s' %target)
				else:
					target = selectdir + filedir.replace(self.file_path,'')
					#print ('%s %s#################### %s' %(filedir,target,filedir.lstrip(self.file_path)))
					
					self.son = GOGOGO(filedir,target,1024)
					self.son.start()
					self.son.trigger.connect(self.signal)
					
					#self.new.plainTextEdit.appendPlainText('%s' %signal.startin())
					
		
		else:                                  #当前选择文件路径
			onefilename = self.dirtree.fileName(self.dirtree.index(self.file_path))
		
			try:
				target = self.targetpath + '\\' + onefilename
			
			except AttributeError:
				self.new.plainTextEdit.appendPlainText('[error] :目的目录未确定,请输入目录后回车确认。')
				return 0
			
			self.son = GOGOGO(self.file_path,target,1024)
			self.son.start()
			self.son.trigger.connect(self.signal)
			
			
	def signal(self, date):
		self.new.plainTextEdit.appendPlainText('%s' %date)
	
	
	def myListWidgetContext(self, point):    
		popMenu = QtWidgets.QMenu()
		actionA = popMenu.addAction(QtWidgets.QAction('上传', self,triggered = self.transmission))    # triggered 为右键菜单点击后的激活事件
		actionB = popMenu.addAction(QtWidgets.QAction('下载', self))
		actionC = popMenu.addAction(QtWidgets.QAction('文件对比', self))
		
		#actionA.triggered.connect(self.actionHandler)
		
		popMenu.exec_(QtGui.QCursor.pos())	

		
	def treeView_double_click(self, signal):
		self.file_path=self.dirtree.filePath(signal)
		
		self.new.comboBox_2.addItem(self.file_path)           #添加下拉框
		# self.new.comboBox_2.setItemText(0,self.file_path)	  #设置下拉框显示
		self.new.comboBox_2.setEditText(self.file_path)       
		
		
		dir = self.file_path
		self.dirtree2.setRootPath(dir)
		self.new.treeView_3.setModel(self.dirtree2)		
		self.new.treeView_3.resizeColumnToContents(0)
		self.new.treeView_3.setRootIndex(self.dirtree2.index(dir))
		
			
	def treeView_2_double_click(self, signal):
		self.file_path2=self.dirtree3.filePath(signal)
		#print (self.file_path2)
		
		self.new.comboBox_3.addItem(self.file_path2)           #添加下拉框
		# self.new.comboBox_3.setItemText(0,self.file_path2)	  #给指定的索引位置设置文本
		self.new.comboBox_3.setEditText(self.file_path2)        #编辑显示位置，文本设置
			
		dir = self.file_path2
		self.dirtree4.setRootPath(dir)
		self.new.treeView_4.setModel(self.dirtree4)
		self.new.treeView_4.resizeColumnToContents(0)
		self.new.treeView_4.setRootIndex(self.dirtree4.index(dir))
		
	
	def getfile(self, directory):   #获取每一个文件的路径
		fileall = []
		for parent,dirnames,files in os.walk(directory):
			for filename in files:                          #输出文件信息
				print (filename)
				fileall.append(os.path.join(parent,filename))
				
		return fileall
		
	def getdir(self, directory):   #获取每一个目录与文件的路径
		fileall = []
		for parent,dirnames,files in os.walk(directory):
			for dirname in dirnames:                          #输出文件信息
				fileall.append(os.path.join(parent,dirname))
			
			for file in files: 
				fileall.append(os.path.join(parent,file))
		return fileall
	
	
	def continueActivated(self, index):          #右侧下拉框回车,选择的是目录路径信号触发动作
		self.file_path = (self.new.comboBox_2.itemText(index))        #当前显示路径
		#self.new.plainTextEdit.appendPlainText("%s 存在" %self.file_path)
		# self.dirtree.setExpanded(self.file_path)
		# self.new.treeView.setModel(self.dirtree)		
		# self.new.treeView.setRootIndex(self.dirtree.index('::{20D04FE0-3AEA-1069-A2D8-08002B30309D}'))
		pathindex = self.dirtree.index(self.file_path)                  #获取路径索引
		
		if os.path.exists(self.file_path):
			self.new.plainTextEdit.appendPlainText("[源目录存在]: %s" %self.file_path)
		else:
			self.new.plainTextEdit.appendPlainText("[error][源目录不存在]: %s" %self.file_path)
		
		self.new.treeView.expand(pathindex)    #展开当前项
		self.new.treeView.scrollTo(pathindex)    #定位到当前项
		self.new.treeView.resizeColumnToContents(0)    #根据其内容的大小调整列的大小
		self.new.treeView.setCurrentIndex(self.dirtree.index(self.file_path))  #设置当前项目，鼠标选中效果
		# expand
		
		
	def handleActivated(self, index):          #右侧下拉框回车,选择的是目录路径信号触发动作
		self.targetpath = (self.new.comboBox_3.itemText(index))        #当前显示路径		
		
		if os.path.exists(self.targetpath):
			self.new.plainTextEdit.appendPlainText("[目的目录存在]: %s " %self.targetpath)
		else:
			self.new.plainTextEdit.appendPlainText("[error][目的目录不存在]: %s " %self.targetpath)
		
		self.dirtree3.setRootPath(self.targetpath)
		self.new.treeView_2.setModel(self.dirtree3)
		self.new.treeView_2.resizeColumnToContents(0)
		self.new.treeView_2.setRootIndex(self.dirtree3.index(self.targetpath))
		
		# print(self.new.comboBox_3.itemData(index))

		
		
class GOGOGO(QtCore.QThread):
	trigger = QtCore.pyqtSignal(str)
	def __init__(self,sourcefile,targetfile,block):
		super(GOGOGO,self).__init__()
		self.sourcefile = sourcefile
		self.targetfile = targetfile
		self.block = block
		#print(self.sourcefile,self.targetfile,self.block)
		#self.startin()
	
	def getfilemaxsize(self,filename):
		try:
			ifis = open(filename, "rb+") 
			ifis.seek(0,2)
			maxsize = (ifis.tell())
			ifis.close()
			if maxsize:
				return maxsize     #返回文件末尾字节针
			else:
				return -2         #文件为空文件
			
		except FileNotFoundError:
			return -1         #文件不存在
			
		except PermissionError:
			return -3         #没有权限

			
	def getmd5(self,filename,maxsize,block):
	
		sha1 = hashlib.sha1()
		if maxsize < block:
			filename = open(filename, "rb")
			line = filename.read(block)
			sha1.update(line)
		return block,sha1.hexdigest(),sha1.hexdigest()
		
		
		intnub = int(maxsize/block)
		cordon = intnub*0.9
		
		filename = open(filename, "rb")
		for frequency in range(int(maxsize/block)):
			newsize = filename.seek(frequency*block, 0)
			line = filename.read(block)
			sha1.update(line)
			
			if frequency > cordon:
				cordonmd5 = sha1.hexdigest()
				cordonfrequency = frequency
			
		line = filename.read(maxsize - (newsize + block))         #写入剩余字节
		sha1.update(line)
		filename.close()

		return cordonfrequency*block,cordonmd5,sha1.hexdigest()

		
	def continuetransmission(self,sourcefile,targetfile,smaxsize,block,minisize):
		startb = int(minisize/block)
		
		fo = open(sourcefile, "rb")
		inn = open(targetfile, "rb+")
		for frequency in range(startb,int(smaxsize/block)):       #接着dmaxsize写入
			
			newsize = fo.seek(frequency*block, 0)
			line = fo.read(block)

			inn.seek(newsize, 0)
			inn.write(line)	

		line = fo.read(smaxsize - (newsize + block))         #写入剩余字节
		inn.seek(newsize + block, 0)
		inn.write(line)
		inn.close()
		fo.close()
		return 1
		
	def __del__(self):
		self.wait()
		
	def run(self):
		smaxsize=self.getfilemaxsize(self.sourcefile)
		dmaxsize=self.getfilemaxsize(self.targetfile)
		#print (dmaxsize)

		newsize=0	
		if dmaxsize == -1:       #目标文件不存在
			fo = open(self.sourcefile, "rb")
			inn = open(self.targetfile, "ab")
			for frequency in range(int(smaxsize/self.block)):       #按smaxsize批量写入字节
				
				newsize = fo.seek(frequency*self.block, 0)
				line = fo.read(self.block)
						
				inn.write(line)	
			
			if smaxsize > self.block:
				line = fo.read(smaxsize - (newsize + self.block))         #写入剩余字节
				inn.write(line)
			else:
				line = fo.read(smaxsize)
				inn.write(line)
			inn.close()
			fo.close()
			self.trigger.emit("[文件传输完成]: %s" %self.targetfile)
			
			
		elif dmaxsize > 0:         #目标文件已经存在，判断断点续传	

			dmd5 = self.getmd5(self.targetfile,dmaxsize,self.block)
			smd5 = self.getmd5(self.sourcefile,dmaxsize,self.block)
			
			if dmd5[2] == smd5[2]:
				if smaxsize == dmaxsize:
					self.trigger.emit("[文件已完成传输]: %s" %self.targetfile)
				else:	
					#return ("[MD5匹配继续传输]:从 %s 到 %s" %(self.sourcefile,self.targetfile))
					if self.continuetransmission(self.sourcefile,self.targetfile,smaxsize,self.block,dmaxsize) == 1:
						#return ("[继续传输完成]: %s" %self.targetfile)
						self.trigger.emit("[MD5匹配继续传输完成]:从 %s 到 %s" %(self.sourcefile,self.targetfile))
			elif dmd5[1] == smd5[1]:
				#return("[文件大部分相似]: %s 在最近相似点进行续传" %self.targetfile)
				if self.continuetransmission(self.sourcefile,self.targetfile,smaxsize,self.block,smd5[1]) == 1:
				#	self.new.plainTextEdit.appendPlainText("[继传完成]: %s" %self.targetfile)
					self.trigger.emit("[文件大部分相似续传完成]: %s" %self.targetfile)
		
		
def mainwindows():
	import sys 
	app = QtWidgets.QApplication(sys.argv) 
	windows = Mywindow()
	windows.show()
	sys.exit(app.exec())
  
  
  
if __name__ == "__main__":
 mainwindows()