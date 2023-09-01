import sys

# Define a Ride class
class Ride:
    # Define the initialization method of the Ride class
    def __init__(self, rideNumber, rideCost, tripDuration):
        # Initialize the rideNumber,rideCost, tripDuration attributes with the values passed as parameters
        self.rideNumber = rideNumber
        self.rideCost = rideCost
        self.tripDuration = tripDuration

# Min Heaps work on the rides with RideNumber , rideCost and tripDuration.
class MinHeap:
    def __init__(self):
        self.heap = []
        self.positions = {}

   # Insert a new ride into the heap
    def insert(self, ride):
        # Add the new ride to the end of the heap
        self.heap.append(ride)
        # Store the position of the new ride in the positions dictionary
        index = len(self.heap)-1
        self.positions[ride.rideNumber] = index
        # Reorder the heap to satisfy the heap property
        self.heapifyUp(index)

    # Remove and return the ride with the minimum rideCost from the heap
    def extract_min(self):
        # If the heap is empty, return None
        if len(self.heap) == 0:
            return None
        # If the heap contains only one ride, remove and return it
        if len(self.heap) == 1:
            ride = self.heap.pop()
            self.positions.pop(ride.rideNumber)
            return ride
        # Otherwise, remove the ride with minimum rideCost from the root
        min_val = self.heap[0]
        # Replace the root with the last ride in the heap
        self.heap[0] = self.heap.pop()
        # Update the position of the new root in the positions dictionary
        self.positions.pop(min_val.rideNumber)
        self.positions[self.heap[0].rideNumber] = 0
        # Reorder the heap to satisfy the heap property
        self.heapifyDown(0)
        # Return the ride with minimum rideCost
        return min_val

    # Remove a ride from the heap
    def delete(self, ride):
        # If the heap is empty, return False
        if len(self.heap) == 0:
            return False
        # If the ride is not in the heap, return False
        if ride.rideNumber not in self.positions:
            return False
        # Find the position of the ride in the heap
        index = self.positions[ride.rideNumber]
        # Replace the ride with the last ride in the heap
        self.heap[index] = self.heap[-1]
        # Update the position of the last ride in the positions dictionary
        self.positions[self.heap[-1].rideNumber] = index
        # Remove the last ride from the heap
        self.heap.pop()
        # Remove the ride from the positions dictionary
        del self.positions[ride.rideNumber]
        # Reorder the heap to satisfy the heap property
        if index == len(self.heap):
            return True
        self.heapifyUp(index)
        self.heapifyDown(index)
        return True

    # Reorder the heap from the given index to the root to satisfy the heap property
    def heapifyUp(self, index):
        # Find the position of the parent node
        prtNode = (index - 1) // 2 # parent Node
        # If the parent node is valid and the child node violates the heap property, swap them and continue with the parent node
        if prtNode >= 0 and (self.heap[prtNode].rideCost > self.heap[index].rideCost or (self.heap[prtNode].rideCost == self.heap[index].rideCost and self.heap[prtNode].tripDuration > self.heap[index].tripDuration)):
            self.swap(index, prtNode)
            self.heapifyUp(prtNode)

    def heapifyDown(self, index):
        # Calculate indices of the left and right child nodes
        lchild = index * 2 + 1
        rchild = index * 2 + 2
        # Set the minimum index to the current index
        minimum = index
        # Check if the left child node exists and has a lower ride cost or has the same ride cost but a shorter trip duration
        if (lchild < len(self.heap) and 
            (self.heap[lchild].rideCost < self.heap[minimum].rideCost or 
            (self.heap[lchild].rideCost == self.heap[minimum].rideCost and 
            self.heap[lchild].tripDuration < self.heap[minimum].tripDuration))):
            minimum = lchild
        # Check if the right child node exists and has a lower ride cost or has the same ride cost but a shorter trip duration
        if (rchild < len(self.heap) and 
            (self.heap[rchild].rideCost < self.heap[minimum].rideCost or 
            (self.heap[rchild].rideCost == self.heap[minimum].rideCost and 
            self.heap[rchild].tripDuration < self.heap[minimum].tripDuration))):
            minimum = rchild
        # If the minimum index has changed, swap the nodes and recursively call heapifyDown on the new index
        if minimum != index:
            self.swap(index, minimum)
            self.heapifyDown(minimum)


    def swap(self, i, j):
        # Update the positions of the two rides in the heap
        self.positions[self.heap[i].rideNumber] = j
        self.positions[self.heap[j].rideNumber] = i
        
        # Swap the two rides in the heap
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]



class Node():
    def __init__(self, data):
        # Initialize the data of the node
        self.data = data 
        # Initialize the parent, left child, and right child of the node
        self.parent = None 
        self.left = None 
        self.right = None 
        # Initialize the color of the node (1 for red, 0 for black)
        self.color = 1


# class RedBlackTree implements the operations in Red Black Tree
class RedBlackTree():
    def __init__(self):
        # Initialize null node with color 0 as the sentinel node
        self.TNULL = Node(0)
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    def searchNode(self, node, key):
        # Search for the node with the given key starting from the given node
        if node == self.TNULL or key == node.data:
            return node
        if key < node.data:
            return self.searchNode(node.left, key)
        return self.searchNode(node.right, key)

    
    def deleteRotationHelper(self, currNode):
        # Fix the tree after node deletion
        while currNode != self.root and currNode.color == 0:
            # If the node is the left child of its parent
            if currNode == currNode.parent.left:
                # Get the sibling node of the current node
                siblingNode = currNode.parent.right
                
                # Case 3.1: If the sibling node is red, we rotate to balance the tree
                if siblingNode.color == 1:
                    siblingNode.color = 0
                    currNode.parent.color = 1
                    self.lrRotation(currNode.parent)
                    siblingNode = currNode.parent.right

                # Case 3.2: If the sibling node and its children are black, we update colors and move up the tree
                if siblingNode.left.color == 0 and siblingNode.right.color == 0:
                    siblingNode.color = 1
                    currNode = currNode.parent
                else:
                    # Case 3.3: If the sibling node's left child is red, we rotate to balance the tree
                    if siblingNode.right.color == 0:
                        siblingNode.left.color = 0
                        siblingNode.color = 1
                        self.rlRotate(siblingNode)
                        siblingNode = currNode.parent.right
                        
                    # Case 3.4: If the sibling node's right child is red, we update colors and rotate to balance the tree
                    siblingNode.color = currNode.parent.color
                    currNode.parent.color = 0
                    siblingNode.right.color = 0
                    self.lrRotation(currNode.parent)
                    currNode = self.root
            # If the node is the right child of its parent
            else:
                # Get the sibling node of the current node
                siblingNode = currNode.parent.left
                
                # Case 3.1: If the sibling node is red, we rotate to balance the tree
                if siblingNode.color == 1:
                    siblingNode.color = 0
                    currNode.parent.color = 1
                    self.rlRotate(currNode.parent)
                    siblingNode = currNode.parent.left

                # Case 3.2: If the sibling node and its children are black, we update colors and move up the tree
                if siblingNode.left.color == 0 and siblingNode.right.color == 0:
                    siblingNode.color = 1
                    currNode = currNode.parent
                else:
                    # Case 3.3: If the sibling node's right child is red, we rotate to balance the tree
                    if siblingNode.left.color == 0:
                        siblingNode.right.color = 0
                        siblingNode.color = 1
                        self.lrRotation(siblingNode)
                        siblingNode = currNode.parent.left 
                        
                    # Case 3.4: If the sibling node's left child is red, we update colors and rotate to balance the tree
                    siblingNode.color = currNode.parent.color
                    currNode.parent.color = 0
                    siblingNode.left.color = 0
                    self.rlRotate(currNode.parent)
                    currNode = self.root
                    
        # Set the color of the current node to black to maintain the red-black tree property
        currNode.color = 0

    # Helper function to swap nodes in a red-black tree
    def swapNodes(self, one, two):
        if one.parent == None:  # If the parent of the first node is None, set the root of the tree to the second node
            self.root = two
        elif one == one.parent.left:  # If the first node is the left child of its parent, set the left child of the parent to the second node
            one.parent.left = two
        else:  # Otherwise, set the right child of the parent to the second node
            one.parent.right = two
        two.parent = one.parent  # Set the parent of the second node to the parent of the first node

    # Helper function to delete a node from a red-black tree
    def deleteNode(self, node, key):
        z = self.TNULL  # Initialize a node with a null value to keep track of the node to be deleted
        while node != self.TNULL:  # Traverse the tree until the node to be deleted is found or we reach a null node
            if node.data == key:  # If the current node's value matches the key, set the node to be deleted to this node
                z = node
            if node.data <= key:  # If the current node's value is less than or equal to the key, traverse to the right child
                node = node.right
            else:  # Otherwise, traverse to the left child
                node = node.left
        if z == self.TNULL:  # If the node to be deleted was not found, return
            return
        copy = z  # Create a copy of the node to be deleted
        copyColor = copy.color  # Store the color of the copied node
        if z.left == self.TNULL:  # If the node to be deleted has no left child, set the child node to be the right child
            childNode = z.right
            self.swapNodes(z, z.right)  # Swap the node to be deleted with its right child
        elif (z.right == self.TNULL):  # If the node to be deleted has no right child, set the child node to be the left child
            childNode = z.left
            self.swapNodes(z, z.left)  # Swap the node to be deleted with its left child
        else:  # If the node to be deleted has both a left and right child
            copy = self.minimum(z.right)  # Find the minimum node in the right subtree of the node to be deleted
            copyColor = copy.color  # Store the color of the copied node
            childNode = copy.right  # Set the child node to be the right child of the copied node
            if copy.parent == z:  # If the copied node is a direct child of the node to be deleted
                childNode.parent = copy  # Set the parent of the child node to be the copied node
            else:  # Otherwise, swap the copied node with its right child and set its right child to be the right child of the node to be deleted
                self.swapNodes(copy, copy.right)
                copy.right = z.right
                copy.right.parent = copy
            self.swapNodes(z, copy)  # Swap the node to be deleted with the copied node
            copy.left = z.left  # Set the left child of the copied node to be the left child of the node to be deleted
            copy.left.parent = copy  # Set the parent of the left child to be the copied node
            copy.color = z.color  # Set the color

        if copyColor == 0:
            self.deleteRotationHelper(childNode)

    def insertRotationHelper(self, key):
        # While the parent of the current node is red
        while key.parent.color == 1:
            # If the parent is the right child of the grandparent
            if key.parent == key.parent.parent.right:
                uncle = key.parent.parent.left # uncle node
                if uncle.color == 1:
                    # case 3.1: both parent and uncle are red
                    uncle.color = 0 # recolor uncle to black
                    key.parent.color = 0 # recolor parent to black
                    key.parent.parent.color = 1 # recolor grandparent to red
                    key = key.parent.parent # move up the tree to the grandparent
                else:
                    if key == key.parent.left:
                        # case 3.2.2: parent is red and uncle is black, and key is a left child
                        key = key.parent
                        self.rlRotate(key) # right-left rotation
                    # case 3.2.1: parent is red and uncle is black, and key is a right child
                    key.parent.color = 0 # recolor parent to black
                    key.parent.parent.color = 1 # recolor grandparent to red
                    self.lrRotation(key.parent.parent) # left-right rotation
            else:
                uncle = key.parent.parent.right # uncle node
                if uncle.color == 1:
                    # mirror case 3.1: both parent and uncle are red
                    uncle.color = 0 # recolor uncle to black
                    key.parent.color = 0 # recolor parent to black
                    key.parent.parent.color = 1 # recolor grandparent to red
                    key = key.parent.parent # move up the tree to the grandparent
                else:
                    if key == key.parent.right:
                        # mirror case 3.2.2: parent is red and uncle is black, and key is a right child
                        key = key.parent
                        self.lrRotation(key) # left-right rotation
                    # mirror case 3.2.1: parent is red and uncle is black, and key is a left child
                    key.parent.color = 0 # recolor parent to black
                    key.parent.parent.color = 1 # recolor grandparent to red
                    self.rlRotate(key.parent.parent) # right-left rotation
            if key == self.root:
                break
        self.root.color = 0 # set the root to black


    # A function to search a node with a given key in the tree
    def searchTree(self, key):
        return self.searchNode(self.root, key)

    # A function to find the minimum node in the tree
    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    # A function to perform a left-right rotation at node x
    def lrRotation(self, x):
        y = x.right   # y is the right child of x
        x.right = y.left  # x's right child becomes y's left child
        # Update the parent of y's left child to be x
        if y.left != self.TNULL:
            y.left.parent = x
        # Update the parent of y to be x's parent
        y.parent = x.parent
        # Update the root of the tree if x is the root, else update x's parent's child
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x  # Make x the left child of y
        x.parent = y  # Update x's parent to be y

    # A function to perform a right-left rotation at node x
    def rlRotate(self, x):
        y = x.left   # y is the left child of x
        x.left = y.right  # x's left child becomes y's right child

        # Update the parent of y's right child to be x
        if y.right != self.TNULL:
            y.right.parent = x

        # Update the parent of y to be x's parent
        y.parent = x.parent

        # Update the root of the tree if x is the root, else update x's parent's child
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x  # Make x the right child of y
        x.parent = y  # Update x's parent to be y


    def insert(self, key):
        # Create a new node with the given key and initialize its attributes
        node = Node(key)
        node.parent = None
        node.data = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1
        
        # Traverse the tree to find the correct position for the new node
        y = None
        x = self.root
        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            elif node.data > x.data:
                x = x.right
            else:
                pass
        
        # Update the parent of the new node and insert it into the tree
        node.parent = y
        if y == None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node
        
        # If the parent of the new node is None, it is the root of the tree and its color should be black
        if node.parent == None:
            node.color = 0
            return
        
        # If the grandparent of the new node is None, the tree is still a valid RB tree
        if node.parent.parent == None:
            return
        
        # Perform the necessary rotations and color changes to maintain the RB tree properties
        self.insertRotationHelper(node)


    def get_root(self):
        return self.root
    
    def delete_node(self, data):
        self.deleteNode(self.root, data)

    def pretty_print(self):
        self.__print_helper(self.root, "", True)





# GATOR TAXI FUNCTIONS
def insertRide(redBlackTree,minHeap,keyValueDict,rideNumber,rideCost,tripDuration):
    try:
        #if there is alreqdy a ride with the same rideNumber return 0 to help terminate the program.
        x=keyValueDict[rideNumber]
        return 0
    except:
        keyValueDict[rideNumber]=[rideCost,tripDuration]
        redBlackTree.insert(rideNumber)
        minHeap.insert(Ride(rideNumber,rideCost,tripDuration))
        return 1
def printRide(redBlackTree,minHeap,keyValueDict,rideNumber):
    try:#try to find the node with the exact rideNumber and stop executing if the node reaches a null] 
        # we can also directly print from the dictionary the value of the rideNumber , rideCost, tripDuration
        return [rideNumber,keyValueDict[rideNumber][0],keyValueDict[rideNumber][1]]
    except:
        return [0,0,0]
def printRides(root,minHeap,keyValueDict,x,rideNumber1,rideNumber2):
    try:#find the values lying in the range and ignore the Null nodes
        printRides(root.left,minHeap,keyValueDict,x,rideNumber1,rideNumber2)
        if root.data >= rideNumber1 and root.data <= rideNumber2:
            x.append([root.data,keyValueDict[root.data][0],keyValueDict[root.data][1]])
        else:
            pass
        printRides(root.right,minHeap,keyValueDict,x,rideNumber1,rideNumber2)
    except:
        pass
def getNextRide(redBlackTree, minHeap, keyValueDict):
    # extract min from the top of the minHeap
    x = minHeap.extract_min()
    try: #if the min heap is empty print that there are no active ride requests
        p = x.rideNumber
        redBlackTree.delete_node(p)
        keyValueDict.pop(p)
        return [x.rideNumber,x.rideCost,x.tripDuration]
    except:
        return "No active ride requests"

def cancelRide(redBlackTree,minHeap,keyValueDict,rideNumber):
    #find the ride Number and do nothing if the rideNumber doesnt exist
    try:
        #delete the ride from the redBlackTree and heap and update the dictionary accordingly
        redBlackTree.delete_node(rideNumber)
        minHeap.delete(Ride(rideNumber,keyValueDict[rideNumber][0],keyValueDict[rideNumber][1]))
        keyValueDict.pop(rideNumber)
    except:
        pass

def updateRide(redBlackTree,minHeap, keyValueDict, rideNumber, newTD):
    try:# if the requested rideNumber isnt found just skip the request.
        x = keyValueDict[rideNumber][1] # get the trip Duration
        if newTD < x: # if the new_tripDuration <= existing tripDuration, there would be no action needed just update the tripDuration.
            minHeap.delete(Ride(rideNumber,keyValueDict[rideNumber][0],keyValueDict[rideNumber][1]))
            minHeap.insert(Ride(rideNumber,keyValueDict[rideNumber][0],newTD))
            keyValueDict[rideNumber][1]=newTD
        elif newTD > x and newTD < 2* x: #if the existing_tripDuration < new_tripDuration <= 2*(existing tripDuration), the driver will cancel the existing ride and a new ride request would be created with a penalty of 10 on existing rideCost . We update the entry in the data structure with (rideNumber, rideCost+10, new_tripDuration)
            minHeap.delete(Ride(rideNumber,keyValueDict[rideNumber][0],keyValueDict[rideNumber][1]))
            minHeap.insert(Ride(rideNumber,keyValueDict[rideNumber][0]+10,newTD))
            keyValueDict[rideNumber][0]=keyValueDict[rideNumber][0]+10
            keyValueDict[rideNumber][1]=newTD
        elif newTD>2*x: #if the new_tripDuration > 2*(existing tripDuration), the ride would be automatically declined and the ride would be removed from the data structure.
            minHeap.delete(Ride(rideNumber,keyValueDict[rideNumber][0],keyValueDict[rideNumber][1]))
            redBlackTree.delete_node(rideNumber)
            keyValueDict.pop(rideNumber)
        else:
            pass
    except:
        pass
if __name__ == "__main__":
    redBlackTree = RedBlackTree()
    minHeap = MinHeap()
    keyValueDict=dict()
    fread = open(sys.argv[1],'r')
    fwrite = open("output_file.txt", 'w')
    flag = 1
    while flag:
        #Reads each line from the file
        line = fread.readline()
        #Check if the command says insert
        if "Insert" in line:
            cmdArgs = line[7:-2:] #Get the arguements from the command
            argList = cmdArgs.split(",") # seperate the arguements for the insert command
            rideNumber=int(argList[0])
            rideCost = int(argList[1])
            tripDuration = int(argList[2])
            flag = insertRide(redBlackTree,minHeap,keyValueDict,rideNumber,rideCost,tripDuration)
            if flag==0:
                fwrite.write("Duplicate RideNumber\n")# if rideNumber already exists in the tree terminate the program and print the following

        #Check if the command says GetNextRide
        if "GetNextRide" in line:
            #extract the min value in the minHeap and delete that corresponding node in the redBlackTree
            l = getNextRide(redBlackTree,minHeap,keyValueDict)
            #if there are no ride requests available print the same
            if "No active ride requests"==l:
                fwrite.write(l + "\n")
            else:
                fwrite.write("("+str(l[0])+","+str(l[1])+","+str(l[2])+")\n")

        #Check if the command says Print
        if "Print" in line:
            cmdArgs = line[6:-2:]
            argList = cmdArgs.split(",")
            #if there is only one arguement in the print command we use the printRide function
            if len(argList)==1:
                l=printRide(redBlackTree,minHeap,keyValueDict,int(argList[0]))
                fwrite.write("("+str(l[0])+","+str(l[1])+","+str(l[2])+")\n")
            # if there are 2 arguements in the print command we use the printRides function
            else:
                #get all the rides within the range of the 2 argumements
                p = []
                printRides(redBlackTree.root,minHeap,keyValueDict,p,int(argList[0]),int(argList[1]))
                string = ""
                #if there are no rides within the range print (0,0,0)
                if len(p)==0:
                    fwrite.write("(0,0,0)\n")
                #print all the rides in a single line
                else:
                    #concatenate the rides to a single line as required
                    for i in p:
                        string += "("+str(i[0])+","+str(i[1])+","+str(i[2])+")" + ","
                    fwrite.write(string[:-1] + "\n")

        #Check if the command says UpdateTrip
        if "UpdateTrip" in line:
            cmdArgs = line[11:-2:]  #Get the numbers to perform the operation
            argList = cmdArgs.split(",") #Get the arguements
            updateRide(redBlackTree,minHeap,keyValueDict,int(argList[0]),int(argList[1]))

        #Check if the command says Cancel
        if "Cancel" in line:
            cmdArgs = line[11:-2:] # Get the number
            argList = cmdArgs.split(',') #get the arguements for which ride to cancel
            cancelRide(redBlackTree,minHeap,keyValueDict,int(argList[0])) #cancel the ride from the redBlackTree and the minHeap

        #Check if the pointer reached the end of the file
        if line == "":
            flag = 0 # change the condition to terminate the group
    # next iteration / exit loop
    #close the files
    fwrite.close() 
    fread.close()  
