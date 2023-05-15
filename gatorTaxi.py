import sys

class Ride:
    def __init__(self, rideNumber, rideCost, tripDuration):
        self.rideNumber = rideNumber
        self.rideCost = rideCost
        self.tripDuration = tripDuration

    #Method to compare two rides based on cost and duration.
    def is_less_than(self, alternate_ride):
        if self.rideCost < alternate_ride.rideCost:
            return True
        elif self.rideCost > alternate_ride.rideCost:
            return False
        elif self.rideCost == alternate_ride.rideCost:
            if self.tripDuration > alternate_ride.tripDuration:
                return False
            else:
                return True
            
            
class MinHeap:
    def __init__(self):
        self.heapList = [0]
        self.current_size = 0
        
    #Method to insert a ride object into the heap
    def insert(self, ele):
        self.heapList.append(ele)
        self.current_size += 1
        self.heapify_up(self.current_size)
        
    #Method to do_swap two values in the heap
    def do_swap(self, ind1, ind2):
        temp = self.heapList[ind1]
        self.heapList[ind1] = self.heapList[ind2]
        self.heapList[ind2] = temp
        self.heapList[ind1].min_heap_index = ind1
        self.heapList[ind2].min_heap_index = ind2
    
    #Method to update the trip duration of a ride object in the heap
    def update_value(self, p, new_key):
        node = self.heapList[p]
        node.ride.tripDuration = new_key
        if p == 1:
            self.heapify_down(p)
        elif self.heapList[p // 2].ride.is_less_than(self.heapList[p].ride):
            self.heapify_down(p)
        else:
            self.heapify_up(p)

    #Method to delete a ride object from the heap
    def delete_value(self, p):
        self.do_swap(p, self.current_size)
        self.current_size -= 1
        *self.heapList, _ = self.heapList
        self.heapify_down(p)

    #Method to remove and return the minimum ride object from the heap
    def pop(self):
        if len(self.heapList) == 1:
            return 'No Rides Available'
        root = self.heapList[1]
        self.do_swap(1, self.current_size)
        self.current_size -= 1
        *self.heapList, _ = self.heapList
        self.heapify_down(1)
        return root

    def heapify_up(self, p):
        while (p // 2) > 0: #loop until the root node is reached
            # compare ride times of parent and child
            if self.heapList[p].ride.is_less_than(self.heapList[p // 2].ride):
                self.do_swap(p, (p // 2)) #do_swap parent and child if child is smaller
            else:
                # break out of the loop if child is larger than parent
                break 
            p = p // 2 # update the index to the parent

    def heapify_down(self, p):
        while (p * 2) <= self.current_size:  # loop until the end of the heap is reached
            ind = self.get_index_min_child(p)
            if not self.heapList[p].ride.is_less_than(self.heapList[ind].ride):
                self.do_swap(p, ind)
            p = ind
    
    def get_index_min_child(self, p):
        if (p * 2) + 1 > self.current_size: #if the right child is beyond the end of the heap, return the left child index
            return p * 2
        else: #otherwise, return the index of the smallest child
            if self.heapList[p * 2].ride.is_less_than(self.heapList[(p * 2) + 1].ride):
                return p * 2
            else:
                return (p * 2) + 1


class MinHeapNode:
    def __init__(self, ride, rbt, min_heap_index):
        self.ride = ride
        self.rbTree = rbt
        self.min_heap_index = min_heap_index
        
        
class RBTNode:
    def __init__(self, ride, min_heap_node):
        self.ride = ride
        self.parent = None  # parent node
        self.left = None  # left node
        self.right = None  # right node
        self.color = 1  # 1=red , 0 = black
        self.min_heap_node = min_heap_node


class RedBlackTree:
    def __init__(self):
        self.null_node = RBTNode(None, None)
        self.null_node.left = None
        self.null_node.right = None
        self.null_node.color = 0
        self.root = self.null_node
        
    def left_rotate(self, x):
        #Rotating the tree left at the given node x
        y = x.right
        x.right = y.left
        if y.left != self.null_node:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        #Rotating the tree right at the given node x
        y = x.left
        x.left = y.right
        if y.right != self.null_node:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
        
    # Searching the tree for the node with a rideNumber equal to key
    def get_ride(self, key):
        temp = self.root
        while temp != self.null_node:
            if temp.ride.rideNumber == key:
                return temp
            if temp.ride.rideNumber < key:
                temp = temp.right
            else:
                temp = temp.left
        # If node with rideNumber key not found, return None
        return None

    def rb_relocate(self, node, child_node):
        # Replace node with child_node in the Red-Black Tree
        if node.parent is None:
            # If node is root, set child_node as root
            self.root = child_node
        elif node == node.parent.right:
            node.parent.right = child_node
        else:
            node.parent.left = child_node
        # Update child_node's parent
        child_node.parent = node.parent

    def deleteNode(self, rideNumber):
        return self.deleteNode_assist(self.root, rideNumber) # Call the helper method with the root node and provided key
    
    #  Helper method for deletion of a node from the tree
    def deleteNode_assist(self, node, key):
        deleteNode = self.null_node
        while node != self.null_node:
            if node.ride.rideNumber == key:
                deleteNode = node
            if node.ride.rideNumber >= key:
                node = node.left
            else:
                node = node.right

        if deleteNode == self.null_node:
            return
        heap_node = deleteNode.min_heap_node
        y = deleteNode
        y_original_color = y.color
        if deleteNode.left == self.null_node:
            x = deleteNode.right
            self.rb_relocate(deleteNode, deleteNode.right)
        elif (deleteNode.right == self.null_node):
            x = deleteNode.left
            self.rb_relocate(deleteNode, deleteNode.left)
        else:
            y = self.minimum(deleteNode.right)
            y_original_color = y.color
            x = y.right
            if y.parent == deleteNode:
                x.parent = y
            else:
                self.rb_relocate(y, y.right)
                y.right = deleteNode.right
                y.right.parent = y

            self.rb_relocate(deleteNode, y)
            y.left = deleteNode.left
            y.left.parent = y
            y.color = deleteNode.color
        if y_original_color == 0:
            self.bt_after_delete(x)
        return heap_node

    #balance the tree after deleting
    def bt_after_delete(self, node):
        while node != self.root and node.color == 0:
            if node == node.parent.right:
                parent_sibling = node.parent.left
                if parent_sibling.color != 0:
                    node.parent.color = 1
                    parent_sibling.color = 0
                    self.right_rotate(node.parent)
                    parent_sibling = node.parent.left

                if parent_sibling.right.color == 0 and parent_sibling.left.color == 0:
                    parent_sibling.color = 1
                    node = node.parent
                else:
                    if parent_sibling.left.color != 1:
                        parent_sibling.right.color = 0
                        parent_sibling.color = 1
                        self.left_rotate(parent_sibling)
                        parent_sibling = node.parent.left

                    parent_sibling.color = node.parent.color
                    node.parent.color = 0
                    parent_sibling.left.color = 0
                    self.right_rotate(node.parent)
                    node = self.root
            else:
                parent_sibling = node.parent.right
                if parent_sibling.color != 0:
                    node.parent.color = 1
                    parent_sibling.color = 0
                    self.left_rotate(node.parent)
                    parent_sibling = node.parent.right

                if parent_sibling.right.color == 0 and parent_sibling.left.color == 0:
                    parent_sibling.color = 1
                    node = node.parent
                else:
                    if parent_sibling.right.color != 1:
                        parent_sibling.left.color = 0
                        parent_sibling.color = 1
                        self.right_rotate(parent_sibling)
                        parent_sibling = node.parent.right

                    parent_sibling.color = node.parent.color
                    node.parent.color = 0
                    parent_sibling.right.color = 0
                    self.left_rotate(node.parent)
                    node = self.root

        node.color = 0
        
    def insert(self, ride, min_heap):
        node = RBTNode(ride, min_heap)
        node.parent = None
        node.left = self.null_node
        node.right = self.null_node
        node.color = 1

        insertion_node = None
        temp_node = self.root

        while temp_node != self.null_node:
            insertion_node = temp_node
            if node.ride.rideNumber < temp_node.ride.rideNumber:
                temp_node = temp_node.left
            else:
                temp_node = temp_node.right

        node.parent = insertion_node
        if insertion_node is None:
            self.root = node
        elif node.ride.rideNumber > insertion_node.ride.rideNumber:
            insertion_node.right = node
        else:
            insertion_node.left = node

        if node.parent is None:
            node.color = 0
            return

        if node.parent.parent is None:
            return

        self.bt_after_insert(node)
    
    #balance the tree after inserting        
    def bt_after_insert(self, curr_node):
        while curr_node.parent.color == 1:
            if curr_node.parent == curr_node.parent.parent.left:
                parent_sibling = curr_node.parent.parent.right

                if parent_sibling.color == 0:
                    if curr_node == curr_node.parent.right:
                        curr_node = curr_node.parent
                        self.left_rotate(curr_node)
                    curr_node.parent.color = 0
                    curr_node.parent.parent.color = 1
                    self.right_rotate(curr_node.parent.parent)
                else:
                    parent_sibling.color = 0
                    curr_node.parent.color = 0
                    curr_node.parent.parent.color = 1
                    curr_node = curr_node.parent.parent

            else:
                parent_sibling = curr_node.parent.parent.left
                if parent_sibling.color == 0:
                    if curr_node == curr_node.parent.left:
                        curr_node = curr_node.parent
                        self.right_rotate(curr_node)
                    curr_node.parent.color = 0
                    curr_node.parent.parent.color = 1
                    self.left_rotate(curr_node.parent.parent)
                else:
                    parent_sibling.color = 0
                    curr_node.parent.color = 0
                    curr_node.parent.parent.color = 1
                    curr_node = curr_node.parent.parent

            if curr_node == self.root:
                break
        self.root.color = 0

    #Finding all rides in the tree whose rideNumber falls within the specified range (inclusive) and append the rides to result list
    def find_rides(self, node, low, high, res):
        if node == self.null_node:
            return

        if low < node.ride.rideNumber:
            self.find_rides(node.left, low, high, res)
        if low <= node.ride.rideNumber <= high:
            res.append(node.ride)
        self.find_rides(node.right, low, high, res)

    #Return list of all rides in the tree whose rideNumber falls within the specified range (inclusive)
    def get_rides(self, low, high):
        res = []
        self.find_rides(self.root, low, high, res)
        return res

    def minimum(self, node):
        while node.left != self.null_node:
            node = node.left
        return node



#Insert new ride
def insert_ride(ride, heap, rbt):
    if rbt.get_ride(ride.rideNumber) is not None:
        write_to_output(None, "Duplicate RideNumber", False)
        sys.exit(0)
        return
    rbt_node = RBTNode(None, None)
    min_heap_node = MinHeapNode(ride, rbt_node, heap.current_size + 1)
    heap.insert(min_heap_node)
    rbt.insert(ride, min_heap_node)


def write_to_output(ride, message, list):
    file = open("output_file.txt", "a")
    if ride is None:
        file.write(message)
    else:
        message = ""
        if not list:
            message += ("(" + str(ride.rideNumber) + "," + str(ride.rideCost) + "," + str(ride.tripDuration) + ")")
        else:
            if len(ride) == 0:
                message += "(0,0,0)"
            for i in range(len(ride)):
                if i != len(ride) - 1:
                    message = message + ("(" + str(ride[i].rideNumber) + "," + str(ride[i].rideCost) + "," + str(
                        ride[i].tripDuration) + "),")
                else:
                    message = message + ("(" + str(ride[i].rideNumber) + "," + str(ride[i].rideCost) + "," + str(
                        ride[i].tripDuration) + ")")

        file.write(message)
    if not (ride is None and message=="Duplicate RideNumber"):
        file.write("\n")
    file.close()

#Print the ride
def print_ride(rideNumber, rbt):
    res = rbt.get_ride(rideNumber)
    if res is None:
        write_to_output(Ride(0, 0, 0), "", False)
    else:
        write_to_output(res.ride, "", False)


def printRides(l, h, rbt):
    list = rbt.get_rides(l, h)
    write_to_output(list, "", True)

#Get the next ride with low cost
def getNextRide(heap, rbt):
    if heap.current_size != 0: # check if there are any ride requests in the heap
        popped_node = heap.pop()
        rbt.deleteNode(popped_node.ride.rideNumber)
        write_to_output(popped_node.ride, "", False)
    else:
        write_to_output(None, "No active ride requests", False)

#Cancel the ride
def cancelRide(ride_number, heap, rbt):
    heap_node = rbt.deleteNode(ride_number)
    if heap_node is not None:
        heap.delete_value(heap_node.min_heap_index)

#Update the ride
def updateRide(rideNumber, new_duration, heap, rbt):
    # Get the node with the given rideNumber from the RBT
    rbt_node = rbt.get_ride(rideNumber)
    if rbt_node is None:
        #no such ride exists, print a blank line
        print("")
    elif new_duration <= rbt_node.ride.tripDuration: # If new duration <= current duration of the ride, update the heap with the new duration
        heap.update_value(rbt_node.min_heap_node.min_heap_index, new_duration)
    elif rbt_node.ride.tripDuration < new_duration <= (2 * rbt_node.ride.tripDuration): # If the new duration is between the current duration and twice the current duration of the ride, cancel the current ride
        # and insert a new ride with an increased cost and the new duration
        cancelRide(rbt_node.ride.rideNumber, heap, rbt)
        insert_ride(Ride(rbt_node.ride.rideNumber, rbt_node.ride.rideCost + 10, new_duration), heap, rbt)
    else: # If new duration is more than twice the current duration of the ride, cancel the ride
        cancelRide(rbt_node.ride.rideNumber, heap, rbt)


if __name__ == "__main__":
    input_file = sys.argv[1]
    heap = MinHeap()
    rbt = RedBlackTree()
    with open("output_file.txt", "w") as output_file:
        pass

    with open(input_file, "r") as input_file:
        for line in input_file.readlines():
            numbers = [int(num) for num in line[line.index("(") + 1:line.index(")")].split(",") if num != '']
            action = line.split("(")[0].strip()

            if action == "Insert":
                insert_ride(Ride(numbers[0], numbers[1], numbers[2]), heap, rbt)
            elif action == "Print":
                if len(numbers) == 1:
                    print_ride(numbers[0], rbt)
                elif len(numbers) == 2:
                    printRides(numbers[0], numbers[1], rbt)
            elif action == "UpdateTrip":
                updateRide(numbers[0], numbers[1], heap, rbt)
            elif action == "GetNextRide":
                getNextRide(heap, rbt)
            elif action == "CancelRide":
                cancelRide(numbers[0], heap, rbt)

    
    

