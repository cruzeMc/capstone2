#!/usr/bin/env python
from copy import *
from inspect import *
from os.path import *
from sys import *
import sys

class TypeError(TypeError): pass
class Exception(Exception): pass

debug = False

def caller_modules():
    try:
        frames = getouterframes(currentframe())
        modules = []
        for frame,filename,line_number,function_name,lines,index in frames:
            module = getmodule(frame)
            if module and module not in modules:
                modules.append(module)
        return modules
    except IndexError:
        return []

def __all__debug(bool=True):
    global debug
    debug = bool

def append(module,name):
    global debug
    __all__ = module.__dict__.setdefault('__all__', [])
    if name not in __all__:  # Prevent duplicates if run from an IDE.
        __all__.append(name)
        if debug:
            print("%s.__all__ +%s" % (module.__name__,name))
        setattr(module,"__all__",sorted(__all__))

def isstring(object):
    try:
        int(object)
        return False
    except ValueError:
        return True
    except:
        return False

def publish2module(object,module,force=False):
    if module is None:
        err = "module is None"
        raise Exception(err)
    if not hasattr(module,"__file__"):
        # system module?
        err = "%s has no attribute __file__" % module
        raise Exception(err)
    file = module.__file__
    if isstring(object): # text
        name = object
        dir = dirname(file)
        if not hasattr(module,name) and not force:
            # not object name or not exists
            # object str value?
            for mname,member in getmembers(module):
                if id(member)==id(name):
                    return publish2module(mname,module)
        append(module,name)
        ismod = basename(file).find("__init__")!=0
        if ismod:
            # find parent package
            # iterate sys.modules
            for _,m in copy(modules).items():
                if not m or not hasattr(m,"__file__"):
                    continue
                ispkg = basename(m.__file__).find("__init__.py")==0
                if ispkg and dirname(m.__file__)==dir:
                    publish2module(name,m)
        return
    if isclass(object) or isroutine(object): 
        name = object.__name__
        return publish2module(name,module,force=True)
    # find object, compare by id
    for mname,member in getmembers(module):
        if id(member)==id(object):
            return publish2module(mname,module)
    # fix imp.load_module with custom name
    # search same module
    for k,m in modules.iteritems():
        if m and hasattr(m,"__file__") and m.__file__==file:
            module = m
            for mname,member in getmembers(module):
                if id(member)==id(object):
                    return publish2module(mname,module)
            for mname,member in getmembers(module):
                if member==object:
                    return publish2module(mname,module)
    # find object last try
    for mname,member in getmembers(module):
        if member==object:
            return publish2module(mname,module)
    err = "%s not exists in %s" % (object,module)
    raise Exception(err)

def public(*objects):
    """public decorator for __all__
    """
    modules = caller_modules()
    if len(modules)==1 or (objects and objects[0]==public):
        module = modules[0]
    else:
        modules = modules[1:] # exclude public
        module = modules[0]
    if not module: # error?
        if len(objects)==1:
            return objects[0]
        else:
            return objects
    for object in objects:
        if not hasattr(object,"__name__"):
            for k,v in module.__dict__.items():
                if v==object:
                    object=k
        if not (isclass(object) or isfunction(object) or isstring(object)):
            err = "@public expected class, function or str object name"
            raise TypeError(err)
        modname = module.__name__
        modnames = modname.split(".")
        for i,modname in enumerate(modnames):
            fullname = ".".join(modnames[0:i+1])
            if fullname in sys.modules:
                module = sys.modules[fullname]
                publish2module(object,module)
    if len(objects)==1:
        return objects[0]
    else:
        return objects

public(public)

if __name__=="__main__":
    print(__all__)
    
    # @public
    @public
    def func(): pass
    print(__all__)

    # public(*objects)
    def func2(): pass
    public(func2)
    print(__all__)
    public("func3")
    print(__all__)

    kwargs=dict(k="v")
    public(kwargs)
    print(__all__)

