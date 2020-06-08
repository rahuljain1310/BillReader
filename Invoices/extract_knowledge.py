import numpy as np
def isKeyword(s):
	# return if s is a key or value
	pass

def isNumber(s):
	# return if text is a number valued, cannot span multiple lines
	pass

# list(list(list(dict(['text':string,'point':dict('minx','miny','maxx','maxy'),'details':)))

def is_align(p1,p2):
	pass
def get_datav(p1,sect):
	width = p1['maxy'] - p1['miny']
	length = p1['maxx'] - p1['minx']
	scores = np.zeros((len(sect)))
	L = 0.1
	R = 1.8
	D = 0.7
	SCORE_MIN = 1
	for i  in range(len(sect)):
		p = sect[i]['point']
		w = p['maxy'] - p['miny']
		l = p['maxx'] - p['minx']
		xdiff = p1['minx'] - p['minx']
		ydiff = p1['miny'] - p['maxy']
		cx = min(p1['maxx'] - p['minx'], p['maxx'] - p1['minx'])

		if (w/width > R or width/w > R):
			scores[i] = 0
		# elif (ydiff/np.sqrt(w*width) < 0.7):
		ys = np.sqrt(w*width)/ydiff 
		if (ys < 1):
			scores[i] = 0
		xs1 = np.sqrt(l*length)/xdiff
		xs2 = cx/np.sqrt(l*length)
		if (xs2 < 0):
			scores[i] = 0
		if (xs1 < 2):
			scores[i] = 0
		scores[i] = ys + xs1 + 2*xs2

	ju = np.argmax(scores)
	if (scores[ju] < SCORE_MIN):
		ju = -1
	return ju

def is_align(p1,p2):
	u_diff = p2['miny'] - p1['miny']
	b_diff = p2['maxy'] - p1['maxy']
	w_diff = abs(u_diff - b_diff)
	L = 0.1
	if (abs(u_diff) > L  or abs(b_diff) > L or w_diff > L):
		return False
	else:
		return True

def group(section):
	h = len(section)
	ind = [0]*h
	
	grouped = list([-1]*len(sec) for sec in section)
	matched = list([False]*len(sec) for sec in section)  ## No constraint
	smatched = list([False]*len(sec) for sec in section) ## Horizontal constraint
	# table_entry = False
	g = 0
	## for 1st row ##
	
	for i in range(h):
		dl = section[i]	
		# if 
		for j in range(len(section[i])):
			if dl[j]['details']['isNumber']:
		 		smatched[i][j] = True
			ginc = False
			if (not dl[j]['details']['isKeyword']):
				if (i==0):
					if (j==0):
						ginc = True
					elif ( is_align(dl[j]['point'],dl[j-1]['point'])):
						if (dl[j-1]['details']['isKeyword'] and (not (matched[i][j-1]))):
							matched[i][j] = True
							section[i][j]['matched'] = True
							grouped[i][j] = grouped[i][j-1]
						elif (dl[j-1]['details']['isKeyword'] or matched[i][j-1]):
							ginc = True
						else:
							grouped[i][j] = grouped[i][j-1]
					else:
						ginc = True
					# if (dl[j]['details']['isNumber']):
					# 	matched[i][j] = True
					# grouped[i][j] = g
				else: ## not first line
					check_above = False
					if (j==0): ## if first element from left
						check_above = True
					else:
						## first check from side
						if ( is_align(dl[j]['point'],dl[j-1]['point'])):
							if (dl[j-1]['details']['isKeyword'] and (not (matched[i][j-1]))):
								matched[i][j-1] = True ## match previous key
								section[i][j-1]['matched'] = True
								# if (dl[j]['details']['isNumber']):
								# 	matched[i][j] = True
								grouped[i][j] = grouped[i][j-1] ## aligned with left
							elif (dl[j-1]['details']['isKeyword'] or matched[i][j-1]):
								check_above = True
							else:
								grouped[i][j] = grouped[i][j-1] ## aligned with left
	
						## check from above
						else: 
							check_above = True

					if (check_above):
						ju = get_datav(dl[j]['point'],section[i-1])
						if (ju==-1 or  matched[i-1][ju] or smatched[i-1][ju]):
							ginc = True
						else:
							if (section[i-1][ju]['details']['isKeyword']):
								matched[i-1][ju] = True
								section[i-1][ju]['matched'] = True
								grouped[i][j] = grouped[i-1][ju]
								# if (dl[j]['details']['isNumber']):
								# 	matched[i][j] = True
							
			
			else: ## if a key then another group
				ginc = True

			if (ginc):
				grouped[i][j] = g
				g+=1
							
	groupes = [[] for i  in range(g)]
	for i in range(h):
		for j in range(len(section[i])):
			groupes[grouped[i][j]].append(section[i][j])
	return groupes


	
	# #
def extract(data):
	groups = []
	knwoledge = dict()
	for section in data:
		groups.extend(group(section))
	i = 0
	l = len(groups)
	extracted =[False]*len(l)
	for g in groups:
		if (len(g)==0):
			extracted[i] = True
		
		elif (len(g)==1):
			knwoledge[str(i)+':'] = g[0]
			extracted[i] = True

		elif (g[0]['details']['isKeyword'] and 'matched' in g[0]):
			pkey = g[0]
			value =  ' '.join(g[1:])
			knwoledge[str(i) + ':' + pkey] = value
			extracted[i] = True
		
		i+=1

	## recognize table
	def half_keys(g):
		numk = 0
		for gi in g:
			if gi['details']['isKeyword']:
				numk +=1
		if (numk >= (len(g)+1)/2):
			return True
		else:
			return False
	return knwoledge
	# i = 0
	# while(i<len(groups)):
	# 	if not extracted[i]:
	# 		if half_keys(groups[i]):

	# 		else:
				
			

	