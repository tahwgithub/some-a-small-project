#!/usr/bin/env python

from time import ctime

print '*** Welcome to Metaclasses!'
print '\tMetaclass declaration first.'

class MetaC(type):
	def __init__(cls,name,bases,attrd):
		super(MetaC,cls).__init__(name,bases,attrd)
		print 'created class %r at:%s' % (name,ctime())

print '\t Class "Foo" declaration next.'

class Foo(object):
	__metaclass__ = MetaC
	def __init__(self):
		print '*** instantinated class %r at: %s' % \
			(self.__class__.__name__,ctime())

print '\tClass "Foo" instantiation next'
f = Foo()
print '\tDone'
