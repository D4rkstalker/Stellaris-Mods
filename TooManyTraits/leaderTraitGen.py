import glob
import os
import re
import collections
import json
import operator
files = []
def genLeaderEvents(leader_traits):
    traits = []
    for _file in leader_traits:
        with open(_file,"r") as f:
            for line in f.readlines():
                traits.append(line)
    start = """namespace = tmt_leader_traits_event
country_event = {
    id = tmt_leader_traits_event.1
    hide_window = yes
    is_triggered_only = yes
    immediate = {
        every_country = {
"""

    event_template = ""
    f = open("scriptOut\\tmt_admiral_event.txt", "w+")
    i = 0
    for trait in traits:
        _type = ""
        trait = trait.strip()
        if "_admiral" in trait:
            _type = "admiral"
        elif "_ruler" in trait:
            _type="ruler"
        elif "_scientist" in trait:
            _type= "scientist"
        elif "_governor" in trait:
            _type= "governor"
        elif "_general" in trait:
            _type= "general"


        event_template += """
        
            every_owned_leader = {
                limit = {
                    species = { has_trait = """+trait.replace("_" + _type, "")+""" }
                    NOT = {has_trait = """+trait+"""}
                }
                if = {
                    limit = { leader_class = """ + _type +""" }
                    add_trait = """+trait+"""
                }
            }
            every_pool_leader = {
                limit = {
                    species = { has_trait = """+trait.replace("_" + _type, "")+""" }
                    NOT = {has_trait = """+trait+"""}
                }
                if = {
                    limit = { leader_class = """ + _type +""" }
                    add_trait = """+trait+"""
                }
            }
            every_owned_leader = {
                limit = {
                    AND = {
                        has_trait = """+trait+"""
                        NOT = {
                            species = { has_trait = """+trait.replace("_" + _type, "")+""" }
                        }
                    }
                }
                remove_trait = """+trait+"""
            }
            every_pool_leader = {
                limit = {
                    AND = {
                        has_trait = """+trait+"""
                        NOT = {
                            species = { has_trait = """+trait.replace("_" + _type, "")+""" }
                        }
                    }
                }
                remove_trait = """+trait+"""
            }
"""
    
    f.write(start + event_template + "    	}")
    f.write("\n\t}\n}")

def parse_dir():
    global files
    target_dir = "leaderIn"

    files += glob.glob(target_dir + '\\*.txt')

parse_dir()
genLeaderEvents(files)
