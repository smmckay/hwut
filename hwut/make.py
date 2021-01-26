from   hwut.aux import find, execute_this
import hwut.io     as io
import hwut.common as common
#
import os
import sys


def this(TestFileList):

    if TestFileList == []:
	return

    # -- if the make version is gnu-make, it supports multiple jobs 
    #    (needs to be changed/deleted for non-gnu systems)
    execute_this("make", ["clean"], common.HWUT_MAKE_CLEAN_LOG_FILE)

    # -- combine make process in bunches according to the job number
    bunch_list = []
    L          = len(TestFileList)
    JobN       = common.MAX_CPU_NUMBER
    for i in range(L/JobN + 1):
	bunch = TestFileList[JobN*i:min(JobN*(i+1),L)]
	if bunch == []: break
	bunch_list.append(bunch)

    unmade_file_list = []
    for bunch in bunch_list:
	gnu_make_job_str = "--jobs=%s" % JobN

	io.on_make_bunch_of_test_programs(bunch)
	execute_this("make", [gnu_make_job_str] + bunch)

	# -- make sure that all required files have been made
	for file in bunch:
	    if not os.access(file, os.F_OK):
		unmade_file_list.append(file)

    if unmade_file_list != []: 
	io.on_error_make_failed(unmade_file_list)

    return unmade_file_list

def clean():
    os.system("make clean")

def is_makefile_present():
    makefiles = find("./", "-name [mM]akefile")
    if makefiles != []: return True
    else:               return False

def get_program_list():
    if is_makefile_present() == False: return []
    program_list = execute_this("make", ["hwut-info"]).split()

    if program_list == []:
	io.on_makefile_does_not_contain_target_hwut_info(common.home_directory)
	sys.exit(-1)

    return program_list

