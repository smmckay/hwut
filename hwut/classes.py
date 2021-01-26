import os
#
import hwut.aux as aux
import hwut.io  as io
from   hwut.frs_py.string_handling import trim

class TestInfo:
    def __init__(self):
	self.__clear()

    def __clear(self):
	self.modification_time = -1L
	self.file_name         = ""
	self.group             = ""
	self.title             = "<no title>"
	self.misc              = ""
	self.choices           = []
	self.results           = ["<no result>"]
	self.present_f         = False

    def parse_file_record(self, Record):
	self.__clear()

	fields = Record.split("\n")
	if len(fields) < 2: return
	idx = fields[0].find("  ")
	self.modification_time = long(fields[0][:idx])
	self.file_name         = fields[0][idx+2:]

	# -- title: optional ':' splits group name and title
        self.__parse_title(fields[1])

	# -- optional things: combine first all into 'misc'
	self.misc = ""
	if len(fields) > 2:
	    for field in fields[2:]:
		self.misc += field

	self.__parse_misc()
	self.present_f = True

    def parse_hwut_info(self, Filename, HwutInfoStr):
	idx = HwutInfoStr.find("\n")

	if idx == -1: 
	    self.__parse_title(HwutInfoStr)
	else:         
	    self.__parse_title(HwutInfoStr[:idx])
	    self.misc  = HwutInfoStr[idx:]

	# -- interpret the 'misc' part
        self.__parse_misc()
	self.file_name = Filename
	self.present_f = True
		
    def write_record(self, fh):
	def nice(the_list):
	    result = ""
	    for element in the_list:
		result += ", " + element
	    if result != "": result = result[2:]	
	    return result
	    
	txt  = repr(long(self.modification_time)) + "  " 
	txt += self.file_name + "\n"
	#
	group = ""
	if self.group != "": group = self.group + ":"
	txt += group + self.title + "\n"
	#
	if self.choices != []:              txt += "CHOICES:  " + nice(self.choices) + ";\n"
	if self.results != ["<no result>"]: txt += "RESULT:   " + nice(self.results) + ";\n"
	#
	fh.write(txt)

    def __parse_title(self, TitleStr):	
	"""Parse title into 'group' and 'sub-title' if there is a colon.
	"""
        field_list = TitleStr.split(":")
	field_list = map(trim, field_list)
        if len(field_list) > 1: self.group = field_list[0]; self.title = field_list[1]
        else:                   self.group = "";            self.title = field_list[0]

    def __parse_misc(self):
	# -- find additional 'commands' and information
	for line in self.misc.split(";"):
	    fields = line.split()
	    if len(fields) < 2: continue
	    # -- choices: only one of them can be active at a time
	    if fields[0] == "CHOICES:":
		self.choices = line[line.find("CHOICES:") + len("CHOICES:"):].split(",")
		self.choices = map(lambda p: trim(p), self.choices)
	    # -- result of the experiment: OK, or FAIL	
	    elif fields[0] == "RESULT:":	
		self.results = line[line.find("RESULT:") + len("RESULT:"):].split(",")
		self.results = map(lambda r: trim(r), self.results)

    def __repr__(self):
        txt  = "GROUP:        " + self.group                         + "\n"
	txt += "TITLE:        " + self.title                         + "\n"
        txt += "FILE:         " + self.file_name                     + "\n"
	txt += "MODIFICATION: " + repr(long(self.modification_time)) + "\n" 
	txt += "PRESENT:      " + repr(self.present_f)               + "\n"
	#
	if self.choices != []:              txt += "CHOICES:  " + nice(self.choices) + ";\n"
	if self.results != ["<no result>"]: txt += "RESULT:   " + nice(self.results) + ";\n"

	return txt

	
class TestInfoDB:
    def __init__(self):
	self.db               = {}
	self.directory        = None
	self.__cache_filename = ""

    def read(self, CacheFileName):
	"""Reads brief info about experiments from a 'cache' file, so they do not 
	   have to be requested each time when an experiment is run.

	   Assumes the current directory (os.getcwd()) to be the directory of concern.
	"""
	# try to find the info file
	try:    info_fh = open(CacheFileName)
	except: self.__cache_filename = CacheFileName; return

	info_str = info_fh.read()
	info_fh.close()	

	info_record_set = info_str.split("\n=====\n")

	self.db = {}
	for record in info_record_set:
	    new_entry = TestInfo()
	    new_entry.parse_file_record(record)
	    self.db[aux.strip_dot_slash(new_entry.file_name)] = new_entry

	self.directory = os.getcwd()
	self.__cache_filename = CacheFileName

    def write(self):
	"""Writes all existing information about files into a database."""
	if self.__cache_filename == "":
	    raise "no cache file defined. 'read()' function must be called before this function."

	info_fh = open(self.__cache_filename, "w")
	for file_name, entry in self.db.items():
	    entry.write_record(info_fh)
            info_fh.write("=====\n")
	info_fh.close()	

    def extract_entries(self, TestProgramList):
	"""Returns a list of (references) to entries in the program data
	   base that relate to the TestProgramList. Note, that the TestEntryDB
	   contains all entries of all files of the directory wherelse,
	   the resulting test_entry_list contains only references to the
	   entries that relate to TestProgramList. Changes to them affect
	   the database. Thus, after changing the entries it is sufficient
	   so save the DB as a whole.
	"""
	# -- sort the test program files 
	TestProgramList.sort()

        test_entry_list = []
	for program in TestProgramList:
	    program = program.replace("\n", " ")
	    # -- get information about the test (either from db or by querying the file)
	    entry = self.__get_entry(program)
	    if entry != None: test_entry_list.append(entry)

	io.on_update_program_entry_info_all_terminated()

	return test_entry_list

    def __get_entry(self, Filename):
	"""Returns an entry to the database about the test program with the given 
	   filename. If the file does not exist, or is not in the database, then
	   a new entry is created.
	"""
	if self.__cache_filename == "":
	    raise "no cache file defined. 'read()' function must be called before this function."

	try:    cachefile_touch_time = os.path.getmtime(self.__cache_filename) 
	except: cachefile_touch_time = -1

	if not self.db.has_key(Filename):
	    self.__create_entry(Filename)

	elif    os.access(Filename, os.F_OK) == False \
	     or os.path.getmtime(Filename) >= cachefile_touch_time:
	    # entry exists but: it is (i) out-dated => delete entry and create new one
	    #                      or (ii) test program does no longer exist in directory
	    del self.db[Filename]
	    self.__create_entry(Filename)

	# -- return entry
	return self.db[Filename]	

    def __create_entry(self, Filename):
	if self.db.has_key(Filename):
	    raise "error:cannot create entry where the original entry still exists in database\n" + \
		  "error: filename = '%s'\n" % Filename

	entry = TestInfo()
	if os.access(Filename, os.F_OK) == False:	
	    entry.file_name = Filename
	    entry.present_f = False
	    self.db[Filename] = entry
	    return entry

	program_name = aux.ensure_dot_slash(Filename)  # program_name: with './' at the beginning
	Filename     = aux.strip_dot_slash(Filename)   # Filename:     without './' at the beginning

	info_str = aux.execute_this(program_name, ["--hwut-info"])

	# -- parse the reply from the program
        entry.parse_hwut_info(Filename, info_str)

	# -- enter info into db
	self.db[Filename] = entry

