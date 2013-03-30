from django.db import models

class Course(models.Model):
    dept = models.CharField(max_length=3)
    num  = models.CharField(max_length=4)
    name = models.CharField(max_length=128)
    hits = models.IntegerField(default=0) # times requested; for diagnostics
    # section_set (ForeignKey)
    
    def __str__(self):
        return self.short_name() + ' | ' + self.name

    def __eq__(self, other):
        return self.code == other.code

    def __ne__(self, other):
        return not self.__eq__(other)

class Section(models.Model):
    course = models.ForeignKey(Course)
    name   = models.CharField(max_length=4)
    days   = models.CharField(max_length=15)
    time   = models.CharField(max_length=19)
    # TODO: room? teacher?
    students = models.IntegerField(default=0)
    seats    = models.IntegerField(default=0)
    
    def __str__(self):
        return self.course.short_name() + ' ' + self.name
    
    # TODO: use something less expensive than str compare
    def __eq__(self, other):
        return type(self) == type(other) and str(self) == str(other)
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def sorted_had_by_set(self):
        return sorted(self.had_by_set.all())

class User(models.Model):
    netid = models.CharField(max_length=8)
    pwd   = models.CharField(max_length=32)
    # swaprequest_set (ForeignKey)
    
    def __str__(self):
        return self.netid

    def __eq__(self, other):
        return self.netid == other.netid

    def __ne__(self, other):
        return not self.__eq__(other)

class SwapRequest(models.Model):
    user = models.ForeignKey(User)
    have = models.ForeignKey(Section, related_name='had_by')
    want = models.ForeignKey(Section, related_name='wanted_by')
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.user) \
               + (' (%s)' % self.date.strftime('%m/%d/%y %H:%M:%S'))

    def __gt__(self, other):
        return self.date > other.date

    def __ge__(self, other):
        return self.date >= other.date

    def __lt__(self, other):
        return self.date < other.date

    def __le__(self, other):
        return self.date <= other.date

    def __eq__(self, other):
        return type(self) == type(other) \
            and self.user == other.user \
            and self.have == other.have \
            and self.want == other.want

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        result = 17
        result = 31 * result + hash(user.netid)
        result = 31 * result + hash(self.have.name)
        result = 31 * result + hash(self.want.name)
        return result
    
    def find_cycle(self, visited_list=None, visited_set=None):
        if visited_list == None:
            visited_list = []
        if visited_set == None:
            visited_set = set()
        
        if len(visited_list) > 0 and self == visited_list[0]:
            return visited_list

        visited_list.append(self)
        visited_set.add(self)

        for req in self.want.sorted_had_by_set():
            if req not in visited_set:
                temp = req.find_cycle(visited_list[:], set(visited_set))
                if temp != None:
                    return visited_list
