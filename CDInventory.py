#------------------------------------------#
# Title: CDInventory.py
# Desc: Updated Assignment 06 with Error Handling and Binary files
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# KRos, 2020-Feb-28, added write_file function
# KRos, 2020-Feb-29, created add_CD and delete_CD functions, added Docstrings
# KRos, 2020-Mar-01, added in try-except for case where file does not exist
# KRos, 2020-Mar-08, added in structured error handling and changed program to read and write binary files
# KRos, 2020-Mar-09, updated some doc strings
#------------------------------------------#

# -- IMPORT MODULES -- #
import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    """Data Processing Functions"""

    @staticmethod
    def add_CD(idno, title, artist, table):
        """Function that adds CD to list of dictionaries, rasies ValueError ifidno is not an int

        Args:
            idno (string): ID number of CD, which will be converted to int
            title (string): CD title
            artist (string): CD artist
            table (list of dicts): 2D table that will be appended with new CD entry

        Returns:
            table (list of dicts): 2D table that has a CD added to it
        """
        try:
            dicRow  = {'ID': int(idno), 'Title': title, 'Artist': artist}
            table.append(dicRow)
        except ValueError as e:
            print('Build in error info:')
            print(type(e), e, e.__doc__, sep='\n')
        return table

    @staticmethod
    def delete_CD(idno, table):
        """Function that deletes a CD entry from a 2D table

        Args:
            idno (int): CD ID number to be deleted
            table (list of dicts): 2D list that CD should be removed from

        Returns:
            table (list of dicts): 2D list that has been edited
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == idno:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        return table

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries
        FileNotFound error is raised if CDInventory.dat does not exist
        EOFError is raised when the end of CDInventory file is reached

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.
        If file does not exist, a file will be created

        Args:
            file_name (string): name of file used to read the data from
            table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            table (list of dicts): table returned from opening file
        """
        try:
            cdInfo = []
            with open(file_name, 'rb') as objFile:
                table.clear()  # this clears existing data and allows to load data from file
                while True:
                    try:
                        cdInfo.append(pickle.load(objFile))
                    except EOFError as e:
                        print(type(e), e, e.__doc__, sep='\n')
                        print("Reached end of File!")
                        break
                for line in cdInfo:
                    data = line.strip().split(',')
                    dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
                    table.append(dicRow)
        except FileNotFoundError as e:
            print('Build in error info:')
            print(type(e), e, e.__doc__, sep='\n')
            
        return table
    @staticmethod
    def write_file(file_name, table):
        """Function that Saves inventory to text file
        Reads 2D table and formats line by line to write to a text file

        Args:
            file_name (string): name of file used to save data to
            table (list of dict): 2D data structure that holds data during runtime

        Returns:
            None
        """
        with open(file_name, 'wb') as objFile:
            for row in table:
                lstValues = list(row.values())
                lstValues[0] = str(lstValues[0])
                tblString = ','.join(lstValues) + '\n'
                pickle.dump(tblString, objFile)

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def input_CD():
        """Asks user for CD inputs

        Args:
            None

        Returns:
            ID, CD title, Artist

        """
        strID = input('Enter ID: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        return strID, strTitle, stArtist

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled \n')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        strID, strTitle, stArtist = IO.input_CD()
        # 3.3.2 Add item to the table
        DataProcessor.add_CD(strID, strTitle, stArtist, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        try:
            intIDDel = int(input('Which ID would you like to delete? ').strip())
            # 3.5.2 search thru table and delete CD
            DataProcessor.delete_CD(intIDDel, lstTbl)
            IO.show_inventory(lstTbl)
        except ValueError as e:
            print('Build in error info:')
            print(type(e), e, e.__doc__, sep='\n')
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')