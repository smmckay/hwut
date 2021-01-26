import os
import time
from   copy import deepcopy
#
import hwut.make      as make
import hwut.common    as common
import hwut.auxiliary as aux
import hwut.directory as directory
import hwut.io        as io
from   hwut.strategies.core import test_info
from   hwut.frs_py.string_handling import trim
#
import xml.sax       as sax
from xml.sax.handler import feature_namespaces

class TestApplicationChoice:
    def __init__(self, Name, Result="", TimeToExecute=0.0):
	self.name                = Name
	self.result              = Result
	self.time_to_execute_sec = TimeToExecute


class TestApplication:
    def __init__(self, Filename):
        self.clear()
	self.file_name = Filename

    def clear(self):
        self.file_name         = ""
        self.group             = ""
        self.title             = ""
        self.misc              = ""
        self.choice_list       = []
        self.results           = []
        self.make_successful_f = False
	self.make_required_f   = False
	self.hwut_info_request_system_time = -1L

    def parse_hwut_info(self, HwutInfoStr):
        idx = HwutInfoStr.find("\n")

        if idx == -1: 
            self.__parse_title(HwutInfoStr)
        else:         
            self.__parse_title(HwutInfoStr[:idx])
            self.misc  = HwutInfoStr[idx:]

        # -- interpret the 'misc' part
        self.__parse_misc()
                
    def write_xml(self, fh):

	make_required_str = "False"
	if self.make_required_f: make_required_str = "True"

        txt  = '<test title="%s" make-required="%s" time-sum-sec="%.2f"> \n' % \
		(str(self.title), make_required_str, self.compute_time_sum())

        txt += '    <application file-name="%s" info-request-time="%s"/>\n' % \
	       (str(self.file_name), repr(self.hwut_info_request_system_time))

	if self.make_required_f:
	    make_successful_str = "False"
	    if self.make_successful_f: make_successful_str = "True"
	    txt += '    <make-procedure success="%s" />\n' % make_successful_str

	txt += '    <choice-list number="%s">\n' % len(self.choice_list)
	for choice in self.choice_list:
	    txt += '       <choice name="%s" result="%s" time-sec="%.2f"/>\n' % \
		    (choice.name, choice.result, choice.time_to_execute_sec)
	txt += "    </choice-list>\n"

        txt += "</test>"

        indent = "    "
        if self.group != "": indent = indent * 2
        fh.write(indent + txt.replace("\n", "\n" + indent) + "\n")
   
    def request_information_if_necessary(self):
	"""At this point, it is required that the application is made. Hwut wants
	   to use the multi-thread feature of make. Thus multiple applications shall
	   be best made in one beat. Here, we require that the application has been 
	   build before, thus no call the make shall be required here.
	"""
	if self.make_required_f and not self.make_successful_f: 
	    io.on_information_required_from_unmade_file(self.file_name)
	    return

	if self.choice_list == []:
	    self.title   = "(Title: information not available)"
	    self.choice_list = [ TestApplicationChoice("") ]
        
	assert os.access(self.file_name, os.F_OK), \
	       "Entry in database that has no application related to it. This should not happen!\n" + \
	       "File '%s' must exist in\n" % self.file_name + \
	       "directory '%s'\n" % os.getcwd()

	modification_time = long(os.stat(self.file_name).st_mtime)
	if self.hwut_info_request_system_time < modification_time:
	    # Ask the application a serious question ...
	    io.on_update_program_entry_info(self.file_name)
	    info_str = aux.execute_this(aux.ensure_dot_slash(self.file_name), ["--hwut-info"])
	    # Parse the reply from the program
	    self.parse_hwut_info(info_str)
	    self.hwut_info_request_system_time = modification_time

    def compute_time_sum(self):
	sum = 0.
	for choice in self.choice_list:
	    sum += choice.time_to_execute_sec
	return sum

    def consistency_check(self):
	"""Check if things make sense.
	"""
	choice_name_list = map(lambda x: x.name, self.choice_list)
	for choice_name in choice_name_list:
	    if choice_name_list.count(choice_name) != 1:
		io.on_database_entry_consistency_check_choice_more_than_once(entry, choice_name)
		return False
	    if choice_name == "" and len(choice_name_list) != 1:
		io.on_database_entry_consistency_check_empty_choice_in_multiple_choices(entry)
		# empty choice and multiple choices cannot be
		return False
	return True

    def __parse_title(self, TitleStr):  
        """Parse title into 'group' and 'sub-title' if there is a colon.
        """
        field_list = TitleStr.split(":")
        field_list = map(trim, field_list)
        if len(field_list) > 1: self.group = field_list[0]; self.title = field_list[1]
        else:                   self.group = "";            self.title = field_list[0]

    def __parse_misc(self):
	if self.choice_list == []:
	    self.choice_list = [ TestApplicationChoice("") ]

	def __handle_new_choice(NewChoiceNameList):
	    for choice_name in NewChoiceNameList:
		if choice_name == "": continue
		if choice_name not in map(lambda x: x.name, self.choice_list):
		    self.choice_list.append(TestApplicationChoice(choice_name, "NONE"))

	def __handle_lost_choices(NewChoiceNameList):
	    for choice in self.choice_list:
		if choice.name not in NewChoiceNameList:
		    idx = self.choice_list.index(choice)
		    del self.choice_list[idx]

        # -- find additional 'commands' and information
        for line in self.misc.split(";"):
            fields = line.split()
            if len(fields) < 2: continue
            # -- choices: only one of them can be active at a time
            if fields[0] == "CHOICES:":
                new_choices = line[line.find("CHOICES:") + len("CHOICES:"):].split(",")
                new_choices = map(lambda p: trim(str(p)), new_choices)
		__handle_new_choice(new_choices)
		__handle_lost_choices(new_choices)

    def __repr__(self):
        txt  = "GROUP:         " + self.group                         + "\n"
        txt += "TITLE:         " + self.title                         + "\n"
        txt += "FILE:          " + self.file_name                     + "\n"
	txt += "MAKE REQUIRED: " + str(type(self.make_required_f))       \
		                 + str(self.make_required_f)          + "\n"
	if self.make_required_f:
	    txt += "MAKE SUCCESS:  " + str(type(self.make_successful_f)) \
	                             + str(self.make_successful_f)    + "\n"
        
        txt += "CHOICES:       " 
	for choice in self.choice_list:
	    txt += "'%s'(%s), " % (choice.name, choice.result)

	return txt[:-2]


class HWUT_XML_Parser(sax.ContentHandler):

    def __init__(self, related_db):
	self.__current_group = ""
        self.__tmp           = TestApplication("")
        self.related_db      = related_db

    def startElement(self, name, attribute_list):
	def __get(Attribute):
	    if not attribute_list.has_key(Attribute):
		io.xml_missing_attribute(name, Attribute)
		return str("(empty)")
	    else:
		return str(attribute_list[Attribute])

	def __get_bool(AttributeName):
	    AttributeValue = __get(AttributeName)
	    if   AttributeValue == "True":  return True
	    elif AttributeValue == "False": return False
	    else:
		raise BaseException("Content of attribute '%s' must be True or False" % AttributeName)

	if name == "test-database":
	    self.related_db.XML_PARSER_set_referred_date(__get("date"))

	elif name == "group":
	    self.__current_group = __get("name")

        elif name == "test":  
            self.__tmp.clear()
            self.__tmp.title           = __get("title")
	    self.__tmp.make_required_f = __get_bool("make-required")

	elif name == "application":
	    self.__tmp.file_name                     = __get("file-name")
	    self.__tmp.hwut_info_request_system_time = long(__get("info-request-time"))

        elif name == "make-procedure":     
	    self.__tmp.make_successful_f = __get_bool("success") 

        elif name == "choice":      
            choice = __get("name")
            result = __get("result")
	    self.__tmp.choice_list.append(TestApplicationChoice(choice, result))

    def endElement(self, name):
	if name == "group":
	    self.__current_group = ""
        elif name == "test":        
	    self.__tmp.group = self.__current_group
	    self.related_db.XML_PARSER_add_entry(self.__tmp)

    def characters(self, Content):
	pass


                        
class TestApplicationDB:
    def __init__(self):
	self.db        = {}   # map: [application file-name] --> [test information]
        self.directory = None
	self.__referred_date = ""

    def init(self, TestApplicationSelection=[]):
        """Initializes the database for all applications in the 
           current directory. If a database file is present, then 
           this file is read and used. Following rules hold:

           -- Old entries from a db are deleted if the corresponding
              application in the current directory is not available
              (either as executable or make-able file).

           -- New entries are entered if an executable or make-able
              application is not found in the db. In this case,
              a make-process may be started (if the application is makeable).
              This is necessary, because the title and the choices need
              to be aquired from the application.

           -- An entry is updated, if the corresponding application is
              younger than then db file or if the application does not
              exist and is make-able.

        """
	self.db.clear()
	self.directory = os.getcwd()

	# -- load xml database for current directory
	self.__parse_xml_database()

        executable_application_list = directory.get_executable_application_list()
	makeable_application_list   = make.get_makeable_application_list()

	# -- if no selection of test applications is defined, then take what there
	#    is in the current directory.
	if TestApplicationSelection == []:
	    unique = {}
	    for application in executable_application_list + makeable_application_list:
		unique[application] = True
	    TestApplicationSelection = unique.keys()


	# -- checkout applications that are not executables and cannot be built by make
	executable_selection = []
	makeable_selection   = []
	for application in TestApplicationSelection:
	    application = aux.strip_dot_slash(application)

	    # Check for makeability first, because a file might be executable that is 
	    # actually to be built by 'make'.
            if   application in makeable_application_list:
		makeable_selection.append(application)
	    elif application in executable_application_list:
		executable_selection.append(application)
	    else:
		io.on_file_not_executable_and_not_makeable(application, makeable_application_list)
	       
	# -- ensure that all makeable test applications are made and up-to-date
	made_selection, unmade_selection = make.this(makeable_selection)

	# -- ensure that any test application has a correspondent entry in the db
	#    (applications, where the 'made' failed can be labeled as such)
	self.__ensure_database_entries_exist(executable_selection, 
		                             made_selection, unmade_selection)

	# -- clean database from entries, that no longer exist
	self.__handle_vanished_applications(executable_application_list 
		                            + makeable_application_list)

    def write(self):
        """Writes all existing information about files into a database."""
        assert self.directory == os.getcwd(), \
               "No cache file defined. 'init()' function must be called before this function."

        if self.directory != os.getcwd(): self.init() 

        test_fh = open(common.HWUT_CACHE_FILE, "w")
        test_fh.write('<test-database execution-time-sec="%.2f" date="%s">\n' % \
		      (self.compute_time_sum(), time.asctime()))

        # sort entries by group
        items = self.db.items()
        items.sort(lambda a, b: cmp(a[1].group, b[1].group))

        current_group = ""
        for file_name, entry in items:
            if entry.group != current_group: 
                if current_group != "":
                    test_fh.write("    </group>\n")
                test_fh.write("    <group name=\"%s\">\n" % entry.group)
                current_group = entry.group
            entry.write_xml(test_fh)

        if current_group != "":
            test_fh.write("    </group>\n")
        test_fh.write("</test-database>\n")

    def compute_time_sum(self):
	sum = 0.
	for entry in self.db.values():
	    sum += entry.compute_time_sum()
	return sum

    def get_test_execution_sequence(self, SpecificApplicationList=[], FailedOnlyF=False, 
                                    SpecificChoice=""):
        assert type(SpecificApplicationList) == list
	assert type(FailedOnlyF) == bool
	assert SpecificChoice == None or type(SpecificChoice) == str

        if self.directory != os.getcwd(): 
	    self.init(SpecificApplicationList) 

        # -- collect entries that belong to the specified applications (or take all)
        if SpecificApplicationList == []: 
            entry_list = self.db.values()
        else:
            entry_list = []
            for application in SpecificApplicationList:
                entry_list.append(self.db[application])

        # -- sort entries by group
        entry_list.sort(lambda a, b: cmp(a.group, b.group))
	
        i = -1
        sequence = []
        for entry in entry_list:
            sequence_for_entry, i = self.__sequentialize_sub_experiments(i, entry, 
                                                                         FailedOnlyF, SpecificChoice)
            if sequence_for_entry != []: 
                sequence.extend(sequence_for_entry)

        return sequence

    def XML_PARSER_add_entry(self, Entry):
	# No initialization required here! no self.init()
	# This function is called during initialization.

        file_name = aux.strip_dot_slash(Entry.file_name)

        if self.db.has_key(file_name): 
            io.on_database_contained_entry_multiple_times(file_name)
            return

	if Entry.consistency_check() == False:
	    io.on_xml_database_entry_consistency_check_failed(Entry)
	    self.db[file_name] = TestApplication(filename) # empty, so it is going to be updated
	else:
	    self.db[file_name] = deepcopy(Entry)

    def XML_PARSER_set_referred_date(self, DateStr):
	self.__referred_date = DateStr

    def get_referred_date(self):
	if self.directory != os.getcwd():
	    self.init()
	return self.__referred_date 

    def __parse_xml_database(self):
        # Create a parser
        parser = sax.make_parser()

        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)

        # Create the handler
        dh = HWUT_XML_Parser(self)

        # Tell the parser to use our handler
        parser.setContentHandler(dh)

        # Parse the input
        try:    
	    info_fh = open(common.HWUT_CACHE_FILE)
        except: 
	    io.on_database_not_found(os.getcwd())
	    return

	try:
	    parser.parse(info_fh)
	except:
	     io.on_xml_database_parsing_error()
	     self.db.clear()

	info_fh.close()

    def __sequentialize_sub_experiments(self, StartIdx, entry, FailedOnlyF, SpecificChoice):
	"""A database entry may provide multiple choices for one application.
	   The application is then to be called multiple times, each time with
	   a different choice as a command line argument. This function builds
	   a list of application calls for a given set of choices. If
	   the SpecificChoice is specified, then only one element is created.
	"""

        sequence   = []
        i          = StartIdx
        for choice in entry.choice_list:
            i      += 1

            if FailedOnlyF and choice.result != "FAIL":
                continue

            if SpecificChoice != "" and choice.name != SpecificChoice:
		continue 

	    present_f = True
	    if entry.make_required_f and not entry.make_successful_f: present_f = False

	    sequence.append(test_info(entry, i, choice, present_f))

        return sequence, i

    def __handle_vanished_applications(self, TestApplicationList):
        """ Check for entries that no longer correspond to available applications
	    DELETE entries that have no application (i.e. no executable or makeable)
	"""
        database_application_list = map(aux.strip_dot_slash, self.db.keys())
        for file_name in database_application_list:
            if file_name not in TestApplicationList:
                io.on_database_entry_not_available(file_name)
                del self.db[file_name]

    def __ensure_database_entries_exist(self, ExecutableList, MadeList, UnmadeList):
	"""Ensures that for any application in ExecutableList, MadeList, and UnmadeList
	   a database entry exists. As for applications in the UnmadeList the
	   make_successful_f will be set to False.
	"""

	def __consider_this(ApplicationFilename, MakeRequiredF, MakeSuccessF):
	    """-- if no entry for Application in DB, then add a new one. 
	       -- adapt 'make_required_f' and 'make_successful_f'
	    """
	    if not self.db.has_key(ApplicationFilename): 
		self.db[application] = TestApplication(ApplicationFilename)
	    
	    entry = self.db[ApplicationFilename]
	    entry.make_required_f   = MakeRequiredF
	    entry.make_successful_f = MakeSuccessF

	    entry.request_information_if_necessary()

	for application in ExecutableList:
	    __consider_this(application, False, False)

	for application in MadeList:
	    __consider_this(application, True, True)

	for application in UnmadeList:
	    __consider_this(application, True, False)

