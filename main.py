import typing

# Click `Run` in the top left corner to run the command line program. Output will appear in the "Program Output" tab in the right pane.


class SigmaFileSystem:

    def __init__(self):
        # store each file type as a dictionary, with key be the folder and values be the files of the given type
        self.dashboard = {}  # {fileId:folderId}
        self.worksheet = {}
        self.folder = {}
        self.all_files = {}  # store a dict with all files
        self.rootId = 0  # rootId set to default

    # Feel free to modify the parameter/return types of these functions
    # as you see fit. Please add comments to indicate your changes with a
    # brief explanation. We care more about your thought process than your
    # adherence to a rigid structure.

    def get_total_dashboards(self) -> int:
        return len(self.dashboard)

    def get_total_worksheets(self) -> int:
        return len(self.worksheet)

    # Add new file
    def add_new_file(self, fileName: str, fileType: str, folderId: int) -> None:
        # If file type is dashboard
        if fileType == 'dashboard':
            id = '1100' + str(len(self.dashboard))
            # If folder already exists in dashboard, add it to folder
            if folderId in self.dashboard:
                # todo: duplicate file name?
                id = int(id + str(len(self.dashboard[folderId])))
                self.dashboard[folderId][fileName] = id
            # create a new key [folder] in dashboard dict, and add fileName to folder
            else:
                id = int(id+"0")
                self.dashboard[folderId] = {fileName: id}
            self.all_files[id] = [fileName, folderId]
        # If file type is worksheet
        elif fileType == 'worksheet':
            id = '1010' + str(len(self.worksheet))
            if folderId in self.worksheet:
                # todo: duplicate file name?
                id = int(id + str(len(self.worksheet[folderId])))
                self.worksheet[folderId][fileName] = id
            else:
                id = int(id+"0")
                self.worksheet[folderId] = {fileName: id}
            self.all_files[id] = [fileName, folderId]
        # If file type is folder
        elif fileType == 'folder':
            id = '1001' + str(len(self.worksheet))
            if folderId in self.folder:
                # todo: duplicate file name?
                id = int(id + str(len(self.folder[folderId])))
                self.folder[folderId][fileName] = id
            else:
                id = int(id+"0")
                self.folder[folderId] = {fileName: id}
            self.all_files[id] = [fileName, folderId]
        return

    def get_file_id(self, fileName: str, folderId: int) -> int:
        # if fileName is root file, returns default rootId
        if fileName == "MyDocuments":
            return self.rootId
        # if the folder that contains the file is in dashboard dict
        if folderId in self.dashboard and fileName in self.dashboard[folderId]:
            print(1)
            # if file in dashboard
            if fileName in self.dashboard[folderId]:
                return self.dashboard[folderId][fileName]
        # if the folder that contains the file is in worksheet dict
        elif folderId in self.worksheet and fileName in self.worksheet[folderId]:
            print(2)
            if fileName in self.worksheet[folderId]:
                return self.worksheet[folderId][fileName]

        # if the folder that contains the file is in folder dict
        elif folderId in self.folder and fileName in self.folder[folderId]:
            print(3)
            if fileName in self.folder[folderId]:
                return self.folder[folderId][fileName]
        else:
            print(fileName, ":file doesn't exist")

    def move_file(self, fileId: int, newFolderId: int) -> None:
        if fileId not in self.all_files:
            print("Move file but file doesn't exist")
            return
        fileName, folderId = self.all_files[fileId]
        del self.all_files[fileId]
        if folderId == newFolderId:
            print("file is already in the folder")
            return

        # delete the file in old folder
        # if folderId in self.dashboard:
        #     if fileName in self.dashboard[folderId]:
        #         del self.dashboard[folderId][fileName]
        #         self.add_new_file(fileName, 'dashboard', newFolderId)
        # elif folderId in self.worksheet:
        #     if fileName in self.worksheet[folderId]:
        #         del self.worksheet[folderId][fileName]
        #         self.add_new_file(fileName, 'worksheet', newFolderId)
        # elif
        if folderId in self.folder:
            if fileName in self.folder[folderId]:
                del self.folder[folderId][fileName]
                if self.folder[folderId] == {}:
                    del self.folder[folderId]
                self.add_new_file(fileName, 'folder', newFolderId)

    def get_files(self, folderId: int) -> typing.List[str]:
        res = []
        if folderId in self.dashboard:
            res.extend(self.dashboard[folderId].keys())
        if folderId in self.worksheet:
            res.extend(self.worksheet[folderId].keys())
        if folderId in self.folder:
            res.extend(self.folder[folderId].keys())
        return res

    def print_files(self) -> None:
        # TODO: implement
        res = {"MyDocuments": {"Folders": [], "Documents": {
            "Dashboards": [], "Worksheets": []}}}
        for folder in self.dashboard:
            res["MyDocuments"]["Documents"]["Dashboards"].extend(
                self.dashboard[folder].keys())
        for folder in self.worksheet:
            res["MyDocuments"]["Documents"]["Worksheets"].extend(
                self.worksheet[folder].keys())
        for folder in self.folder:
            res["MyDocuments"]["Folders"].extend(self.folder[folder].keys())
        print(res)
        return


# /////////////////////////////////////////////////////////
# // YOU DO NOT NEED TO MAKE CHANGES BELOW UNLESS NECESSARY
# /////////////////////////////////////////////////////////

# PLEASE ENSURE run_example() RUNS BEFORE SUBMITTING.
def run_example():
    fs = SigmaFileSystem()

    rootId = fs.get_file_id("MyDocuments", None)
    fs.add_new_file("draft", "folder", rootId)
    fs.add_new_file("complete", "folder", rootId)
    draftId = fs.get_file_id("draft", rootId)
    completeId = fs.get_file_id("complete", rootId)
    fs.add_new_file("foo", "worksheet", draftId)
    fs.add_new_file("bar", "dashboard", completeId)
    fooId = fs.get_file_id("foo", draftId)
    fs.move_file(fooId, completeId)

    print(", ".join(fs.get_files(rootId)))
    print(", ".join(fs.get_files(draftId)))
    print(", ".join(fs.get_files(completeId)))

    fs.add_new_file("project", "folder", draftId)
    projectId = fs.get_file_id("project", draftId)

    for filename in ["page1", "page2", "page3"]:
        fs.add_new_file(filename, "worksheet", projectId)

    fs.add_new_file("cover", "dashboard", projectId)
    print(fs.dashboard)
    fs.move_file(projectId, completeId)
    projectId = fs.get_file_id("project", completeId)
    print(projectId)
    coverId = fs.get_file_id("cover", projectId)
    print(coverId)
    fs.move_file(coverId, rootId)

    print(", ".join(fs.get_files(rootId)))
    print(", ".join(fs.get_files(draftId)))
    print(", ".join(fs.get_files(completeId)))
    print(", ".join(fs.get_files(projectId)))

    print(fs.get_total_dashboards())
    print(fs.get_total_worksheets())
    fs.print_files()


def ask_for_int(question: str) -> int:
    val = input(question)
    try:
        return int(val)
    except:
        print('Please enter a valid integer value\n')
        return ask_for_int(question)


def ask_question():
    fs = SigmaFileSystem()
    running = True
    while (running):
        command = ask_for_int(
            "\nEnter an integer to indicate a command: \n[1] get_total_dashboards\n[2] get_total_worksheets\n[3] add_new_folder\n[4] get_file_id\n[5] move_file\n[6] get_files \n[7] print_files\n[8] exit\n")
        if command == 1:
            totalDashboards = fs.get_total_dashboards()
            print("There are {0} dashboards in the file system.".format(
                totalDashboards))
        elif command == 2:
            totalWorksheets = fs.get_total_worksheets()
            print("There are {0} worksheets in the file system.".format(
                totalWorksheets))
        elif command == 3:
            fileName = input("Enter a new file name: ")
            fileType = input(
                "Enter a file type (worksheet, dashboard, or folder): ")
            folderId = ask_for_int(
                "Enter a folder id where you'd like to put this file: ")
            fs.add_new_file(fileName, fileType, folderId)
            print("{0} has been added to folder {1}".format(fileName, folderId))
        elif command == 4:
            fileName = input("Enter the file name: ")
            folderId = ask_for_int("Enter the folder id: ")
            fileId = fs.get_file_id(fileName, folderId)
            print("{0} is file {1}".format(fileName, fileId))
        elif command == 5:
            fileId = ask_for_int("Enter a file id:")
            newFileId = ask_for_int(
                "Enter the folder id where you'd like to move this file: ")
            fs.move_file(fileId, newFileId)
            print("Successfully moved file {0} to folder {1}".format(
                fileId, newFileId))
        elif command == 6:
            folderId = ask_for_int("Enter a folderId:")
            fileNames = fs.get_files(folderId)
            if (len(fileNames) == 0):
                print("There are no files in folder {0}".format(folderId))
            else:
                print(
                    "The following files are in folder {0}: ".format(folderId))
                for fileName in fileNames:
                    print("\t{0}".format(fileName))
        elif command == 7:
            fs.print_files()
        elif command == 8:
            print("Exiting program.")
            running = False
        else:
            print("Invalid command: {0}. Please try again.\n".format(command))


# ask_question()
run_example()
