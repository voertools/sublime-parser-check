import sublime, sublime_plugin
 
class ParserCheckCommand(sublime_plugin.TextCommand):
    def run(self, edit):
		parserCalls = ['pc.crotch','pc.groind','pc.cock','pc.cockBiggest','pc.biggestCock','pc.CockHead','pc.cockHeadBiggest','pc.biggestCockHead','pc.cockSmallest','pc.smallestCock','pc.sheath','pc.biggestSheath','pc.sheathBiggest','pc.knot','pc.cocks','pc.cocksLight','pc.multiCocks','pc.cockNounComplex','pc.cockNounSimple','pc.cockColor','pc.dickColor','pc.cockHeads','pc.eachCockHead','pc.eachCock','pc.oneCock','pc.sack','pc.ball','pc.balls','pc.vaginaColor','pc.cuntColor','pc.vagina','pc.cunt','pc.pussy','pc.vaginas','pc.cunts','pc.pussies','pc.eachVagina','pc.eachVagina','pc.oneVagina','pc.vagOrAss','pc.pussyOrAsshole','pc.clit','pc.clits','pc.eachClit','pc.oneClit','pc.nipple','pc.nipples','pc.milkyNipple','pc.milkyNipples','pc.nippleCock','pc.dickNipple','pc.nippleCocks','pc.dickNipples','pc.nippleColor','pc.chest','pc.fullChest','pc.biggestBreastDescript','pc.breasts','pc.breastCupSize','pc.tailCock','pc.cockTail','pc.tailgina','pc.cuntTail','pc.tailCunt','pc.tailVagina','pc.oneTailgina','pc.oneTailCunt','pc.cum','pc.milk','pc.girlCum','pc.cumNoun','pc.milkNoun','pc.girlCumNoun','pc.cumColor','pc.milkColor','pc.girlCumColor','pc.cumVisc','pc.milkVisc','pc.girlCumVisc','pc.cumFlavor','pc.milkFlavor','pc.girlCumFlavor','pc.asshole','pc.gear','pc.armor','pc.lowerUnderGarment','pc.upperUndergarment','pc.upperGarment','pc.upperGarments','pc.lowerGarment','pc.underGarment','pc.lowerGarments','pc.underGarments','pc.height','pc.race','pc.name','pc.short','pc.skinFurScales','pc.skin','pc.skinFurScalesNoun','pc.skinNoun','pc.ears','pc.ear','pc.eyes','pc.eye','pc.eyePigment','pc.eyeColor','pc.hair','pc.hairs','pc.face','pc.lips','pc.lip','pc.tonuge','pc.tail','pc.tails','pc.oneTail','pc.eachTail','pc.butt','pc.ass','pc.hip','pc.hips','pc.thigh','pc.thighs','pc.leg','pc.legs','pc.feet','pc.foot','pc.toes','pc.knees','pc.belly','pc.he','pc.she','pc.heShe','pc.him','pc.himHer','pc.his','pc.hisHer','pc.hisHers'];
        braces = False
		sels = self.view.sel()
		for sel in sels:
			if self.view.substr(sel).find('output(\"') != -1:
				braces = True
		if not braces:
			new_sels = []
			for sel in sels:
				new_sels.append(self.view.find('\")', sel.end()))
			sels.clear()
			for sel in new_sels:
				sels.add(sel)
			self.view.run_command("expand_selection", {"to": "brackets"})
		for sel in sels:
			new_sels = []
			for sel in sels:
				new_sels.append(self.view.find(']', sel.end()))
			sels.clear()
			for sel in new_sels:
				sels.add(sel)
			self.view.run_command("expand_selection", {"to": "brackets"})
		
		edit = self.view.begin_edit('parser_check')
		
		for sel in sels:
			str = self.view.substr(sel)
			if str not in parserCalls:
				self.view.replace(edit,sel,str+"**");