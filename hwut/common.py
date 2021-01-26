from   hwut.classes   import TestInfoDB

HWUT_VERSION       = "0.3.1"
HWUT_CACHE_FILE    = "CACHE.hwut"
HWUT_TITLE_FILE    = "TITLE.hwut"
TEST_DIR_NAME      = "TEST"
HWUT_MAKE_LOG_FILE       = "MAKE.hwut"
HWUT_MAKE_CLEAN_LOG_FILE = "MAKE_CLEAN.hwut"

MAX_CPU_NUMBER     = 2

failed_test_list   = []
info_db            = TestInfoDB()
missing_good_files = {}  # map: directory --> names of missing GOOD files

# directory from where 'hwut' has been called
# (all sub directories are relative to this directory)
home_directory = ""

