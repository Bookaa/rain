from . import ast as A

class RunMacro:
  def __init__(self, params, args):
    self.params = params
    self.args = args
    self.values = {}
    self.retptr = None

  def run_block(self, block):
    for stmt in block.stmts:
      if isinstance(stmt, A.return_node):
        val = self.run(stmt.value)
        return val
      if isinstance(stmt, A.assn_node):
        if isinstance(stmt.lhs, A.name_node):
          name = stmt.lhs.value
          value = self.run(stmt.rhs)
          self.values[name] = value
          continue
        if isinstance(stmt.lhs, A.idx_node) and isinstance(stmt.lhs.rhs, A.int_node):
          lhs = self.run(stmt.lhs.lhs)
          n = stmt.lhs.rhs.value
          value = self.run(stmt.rhs)
          assert isinstance(lhs, list)
          lhs[n] = value
          continue
      if isinstance(stmt, A.save_node):
        val = self.run(stmt.value)
        self.retptr = val
        continue
      if isinstance(stmt, A.for_node):
        aa = stmt.body, stmt.funcs, stmt.names
        assert len(stmt.funcs) == 1
        assert len(stmt.names) == 1
        name1 = stmt.names[0]
        func1 = stmt.funcs[0]
        vals = self.run(func1)
        assert isinstance(vals, list)
        for val in vals:
          self.values[name1] = val
          self.run_block(stmt.body)
        continue
      if isinstance(stmt, A.meth_node):
        args = self.runs(stmt.args)
        if isinstance(stmt.rhs, A.str_node):
          lhs = self.run(stmt.lhs)
          name = stmt.rhs.value
          if isinstance(lhs, A.block_node) and name == 'add':
            (arg,) = args
            lhs.stmts.append(arg)
            continue
    return self.retptr
  def runs(self, args):
    lst = []
    for arg in args:
      val = self.run(arg)
      lst.append(val)
    return lst
  def run(self, node):
    if isinstance(node, A.null_node):
      return None
    if isinstance(node, A.name_node):
      name = node.value
      if name in self.params:
        idx = self.params.index(name)
        return self.args[idx]
      if name in self.values:
        bb = self.values[name]
        if isinstance(bb, A.name_node):
          return A.name_node(bb.value)
        return bb
      return node
    if isinstance(node, A.meth_node):
      assert not node.catch
      lhs = node.lhs
      rhs = node.rhs
      if isinstance(lhs, A.name_node) and isinstance(rhs, A.str_node):
        lhs_val = self.run(lhs)
        rhs_name = rhs.value
        if rhs_name == 'items':
          assert isinstance(lhs_val, list)
          return lhs_val
        if rhs_name == 'call':
          (arg2,) = self.runs(node.args)
          return A.call_node(lhs_val, arg2)
      if isinstance(lhs, A.idx_node) and isinstance(rhs, A.str_node):
        if isinstance(lhs.lhs, A.name_node) and isinstance(lhs.rhs, A.str_node):
          if (lhs.lhs.value, lhs.rhs.value, rhs.value) == ('ast', 'if', 'new'):
            # astr.if_.new
            pred, body, els = self.runs(node.args)
            return A.if_node(pred, body, els)
          if (lhs.lhs.value, lhs.rhs.value, rhs.value) == ('ast', 'block', 'empty'):
            # astr.block.new
            assert node.args == []
            return A.block_node([])
          if (lhs.lhs.value, lhs.rhs.value, rhs.value) == ('ast', 'call', 'new'):
            # astr.call.new
            arg1, arg2 = self.runs(node.args)
            return A.call_node(arg1, [arg2])
          if (lhs.lhs.value, lhs.rhs.value, rhs.value) == ('ast', 'name', 'new'):
            # astr.name.new
            (arg,) = node.args
            assert isinstance(arg, A.str_node)
            return A.name_node(arg.value)

    if isinstance(node, A.idx_node):
      if isinstance(node.rhs, A.str_node):
        lhs = self.run(node.lhs)
        name = node.rhs.value
        return getattr(lhs, name)

    if isinstance(node, A.table_node):
      return node

    if isinstance(node, A.array_node):
      return [self.run(a) for a in node.items]

    assert False

def macro_expand(node, args):
  the = RunMacro(node.params, args)
  return the.run_block(node.body)

