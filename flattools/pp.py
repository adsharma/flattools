"""
Add this to your .gdbinit

python
import sys
import gdb
sys.path.insert(0, '/path/to/flattools')
import flattools.pp
flattools.pp.register_printers()
end
"""

###

import gdb
import re

class FlatbufferPrinter(object):
  """Prints a flatbuffer."""
  def __init__(self, value):
    self.value = value
    cptr_type = gdb.lookup_type("unsigned char").pointer()
    ptr_type = gdb.lookup_type("flatbuffers::soffset_t").pointer()
    voff_type = gdb.lookup_type("flatbuffers::voffset_t").pointer()
    # See Table::GetVTable()
    vtable_off = value.address.cast(ptr_type).dereference()
    self.vtable = value.address.cast(cptr_type) - vtable_off
    self.size = self.vtable.reinterpret_cast(voff_type).dereference()

  def to_string(self):
    out = "flatbuffer: (vtable: %x, size: %d)" % (self.vtable, self.size)
    voff_type = gdb.lookup_type("flatbuffers::voffset_t")
    soff_type = gdb.lookup_type("flatbuffers::soffset_t")
    start = self.vtable + voff_type.sizeof * 2 # offset, size
    end = self.vtable + self.size
    for i, p in enumerate(range(start, end, voff_type.sizeof)):
        val = gdb.Value(p).cast(voff_type.pointer()).dereference()
        out += "\nslot %d, addr: %x, pointer: %x" % (i, p, end + val)
    out += "\n"
    return out

def lookup_function(val):
    type = val.type
    if type.code == gdb.TYPE_CODE_REF:
        type = type.target()
    type = type.unqualified().strip_typedefs()
    typename = type.tag
    if not typename:
        return None
    for function, pretty_printer in pretty_printers_dict.items():
        if function.search(typename):
            return pretty_printer(val)
    return None


def build_pretty_printers_dict():
    pretty_printers_dict[re.compile('^.*flatbuffers::Table')] = FlatbufferPrinter

pretty_printers_dict = {}

build_pretty_printers_dict()

def register_printers():
    gdb.pretty_printers.append(lookup_function)
