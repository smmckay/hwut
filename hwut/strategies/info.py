import hwut.io as io
import hwut.common as common
from hwut.strategies.core import CoreStrategy

class InfoStrategy(CoreStrategy):
    def __init__(self, Setup):
        self.directory = "/dev/null/"
        CoreStrategy.__init__(self, Setup)

    def start_directory(self, Dir):
        self.directory = Dir
        self.failed_test_list = []

    def do(self, Element):
        """NOTE: The printout already happens by the hwut.core framework,
                 so there is not much to be done here.
        """
        if Element.last_result not in ["OK", "NO GOOD FILE", "DONE"]: 
            self.failed_test_list.append(Element)

        return Element.last_result

    def end_directory(self):
        self.directory = "/dev/null/"
        if self.failed_test_list != []: 
            io.print_failure(self.directory, self.failed_test_list)
            return "FAIL"
        else:           
            io.print_ok(self.directory)
            return "OK"

    def xml_database_write_permission(self):
        return False

    def get_referred_date(self):
        """In the info strategy the date is printed, when the test results were safed.
        """
        return common.application_db.get_referred_date()
