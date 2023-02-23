import typing
import uuid

# Click `Run` in the top left corner to run the command line program. Output will appear in the "Program Output" tab in the right pane.


class SigmaFileSystem:

    def __init__(self):
        # store each file type as a dictionary
        self.dashboard = {}  # {fileId:[fileName, folderId]}
        self.worksheet = {}
        self.folder = {}
        # store a dict with all files, {parentId:[childrenId]}
        self.all_files = {}
        self.rootId = 0  # rootId set to default

    # Feel free to modify the parameter/return types of these functions
    # as you see fit. Please add comments to indicate your changes with a
    # brief explanation. We care more about your thought process than your
    # adherence to a rigid structure.

    def get_total_dashboards(self) -> int:
        return len(self.dashboard)

    def get_total_worksheets(self) -> int:
        return len(self.worksheet)

    # def generateId(self, fileType, folderId):
    #     if fileType == 'dashboard':
    #         id = '1100' + str(len(self.dashboard))
    #         id = int(id + str(len(self.dashboard[folderId])))
    #     elif fileType == 'worksheet':
    #         id = '1010' + str(len(self.worksheet))
    #         id = int(id + str(len(self.worksheet[folderId])))
    #     elif fileType == 'folder':
    #         id = '1001' + str(len(self.worksheet))
    #         id = int(id + str(len(self.worksheet[folderId])))
    #     return id

    # Add new file
    # todo: duplicate file name?
    def add_new_file(self, fileName: str, fileType: str, folderId: int) -> None:

        # generate unique id
        id = str(uuid.uuid1())

        # If file type is dashboard
        if fileType == 'dashboard':
            # add to dashboard dict
            self.dashboard[id] = [fileName, folderId]

        # If file type is worksheet
        elif fileType == 'worksheet':
            self.worksheet[id] = [fileName, folderId]

        # If file type is folder
        # only hold a list of folders
        elif fileType == 'folder':
            self.folder[id] = [fileName, folderId]

        # add to all files, regardless its types is Folder, Dashboard or Worksheet
        # holder a list of folders and show what's inside each folder (can be folders, worksheets and/or dashboards)
        if folderId in self.all_files:
            self.all_files[folderId].append(id)
        else:
            self.all_files[folderId] = [id]
        return

    def get_file_id(self, fileName: str, folderId: int) -> int:
        # if folderId is None, it's MyDocuments -- root folder
        if folderId == None:
            return self.rootId

        all_files_in_folder = self.all_files[folderId]  # [parent:[children]]
        for fileId in all_files_in_folder:
            if fileId in self.dashboard and self.dashboard[fileId][0] == fileName:
                return fileId
            if fileId in self.worksheet and self.worksheet[fileId][0] == fileName:
                return fileId
            if fileId in self.folder and self.folder[fileId][0] == fileName:
                return fileId
        return

    def move_file(self, fileId: int, newFolderId: int) -> None:
        # find the type of file
        if fileId in self.dashboard:
            fileName, folderId = self.dashboard[fileId]
            # update newFileId in the self.fileType
            self.dashboard[fileId] = [fileName, newFolderId]

        elif fileId in self.worksheet:
            fileName, folderId = self.worksheet[fileId]
            # update newFileId in the self.fileType
            self.worksheet[fileId] = [fileName, newFolderId]

        elif fileId in self.folder:
            fileName, folderId = self.folder[fileId]
            # update newFileId in the self.fileType
            self.folder[fileId] = [fileName, newFolderId]

        # move the position in self.all_files
        self.all_files[folderId].remove(fileId)

        self.all_files[newFolderId].append(fileId)

    def get_files(self, folderId: int) -> typing.List[str]:
        res = []
        all_ids = self.all_files[folderId]
        for id in all_ids:
            # find the fileType, get fileName
            if id in self.dashboard:
                res.append(self.dashboard[id][0])
            elif id in self.worksheet:
                res.append(self.worksheet[id][0])
            elif id in self.folder:
                res.append(self.folder[id][0])

        return res

    def print_files(self) -> None:
        # TODO: implement by BFS or DFS
        folders = self.all_files
        #all_folders = self.all_files.items()
        visited = set()
        root = self.rootId

        def dfs(folderId, parent):
            # not a folder but a worksheet or a dashboard
            if folderId not in folders:
                if folderId in self.dashboard:
                    if parent == 0:
                        print(self.dashboard[folderId][0],
                              " in ", "MyDocuments")
                    else:
                        print(self.dashboard[folderId][0],
                              " in ", self.folder[parent][0])
                elif folderId in self.worksheet:
                    if parent == 0:
                        print(self.worksheet[folderId][0],
                              " in ", "MyDocuments")
                    else:
                        print(self.worksheet[folderId][0],
                              " in ", self.folder[parent][0])
                return

            # an empty folder
            if folders[folderId] == []:
                return {}

            # print folderName, if folderId
            if folderId == self.rootId:
                print("MyDocuments")
            else:
                if parent == self.rootId:
                    print(self.folder[folderId][0],
                          " in ", "MyDocuments")
                else:
                    print(self.folder[folderId][0],
                          " in ", self.folder[parent][0])

            # loop through each folder/file in the folder and do dfs on it
            visited.add(folderId)
            for child_folder in folders[folderId]:
                if child_folder not in visited:
                    visited.add(child_folder)
                    dfs(child_folder, folderId)
        dfs(root, None)

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
    fs.move_file(projectId, completeId)
    projectId = fs.get_file_id("project", completeId)
    coverId = fs.get_file_id("cover", projectId)
    fs.move_file(coverId, rootId)

    print(", ".join(fs.get_files(rootId)))
    print(", ".join(fs.get_files(draftId)))
    print(", ".join(fs.get_files(completeId)))
    print(", ".join(fs.get_files(projectId)))

    print(fs.get_total_dashboards())
    print(fs.get_total_worksheets())
    print(fs.print_files())


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
