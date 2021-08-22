import glob
import os
import re
import collections
import json
import operator
import copy

files = []
files2 = []
alltraits = []

class Trait: 
    def __hash__(self):
        return hash(('name', self.trait_name))
    def __eq__(self, other):
        return self.trait_name==other.trait_name

    def __init__(self,trait_name,cost,initial,randomized,modification, opposites, archetypes, modifiers,icon,species_potential_add,custom_tooltip,prerequisites,leader_trait,leader_class,requires_traits,ai_weight, forced_happiness):
        self.trait_name = trait_name
        self.cost = cost
        self.opposites = opposites
        self.archetypes = archetypes
        self.modifiers = modifiers
        self.modifierCount = len(modifiers)
        self.initial = initial
        self.randomized = randomized
        self.modification = modification
        self.icon = icon
        self.potential = species_potential_add
        self.custom_tooltip = custom_tooltip
        self.prerequisites = prerequisites
        self.leader_trait = leader_trait
        self.leader_class = leader_class
        self.requires_traits = requires_traits
        self.ai_weight = ai_weight
        self.forced_happiness = forced_happiness
    def toString(self):
        template = self.trait_name + "= {\n"
        if self.icon.strip() != "" :
            template += "\ticon = "+self.icon + "\n"
        template += "\tcost = "+str(self.cost)+ "\n"
        if self.initial:
            template += "\tinitial = "+self.initial+ "\n"
        if self.randomized:
            template += "\trandomized = "+self.randomized+ "\n"
        if self.modification:
            template += "\tmodification = "+self.modification+ "\n"
        if self.forced_happiness:
            template += "\tforced_happiness = " + self.forced_happiness + "\n"
        # if len(self.prerequisites) > 0:
        #     template +="\tprerequisites = {\n"""+ "\n".join(self.prerequisites)+"\n\t}\n"
        template +="\tallowed_archetypes = { """+ " ".join(self.archetypes)+" }\n"
        if len(self.custom_tooltip) > 0:
            template += "\tcustom_tooltip = " + self.custom_tooltip + "\n"
        # if len(self.potential) > 0:
        #     template += "\tspecies_potential_add = {\n" 
        #     template +='\n'.join(self.potential)
        #     template +="\n\t}"
        template += "\n\topposites = { " + " ".join(self.opposites) +"}\n"
        if self.leader_trait:
            template += "\tleader_trait = " + self.leader_trait + "\n"
        if len(self.leader_class) > 0:
            template += "\n\tleader_class = { " + " ".join(self.leader_class) +"}\n"
        if len(self.requires_traits) > 0:
            template += "\n\trequires_traits = { " + " ".join(self.requires_traits) +"}\n"
        template += "\tmodifier = {\n"
        for key in self.modifiers:
            template += "\t\t" + key + " = " + self.modifiers[key] + "\n"
        template += "\t}\n"     
        if self.cost < 1:
            template +="\tai_weight = {\nweight = 0\n\t}\n"
        # if len(self.ai_weight) > 0:
        #     template +="\tai_weight = {\n"+ "\n".join(self.ai_weight)+"\n\t}\n"
        template += "}"
        return template


def get_traits(files):
    for file in files:
        f =  open(file, 'r')
        _file = f.read()
        f.close()
        text = ""
        for line in _file.split("\n"):
            if "#" in line:
                line = line.split("#")[0]
            text += line + "\n"
        #print(text)
        #out_file = os.path.join(out_dir, os.path.basename(file))
        text = text.replace("just-more-traits", "JMTCOMPAT")
        text = re.sub('\t*\n', '\n', text)
        text = re.sub(' *\n', '\n', text)
        traits = re.findall(r'\w*? *= {.*?\n}', text, re.DOTALL)
        
        for trait in traits:
            #print("\n----------")
            #print(trait)
            trait = re.sub('{','{\n',trait)
            trait = re.sub('}','\n}',trait)

            currentTrait = Trait("trait_name",0,"yes","yes",[], [], [], {},"",[],"",[],"",[],[],[],"")
            lines = str(trait).split("\n")
            layer = 0
            matched = {"species_potential_add" : False, "modifier" : False, "ai_weight" : False, "prerequisites" : False, "allowed_archetypes" : False, "leader_class" : False, "requires_traits": False}
            currentTrait.trait_name = (lines[0].split("=")[0]).replace("JMTCOMPAT", "just-more-traits")
            #print(currentTrait.trait_name)
            # print("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
            for i in range(len(lines)):
                #try:
                    line = lines[i]
                    
                    
                    if "#" in line:
                        line = line.split("#")[0]
                    if line.strip() != "":
                        
                        if "{" in line:
                            layer +=1
                        if "}" in line:
                            layer -=1
                            if layer == 1:
                                for key in matched.keys():
                                    matched[key] = False

                        #print(line + str( layer))
                        if layer == 1:
                            if len(re.findall(r"\bcost\b",line)) >0:
                                currentTrait.cost = int(line.split("=")[-1])
                            if len(re.findall(r"\bmodification\b",line)) >0:
                                currentTrait.modification = line.split("=")[-1]
                            if len(re.findall(r"\binitial\b",line)) >0:
                                currentTrait.initial = line.split("=")[-1]
                            if len(re.findall(r"\brandomized\b",line)) >0:
                                currentTrait.randomized = line.split("=")[-1]
                            if len(re.findall(r"\bcustom_tooltip\b",line)) >0:
                                currentTrait.custom_tooltip = line.split("=")[-1]
                            if len(re.findall(r"\bicon\b",line)) > 0:
                                currentTrait.icon = line.split("=")[-1]  
                            if len(re.findall(r"\bleader_trait\b",line)) > 0:
                                currentTrait.leader_trait = line.split("=")[-1]  
                            if len(re.findall(r"\bforced_happiness\b",line)) > 0:
                                currentTrait.forced_happiness = line.split("=")[-1]  
                        if "requires_traits" in line:
                            temp = line.split("=")[-1]
                            temp = temp.replace("{","").replace("}","")
                            currentTrait.requires_traits = [string for string in temp.split(" ") if string != ""]

                        elif layer > 1:
                            
                            if matched["species_potential_add"]:
                                currentTrait.potential.append(line)
                            if matched["prerequisites"]:
                                currentTrait.prerequisites.append(line)
                            if matched["allowed_archetypes"]:
                                currentTrait.archetypes.append(line)
                            if matched["ai_weight"]:
                                currentTrait.ai_weight.append(line)
                            if matched["leader_class"]:
                                currentTrait.leader_class.append(line)
                            if matched["modifier"]:
                                #print(trait)
                                #print(line)
                                line = line.strip().split("=")
                                currentTrait.modifiers[line[0].strip()] = line[1].strip()
                        if  layer == 2:
                            for key in matched.keys():
                                if key in line:
                                    #print(key + line)
                                    matched[key] = True  
                                # print(lines[i+1])
                            # currentTrait.modifiers(line.strip())
                            

                # except Exception as e: 
                #     print("\n----------")
                #     print("~~~~~")
                #     print(file)
                #     print("~~~~~")
                #     print(trait)
                #     print("~~~~~")
                #     print(lines[i])
                #     print("~~~~~")
                #     print("trait Errored:" + str(e))
                #     print("----------\n")
            #print(currentTrait.modifiers.keys())
            #print(currentTrait.archetypes)

            if len(currentTrait.archetypes) > 0:
                temp = []
                machine = False
                robot = False
                if len(re.findall(r"\bMACHINE\b",currentTrait.archetypes[0])) >0:
                    temp.append("MACHINE")
                    machine = True
                if "ROBOT" in currentTrait.archetypes[0]:
                    temp.append("ROBOT")
                    robot = True
                if "LITHOID" in currentTrait.archetypes[0]:
                    temp.append("LITHOID")
                if "BIOLOGICAL" in currentTrait.archetypes[0]:
                    temp.append("BIOLOGICAL")
                if "PRESAPIENT" in currentTrait.archetypes[0]:
                    temp.append("PRESAPIENT")
                if machine and not robot:
                    temp.append("ROBOT")
                if robot and not machine:
                    temp.append("MACHINE")

            if len(currentTrait.modifiers) > 0:
                speedMult = 0.0
                costMult = 0.0
                for modifier in currentTrait.modifiers.keys():
                    if "pop_assembly_speed" in modifier:
                        speedMult = currentTrait.modifiers[modifier]
                    if "planet_pop_assemblers_upkeep_mult" in modifier:
                        costMult = currentTrait.modifiers[modifier]
                if speedMult != 0 and costMult == 0:
                    currentTrait.modifiers["planet_pop_assemblers_upkeep_mult"] = str(speedMult)

            currentTrait.archetypes = temp
            alltraits.append(currentTrait)

def genAllModifiers(allTraits):
    allModifiers = {}
    for trait in alltraits:
        for key in trait.modifiers.keys():
            allModifiers[key] = ""
    return allModifiers.keys()

def sortTraits(allModifiers, allTraits):
    allTraits = list(set(allTraits))
    sortedTraits = {}  
    compoundTraits = []
    for key in genAllModifiers(alltraits):
        sortedTraits[key] = list()
    for trait in allTraits:
        if len(trait.modifiers.keys()) > 0 and len(trait.modifiers.keys()) < 4:
            _key = ""
            for key in trait.modifiers.keys():
                _key += key
            try:
                sortedTraits[_key].append(trait)
            except:
                try: 
                    sortedTraits[_key] = list()
                    sortedTraits[_key].append(trait)
                except Exception as e:
                    print(trait)
        else:
            compoundTraits.append(trait)
    for modifier in sortedTraits:
        sortedTraits[modifier] = sorted(sortedTraits[modifier], key=operator.attrgetter("cost", "modifierCount"), reverse = True)
    compoundTraits = sorted(compoundTraits, key=operator.attrgetter("modifierCount", "cost"), reverse = True)
    # for key in sortedTraits:
    #     print(key + ":" + str( sortedTraits[key]))
    return sortedTraits,compoundTraits

def output(sortedTraits, compoundTraits):
    # for key in sortedTraits:
    #     for trait in sortedTraits[key]:
    #         for _trait in sortedTraits[key]:
    #             if _trait.trait_name != trait.trait_name:
    #                 trait.opposites.append(_trait.trait_name)



    for key in sortedTraits:
        if len(sortedTraits[key]) > 0:
                for trait in sortedTraits[key]:
                    if "trait_pc_" in trait.trait_name:
                        with open("out\\Trait_Overhual_habitability.txt", "a+") as f:
                                f.write(trait.toString())
                                f.write("\n")             
                for trait in sortedTraits[key]:
                    if "ROBOT" not in trait.archetypes and "MACHINE" not in trait.archetypes and "trait_pc_" not in trait.trait_name:
                        with open("out\\Trait_Overhual_BIO_" + key + ".txt", "a+") as f:
                            f.write(trait.toString())
                            f.write("\n")
                for trait in sortedTraits[key]:
                    if "ROBOT" in trait.archetypes or "MACHINE" in trait.archetypes and "trait_pc_" not in trait.trait_name:
                        with open("out\\Trait_Overhual_MECH_" + key + ".txt", "a+") as f:
                            f.write(trait.toString())
                            f.write("\n")
    with open("out\\TMT_Misc_Organic.txt", "w+") as o:
        with open("out\\TMT_Misc_Machine.txt", "w+") as m:
            for trait in compoundTraits:
                if "trait_pc_" in trait.trait_name:
                    with open("out\\TMT_habitability.txt", "a+") as f:
                        f.write(trait.toString())
                        f.write("\n")
                else:     
                    if "ROBOT" not in trait.archetypes and "MACHINE" not in trait.archetypes:
                        o.write(trait.toString())
                        o.write("\n")
                    if "ROBOT" in trait.archetypes or "MACHINE" in trait.archetypes:
                        m.write(trait.toString())
                        m.write("\n")

        






def parse_dir():
    global files, files2
    target_dir = "traits"

    files += glob.glob(target_dir + '\\*.txt')
    files2 += glob.glob("overrides" + '\\*.txt')


parse_dir()
get_traits(files2)
get_traits(files)
sortedTraits,compoundTraits = sortTraits(genAllModifiers(alltraits), alltraits)
output(sortedTraits,compoundTraits)
#genLeaderTraits(sortedTraits)
#for trait in alltraits:
    #print(json.dumps(trait.__dict__))
print("Done")
#input()
