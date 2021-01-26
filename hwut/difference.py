import os
import hwut.directory as directory
import hwut.common    as common
import hwut.aux       as aux

def show(ProgramName, Choice, DiffProgram="diff", ExecuteF=False):
    """Shows the difference between an output file and the stored 'good' file.
       ARGV contains the list of arguments passed to this program from the 
       command line. It is expected that the name of the program under 
       concern directly follows the '--diff' option.
    """
    if ExecuteF: 
	entry = common.info_db.get(program_name)
        print  # newline after possible "// update:" messages
	if entry != None: perform_test(entry, CreateOnlyOutputF=True) 

    protocol_file_name = aux.get_protocol_filename(ProgramName, Choice)

    os.system("%s OUT/%s GOOD/%s" % (DiffProgram, protocol_file_name, protocol_file_name))
