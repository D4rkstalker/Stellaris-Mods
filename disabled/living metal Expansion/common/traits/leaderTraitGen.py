 
traitList ="""trait_overhual_combat_1
trait_overhual_combat_2
trait_overhual_combat_3
trait_overhual_combat_4
trait_overhual_shield_1
trait_overhual_shield_2
trait_overhual_shield_3
trait_overhual_missile_1
trait_overhual_missile_3
trait_overhual_kinetic_2\t
trait_overhual_kinetic_4
trait_overhual_laser_2
trait_overhual_laser_4
trait_overhual_bombardment_4
trait_overhual_disruptor_4
trait_overhual_speed_4
trait_overhual_strikecraft_1
trait_overhual_strikecraft_3
trait_overhual_radar_1
trait_overhual_radar_2
trait_overhual_radar_3
trait_overhual_radar_4
trait_overhual_coordination_1
trait_overhual_coordination_2
trait_overhual_fabrication_1
trait_overhual_fabrication_2
trait_overhual_fabrication_3
trait_overhual_fabrication_4
trait_overhual_gateway_1
trait_overhual_gateway_2
trait_overhual_gateway_3
trait_overhual_gateway_4
trait_overhual_jamming_1
trait_overhual_jamming_2
trait_overhual_jamming_3
trait_overhual_jamming_4"""

traits = traitList.split("\n")

frame = """ = {
	inline_script = {
		script = trait/icon
		CLASS = leader
		ICON = GFX_leader_<<<REPLACE>>>
		RARITY = common
		COUNCIL = triggered
		TIER = none
	}
	initial = no
	randomized = no
}
"""

for trait in traits:
	if "4" in trait:
		out = trait + frame.replace("<<<REPLACE>>>",trait)
		# print(out)
print("spriteTypes = {")
for trait in traits:
	temp = """	spriteType = {
		name = \"GFX_leader_"""+ trait+"""\"
		texturefile = "gfx/interface/icons/traits/"""+ trait +""".dds"
	}""" 
	print(temp)
print("}")