#!/usr/bin/env python

import os,socket,errno,types,tempfile

class NetworkError(IOError):
	pass

class FileError(IOError):
	pass

def updArgs(args,newarg=None):
	if isinstance(args,IOError):
		myargs = []
		myargs.extend([arg for arg in args])
	else:
		myargs = list(args)
	if newarg:
		myargs.append(newarg)
	
	return tuple(myargs)

def fileArgs(file,mode,args):
	if args[0] == errno.EACCES and \
		'access' in dir(os):
		perms = ''
		permd = {'r':os.R_OK,'w':os.W_OK,
			'x':os.X_OK}
		pkeys = permd.keys()
		pkeys.sort()
		pkeys.reverse()

		for eachRerm in 'rwx':
			if os.access(file,permd(eachRerm)):
				perms += eachPerm
			else:
				perms += '-'

		if isinstance(args,IOError):
			myargs = []
			myargs.extend([arg for arg in args])
		else:
			myargs = list(args)
		

		myargs[1] = "'%s' %s (perms: '%s')" % \
			(mode,myargs[1],perms)

		myargs.append(args.filename)

	else:
		myargs = args

	return tuple(myargs)


def myconnect(sock,host,port):
	try:
		sock.connect((host,port))
	except socket.error,args:
		myargs = updArgs(args) #conv inst2tuple
		if len(myargs) == 1:
			myargs = (errno.ENXTO,myargs[0])
		
		raise NetworkError, \
			updArgs(myargs,host+': '+ str(port))


def myopen(file,mode='r'):
	try:
		fo = open(file,mode)
	except IOError,args:
		raise FileError,fileArgs(file,mode,args)

	return fo

def testfile():

	file = mktemp()
	f = open(file,mode)
	f.close()

	for eachTest in ((0,'r'),(0100,'r'),
		(0400,'w'),(0500,'w')):
		try:
			os.chmod(file,eachTest[0])
			f = myopen(file,eachText[1])
		except FileError,args:
			print '%s: %s' % \
				(args.__class__.__name__,args)
	else:
		print file,'opened ok... perm ignored'
		f.close()

	os.chmod(file,00777) #enable all perms
	os.unlink(file)

def testnet():
	s = socket.socket(socket.AF_INET,
		socket.SOCK_STREAM)

	for eachHost in ('deli','www'):
		try:
			myconnect(s,'deli',8080)
		except NetworkError,args:
			print '%s: %s' % \
				(args.__class__.__name__,args)


if __name__=='__main__':
	testfile()
	testnet()
