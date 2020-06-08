import numpy as np
def isKeyword(s):
	# return if s is a key or value
	pass

def isNumber(s):
	# return if text is a number valued, cannot span multiple lines
	pass

# list(list(list(dict(['text':string,'point':dict('minX','minY','maxX','maxY'),'details':)))

# def is_align(p1,p2):
# 	pass
def get_datav(p1,sect):
	width = p1['maxY'] - p1['minY']
	length = p1['maxX'] - p1['minX']
	scores = np.zeros((len(sect)))
	L = 0.1
	R = 1.8
	D = 0.7
	SCORE_MIN = 1
	for i  in range(len(sect)):
		p = sect[i]['point']
		w = p['maxY'] - p['minY']
		l = p['maxX'] - p['minX']
		xdiff = p1['minX'] - p['minX'] + 0.01
		ydiff = p1['minY'] - p['maxY'] + 0.01
		cx = min(p1['maxX'] - p['minX'], p['maxX'] - p1['minX'])

		if (w/width > R or width/w > R):
			scores[i] = 0
		# elif (ydiff/np.sqrt(w*width) < 0.7):
		ys = ydiff/np.sqrt(w*width)
		xs1 = np.sqrt(l*length)/xdiff
		xs2 = cx/np.sqrt(l*length)
		scores[i] = ys + xs1 + 2*xs2
		
		if (ys > 1.3):
			scores[i] = 0
		if (xs2 < 0):
			scores[i] = 0
		if (xs1 < 2):
			scores[i] = 0
		

	ju = np.argmax(scores)
	if (scores[ju] < SCORE_MIN):
		ju = -1
	return ju

def is_align(p1,p2):
	u_diff = p2['minY'] - p1['minY']
	b_diff = p2['maxY'] - p1['maxY']
	w1 = p1['maxY'] - p1['minY']
	w2 = p2['maxY'] - p1['minY']
	w = np.sqrt(w1*w2)
	w_diff = abs(u_diff - b_diff)
	L = 2
	if (abs(u_diff/w) > L  or abs(b_diff/w) > L or w_diff/w > L):
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
			section[i][j]['matched'] = False
			if dl[j]['details']['isNumber']:
		 		smatched[i][j] = True
			ginc = False
			if (not dl[j]['details']['isKeyword']):
				if (i==0):
					if (j==0):
						ginc = True
					elif ( is_align(dl[j]['point'],dl[j-1]['point'])):
						# previoues keyword and unmatched
						if (dl[j-1]['details']['isKeyword'] and (not (matched[i][j-1]))):
							matched[i][j-1] = True
							section[i][j-1]['matched'] = True
							grouped[i][j] = grouped[i][j-1]
						# previous keyword matched or value matched
						elif (dl[j-1]['details']['isKeyword'] or matched[i][j-1]):
							ginc = True
						else:
							# previous value unmatched
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
								if (dl[j]['isNumber']):
									ginc=True
								else:
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
							## above is key unmatched
							if (section[i-1][ju]['details']['isKeyword']):
								matched[i-1][ju] = True
								section[i-1][ju]['matched'] = True
								grouped[i][j] = grouped[i-1][ju]
							## above is value unmatched
							else:
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
	knwoledge = []
	for section in data:
		groups.extend(group(section))
	i = 0
	l = len(groups)
	extracted =[False]*l
	for g in groups:
		if (len(g)==0):
			extracted[i] = True
		elif (len(g)==1):
			knwoledge.append(g[0])
			extracted[i] = True
		elif (g[0]['details']['isKeyword'] and g[0]['matched']):
			pkey = g[0]
			value =  g[1:]
			knwoledge.append((g[0],g[1]))
			# knwoledge[str(i) + ':' + pkey['text']] = value
			extracted[i] = True
		else:
			knwoledge.append(g)
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
	return groups,knwoledge
	# i = 0
	# while(i<len(groups)):
	# 	if not extracted[i]:
	# 		if half_keys(groups[i]):

	# 		else:
				
			

	