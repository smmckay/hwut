import time

class test_info:

    def __init__(self, Entry, ID, Choice, ProgramPresentF):
        assert type(ProgramPresentF) == bool
        assert Choice.__class__.__name__ == "TestApplicationChoice", \
               "type(Choice) == str! receive '%s'" % repr(Choice)
        assert type(ID) == int
        assert Entry.__class__.__name__ == "TestApplication"

        choice_name_list = map(lambda x: x.name, Entry.choice_list)
        assert Choice.name in choice_name_list, \
                "Choice '%s' not in choice list: " % Choice + repr(choice_name_list)
        assert Entry.choice_list != []

        self.related_entry = Entry
        self.group        = Entry.group
        self.program      = Entry.file_name
        self.execution_id = ID
        self.choice       = Choice.name
        self.choice_idx   = choice_name_list.index(self.choice)
        self.last_result  = Entry.choice_list[self.choice_idx].result
        self.present_f    = ProgramPresentF
        self.thread       = None

    def __repr__(self):
        txt  = "PROGRAM: " + self.program + "\n"
        txt += "CHOICE:  " + self.choice  + "\n"  
        return txt

class CoreStrategy:

    def __init__(self, FailedOnlyF):
        self.__break_up_f    = False
        self.__failed_only_f = FailedOnlyF

    def start_directory_tree(self, DirectoryList):
        pass

    def start_directory(self, Dir):
        pass

    def do(self, element):
        print "Strategy::do(element) not implemented"
        sys.exit(0)

    def end_directory_tree(self):
        return None # default: no result

    def end_directory(self):
        return None # default: no result

    def break_up_requested(self):
        return self.__break_up_f

    def handle_only_failed_experiments(self):
        return self.__failed_only_f

    def xml_database_write_permission(self):
        return True

    def get_referred_date(self):
        return time.asctime()
