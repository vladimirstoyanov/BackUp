'''
This script is a free: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This script is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this script.  If not, see <http://www.gnu.org/licenses/>.

Author: Vladimir Stoyanov
e-mail: vlado_stoyanov@yahoo.com
'''

import hashlib
import os
import os.path
import sys
import time
import codecs
import platform
if (platform.system() == "Windows"):
        from _winreg import *

#=====RecoveryData class=====
class RecoveryData:
	def recoveryData (self,path, destination):
		"""
		'recoveryData()' method extract file archive with name set it to 'full_name' variable
		consequently extract archives to current data 
		'full_name' must contain date in format <dd>.<mm>.<yy> or this method doesn't work.
		args:
		full_name - full name of file archive 
		destination - destination of extracted data
		return 1 if success recovery data or return 0 if have some error
		"""
		if (os.path.isfile(full_name) == False):
			return 0
  
		file_name, file_dir = self.getFileAndPathFromAbsolute(path)
		
		##return list with name of archives who will be extracted 
		l_archives = self.getArchives(file_dir, file_name)
		
		if (len(l_archives) == 0):
			return 0
  
		self.extractArchives(l_archives, destination)
		return 1
	
	def extractArchives(self, l_archives, destination):
		"""
		'extractArchives()' method extract archives consequently ordered in list 'l_archives' to 
		destination
		args:
		l_archives - list with archives file names
		destination - destination of extracted data
		return 1 if successfully extract archives or return 0 if has some error
		"""
		if (len(l_archives) == 0):
			#print "No archives to recovery!"
			return 0
		
		bu = BackUp()
		path_to_rar = ""
		if (platform.system() == "Windows"):
			##get path to rar.exe
			path_to_rar = bu.getPathToRar()
		
		separator = self.getSeparator()
		if (destination == "" or destination == "." + separator):
			destination = os.path.dirname(os.path.realpath(__file__))
		
		if (os.path.isdir(destination) == False):
			print "In \"extractArchives()\" method, extract destionation \""+ destination + "\" is not valid!"
			return
			
		for i in range(len(l_archives)):
			command = ""
			if (platform.system() == "Windows"):
				command = path_to_rar + " x -y " + l_archives[i] + " " + destination
			else:
				#linux
				command = "tar -zxvf " + l_archives[i] + " -C " + destination
			
			##execute command
			os.system(command) 
	
	def getSeparator(self):
		"""
		'getSeparator()' method return separator 
		"""
		separator = '/'
		if (platform.system() == "Windows"):
			separator = '\\'
		return separator
	      
	def getFilesFromDirectory(self, dir_name):
		"""
		'getFilesFromDirectory()' method return list with files from directory - 'dir_name'
		dir_name - directory path
		"""
		return_list = []
  
		separator = self.getSeparator()
		if (dir_name=="" or dir_name == "." + separator):
			dir_name+=os.path.dirname(os.path.realpath(__file__))
		
		
		if (os.path.isdir(dir_name) == False):
			print "In \"getFilesFromDirectory()\" method, \'dir_name\' variable: \""+ destination + "\" is not valid directory!"
			return []
		
		if (dir_name[len(dir_name)-1] != separator):
			dir_name+=separator
  
		print "dir_name: " + dir_name
  
		for i in os.listdir(dir_name):
			print dir_name + i
			#time.sleep(1)
			if os.path.isfile(dir_name+i) == True:
				return_list.append(i)
        
		return return_list
		
	def getFileAndPathFromAbsolute(self, full_name):
		"""
		'getFileAndPathFromAbsolute()' method return file name and dir name of absoulute file path
		args:
		full_name - absoulute file path
		"""
		if (os.path.isfile(full_name) == False):
			return "",""
  
		separator = self.getSeparator()
  
		name = ""
		index = -1
		
		for i in range(len(full_name)-1, -1, -1):
			if (full_name[i] == separator):
				index = i
				break
			if (i==0):
				index = 0
			name = full_name[i] + name 
    
		if (index == -1):
			return "",""
  
		path = full_name[:index]
		if (path!=""):
			path+=separator
  
		return name, path

	
	def checkContain(self,file_name, name):
		"""
		'checkContain()' if file_name in begining contain name then return 1, else return 0 
		"""
		if (len(file_name)< len(name)):
			return 0
  
		for i in range(len(file_name)):
			if (i==len(name)):
				return 1
		if (file_name[i]!=name[i]):
			return 0
		return 0
	
	def getArchives(self, dir_name, file_name):
		"""
		'getArchives()' method return list with file names of archives who will be extracted
		args:
		dir_name - directory of file archive
		file_name - name of file archive
		"""
		l_ret_files = []
		l_nums = []
  
		##get files from dir_name directory
		l_files = self.getFilesFromDirectory(dir_name)
		
		for i in range(len(l_files)):
			date,name, num = self.getDateAndName(l_files[i])
    
			if (date ==""): ##ignore invalid name of archive
				continue
    
			##check if 'file_name' containg at begining 'name'
			if (self.checkContain(file_name, name)==False):
				continue
	    
			l_ret_files.append(l_files[i])
			l_nums.append(num)
    
		l_ret_files = self.sortByDate(l_ret_files, l_nums)
		
		#remove_unnecessary_elements(l_ret_files,file_name)
		index =-1
		for i in range(len(l_ret_files)):
			if (l_ret_files[i] == file_name):
				index = i
				break
		
		if (index!=-1):
			for i in range(index-1,-1,-1):
				del l_ret_files[i]
		
		print l_ret_files
			
		return l_ret_files
	
	def getDateAndName(self, name): 
		"""
		'getDateAndName()' method return date and name from 'name'
		args:
		name - name of archive
		return "","",-1 if has some error, otherwise 'return date, name, num', where 'date' is date, 'name' is name
		and 'num' is date converted by number
		"""
		#date format <name>_<dd>.<mm>.<yy>.rar
		print "Name: " + name
		num = 0
		
		if platform.system() == "Windows":
		        num = 12
		else:
			num = 15
			
		if (len(name)<num):
			#print "len(archive_name)<num: " + name
			return "", "", -1
  
		date = name[len(name)-num:]
		#print "Date:" + date
  
		name_ = name[:len(name)-num]
		if platform.system() == "Windows":
		        num = 4
		else:
			num = 7
		
		extension = name[len(name)-num:]
	
		if (extension!='.rar' and extension!='.tar.gz'):
	                return "","",-1
			
		if (len(date)<num): #.rar #.tar.gz
			print "Can't get data from archive file name: " + name
			return "","", -1
  
		date = date[:len(date)-num]
		
		check, num = self.checkDateAndReturnConvertedDateToInt(date)
		if (check == False):
			return "", "", -1
  
		return date,name_, num

	def checkForLeapYear(self, year):
		"""
		'checkForLeapYear()' method return 1 if year is leap-year, otherwise return 0
		"""
		if (year%4 == 0):
			if (year%100 == 0):
				if (year%400 == 0):
					return 1
			else:
				return 1
		return 0
	
	def checkDateAndReturnConvertedDateToInt(self,date):
		"""
		'checkDateAndReturnConvertedDateToInt()' method check date and return date to int
		return 0,-1 if has some error, otherwise return date and converted date to int
		"""
		l_date = date.split('.')
		
		if (len(l_date)!=3):
			print "Invalid date \""+ date + "\" . Format  must be like <dd>.<mm>.<yy>."
			return False, -1
  
		if (len(l_date[0])!=2 or len(l_date[1])!=2 or len(l_date[2])!=2):
			print "Invalid date \""+ date + "\" . Format  must be like <dd>.<mm>.<yy>."
			return False, -1
    
		day = 0
		month = 0
		year = 0 
  
		try:
			day = int(l_date[0])
		except:
			print "In checDate(date), cannot convert day to int!"
			return False, -1
  
		try:
			month = int(l_date[1])
		except:
			print "In checkDate(date), cannot convert month to int!"
			return False, -1
  
		try:
			year = int("20" + l_date[2])
		except:
			print "In checkDate(date), cannot convert year to int!"
			return False, -1
  
		if (month<0 or month>12):
			print "Incorect month in : \"" + str(month) + "\"."
			return False
  
		if (day>31 or day<1):
			print "Incorect day \"" + str(day) + "\"."
			return False, -1
  
		#1,3,5,7,8,10,12
		if (day == 31 and (month!=1 or month!=3 or month!=5 or month!=7 or month!=8 or month!=10 or month!=12)):
			print "It havent 31 days in " + str(month) + " month."
			return False, -1
    
		leap_year = self.checkForLeapYear(year)
		if (month == 2 and day>28 and leap_year==False):
			print "In February, when is not leap-year, it haven't more than 28 days."
			return False, -1
    
		if (month == 2 and day>29):
			print "In February, when is leap-year, it haven't more than 29 days."
			return False, -1
  
		try:
			num = l_date[2] + l_date[1] + l_date[0]
			num = int(num)
		except:
			print "Cannot convert " + num + " to string."
			return False, -1
  
		return True, num
		
	def sortByDate(self,dates, l_num_dates):
		"""
		'sortByDate()' method, sort file names of archives by dates
		return [] if has some error, otherwise return list with sorted file names by dates
		"""
		if (len(l_num_dates)!=len(dates)):
			print "Error in sortByDate: len(l_num_dates)!=len(dates)"
			return []
  
		for i in range(len(l_num_dates)-1):
			for j in range(i+1, len(l_num_dates), 1):
				if (l_num_dates[i] > l_num_dates[j]):
					temp = l_num_dates[i]
					l_num_dates[i] = l_num_dates[j]
					l_num_dates[j] = temp
					    
					temp = dates[i]
					dates[i] = dates[j]
					dates[j] = temp
	    
		return dates
		
#=====BackUp class=====
class BackUp:
	def __init__(self):
		self.path_to_rar="" #
		self.l_exclude = [] ##list with exlude file names who will archived
		self.l_all = []
		self.l_current = []
		self.l_previous = []
		
		self.current_log = "current_log.txt" ##file with current log of hashs of files 
		self.previous_log = "previous_log.txt" ##file with previous log of hashs of files
		self.dirs = [] ##list with directories who will backed up
		self.archive_name = str(time.strftime("%d.%m.%Y")) ##set default name of archive
		
		if (platform.system() == "Windows"):
		  self.archive_name += ".rar"
		else:
		  self.archive_name += ".tar.gz"
		  
	def setArchiveName(self, name):
		"""
		'setArchiveName()' method, set name of archive
		args:
		name - name of archive
		"""
		self.archive_name = name + "_" + str(time.strftime("%d.%m.%y")) ##after name set current date
		if (platform.system() == "Windows"): ##if OS is Windows, set .rar at the end
		  self.archive_name += '.rar'
		else:
		  self.archive_name += '.tar.gz' 
	
	def getPathToRar(self):
		"""
		'getPathToRar()' method return path to 'rar.exe'
		this method is only must used if OS is Windows
		"""
		if (platform.sysmte() != "Windows"):
		        return ""
		      
		value = []
		try:
			key = OpenKey(HKEY_CLASSES_ROOT, "WinRAR\shell\open\command",0, KEY_ALL_ACCESS) ##open key from windows registry
			value = QueryValueEx(key,"") ##get value of key
		except:
			return ""
			
		if (len(value)<1):
			return ""
		
		path = ""
		index_slash = 0
		count = 0
		dir = ""
		for i in range(len(value[0])):
			if value[0][i] == '\"':
				if count == 0:
					count = 1
					continue
				else:
					break
					
			if value[0][i] == '\\':
				index_slash = i
			dir+=value[0][i]
		
		if (dir == ""):
			return ""

		dir = dir[:index_slash]
		dir+='rar.exe'
		
		
		if (os.path.isfile(dir)):
			return "\""+ dir + "\""
		return ""
		
	def ReturnCheckSumOfFile(self, filepath, block_size=2**20):
		"""
		'ReturnCheckSumOfFile()' method return hash of file - 'filepath'
		args:
		filepath - absolute path to file
		block_size - block size to read from 'filepath'
		"""
		sha256 = hashlib.sha256()
		
		f10=open('log','wb')
		
		try:
		        f = open(filepath, 'rb')
		except IOError:
		        f10.write("Could not open file \"" + filepath + "\" to reading!\n")
		        f10.close()
		        return ""
		      
		while True:
			try:
			        data = f.read(block_size)
			except IOError:
			        f10.write("Could not read file \"" + filepath + "\"!\n")
			        f.close()
			        f10.close()
			        return ""
			if not data:
				break
			sha256.update(data)
		f.close()
		f10.close()
		return sha256.hexdigest()
		
	def ScanDirChecksums(self, dir_name):
		"""
		'ScanDirChecksums()' - scan dirs and get checksums for every file
		"""
		#print "Current dir: " + dir_name
		l=os.listdir(dir_name)
		
		rd = RecoveryData()
		separator = rd.getSeparator()
		
		##get checksum of files
		for i in range(len(l)):
			if (platform.system()!="Windows"):
			        l[i] = l[i].replace(' ', '\\ ')
			full_path = dir_name + separator + l[i]
			if (full_path == "/dev/core"):
			    continue
			print "full_path:" + full_path
			if (os.path.isdir(full_path)):
				self.ScanDirChecksums(full_path)
			else:
				if (os.path.isfile(full_path) == False):
				        continue
				check_sum = self.ReturnCheckSumOfFile(full_path)
				if check_sum == "":
				    continue
				print "Checksum:" + str(check_sum)
				self.l_current.append([check_sum,full_path+'\n'])
				self.f1.write(check_sum + "  " + full_path + "\n")

	def GetChecksumsOfDirs (self):
		"""
		'GetChecksumsOfDirs()' - get checksums of files from directories ('self.dirs' list)
		"""
		result = False
		print self.dirs
		#time.sleep(5)
		for i in range(len(self.dirs)):
			if (os.path.isdir(self.dirs[i]) == False):
				print "Directory " + self.dirs[i] + " not exist."
				continue
			result = True
			self.ScanDirChecksums(self.dirs[i])
		return result
	
	def LoadListFromFile(self, filename):
		"""
		'LoadListFromFile()' load hash sums of file e. g. self.current_log or self.previos_log files
		args:
		filename - absolute path to file from whom load hash sums 
		"""
		try:
			self.f1 = open(filename,'r')
		except:
			return []
		
		l_hash_path = []
		for str1 in self.f1.readlines():
			if (len(str1)>66):
				l_hash_path.append([str1[:64], str1[66:]])
		return l_hash_path

	def CompareCurrentAndPreviousData(self):
		"""
		'CompareCurrentAndPreviousData()' - compare list with current hash sums and list with previous hash sums
		"""
		index_current = 0
		index_previous = 0
		
		current_count = len(self.l_current)
		previous_count = len(self.l_previous)
		
		f4 = codecs.open('archive_file.txt', 'w', encoding='utf-8')
		
		while True:
			#time.sleep(1)
			
			if (index_current == current_count):
				break
			if (index_previous == previous_count):
				while (index_current<current_count):
					self.l_exclude.append(self.l_current[index_current][1])
					exclude = self.l_current[index_current][1].replace('\n', '')
					#exclude = exclude[3:]
					
					print exclude
					if(platform.system() == "Windows"):
					  exclude = "\"" + exclude + "\""
					  f4.write(exclude + "\r\n")
					else:
					  exclude = exclude.decode('utf-8')
					  f4.write(exclude + "\n")
					index_current+=1
				break
			print "Current:" + self.l_current[index_current][1] + " Previous: " + self.l_previous[index_previous][1]
				
			if (self.l_current[index_current][1] < self.l_previous[index_previous][1]): ##new file
				self.l_exclude.append(self.l_current[index_current][1])
				exclude = self.l_current[index_current][1].replace('\n', '')
				#exclude = exclude[3:]
				
				if(platform.system() == "Windows"):
					  exclude = "\"" + exclude + "\""
					  f4.write(exclude + "\r\n")
				else:
					  exclude = exclude.decode('utf-8')
					  f4.write(exclude + "\n")
				index_current+=1
				#print "Current < Previous"
				continue
			if (self.l_current[index_current][1] > self.l_previous[index_previous][1]): ##file has been deleted
				index_previous+=1
				#print "Current > Previous"
				continue
			
			if (self.l_current[index_current][0] != self.l_previous[index_previous][0]): ##file is changed
				#print "Different hashcode."
				self.l_exclude.append(self.l_current[index_current][1])
				exclude = self.l_current[index_current][1].replace('\n', '')
				#exclude = exclude[3:]
				
				if(platform.system() == "Windows"):
					  f4.write(exclude + "\r\n")
					  exclude = "\"" + exclude + "\""
				else:
					  exclude = exclude.decode('utf-8')
					  f4.write(exclude + "\n")
				
			index_current+=1
			index_previous+=1
			
		f4.close()
	
	def CreateArchive(self):
		"""
		'CreateArchive()' method create archive with list of files from 'archive_file.txt'
		"""
		if (platform.system() == "Windows"):
		  self.path_to_rar = self.getPathToRar()
		  if self.path_to_rar == "":
			  print "WinRar is not installed. Please install it, before use this script!"
			  return
		
		if (platform.system() == "Windows"):
		  command = self.path_to_rar + ' a .\\' + self.archive_name + ' @archive_file.txt'
		else:
		  command = "tar -pczf " + self.archive_name + " `cat archive_file.txt`"
		print "command: " + command
		os.system(command)
	
	def startTimer(self):
		"""
		'startTimer()' method start timer
		"""
		self.start_millis = int(round(time.time() * 1000))
	
	
	def endTimer(self):
		"""
		'endTimer()' method stop timer and print elapsed time
		"""
		##end time of timer
		end_millis = int(round(time.time() * 1000))
		print "Elapsed time: " + str(end_millis - self.start_millis)
	
	def createBackUp(self):
		"""
		'createBackUp()' method create back up 
		"""
		##start timer
		self.startTimer()
		
		##delete previos_log
		try:
			os.remove(self.previous_log)
		except:
			print "Can't remove: " + self.previous_log
		
		##rename current log name to previous log name
		try:
			os.rename(self.current_log, self.previous_log)
		except:
			print "Can't rename current log file - \"" + self.current_log  + "\" to previous log file - \"" + self.previous_log + "\"."
		
		self.f1 = open (self.current_log, "w") ##if file not exist
		
		if len(self.dirs) == 0:
		  print "You cannot set list from directories whom will make back up. For example self.dirs = [\'/home/user\', '/home/user2/Programing\']."
		  system.exit(0)
		
		if (self.GetChecksumsOfDirs() == False):
			print "Error: File \"" + self.dirs + "\" is empty or directories in it not exist!"
			sys.exit(0)

		self.f1.close()
			
		self.l_previous = self.LoadListFromFile(self.previous_log)

		if (len(self.l_current)>0):
			for i in range(len(self.l_current)):
				if (len(self.l_current[i])>0):
					self.l_all.append(self.l_current[i][1])

		self.CompareCurrentAndPreviousData()

		for i in self.l_exclude:
			self.l_all.remove(i)

		f5 = open ('exclude_files.txt', 'w')
		for i in range (len(self.l_all)):
			test=self.l_all[i][2:]
			test = test.replace('\n','')
			if platform.system() == "Windows":
			  f5.write('\".'+test+"\"\n")
			else:
			  print "test:" + test
			  f5.write(test + '\n')
		f5.close()	
		self.CreateArchive()
		
		

if __name__ == '__main__':
    pass
    #bu = BackUp()
    #bu.dirs = ['/var']
    #bu.setArchiveName("var")
    #bu.createBackUp()