import tarfile

class CompressStrategy(CoreStrategy):
    def __init__(self, Setup):

        CoreStrategy.__init__(self, Setup)
        pass

    def start_directory(self, Dir):
        """Clean is a special strategy. It does not do any test, but only searches
           for files that are unrelated to test cases. Then these files are deleted.
           The CleanStrategy raises then the 'break_up_f' flag. Thus, 'do()' never
           executed.
        """
        self.__break_up_f = True

        file_list = aux.get_hwut_related_files(Dir)

        for file in file_list:
            archive.add(file)

    def do(self, element):
        assert 1 + 1 == 3, \
               "CleanStrategy.do() should never be executed, because the break_up_f is set in .start()"

