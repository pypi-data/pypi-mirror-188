from . import utils
from .f import F
from . import d
from .dbtypes import DB_PGSQL, DB_SQLITE3, DB_ORACLE, DB_MYSQL

OPS = {
	"gt": ">",
	"gte": ">=",
	"lt": "<",
	"lte": "<=",
	"neq": "<>",
	"eq": "=",
	"exact": "=",
	"regex": "~",
	"in": "IN",
	"notin": "NOT IN",
	"isnull": "IS",
	"exists": "EXISTS",
	"nexists": "NOT EXISTS",
	"notexist": "NOT EXISTS",
	"between": "BETWEEN",
	"range": "BETWEEN",
	"contains": "LIKE",
	"startswith": "LIKE",
	"endswith": "LIKE",
	"iexact": "ILIKE",
	"iregex": "~*",
	"icontains": "ILIKE",
	"istartswith": "ILIKE",
	"iendswith": "ILIKE",
	"ncontains": "NOT LIKE",
	"notcontain": "NOT LIKE",
	"nstartswith": "NOT LIKE",
	"notstartwith": "NOT LIKE",
	"nendswith": "NOT LIKE",
	"notendwith": "NOT LIKE",
	"haskey": "?",
	"haskeyin": "?|",
	"all": "=",
	"century": "date_part",
	"decade": "date_part",
	"year": "date_part",
	"iso_year": "date_part",
	"month": "date_part",
	"day": "date_part",
	"hour": "date_part",
	"minute": "date_part",
	"second": "date_part",
	"quarter": "date_part",
	"week": "date_part",
	"week_day": "date_part",
	"iso_week_day": "date_part",
	"day_of_year": "date_part",
	"date": "to_char",
	"time": "to_char",
}

class _Q:
	def __init__ (self, *args, **kargs):
		self._clause = None
		self._value = None
		self._void = False

		if kargs:
			assert len (kargs) == 1
			self.k, self.v = kargs.popitem ()
		elif len (args) == 0:
			self.k, self.v = "", None
		elif len (args) == 2:
			self.k, self.v = args
		else:
			self._clause = args [0]
		self._exclude = False

	def add_percent (self, val, pos = 0):
		if isinstance (val, F):
			val.add_percent (pos)
			return val
		val = val.replace ("%", "\\%")
		if pos == 0:
			return "%" + val + "%"
		elif pos == 1:
			return "%" + val
		return val + "%"

	def render (self, engine = DB_PGSQL, field_resolver = None, haystack_resolver = None):
		from .sql import SQL

		if self._clause is not None:
			if haystack_resolver:
				self._clause = haystack_resolver (self._clause)
			if self._exclude and self._clause:
				self._clause = "NOT (" + self._clause + ")"
				self._exclude = False
			return self._clause

		elif self.v is None:
			self._clause = ""
			self._void = True
			return self._clause

		else:
			if field_resolver:
				self.k = field_resolver (self.k, True)
			k, v = self.k, self.v
			es = k.split ('___')
			if len (es) > 1:
				assert engine == DB_PGSQL, 'JSON query is not available'
				tail = ''
				fd_ = [es [0]]
				for idx, e in enumerate (es [1:]):
					if idx + 2 == len (es):
						_ops = '>>'
					else:
						_ops = '>'
					e, *index = e.split ('__')
					if not index:
						index = None
					else:
						if index [0].isdigit ():
							tail = index [1:] or ''
							index = int (index [0])
						else:
							index, tail = None, index
						if tail:
							tail = '__{}'.format ('__'.join (tail))
					if index is not None:
						fd_.append (" #%s '{%s, %d}'" % (_ops, e, index))
					else:
						fd_.append (" -{} '{}'".format (_ops, e))
				k = ''.join (fd_) + tail

			ll = k.split ("__")
			if len (ll) == 1:
				fd, op = k, "eq"
			else:
				if ll [-1] in (OPS):
					fd, op = ".".join (ll [:-1]), ll [-1]
				else:
					fd, op = ".".join (ll), "eq"

			try:
				_op = OPS [op]
			except KeyError:
				raise TypeError ('Unknown Operator: {}'.format (op))

			_val = v
			_escape = True

			if fd.find ('>') != -1:
				if isinstance (_val, bool):
					fd = "CAST ({} AS boolean)".format (fd)
				elif isinstance (_val, int):
					fd = "CAST ({} AS int)".format (fd)
				elif isinstance (_val, float):
					fd = "CAST ({} AS float)".format (fd)

			if _op == 'date_part':
				arg = op
				if op.endswith ("iso_week_day"):
					arg = "isodow"
				elif op.endswith ("iso_year"):
					arg = "isoyear"
				elif op.endswith ("week_day"):
					arg = "dow"
				elif op == "day_of_year":
					arg = "doy"
				fd = f"DATE_APRT('{arg.upper ()}', {fd})"
				_op = '='
			elif op == "date":
				fd = f"TO_CAHR({fd}, 'yyyy-mm-dd')"
				_op = '='
				_val = _val.strftime ("%Y-%m-%d")
			elif op == "time":
				fd = f"TO_CAHR({fd}, 'hh24-mi-ss')"
				_op = '='
				_val = _val.strftime ("%H:%M:%S")

			if op.endswith ("all"):
				fd, _val = "1", int (_val)
			elif op in ("between", "range"):
				_val = "{} AND {}".format (d.toval (_val [0], engine), d.toval (_val [1], engine))
				_escape = False
			elif op == "isnull":
				if not _val: # False
					_op = "IS NOT"
				_val = None
			elif op == "haskey":
				assert isinstance (_val, str), "str type required"
				_op = "?"
			elif op == "haskeyin":
				assert isinstance (_val, (list, tuple)), "list or tuple type required"
				_op = "?| array"
				_val = '[' + ",".join (["'{}'".format (e) for e in _val]) + ']'
				_escape = False
			elif op in ('notin', 'in'):
				if isinstance (_val, (list, tuple)):
					_val = "({})".format (",".join ([d.toval (each, engine) for each in _val]))
				else:
					_val = "({})".format (str (_val))
				_escape = False
			elif op.endswith ("ains") or op.endswith ("ain"):
				_val = self.add_percent (_val, 0)
			elif op.endswith ("dswith") or op.endswith ("dwith"):
				_val = self.add_percent (_val, 1)
			elif op.endswith ("tswith") or op.endswith ("twith"):
				_val = self.add_percent (_val, 2)
			elif isinstance (_val, SQL):
				_val = "({})".format (str (_val))
				_escape = False

			self._value = _escape and d.toval (_val, engine) or _val
			self._clause = "{}{} {}".format (fd and (fd + ' ') or '', _op, self._value)

		if self._exclude and self._clause:
			self._clause =  "NOT (" + self._clause + ")"
			self._exclude = False
		return self._clause

	def _joinwith (self, op, b):
		if self and b:
			return Q ("({} {} {})".format (self, op, b))
		return self or b

	def __len__ (self):
		return (self._clause or self.v is not None) and 1 or 0

	def __str__ (self):
		return self.render ()

	def __repr__ (self):
		return "<sqlphile.q.Q_ object: {}>".format (self.render ())

	def __or__ (self, b):
		return self._joinwith ("OR", b)

	def __and__ (self, b):
		return self._joinwith ("AND", b)

	def __invert__ (self):
		self._exclude = True
		return self

def Q (*args, **kargs):
	clauses = []
	if args:
		for s in args:
			if s is None:
				continue
			clauses.append (_Q (s))

	if kargs:
		for k, v in kargs.items ():
			clauses.append (_Q (**{k : v}))

	if len (clauses) == 1:
		return clauses [0]

	stack = []
	for clause in clauses:
		res = clause.render ()
		if res:
			stack.append (res)

	if stack:
		return _Q ("(" + " AND ".join (stack) + ")")

	return _Q ("")

class V (_Q):
	def __init__ (self, *args, **kargs):
		self._clause = None
		self._value = None
		if kargs:
			assert len (kargs) == 1
			self.k, self.v = kargs.popitem ()
		elif len (args) == 2:
			self.k, self.v = args
		elif not args or args [0] is None:
			self.k, self.v = "", None
		else:
			self.k, self.v = "__eq", args [0]
		self._exclude = False

	def render (self, engine = DB_PGSQL):
		if self.v is None:
			return "NULL"
		_Q.render (self, engine)
		return self._value

	def __str__ (self):
		return self.render ()


def batch (**filters):
	Qs = []
	for k, v in filters.items ():
		if v is None:
			continue
		Qs.append (Q (**{k: v}))
	return Qs
