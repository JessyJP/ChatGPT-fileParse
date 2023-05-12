"""
File and Directory Processing Tool

Author: JessyJP
Date: May 10, 2023

This Python script is a file and directory processing tool that provides various functionalities such as 
path sanitizing, file and directory structuring, data processing, and automatic executable creation. 
It supports both text and binary file processing with versatile viewing modes. 

MIT License

Copyright (c) 2023 JessyJP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import platform
import shlex
import argparse
import keyboard
from typing import List, Dict, Tuple
import time
import pyperclip
import win32gui
from tabulate import tabulate
from WelcomeScreen import *

# Create a global variable for progress update timeout
progressUpdateTimeout = 0.05  # Update every 100ms

## ================= Control Class, Default Control Structures and Control Loop [1] =================
class ControlStateVariable:
    varCounter = 0
    def __init__(self, default_state, kbKey, help_message, options, data_type, state_name=""):
        self.name = state_name
        self.state = default_state
        self.kbKey = kbKey
        self.help_message = help_message.replace("#key#", self.format_kbKey())
        self.options = options
        self.data_type = data_type

        # Assign Order in order of creation
        ControlStateVariable.varCounter = ControlStateVariable.varCounter+1
        self.legend_order = ControlStateVariable.varCounter+1
    #end

    def format_kbKey(self):
        # If kbKey is a list, parse the values with a "/"
        if isinstance(self.kbKey, list):
            return "/".join(self.kbKey)
        else:
            return self.kbKey
        #end
    #end

    def nextState(self):
        if self.data_type == bool:
            self.state = not self.state
        elif self.data_type == int or isinstance(self.options, list):
            index = self.options.index(self.state)
            self.state = self.options[(index + 1) % len(self.options)]
        #end
        return self.state
    #end

    def previousState(self):
        if self.data_type == bool:
            self.state = not self.state
        elif self.data_type == int or isinstance(self.options, list):
            index = self.options.index(self.state)
            self.state = self.options[(index - 1) % len(self.options)]
        #end
        return self.state
    #end
    
    def checkState(self, input_state):
        if not isinstance(input_state, self.data_type):
            raise Exception("The input state has an invalid data type.")
        #end

        if isinstance(self.options, list) and input_state not in self.options:
            raise Exception("The input state is not in the options list.")
        #end

        return self.state == input_state
    #end

    def getPrintStr(self, detailedLegend=True):
        if (self.name == ""):
            return ""
        #end
        
        msg = f"{self.name}({self.format_kbKey().upper()}) : {self.state}  "
        if detailedLegend:
            msg = msg + " - "+ self.help_message
        #end
        return msg
    #end
#end

class ControlStructure:
    # Placeholder structure
    def __init__(self):
        pressStr = "Press '#key#' "
        
        # Panel section
        self.PanelView = ControlStateVariable(
                state_name = "Panel View",
                default_state="DirectoryViewPanel",
                kbKey="w",
                help_message=pressStr+"to change the control state.",
                options=["DirectoryViewPanel", "FileViewPanel"],
                data_type=str,
            )
        
        # Window Focus
        self.WindowFocus = ControlStateVariable(
                state_name = "Window Focus",
                default_state=False,
                kbKey="q",
                help_message=pressStr+"to require window focus.",
                options=[True, False],
                data_type=str,
            )
            
        # Tree section
        self.DirectoryViewMode = ControlStateVariable(
                state_name = "Directory View Mode",
                default_state="Tree",
                kbKey="t",
                help_message=pressStr+"to change directory view mode",
                options=["Tree", "List","Table"],
                data_type=str,
            )
        # Set global control variables
        self.ExitFlag = ControlStateVariable(
                default_state=False,
                kbKey="ESC",
                help_message=pressStr+"to exit the program.",
                options=[True, False],
                data_type=bool,
            )

        self.LegendShow = ControlStateVariable(
                state_name = "Show Legend ON",
                default_state=True,
                kbKey="s",
                help_message=pressStr+" to show legend in the console",
                options=[True, False],
                data_type=bool,
            )

        self.LegendDetail = ControlStateVariable(
                state_name = "Detailed Legend ON",
                default_state=False,
                kbKey="l",
                help_message=pressStr+"for detailed legend output in the console",
                options=[True, False],
                data_type=bool,
            )

        self.Verbose = ControlStateVariable(
                state_name = "Verbose Detail ON",
                default_state=True,
                kbKey="d",
                help_message=pressStr+"for detailed output in the console",
                options=[True, False],
                data_type=bool,
            )

        # Character limit
        self.Limit = ControlStateVariable(
                state_name = "Character Limit",
                default_state=4096,
                kbKey=["+","-"],
                help_message="Limit the number of characters to be processed at a time for copying to the clipboard. Default is 4096.",
                options=list(range(0, 5000)),
                data_type=int,
            )

        # Chat GPT accepts around 4096 characters, so we set the default limit to 4096 - 100.
        # If you want a different value, change the default value for the --limit argument above.

        # Set Panel control variables
        self.Recursive = ControlStateVariable(
                state_name = "Include Recursive",
                default_state=True,
                kbKey="r",
                help_message=pressStr + "for recursion for directories",
                options=[True, False],
                data_type=bool,
            )
        
        self.AbsolutePath = ControlStateVariable(
                state_name = "Absolute Path",
                default_state=True,
                kbKey="a",
                help_message=pressStr + "to use relative path",
                options=[True, False],
                data_type=bool,
            )

        self.Binary = ControlStateVariable(
                state_name = "Include Binary",
                default_state=True,
                kbKey="b",
                help_message=pressStr + "to include binary files when copying to the clipboard",
                options=[True, False],
                data_type=bool,
            )
        
        self.Continuous = ControlStateVariable(
                state_name = "Continuous Unified Mode",
                default_state=False,
                kbKey="u",
                help_message=pressStr+"for continuous mode prints the file(s) content as continuous stream",
                options=[True, False],
                data_type=bool,
            )
        
        self.Partition = ControlStateVariable(
                state_name = "Partition Mode",
                default_state=False,
                kbKey="p",
                help_message=pressStr + "to partition the file content",
                options=[True, False],
                data_type=bool,
            )
        
        self.SimpleHeaderFooter = ControlStateVariable(
                state_name = "Simple Header & Footer",
                default_state=False,
                kbKey="h",
                help_message=pressStr + "to partition the file content",
                options=[True, False],
                data_type=bool,
            )
        
        # Navigation action Keys
        self.kbKey_nextFile = 'right'
        self.kbKey_previousFile = 'left'
        self.kbKey_nextPart = 'down'
        self.kbKey_previousPart = 'up'

        # This section is for file the navigation and display
        self.numberOfBinaryFiles = 0
        self.numberOfTextFiles = 0
        self.numberOfFiles = 0
        self.currentFile_Ind = 0
        self.currentFile_TotalParts = 1
        self.currentFile_CurrentPart = 1

        self.buff = "";# The text buffer that will be displayed and copied to the clipboard 
    #end

    def nextFile(self):
        if self.currentFile_Ind < self.numberOfFiles: # Check if not at the last file
            self.currentFile_Ind += 1
            # Reset the part index
            self.currentFile_CurrentPart = 1
        #end
    #end

    def previousFile(self):
        if self.currentFile_Ind > 1: # Check if not at the first file
            self.currentFile_Ind -= 1
            # Reset the part index
            self.currentFile_CurrentPart = 1
        #end
    #end

    def nextPart(self):
        if self.currentFile_CurrentPart < self.currentFile_TotalParts: # Check if not at the last part
            self.currentFile_CurrentPart += 1
        #end
    #end

    def previousPart(self):
        if self.currentFile_CurrentPart > 1: # Check if not at the first part
            self.currentFile_CurrentPart -= 1
        #end
    #end

    def _get_sorted_attributes(self):
        attrs = []
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, ControlStateVariable):
                attrs.append(attr)
            #end
        #end
        attrs.sort(key=lambda x: x.legend_order)
        return attrs
    #end

    def get_list_all_keyboard_keys(self) -> List[str]:
        keys = []
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, ControlStateVariable) and attr.kbKey:
                
                if isinstance(attr.kbKey, list):
                    keys = keys + attr.kbKey
                else:
                    keys.append(attr.kbKey)
                #end
            elif attr_name.startswith("kbKey_"):
                keys.append(getattr(self, attr_name))
            #end
        #end
        keys = [key.lower() for key in keys]
        return keys
    #end

    def printStateAndLegend(self, attributeFilter=[], skip=True):
        if self.LegendDetail.state:
            sepLineLen = 100
        else:
            sepLineLen = 40
        #end

        if self.LegendShow.state:
            print("-" * sepLineLen)  # print dashes at the beginning
            for attr in self._get_sorted_attributes():
                if attributeFilter and skip == (attr.name in attributeFilter):
                    continue  # Skip this attribute if it's not in the attributeFilter list
                #end
                
                print_str = attr.getPrintStr(self.LegendDetail.state)
                if print_str:
                    print(print_str)
                #end
            #end
            
            # If in FileViewPanel mode, print additional information
            # if self.PanelView.state == "FileViewPanel":
            print("-" * sepLineLen)  # print dashes at the end
            if self.Continuous.state:
                print(f"Total number of files: {self.numberOfFiles}")
            else:
                print(f"Current File Index: {self.currentFile_Ind} out of {self.numberOfFiles} ({self.kbKey_previousFile}/{self.kbKey_nextFile})")
            #end
            print(f"Current Part: {self.currentFile_CurrentPart} out of {self.currentFile_TotalParts} ({self.kbKey_previousPart}/{self.kbKey_nextPart})")
                
            print("-" * sepLineLen)  # print dashes at the end
        #end
    #end

    # --- Methods for printing, copying and clearing the text buffer ---
    def bufferAndPrint(self, s: str, bufferOutSubstitute="") -> None:
        """Custom function that appends to a buffer."""
        self.buff += s + "\n"
        # If the verbose substitution is empty then print the buffer otherwise print a substitute message
        if not bufferOutSubstitute:
            print(s)
        else:
            print(bufferOutSubstitute)
        #end
    #end

    def copyBufferToClipboardAndClear(self) -> None:
        """Copy the text buffer to the clipboard and clear it."""
        pyperclip.copy(self.buff)
        self.buff = ""
    #end
#end

def controlLoopProcess(file_list: List[str]):
    CTL = ControlStructure()# Make the default control structure
    file_structures = process_input(file_list, CTL)# The the file tree
    CTL.printStateAndLegend()
    printWelcomeScreen()

    appTitle = "Chat GPT File Navigator Pro"

    # Set a unique title for the console window
    os.system(f'title {appTitle}')

    allKeysList = CTL.get_list_all_keyboard_keys();
    # Control Loop
    while True:
        # Wait for a keyboard key to be pressed  
        event = keyboard.read_event()

        # Get the title of the active window
        active_window_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())

        # If the active window is not your console window, continue the loop
        if active_window_title != appTitle and CTL.WindowFocus.state:
            continue
        #end

        if not(event.name in allKeysList):
            continue # Just ignore keys that are not control input
        #end

        clearScreen()

        # Update the Control structure for the Global states
        if keyboard.is_pressed(CTL.PanelView.kbKey):
            CTL.PanelView.nextState()
        #end
        if keyboard.is_pressed(CTL.WindowFocus.kbKey):
            CTL.WindowFocus.nextState()
        #end
        if keyboard.is_pressed(CTL.LegendShow.kbKey):
            CTL.LegendShow.nextState()
        #end
        if keyboard.is_pressed(CTL.LegendDetail.kbKey):
            CTL.LegendDetail.nextState()
        #end
        if keyboard.is_pressed(CTL.Verbose.kbKey):
            CTL.Verbose.nextState()
        #end
        if keyboard.is_pressed(CTL.Continuous.kbKey):
            CTL.Continuous.nextState()
        #end
        if keyboard.is_pressed(CTL.Partition.kbKey):
            CTL.Partition.nextState()
        #end
        if keyboard.is_pressed(CTL.SimpleHeaderFooter.kbKey):
            CTL.SimpleHeaderFooter.nextState()
        #end
        # Quick change before screen is even updated
        if keyboard.is_pressed(CTL.Limit.kbKey[0]):
            CTL.Limit.nextState()
            if not(CTL.Partition.state): 
                CTL.printStateAndLegend()
                continue;
            #end
        #end
        if keyboard.is_pressed(CTL.Limit.kbKey[1]):
            CTL.Limit.previousState()
            if not(CTL.Partition.state): 
                CTL.printStateAndLegend()
                continue;
            #end
        #end
        if keyboard.is_pressed(CTL.ExitFlag.kbKey):
            break
        #end
        
        # Update the Control structure for the Global states per panel # TODO: decide if this will be panel specific of global switch
        if keyboard.is_pressed(CTL.DirectoryViewMode.kbKey):
            CTL.DirectoryViewMode.nextState()
        #end
        if keyboard.is_pressed(CTL.Recursive.kbKey):
            CTL.Recursive.nextState()
            # Update the file Structure
            file_structures = process_input(file_list, CTL)
        #end
        if keyboard.is_pressed(CTL.AbsolutePath.kbKey):
            CTL.AbsolutePath.nextState()
        #end
        if keyboard.is_pressed(CTL.Binary.kbKey):
            CTL.Binary.nextState() 
            CTL.numberOfFiles = CTL.numberOfBinaryFiles+CTL.numberOfTextFiles if CTL.Binary.state else CTL.numberOfTextFiles
            # Reset the file position 
            CTL.currentFile_Ind = 1;
            CTL.currentFile_TotalParts = 1 if CTL.numberOfFiles else 0
            CTL.currentFile_CurrentPart = 1 if  CTL.numberOfFiles else 0
        #end

        # Export executable script
        if keyboard.is_pressed("e"):
            create_executable(file_list)
        #end

        # Print the legend
        CTL.printStateAndLegend()

        if (CTL.PanelView.checkState('DirectoryViewPanel')):

            # Print the legend
            # CTL.printStateAndLegend()

            # Print file structure
            print_directory_structures(file_structures, CTL)
        #end

        if (CTL.PanelView.checkState('FileViewPanel')):
            # Navigation next/ previous file and part with the arrow keys
            if keyboard.is_pressed(CTL.kbKey_previousFile):  # Previous file
                CTL.previousFile()
            #end
            if keyboard.is_pressed(CTL.kbKey_nextFile):  # Next file
                CTL.nextFile()
            #end
            if keyboard.is_pressed(CTL.kbKey_previousPart):  # Previous part
                CTL.previousPart()
            #end
            if keyboard.is_pressed(CTL.kbKey_nextPart):  # Next part
                CTL.nextPart()
            #end

            # Print the legend
            # CTL.printStateAndLegend([CTL.Recursive.name, CTL.Binary.name, CTL.DirectoryViewMode.name])

            if CTL.Continuous.state:
                process_unified_continuous_mode(CTL, file_structures)
            else:
                process_selected_file(file_structures, CTL)
            #end
        #end

        # Clear the print buffer
        CTL.copyBufferToClipboardAndClear()
    #end
#end

## ================= Input File path processing functions [2] =================
def sanitizePath(input_path):
    # Remove leading/trailing whitespaces
    sanitized_path = input_path.strip()
    # Replace backslashes with forward slashes
    sanitized_path = sanitized_path.replace("\\", "/")

    # Check if the path exists and is a directory
    if not os.path.exists(sanitized_path):
        print(f"[ERROR] Path does not exist: {sanitized_path}")
        return None
    #end

    # if not os.path.isdir(sanitized_path): # TODO: remove this code snippet
    #     print(f"Path is not a directory: {sanitized_path}")
    #     return None

    # If the path is a directory, list the files in it
    try:
        if os.path.isdir(sanitized_path):
            files = os.listdir(sanitized_path)
        #end
    except PermissionError:
        print(f"[ERROR] Permission denied: {sanitized_path}")
        return None
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
        return None
    #end

    return sanitized_path
#end

def process_input(paths: List[str], CTL: ControlStructure) -> List[Dict]:
    file_structures = []
    progress = [{'total': len(paths), 'processed': 0}]
    last_update_time = [time.time()] # Initialize a variable to store the last update time
    
    # Determine the common prefix-path initially
    common_prefix = os.path.commonprefix(paths)

    def update_progress(level, path):
        progress[level]['processed'] += 1

        # Check if the specified timeout has passed since the last update
        if time.time() - last_update_time[0] < progressUpdateTimeout:
            return # If not enough time has passed, return without updating
        #end
        if CTL.Verbose.state:
            clearScreen()
            print(f"Current file : [{path}]")
            for i, p in enumerate(progress):
                printProgressBar(p['processed'], p['total'], prefix=f'Level {i} Progress:', suffix='Complete', length=50)
            #end
        #end
        last_update_time[0] = time.time()
    #end

    def process_path(path: str, level: int) -> None:
        if os.path.isfile(path):
            with open(path, "rb") as file:
                content = file.read(512)
                is_binary = b'\x00' in content
                file_type = "bin" if is_binary else "txt"
            #end
            relative_path = path.replace(common_prefix, '', 1)
            file_structures.append({"absolute_path": path, "relative_path": relative_path, "type": file_type})
            update_progress(level,path)
        elif os.path.isdir(path) and CTL.Recursive.state:
            files = os.listdir(path)
            progress.append({'total': len(files), 'processed': 0})
            level += 1
            for f in files:
                process_path(os.path.join(path, f), level)
            #end
            progress.pop()
            level -= 1
        else:
            return
        #end
    #end
    
    for path in paths:
        process_path(path, 0)
    #end

    clearScreen()

    # Update the CTL structure after compiling the data
    CTL.numberOfBinaryFiles = len([f for f in file_structures if f["type"] == "bin"])
    CTL.numberOfTextFiles = len([f for f in file_structures if f["type"] == "txt"])
    CTL.numberOfFiles = CTL.numberOfBinaryFiles+CTL.numberOfTextFiles if CTL.Binary.state else CTL.numberOfTextFiles
    CTL.currentFile_Ind = 0 if not file_structures else 1
    CTL.currentFile_TotalParts = 0 if not file_structures else 1
    CTL.currentFile_CurrentPart = 0 if not file_structures else 1

    return file_structures
#end

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()
    #end
#end

## ================= DIrectory processing functions [3] =================

def print_directory_structures(file_structures: List[Dict], CTL: ControlStructure) -> None:
    # Filter out binary files if Binary is set to False
    if not CTL.Binary.state:
        file_structures = [fs for fs in file_structures if fs['type'] != 'bin']
    #end

    # Choose the key to access the path to display based on the AbsolutePath setting
    path_key = 'absolute_path' if CTL.AbsolutePath.state else 'relative_path'

    if CTL.DirectoryViewMode.state == CTL.DirectoryViewMode.options[0]:  # Tree
        # Print as a tree
        tree = {}
        for file_structure in file_structures:
            parts = file_structure[path_key].split('/')
            node = tree
            for part in parts:
                node = node.setdefault(part, {})
            #end
        #end
                
        def print_tree(node, prefix=""):
            for key, value in node.items():
                if value:
                    CTL.bufferAndPrint(f"{prefix}├── {key}")
                    print_tree(value, prefix + "│   ")
                else:
                    CTL.bufferAndPrint(f"{prefix}└── {key}")
                #end
            #end
        #end
                    
        print_tree(tree)

    elif CTL.DirectoryViewMode.state == CTL.DirectoryViewMode.options[1]:  # List
        # Print as a list
        for file_structure in file_structures:
            CTL.bufferAndPrint(f"[{file_structure['type']}] {file_structure[path_key]}")
        #end

    elif CTL.DirectoryViewMode.state == CTL.DirectoryViewMode.options[2]:  # Table
        # Print as a table
        table = [["Type", "Path"]] + [[fs['type'], fs[path_key]] for fs in file_structures]
        CTL.bufferAndPrint(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    else:
        raise Exception("Invalid DirectoryViewMode state")
    #end
#end
  
## ================= File processing functions [4] =================
   
def process_selected_file(file_structures: List[Dict], CTL: ControlStructure) -> None:
    """
    This function processes the content of the selected file to be printed.

    Args:
        file_structures (List[Dict]): List of file structures.
        CTL (ControlStructure): Control structure that keeps track of application state.
    """

    # If the binary switch is off, filter out binary files
    if not CTL.Binary.state:
        filtered_Structures = [fs for fs in file_structures if fs['type'] != 'bin']
    else:
        filtered_Structures = file_structures
    #end

    # If there's no file to process, return early
    if CTL.currentFile_Ind == 0 or CTL.currentFile_Ind > len(filtered_Structures):
        print("[ERROR] No file selected for display.")
        return
    #end

    selected_file_structure = filtered_Structures[CTL.currentFile_Ind - 1]
    file_path = selected_file_structure['absolute_path']

    if selected_file_structure['type'] == 'bin':
        print("[INFO] The selected file is a binary file and cannot be displayed.")
        return
    #end

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Get the file content
            file_content = file.read()
            # Process the partitioning
            partitionTextPrint(file_content, file_path, CTL.Limit.state, CTL)
        #end

    except Exception as e:
        print(f"[ERROR] An error occurred while reading the file: {e}")
    #end
    return
#end

## ================= Unified Continuous File processing functions [5] =================

persistent_unified_mode_state = {}

def get_current_sub_control_state(CTL: ControlStructure) -> Dict:
    """
    This function gets the current state of the sub-controls.

    Args:
        CTL (ControlStructure): Control structure that keeps track of application state.

    Returns:
        Dict: The current state of the sub-controls.
    """
    return {
        'binary_mode': CTL.Binary.state,
        'recursive_mode': CTL.Recursive.state,
        'directory_view_mode': CTL.DirectoryViewMode.state,
        'character_limit': CTL.Limit.state,
        'absolute_path': CTL.AbsolutePath.state,
        'continuous_unified_mode': True,  # Always True in this function
        # 'partition_mode': CTL.Partition.state,
        'simple_header_footer_mode': CTL.SimpleHeaderFooter.state,
    }
#end

def compare_mode_states(CTL: ControlStructure) -> bool:
    """
    This function compares the current state and the persistent state.

    Args:
        CTL (ControlStructure): Control structure that keeps track of application state.

    Returns:
        bool: True if the states are the same, False otherwise.
    """
    current_state = get_current_sub_control_state(CTL)
    persistent_state = {k: v for k, v in persistent_unified_mode_state.items() if k != 'data'}
    return current_state == persistent_state
#end

def process_unified_continuous_mode(CTL: ControlStructure, file_structures: List[Dict]) -> None:
    """
    This function reads all the files, combines them into a single stream, and prints them out.
    It adds a header and footer to each file and respects the control structure states.
    """
    if not persistent_unified_mode_state or not compare_mode_states(CTL):
        # Compute the unified mode state
        persistent_unified_mode_state.update(get_current_sub_control_state(CTL))
        
        sepLine = lambda n=30: '\n'+n*'='+'\n'
        CTL.bufferAndPrint(f"{sepLine()}File structure:{sepLine()}")
        # Add the directory file structure
        print_directory_structures(file_structures, CTL) 
        CTL.bufferAndPrint(f"{sepLine()}File(s) Content:{sepLine()}")

        # Overwrite partition state
        partitionState = CTL.Partition.state
        CTL.Partition.state = False
        CTL.Continuous.state = False
        # Loop over all files and load them into memory
        for file_structure in file_structures:
            file_path = file_structure['absolute_path']
            if file_structure['type'] != 'bin':
                try:    
                    with open(file_path, 'r', encoding='utf-8') as file:
                        # Get the file content
                        file_content = file.read()
                        
                        # Compute and add header and footer
                        header, footer = compute_header_footer(CTL, file_path)
                        fileContent = sepLine() + header + file_content + footer
                        # CTL.buff += fileContent
                        CTL.bufferAndPrint(fileContent)
                    #end

                except Exception as e:
                    print(f"[ERROR] An error occurred while reading the file: {e}")
                #end
            else:
                CTL.bufferAndPrint(sepLine()+"[INFO] binary file: " + file_path)
            #end
        #end
        CTL.Partition.state = partitionState# Restore original state
        CTL.Continuous.state = True

        persistent_unified_mode_state['data'] = CTL.buff# Initialize the data field
    else:
        # Print the combined text
        partitionTextPrint(persistent_unified_mode_state['data'], "Continuous file stream.", CTL.Limit.state, CTL)
    #end
#end

## ================= Text Partitioning Functions [*Utility] =================

def compute_header_footer(CTL: ControlStructure, file_path: str, part_n: int = None, tot_parts: int = None) -> Tuple[str, str]:
    """
    This function computes and returns the header and footer strings.

    Args:
        CTL (ControlStructure): Control structure that keeps track of application state.
        file_path (str): The path to the file.
        part_n: int = 0 Default total file parts 
        tot_parts: int = 0 Default file part 

    Returns:
        Tuple[str, str]: The header and footer strings.
    """
    part_info = None
    if CTL.Partition.state:
        if tot_parts is None or part_n is None:
            tot_parts = CTL.currentFile_TotalParts
            part_n = CTL.currentFile_CurrentPart
        #end
        part_info = f'Part {part_n}/{tot_parts}'
    #end

    if CTL.Continuous.state:
        stream = "Text Stream"
    else:
        stream = "File"
    #end

    if CTL.SimpleHeaderFooter.state:    
        header = f'{stream}: "{file_path}" {part_info if part_info else ""}:\n"'
        footer = f'"'
    else:
        header = f'{stream}: "{file_path}"\n--- Beginning of {stream} {part_info if part_info else ""} ---\n'
        footer = f'\n--- End of {stream} {part_info if part_info else ""} ---\n'
    #end

    return header, footer
#end

def partitionTextPrint(text_content: str, file_path:str, characterLimit:int, CTL: ControlStructure):
    # Edit if there is character limit, i.e. partitioning is ON
    if CTL.Partition.state:
        # Compute optimal text character length
        optimal_text_part_length = get_optimal_part_text_length(text_content, file_path, characterLimit, CTL)

        parts = split_text_into_parts(text_content, optimal_text_part_length)
        CTL.currentFile_TotalParts = len(parts)
        if CTL.currentFile_CurrentPart > len(parts):
            print(f"[INFO] No more parts to display for file: {file_path}")
            return
        #end

        text_content = parts[CTL.currentFile_CurrentPart - 1]
    #end
    
    verbosePrintOut = ""
    if not CTL.Verbose.state:
        verbosePrintOut = " [Text content console output only - Verbose State (OFF) ] "
    #end

    # Compute and print header and footer based on the control settings
    header, footer = compute_header_footer(CTL, file_path)
    # Read and print the file content or the selected part
    CTL.bufferAndPrint(header)
    CTL.bufferAndPrint(text_content, verbosePrintOut)
    CTL.bufferAndPrint(footer)
    
    print(f"\n Total character length : {len(header)+len(text_content)+len(footer)}")
#end

def get_optimal_part_text_length(text_content: str, file_path:str, absolute_limit:int, CTL: ControlStructure) -> int:
    """
    This function determines the optimal text part length so that 
    each part does not exceed the absolute character limit when the header and footer are included.

    Args:
        text_content (str): The content of the file.
        CTL (ControlStructure): Control structure that keeps track of application state.

    Returns:
        int: The optimal part text length.
    """
    # Get the full file size in characters
    full_file_size = len(text_content)

    # Start with an estimate of 1 part
    p = 1 # number of parts

    while True:
        # Compute the length of the header and footer for the current part count
        header, footer = compute_header_footer(CTL, file_path,p,p)
        hf_length = len(header) + len(footer)

        # Compute the text character limit for the file content
        text_limit = absolute_limit - hf_length

        # Compute the new number of parts
        new_p = full_file_size // text_limit
        if full_file_size % text_limit != 0:
            new_p += 1
        #end
        # TODO: test the algorithm in more detail
        # If the total characters (file content + header/footer) is less than the absolute character limit,
        # or the number of parts didn't change, return the current text character limit
        if text_limit * new_p + hf_length * new_p <= absolute_limit or new_p == p:
            return text_limit
        #end

        # Otherwise, continue the loop with the new part count
        p = new_p
    #end
#end

def split_text_into_parts(text_content: str, character_limit: int) -> List[str]:
    """
    This function reads a text from memory and splits it into parts. Each part will not exceed 
    the character limit and will not break in the middle of a line. 

    Args:
        text_content (str): The content of the file.
        character_limit (int): The maximum number of characters for each part.

    Returns:
        List[str]: A list of strings where each string is a part of the file.
    """
    parts = []
    part = []
    part_length = 0
    for line in text_content.split('\n'):
        line_length = len(line) + 1  # Adding 1 for the newline character
        if part_length + line_length > character_limit:
            parts.append("".join(part))
            part = []
            part_length = 0
        #end
        part.append(line + '\n')  # Adding back the newline character
        part_length += line_length
    #end
    if part:
        parts.append("".join(part))
    #end
    return parts
#end

## ================= Screen & Custom Print/Buffer Functions [*Utility] =================
def clearScreen():
    # Clear the terminal
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux, macOS, etc.
        os.system('clear')
    #end
#end

## ================= Export function [*] =================

def create_executable(file_list: List[str]) -> None:
    # Convert file_list to a single string with space-separated file paths
    file_list_str = ' '.join(map(shlex.quote, file_list))

    # Determine the current platform
    current_platform = platform.system()

    if current_platform == "Windows":
        # Create a .bat file for Windows
        with open("run.bat", "w") as f:
            f.write(f"@echo off\n")
            f.write(f"python main.py {file_list_str}\n")
        #end
    elif current_platform == "Linux" or current_platform == "Darwin":
        # Create a .sh file for Unix/Linux
        with open("run.sh", "w") as f:
            f.write(f"#!/bin/sh\n")
            f.write(f"python3 main.py {file_list_str}\n")
        #end
        # Make the .sh file executable
        os.chmod("run.sh", 0o755)
    else:
        print(f"[ERROR] Unsupported platform: {current_platform}")
    #end
#end

## ================= Call the main function [0] =================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File and directory processing tool that copies file content to the clipboard in a continuous way.")
    parser.add_argument("paths", nargs="+", help="List of files and directories to process")
    
    args = parser.parse_args()
    paths = args.paths

    # Sanitize the Paths    
    paths = [sanitizePath(path) for path in paths]

    controlLoopProcess(paths)
#end