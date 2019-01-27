
import math

def calculate_distance(ptA, ptB):
    xA, yA = ptA
    xB, yB = ptB
    d = math.sqrt((xB-xA)**2 + (yB-yA)**2)
    return d

class Path(object):
    def __init__(self):
        self.points = []

    def clear_path(self):
        self.points = []

    def get_points(self):
        return self.points

    def get_total_length(self):
        n = len(self.points)
        total_length = 0
        if n < 2:
            return total_length
        for i in range(n-1):
            xA, yA = self.points[i]
            xB, yB = self.points[i+1]
            d = math.sqrt((xB-xA)**2 + (yB-yA)**2)
            total_length += d
        return total_length

    def add_point(self, point):
        self.points.append(point)

    def read_from_file(self, filename):
        """ Create path from file with list of points """
        delimiter = ','
        self.clear_path()
        with open(filename, 'r') as f:
            for line in f:
                x, y = [int(val.strip()) for val in line.split(delimiter)]
                self.add_point((x,y))

    def get_step_count(self):
        """ Get number of steps (segments) of this path """
        step_count = len(self.points) - 1
        if step_count < 0: step_count = 0
        return step_count

    def get_step(self, index):
        """ Return tuple of two points. ((FromX,FromY),(ToX,ToY))
            One-based. Step 1 is first.
            Return None if index out of bounds.
        """
        if index < 1 or index > self.get_step_count():
            return None
        else:
            ptA = self.points[index - 1]
            ptB = self.points[index]
            return (ptA, ptB)

    def get_step_length(self, index):
        step = self.get_step(index)
        if not step:
            return 0
        else:
            pts = self.get_step(index)
            xA, yA = pts[0]
            xB, yB = pts[1]
            d = math.sqrt((xB-xA)**2 + (yB-yA)**2)
            return d

    def get_position(self, current_step, step_position, distance_traveled):
        """ Get new (step, pos) pair given starting position and dist traveled """
        if current_step > self.get_step_count():
            return (current_step, step_position + 100)
        elif current_step < 1:
            return (0, 0)
        else:
            step_length = self.get_step_length(current_step)
            remaining = step_length - step_position
            if distance_traveled < remaining:
                step_position += distance_traveled
                return (current_step, step_position)
            else:
                distance_traveled -= remaining
                current_step += 1
                step_length = self.get_step_length(current_step)
                step_position = 0
                while step_position + distance_traveled > step_length and current_step <= self.get_step_count():
                    current_step += 1
                    distance_traveled -= step_length
                step_position = distance_traveled
                return (current_step, step_position)

    def get_location(self, current_step, current_step_distance):
        loc = None
        if current_step <= self.get_step_count():
            step_length = self.get_step_length(current_step)
            ptA, ptB = self.get_step(current_step)
            xA, yA = ptA
            xB, yB = ptB
            fraction = (current_step_distance * 1.0) / step_length
            locX = xA + (xB - xA) * fraction
            locY = yA + (yB - yA) * fraction
            loc = (locX, locY)
        return loc





    def print_path(self):
        print("Printing path...")
        for pt in self.points:
            print("Point: ", pt)


if __name__ == '__main__':
    fn = 'data/path01.txt'
    p = Path()
    p.read_from_file(fn)
    p.print_path()
