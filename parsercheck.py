import sublime, sublime_plugin
 
class ParserCheckCommand(sublime_plugin.TextCommand):
	original_regions = []
	history = [ "" ]
	history_index = 0
	parserCalls = ['pc.crotch','pc.groin','pc.cock','pc.cockBiggest','pc.biggestCock','pc.cockHead','pc.cockHeadBiggest','pc.biggestCockHead','pc.cockSmallest','pc.smallestCock','pc.sheath','pc.biggestSheath','pc.sheathBiggest','pc.knot','pc.cocks','pc.cocksLight','pc.multiCocks','pc.cockNounComplex','pc.cockNounSimple','pc.cockColor','pc.dickColor','pc.cockHeads','pc.eachCockHead','pc.eachCock','pc.oneCock','pc.sack','pc.ball','pc.balls','pc.vaginaColor','pc.cuntColor','pc.vagina','pc.cunt','pc.pussy','pc.vaginas','pc.cunts','pc.pussies','pc.eachVagina','pc.eachVagina','pc.oneVagina','pc.vagOrAss','pc.pussyOrAsshole','pc.clit','pc.clits','pc.eachClit','pc.oneClit','pc.nipple','pc.nipples','pc.milkyNipple','pc.milkyNipples','pc.nippleCock','pc.dickNipple','pc.nippleCocks','pc.dickNipples','pc.nippleColor','pc.chest','pc.fullChest','pc.biggestBreastDescript','pc.breasts','pc.breastCupSize','pc.tailCock','pc.cockTail','pc.tailgina','pc.cuntTail','pc.tailCunt','pc.tailVagina','pc.oneTailgina','pc.oneTailCunt','pc.cum','pc.milk','pc.girlCum','pc.cumNoun','pc.milkNoun','pc.girlCumNoun','pc.cumColor','pc.milkColor','pc.girlCumColor','pc.cumVisc','pc.milkVisc','pc.girlCumVisc','pc.cumFlavor','pc.milkFlavor','pc.girlCumFlavor','pc.asshole','pc.gear','pc.armor','pc.lowerUndergarment','pc.upperUndergarment','pc.upperGarment','pc.upperGarments','pc.lowerGarment','pc.underGarment','pc.lowerGarments','pc.underGarments','pc.height','pc.race','pc.name','pc.short','pc.skinFurScales','pc.skin','pc.skinFurScalesNoun','pc.skinNoun','pc.ears','pc.ear','pc.eyes','pc.eye','pc.eyePigment','pc.eyeColor','pc.hair','pc.hairs','pc.face','pc.lips','pc.lip','pc.tonuge','pc.tail','pc.tails','pc.oneTail','pc.eachTail','pc.butt','pc.ass','pc.hip','pc.hips','pc.thigh','pc.thighs','pc.leg','pc.legs','pc.feet','pc.foot','pc.toes','pc.knees','pc.belly','pc.he','pc.she','pc.heShe','pc.him','pc.himHer','pc.his','pc.hisHer','pc.hisHers']

	def run(self, edit):
		ParserCheckCommand.original_regions = []
		for region in self.view.sel(): 
			ParserCheckCommand.original_regions = [ sublime.Region(0, self.view.size()) ]

		regex = r'"([^"]*)"'
		self.search(regex)
		regex = r'(?<=\[)[^]]+(?=\])'
		self.search(regex)

		edit = self.view.begin_edit("parser_check")

		for sel in self.view.sel():
			s = self.view.substr(sel)
			if s not in ParserCheckCommand.parserCalls:
				self.view.replace(edit,sel,self.findClosest(s))

	def search(self,regex):
        # Cache view for speed
		view = self.view
        # Initialize our array of results
		new_regions = []
        # Run this command on each region
		for region in ParserCheckCommand.original_regions:
            # If this region is backwards, then flip it
			if(region.b < region.a): region = sublime.Region(region.b, region.a)
            # If the region is empty, then select the whole line
			if(region.size() == 0): region = view.line(region)
            # Initialize our search cursor to the beginning of the region region
			caret = region.a
            
			while(caret < region.b):
                # Find the next instance of the regex
				match = view.find(regex, caret)
                # If the match is zero-length, then increment the caret and continue
				if not match: caret += 1
				else:
                    # Check to see if the match is in the current region
					if(region.contains(match)): new_regions += [ match ]
                    # Move the caret past this region
					caret = match.b
        # Empty the selection
		view.sel().clear()
        # Draw borders around the matches    
		# Skip empty regions, because that would empty the selection (annoying)
		if len(new_regions): 
            # Add each selection to the view
			for region in new_regions: view.sel().add(region)
	def findClosest(self,word):
		tmp = word.split(" ")
		compare = tmp.pop(0)
		args = " ".join(tmp)
		match = compare + "**"
		distance = 10
		for c in ParserCheckCommand.parserCalls:
			d = self.findDistance(compare,c)
			if (d<distance):
				match = c
				distance = d
		return match + args


	def findDistance(self,first,second):
		if len(first) > len(second):
			first, second = second, first
		if len(second) == 0:
			return len(first)
		first_length = len(first) + 1
		second_length = len(second) + 1
		distance_matrix = [[0] * second_length for x in range(first_length)]
		for i in range(first_length):
			distance_matrix[i][0] = i
		for j in range(second_length):
			distance_matrix[0][j]=j
		for i in xrange(1, first_length):
			for j in range(1, second_length):
				deletion = distance_matrix[i-1][j] + 1
				insertion = distance_matrix[i][j-1] + 1
				substitution = distance_matrix[i-1][j-1]
				if first[i-1] != second[j-1]:
					substitution += 1
	 			distance_matrix[i][j] = min(insertion, deletion, substitution)
		return distance_matrix[first_length-1][second_length-1]