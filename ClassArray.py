try:
    # Python 3
    from collections.abc import MutableSequence
except ImportError:
    # Python 2.7
    from collections import MutableSequence

from Vector3 import *


def all_subclasses(clss=object):
    return list(set(clss.__subclasses__()).union(
        [s for c in clss.__subclasses__() for s in all_subclasses(c)]))


class TypedList(MutableSequence):
    """A container for manipulating lists of hosts"""

    def __init__(self, type_of=int, data=None, from_dict: dict = None):
        """Initialize the class"""
        super(TypedList, self).__init__()
        if from_dict == None:
            self.type_of = type_of
            for i in range(len(list(data))):
                if not isinstance(list(data)[i], self.type_of):
                    raise ValueError(
                        f"Value ({list(data)[i]}; class: {list(data)[i].__class__.__name__}; position: {i}) must be of type \"{self.type_of.__name__}\"")

            if data is not None:
                self._list = list(data)
            else:
                self._list = list()
        else:
            for i in object.__subclasses__():
                if from_dict["type_of"] == i.__name__:
                    self.type_of = i
                    break
            for i in range(len(from_dict['_list'])):
                if self.type_of == Vector3:
                    try:
                        from_dict['_list'][i] = Vector3(from_dict['_list'][i]['x'], from_dict['_list'][i]['y'],
                                                        from_dict['_list'][i]['z'])
                        continue
                    except TypeError:
                        raise ValueError(
                            f"Value \"{from_dict['_list'][i]}\" of type \"{Vector3.__name__}\" at position \"{i}\" must be of type \"{self.type_of.__name__}\"")
                if not isinstance(from_dict['_list'][i], self.type_of):
                    raise ValueError(
                        f"Value ({from_dict['_list'][i]}; class: {from_dict['_list'][i].__class__.__name__}; position: {i}) must be of type \"{self.type_of.__name__}\"")

            if from_dict['_list'] is not None:
                self._list = from_dict['_list']
            else:
                self._list = list()

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self._list)

    def __len__(self):
        """List length"""
        return len(self._list)

    def __getitem__(self, ii):
        """Get a list item"""
        if isinstance(ii, slice):
            return self.__class__(self._list[ii])
        else:
            return self._list[ii]

    def __delitem__(self, ii):
        """Delete an item"""
        del self._list[ii]

    def __setitem__(self, ii, val):
        # optional: self._acl_check(val)
        if isinstance(val, self.type_of):
            self._list[ii] = val
        else:
            raise ValueError(
                f"Value ({val}; class: {val.__class__.__name__}) must be of type \"{self.type_of.__name__}\"")

    def __str__(self):
        s = f'(Class: {self.type_of.__name__})['
        for i in range(len(self._list)):
            if i < len(self._list) - 1:
                s += f'{str(self._list[i])}, '
            else:
                s += f'{str(self._list[i])}]'
        return s

    def insert(self, ii, val):
        # optional: self._acl_check(val)
        if isinstance(val, self.type_of):
            self._list.insert(ii, val)
        else:
            raise ValueError(
                f"Value ({val}; class: {val.__class__.__name__}) must be of type \"{self.type_of.__name__}\"")

    def append(self, val):
        if isinstance(val, self.type_of):
            self.insert(len(self._list), val)
        else:
            raise ValueError(
                f"Value ({val}; class: {val.__class__.__name__}) must be of type \"{self.type_of.__name__}\"")

    def returnAsDict(self):
        return {"type_of": self.type_of.__name__, "_list": self._list}

    def returnAsList(self):
        return self._list


if __name__ == '__main__':
    foo = TypedList(int, [1, 2, 3, 4, 5])
    foo.append(6)
    print(foo)  # (Class: int)[1; 2; 3; 4; 5; 6]

    for idx, ii in enumerate(foo):
        print(f"MyList[{idx}] = {ii}")
