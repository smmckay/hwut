import hwut.auxiliary as aux
import hwut.io        as io
import hwut.common    as common
#
import os
import sys


def this(TestFileList):

    if TestFileList == [] or TestFileList == [""]:
        return [], []

    TestFileList.sort()

    unmade_file_list = []
    made_file_list   = []

    for file in TestFileList:
        # "make -q" returns 0 if the target is already up-to-date
        if os.system("make -q %s" % file) == 0: made_file_list.append(file)
        else:                                   unmade_file_list.append(file)

    # -- delete any file to be made, 
    for file in unmade_file_list:
        try: 
           os.remove(file)
           io.on_delete_file_out_of_date(file)
        except:
           pass 

    # -- if the make version is gnu-make, it supports multiple jobs 
    #    (needs to be changed/deleted for non-gnu systems)
    # -- combine make process in bunches according to the job number
    bunch_list = []
    L          = len(unmade_file_list)
    JobN       = common.MAX_CPU_NUMBER
    for i in range(L/JobN + 1):
        bunch = unmade_file_list[JobN*i:min(JobN*(i+1),L)]
        if bunch == []: break
        bunch_list.append(bunch)

    for bunch in bunch_list:
        gnu_make_job_str = "--jobs=%s" % JobN

        io.on_make_bunch_of_test_programs(bunch)
        aux.execute_this("make", [gnu_make_job_str] + bunch)

        # -- check if required files have been made
        for file in bunch:
            if os.access(file, (os.F_OK | os.X_OK)):
                del unmade_file_list[unmade_file_list.index(file)]
                made_file_list.append(file)

    if unmade_file_list != []: 
        io.on_error_make_failed(unmade_file_list)

    return made_file_list, unmade_file_list

def simply_this(MakeTarget):
    if MakeTarget == "": return

    JobN       = common.MAX_CPU_NUMBER
    gnu_make_job_str = "--jobs=%s" % JobN
    aux.execute_this("make", [gnu_make_job_str] + [MakeTarget])

def is_makefile_present():
    makefiles = aux.find("./", "-name [mM]akefile")
    if makefiles != []: return True
    else:               return False

def get_makeable_application_list():
    if is_makefile_present() == False: return []
    program_list = aux.execute_this("make", ["hwut-info"]).split()

    if program_list == []:
        io.on_makefile_does_not_contain_target_hwut_info(os.getcwd())
        sys.exit(-1)

    return map(aux.strip_dot_slash, program_list)

