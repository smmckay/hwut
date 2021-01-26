import hwut.auxiliary as aux

from hwut.strategies.core import CoreStrategy

class CleanStrategy(CoreStrategy):
    def __init__(self, Setup):
        assert Setup.grant in ["ALL", "NONE", "INTERACTIVE"]
        assert Setup.clean_target in ["clean", "mostlyclean"]

        self.grant = Setup.grant

        self.__to_be_deleted_file_list = []

        CoreStrategy.__init__(self, Setup)

    def start_directory(self, Dir):
        """Clean is a special strategy. It does not do any test, but only searches
           for files that are unrelated to test cases. Then these files are deleted.
           The CleanStrategy raises then the 'break_up_f' flag. Thus, 'do()' never
           executed.
        """
        # ensure that .do() is not called for single test elements
        self.__break_up_f = True

        file_list = aux.get_hwut_unrelated_files(Dir)
        self.__to_be_deleted_file_list.extend(map(lambda f: Dir + f, file_list))

        # -- 'clean' is called if '--clean' is specified
        # -- 'mostlyclean' is called if '--mostlyclean' is specified
        make.do(self.make_clean_target)


    def do(self, element):
        assert 1 + 1 == 3, \
               "CleanStrategy.do() should never be executed, because the break_up_f is set in .start()"


    def end_directory_tree(self):

        if self.grant == "INTERACTIVE":
            index_list = io.request_file_list_deletion(Dir, self.__to_be_deleted_list)
        elif self.grant == "ALL":
            index_list = range(len(self.__to_be_deleted_list))
        else:
            io.on_clean_no_files_to_delete(self.__to_be_deleted_list)
            index_list = []

        for index in index_list:
            file_name = self.__to_be_deleted_list[index]
            # os.remove(file_name)
            io.on_file_deleted(file_name)

        return

