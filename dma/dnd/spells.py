from random import sample,choice
from decimal import Decimal

from .roll import roll
from .time import TimePeriod, TimeUnit
from .sourcebook import SourceBook

#aliases for the lazy
S = TimeUnit.segment
R = TimeUnit.round
T = TimeUnit.turn
H = TimeUnit.hour
D = TimeUnit.day
Y = TimeUnit.year
VA = TimeUnit.variable
P = TimeUnit.permanent
tp = TimePeriod

V = SourceBook.v
U = SourceBook.ua

#contains minimal info on spells (name, class and level)
class Spell():
    def __init__(self, name, spell_class, level,
            cast=None, duration=TimePeriod(0,R), duration_lvl=TimePeriod(0,S),
            sourcebook=None, desc="Missing description"):
        self.name = name
        self.role = spell_class
        self.level = level

        #additional information (not yet defined for most spells
        self.cast_time = cast
        self.duration = duration
        self.duration_per_level = duration_lvl
        self.sourcebook = sourcebook
        self.description = desc

    def __str__(self):
        spell_class = ''
        if self.role == 'M':
            spell_class = 'Magic-User'
        elif self.role == 'I':
            spell_class = 'Illusionist'
        elif self.role == 'C':
            spell_class = 'Cleric'
        elif self.role == 'D':
            spell_class = 'Druid'


        ret = '{} ({} Lvl {})'.format(self.name,spell_class,self.level)
        return ret

    def __lt__(self,other):
        if self.level < other.level:
            return True
        elif self.level > other.level:
            return False
        else:
            if self.name.lower() < other.name.lower():
                return True
            else:
                return False

    def __eq__(self,other):
        if (self.name == other.name and
            self.level == other.level and
            self.role == other.role):
            return True
        else: return False

def randomSpellScroll(num,mu_min,mu_max,cl_min=0,cl_max=0):
    #Set cleric range to mu_range if cl_min/max are not given
    if (not cl_min): cl_min = mu_min
    if (not cl_max): cl_max = mu_max

    spells = ''

    r = roll(100)
    if r > 70:
        r = roll(100)
        if r > 75:
            spells = [s for s in druid_spells
                if s.level >= cl_min and s.level <= cl_max]
        else:
            spells = [s for s in cleric_spells
                if s.level >= cl_min and s.level <= cl_max]
    else:
        r = roll(100)
        if r > 90:
            spells = [s for s in illusionist_spells
                if s.level >= mu_min and s.level <= mu_max]
        else:
            spells = [s for s in mu_spells
                if s.level >= mu_min and s.level <= mu_max]

    spells = sample(spells, num)
    spells = sorted(spells, key=lambda spell: spell.level)
    spells = [str(s) for s in spells]
    return spells

cleric_spells = [
    Spell(
        name='Bless',
        spell_class='C',
        level=1,
        cast=tp(1,R),
        duration=tp(6,R),
        sourcebook=V,
        desc="Upon uttering the Bless spell, the caster raises the morale of friendly creatures by +1. Furthermore, it raises their \"to hit\" dice rolls by +1. A blessing, however, will affect only those not already engaged in melee combat. This spell can be reversed by the cleric to a curse upon enemies which lowers morale and \"to hit\" by -1. The caster determines at what range (up to 6\") he or she will cast the spell, and it then affects all creatures in on area 5\" square centred on the point the spell was cast upon. In addition to the verbal and somatic gesture components, the Bless requires holy water, while the Curse requires the sprinkling of specially polluted water."
    ),
    Spell('Ceremony','C',1,
        cast=tp(1,H),
        duration=tp(1,P),
        sourcebook=U
    ),
    Spell('Combine','C',1,
        cast=tp(1,R),
        duration=tp(1,VA),
        sourcebook=U,
        desc="This spell enables three to five clerics to combine their abilities and thereby empower one of their number to cast a spell or turn undead with greater efficacy. The highest-level cleric of the group (or one of such, as applicable) stands, while the other clerics join hands in a surrounding circle. All the participating clerics then cast the combine spell together. The central cleric temporarily functions as if of higher level, gaining one level for each encircling cleric. The maximum gain is four levels, and the maximum duration is 3 turns. The increase applies to the cleric's effective level for determining the results of attempts to turn undead, and to spell details which vary by the level of the caster. The encircling clerics must concentrate on maintaining the combine effect. They gain no armor class bonuses from shield or dexterity, and their attackers gain a +4 bonus on all \"to hit\" rolls. The central cleric gains no additional spells, but may cast any previously memorized spell(s), often with bonus effects."
    ),
    Spell('Command','C',1,
        cast=tp(1,S),
        duration=tp(1,R),
        sourcebook=V,
        desc="This spell enables the cleric to issue a command of a single word. The command must be uttered in a language which the spell recipient is able to understand. The individual will obey to the best of his/her/its ability only so long as the command is absolutely clear and unequivocal, i.e. \"Suicide!\" could be a noun, so the creature would ignore the command. A command to \"Die!\" would cause the recipient to fall in a faint or cataleptic state for 1 round, but thereafter the creature would be alive and well. Typical command words are: back, halt, flee, run, stop, fall, fly, go, leave, surrender, sleep. rest, etc. Undead are not affected by a command. Creatures with intelligence of 13 or more, and creatures with 6 or more hit dice (or experience levels) are entitled to a saving throw versus magic. (Creatures with 13 or higher intelligence and 6 hit dice/levels do not get 2 saving throws!)"
    ),
    Spell('Create Water','C',1,
        cast=tp(1,R),
        duration=tp(1,P),
        sourcebook=V,
        desc="When the cleric casts a Create Water spell, four gallons of water are generated for every level of experience of the caster, i.e. a 2nd level cleric creates eight gallons of water, a 3rd level twelve gallons, a 4th level sixteen gallons, etc. The water is clean and drinkable (it is just like rain water). Reversing the spell, Destroy Water, obliterates without trace (such as vapour, mist, fog or steam) a like quantity of water. Created water will last until normally used or evaporated, spilled, etc. Water can be created or destroyed in an area as small as will actually contain the liquid or in an area as large as 27 cubic feet (one cubic yard). The spell requires at least a drop of water to create, or a pinch of dust to destroy, water. Note that water cannot be created within a living thing."
    ),
    Spell('Cure Light Wounds','C',1,
        cast=tp(5,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="Upon laying his or her hand upon a creature, the cleric causes from 1 to 8 hit points of wound or other injury damage to the creature's body to be healed. This healing will not affect creatures without corporeal bodies, nor will it cure wounds of creatures not living or those which can be harmed only by iron, silver, and/or magical weapons. Its reverse, Cause Light Wounds, operates in the same manner; and if a person is avoiding this touch, a melee combat \"to hit\" die is rolled to determine if the cleric's hand strikes the opponent and causes such a wound. Note that cured wounds are permanent only insofar as the creature does not sustain further damage, and that caused wounds will heal - or can be cured - just as any normal injury will. Caused light wounds are 1 to 8 hit points of damage."
    ),
    Spell('Detect Evil','C',1,
        cast=tp(1,R),
        duration=tp(1,T),
        duration_lvl=tp(5,R),
        sourcebook=V,
        desc="This is a spell which discovers emanations of evil, or of good in the case of the reverse spell, from any creature or object. For example, evil alignment or an evilly cursed object will radiate evil, but a hidden trop or an unintelligent viper will not. The duration of a Detect Evil (or Detect Good) spell is 1 turn + ½ turn (5 rounds, or 5 minutes) per level of the cleric. Thus a cleric of 1st level of experience can cast a spell with a 1½ turn duration, at 2nd level a 2 turn duration, 2½ at 3rd, etc. The spell has a path of detection 1\" wide in the direction in which the cleric is facing. It requires the use of the cleric's holy (or unholy) symbol as its material component, with the cleric holding it before him or her."
    ),
    Spell('Detect Magic','C',1,
        cast=tp(1,R),
        duration=tp(1,T),
        sourcebook=V,
        desc="When the Detect Magic spell is cast, the cleric detects magical radiations in a path 1\" wide, and up to 3\", long, in the direction he or she is facing. The caster can turn 60° per round. Note that stone walls of 1' or more thickness, solid metal of but 1/12' thickness, or 3' or more of solid wood will black the spell. The spell requires the use of the cleric's holy (or unholy) symbol."
    ),
    Spell('Endure Cold/Heat','C',1,
        cast=tp(1,R),
        duration_lvl=tp(9,T),
        sourcebook=U,
        desc="The recipient of this spell is provided with protection from normal extremes of cold or heat (depending on which application is used). He or she can stand unclothed in temperatures as low as -30°F or as high as 130°F (depending on application) with no ill effect. A temperature extreme beyond either of those limits will cause 1 hit point of exposure damage per hour for every degree above or below those limits. (Without the benefit of protection such as this, exposure damage is 1 hit point per turn for each degree of temperature.) The spell will last for the prescribed duration, or until the recipient is affected by any form of magical cold (including white dragon breath) or magical heat. The cancellation of the spell will occur regardless of which application was used and regardless of which type of magical effect hits the character (e.g. Endure Cold will be cancelled by magical heat or fire as well as by magical cold). The recipient of the spell will not suffer damage from the magical heat or cold during the round in which the spell is broken, but will be vulnerable to all such attacks starting on the following round. The spell will be cancelled instantly if either Resist Fire or Resist Cold is cast upon the recipient."
    ),
    Spell('Invisibility to Undead','C',1,
        cast=tp(4,S),
        duration=tp(6,R),
        sourcebook=U,
        desc="This spell is quite similar to Sanctuary, but only affects undead of 4 or fewer hit dice. A saving throw versus spell is made for each type of undead within 30 feet of the caster, and if failed, all undead of that type will ignore the caster completely for the duration of the spell. (Note that this negates subsequent attempts by the caster to turn those undead.) However, if the saving throw suceeds, all undead of that type will attack the spell caster in preference to any other possible targets. The effect of this spell ends if the caster attacks or attempts to cast any other spell. If the caster is of neutral morals (with respect to good and evil), the undead save at -2. The material component is the cleric's holy symbol."
    ),
    Spell('Light','C',1,
        cast=tp(4,S),
        duration=tp(6,T),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="This spell causes excitation of molecules so as to make them brightly luminous. The light thus caused is equal to torch light in brightness, but its sphere is limited to 4\" in diameter. It lasts for the duration indicated (7 turns at 1st experience level, 8 at 2nd, 9 at 3rd, etc.) or until the caster utters a word to extinguish the light. The Light spell is reversible, causing darkness in the same area and under the same conditions, except the blackness persists for only one half the duration that light would last. If this spell is cast upon a creature, the applicable magic resistance and saving throw dice rolls must be made. Success indicates that the spell affects the area immediately behind the creature, rather than the creature itself. In all other cases, the spell takes effect where the caster directs as long as he or she has a line of sight or unobstructed path for the spell; fight can spring from air, rock, metal, wood, or almost any similar substance."
    ),
    Spell('Magic Stone','C',1,
        cast=tp(1,R),
        duration=tp(6,R),
        sourcebook=U,
        desc="To use this spell, the cleric picks up a small stone or pebble and then (via the casting process) places a magical aura on it. The spell cannot affect stones that are already magical. The magic stone can be thrown at a target up to 4\" distant (assuming no intervening obstacles and sufficient head room). It will act as a +1 weapon for \"to hit\" determination, and if a hit is scored the stone will do 1 point of damage. Ranges are 2\"/3\"/4\", with standard modifications. If the stone travels more than 4\" from the thrower or if it does not score a hit, the missile loses its dweomer and falls harmlessly to the ground. A magic stone must be thrown within 6 rounds after the casting of the spell is completed, or it turns back into an ordinary item. A hit from the stone will break the concentration of a spell caster only if the victim fails a saving throw versus spell. Any target with innate magic resistance cannot be affected by the stone. A Shield spell will protect a target from a magic stone, as will a Brooch of Shielding, a Protection from Normal Missiles spell, a Minor Globe of Invulnerability, or any similar (more powerful) magic. A cleric of 6th through 10th level can enchant 2 stones with this spell, one of 11th through 15th level can use it on 3 stones, and an additional stone is allowed for every five levels of experience the caster has gained beyond the 11th (i.e., 4 stones at 16th level, 5 stones at 21st level, etc.). It is possible for a cleric to give the enchanted stone(s) to another character to throw. Note that some religious organizations forbid their clerics from using this spell, since it enables the cleric to use a missile weapon (of sorts)."
    ),
    Spell('Penetrate Disguise','C',1,
        cast=tp(2,R),
        duration=tp(1,R),
        sourcebook=U,
        desc="By means of this spell, the cleric is empowered to see through a disguise composed solely of makeup or altered clothing (i.e., non-magical in nature). The cleric cannot identify what class or profession the disguised figure actually belongs to, nor the true appearance of the figure; the spell merely points out that the target figure is posing as someone or something else. The spell doesn not detect actual rank or status and cannot reaveal an illusion for what it is, but it can detect whether a figure is the object of a Friends spell. The spell cannot detect any deception involving alignment. The target of the spell is allowed a saving throw versus spell, and if this saving throw is made, the disguise will be enhanced in the eyes of the cleric, so that the caster becomes convinced that the target figure actually is what he claims to be. Being under the effect of a Bless spell, wearing magic armor, or using a magic item of protection (such as a cloak or ring) will give the target an appropriate bonus to the saving throw."
    ),
    Spell('Portent','C',1,
        cast=tp(1,T),
        duration=tp(1,VA),
        sourcebook=U,
        desc="This spell enables the cleric to tell something of his or another figure's future \"luck\". This \"luck\" takes the form of an improvement or reduction in a \"to hit\" roll or a saving throw at some point in the future unknown to the character who is the object of the portent. After this spell is cast, the Dungeon Master makes two die rolls in secret: First, 1d12, to determine at what point in the future the portent takes effect; second, 1d6 to determine the exact effect (roll of 1 = -3; 2 = -2; 3 = -1; 4 = +1; 5 = +2; 6 = +3). Based upon the result of the 1d6 roll, the DM should indicate to the player of the cleric character whether the portent is good, fair(which can be moderately good or moderately bad), or poor. The recipient of the spell will usually also be given this information. The result of the d12 roll represents the number of \"to hit\" rolls or saving throws that the target character must make before the roll to be affected by the portent occurs; e.g. if a 12 is rolled, then the 12th such roll thereafter will be the one to which the portent is applied. Die rolls only apply toward this count if they are taken in life-or-death (i.e., combat or peril) situations; the count is suspended if the character contrives to perform (for instance) saving throws against non-harmful effects in an effort to \"sidestep\" the portent. Die rolls that do apply toward this count include: Saving throws made in combat or against magical effects, \"to hit\" rolls made by an opponent against the character. When the die roll designated by the portent is made, the result will be adjusted upward or downward as indicated by the result of the d6 roll; thus, the character will be either more or less likely to succeed on a saving throw. The material component for this spell is either a numbered wheel or tea leaves."
    ),
    Spell('Precipitation','C',1,
        cast=tp(3,S),
        duration_lvl=tp(1,S),
        sourcebook=U
    ),
    Spell('Protection From Evil','C',1,
        cast=tp(4,S),
        duration=tp(0,R),
        duration_lvl=tp(3,R),
        sourcebook=V,
        desc="When this spell is cast, it acts as if it were a magical armour upon the recipient. The protection encircles the recipient at a one foot distance, thus preventing bodily contact by creatures of an enchanted or conjured nature such as aerial servants, demons, devils, djinn, efreet, elementals, imps, invisible stalkers, night hags, quasits, salamanders, water weirds, wind walkers, and xorn. Summoned animals or monsters are similarly hedged from the protected creature. Furthermore, any and all attacks launched by evil creatures incur a penalty of -2 from dice rolls \"to hit\" the protected creature, and any saving throws caused by such attacks are made at +2 on the protected creature's dice. This spell can be reversed to become Protection From Good, although it still keeps out enchanted evil creatures as well. To complete this spell, the cleric must truce a 3' diameter circle upon the floor (or ground) with holy water for Protection From Evil, with blood for Protection From Good - or in the air using burning incense or smouldering dung with respect to evil/good."
    ),
    Spell('Purify Food & Drink','C',1,
        cast=tp(1,R),
        duration=tp(1,P),
        sourcebook=V,
        desc="When cast, the spell will make spoiled, rotten, poisonous or otherwise contaminated food and/or water pure and suitable for eating and/or drinking. Up to 1 cubic foot of food and/or drink can be thus made suitable for consumption. The reverse of the spell putrefies food and drink, even spoiling holy water. Unholy water is spoiled by pure water."
    ),
    Spell('Remove Fear','C',1,
        cast=tp(4,S),
        duration=tp(0),
        sourcebook=V,
        desc="By touch, the cleric instils courage in the spell recipient, raising the creature's saving throw against magical fear attacks by +4 on dice rolls for 1 turn. If the recipient has already been affected by fear, and failed the appropriate saving throw, the touch allows another saving throw to be made, with a bonus of +1 on the dice for every level of experience of the caster, i.e. a 2nd level cleric gives a +2 bonus, a 3rd level +3, etc. A \"to hit\" dice roll must be made to touch an unwilling recipient. The reverse of the spell, Cause Fear, causes the victim to flee in panic at maximum movement speed away from the caster for 1 round per level of the cleric causing such fear. Of course, Cause Fear can be countered by Remove Fear and vice versa."
    ),
    Spell('Resist Cold','C',1,
        cast=tp(1,R),
        duration=tp(0),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="When this spell is placed on a creature by a cleric, the creature's body is inured to cold. The recipient can stand zero degrees Fahrenheit without discomfort, even totally nude. Greater cold, such as that produced by a sword of cold, ice storm, cold wand, or white dragon's breath, must be saved against. All saving throws against cold are made with a bonus of +3, and damage sustained is one-half (if the saving throw is not made) or one-quarter (if the saving throw is made) of damage normal from that attack form. The resistance lasts for 1 turn per level of experience of the caster. A pinch of sulphur is necessary to complete this spell."
    ),
    Spell('Sanctuary','C',1,
        cast=tp(4,S),
        duration=tp(2,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="When the cleric casts a Sanctuary spell, any opponent must make a saving throw versus magic in order to strike or otherwise attack him or her. If the saving throw is not made, the creature will attack another and totally ignore the cleric protected by the spell. If the saving throw is made, the cleric is subject to normal attack process including dicing for weapons to hit, saving throws, damage. Note that this spell does not prevent the operation of area attacks (Fireball, Ice Storm, etc.). During the period of protection afforded by this spell, the cleric cannot take offensive action, but he or she may use non-attack spells or otherwise act in any way which does not violate the prohibition against offensive action, This allows the cleric to heal wounds, for example, or to bless, perform an augury, chant, cast a light in the area (not upon on opponent!), and so on, The components of the spell include the cleric's holy/unholy symbol and a small silver mirror."
    ),
    Spell('Aid','C',2,
        cast=tp(4,S),
        duration=tp(1,R),
        duration_lvl=tp(1,R),
        sourcebook=U,
        desc="The recipient of this spell gains the benefit of a Bless spell and a special benison of 1-8 additional hit points. The bless lasts as long as the aid spell, as do the hit points thus gained. The aid allows a character to actually have more hit points than the character's full normal total. The added hit points last only for the duration of the aid spell. Any damage taken by the recipient while the aid spell is in effect is taken off the 1-8 additional hit points before regular ones are lost. Hit points bestowed by an aid spell and then lost cannot be regained by curative magic. Example: A 1st-level fighter has 8 hit points, takes 2 points of damage, and then recieves and aid spell which gives 6 additional hit points. The fighter now has 12 hit points, 6 of which are temporary. If he is then hit for 7 points of damage, 1 regular point and all 6 of the temporary points are lost. The material components of this spell are a tiny strip of white cloth with a sticky substance (such as tree sap) on the ends, plus the cleric's holy symbol."
    ),
    Spell('Augury','C',2,
        cast=tp(2,R),
        duration=tp(0),
        sourcebook=V,
        desc="The cleric casting an Augury spell seeks to divine whether an action in the immediate future (within 3 turns) will be for the benefit of, or harmful to, the party. The base chance for correctly divining the augury is 70%, plus 1% far each level of the cleric casting the spell, i.e. 71% at 1st level, 72% at 2nd, etc, Your referee will determine any adjustments due far the particular conditions of each augury. For example, assume that a party is considering the destruction of a weird seal which closes a portal. Augury is used to find if weal or woe will be the ultimate result to the party. The material component for Augury is a set of gem-inlaid sticks, dragon bones, or similar tokens, or the wet leaves of on infusion which remain in the container after the infused brew is consumed. If the last method is used, a crushed pearl of at least 100 g.p. value must be added to the concoction before it is consumed."
    ),
    Spell('Chant','C',2,
        cast=tp(1,T),
        duration=tp(0),
        sourcebook=V,
        desc="By means of the chant, the cleric brings into being a special favour upon himself or herself and his or her party, and causes harm to his or her enemies. Once the Chant spell is completed, all attacks, damage and saving throws made by those in the area of effect who are friendly to the cleric are at +1, while those of the cleric's enemies are at -1. This bonus/penalty continues as long as the cleric continues to chant the mystic syllables and is stationary. An interruption, however, such as an attack which succeeds and causes damage, grappling the chanter, or a magical silence, will break the spell."
    ),
    Spell('Detect Charm','C',2,
        cast=tp(1,R),
        duration=tp(1,T),
        sourcebook=V,
        desc="When used by a cleric, this spell will detect whether or not a person or monster is under the influence of a Charm spell. Up to 10 creatures can be thus checked before the spell wanes. The reverse of the spell protects from such detection, but only a single creature can be so shielded."
    ),
    Spell('Detect Life','C',2,
        cast=tp(1,R),
        duration=tp(5,R),
        sourcebook=U,
        desc="By the use of this spell, a cleric can tell if a target creature is alive. The magic will detect life in the recipient of a Feign Death spell, or someone in a coma, deathlike trance, or state of suspended animation. If cast upon the body of a creature that is engaged with astral travel, it will reveal that the creature is alive. The spell works on plants and plant creatures as well as animals. The spell's range is diminished if more than a one-inch thickness of wood or stone lies between the cleric and the subject. Each inch of thickness of a wood or stone barrier is treated as 10 feet of open space. A barrier of metal of any thickness will cause the spell to fail and be ruined. Any form of mental protection, including those of psionic or magical nature, will likewise ruin the spell without anything being detected. The spell will detect the first living creature that lies along the cleric's line of sight (and within range), or else the first creature that crosses the line-of-sight path before the duration expires."
    ),
    Spell('Dust Devil','C',2,
        cast=tp(3,R),
        duration_lvl=tp(1,R),
        sourcebook=U,
        desc="This spell enables a cleric to conjure up a weak air elemental - a dust devil of AC 4, 2 HD, MV 18\", 1 attack for 1-4 points of damage, which can be hit by normal weapons. Magic weapons of any type cause it double damage. The dust devil appears as a small whirlwind 5 feet in diameter at its base, 15 feet tall, and 10 feet across at the top. It will move as directed by the cleric, but will be dispelled if ordered to go farther than 3\" away from the spell caster. The winds of the dust devil can hold a gas cloud or a creature in gaseous form at bay or push it away from the caster (though it cannot damage or dispel such a cloud). Its winds are sufficient to put out torches, small campfires, exposed lanterns, and other small, open flames of non-magical origin. If skimming along the ground in an area of loose dust, sand or ash, the dust devil will pick up these particles and disperse them in a cloud 30 feet in diameter centered around the dust devil. Normal vision is not possible through the cloud, and creatures caught in the cloud will be effectively blinded until one round after they are free of it. Spell casting is virtually impossible for someone caught inside such a cloud or inside the dust devil itself; even if the creature fails to score damage on the victim from the buffeting of its winds, a spell caster must make a saving throw versus spell to keep his or her concentration (and the spell) from being ruined. Any creature native to the Elemental Plane of Air - even another creature of the same sort - can dismiss a dust devil at will from a distance of 3\" or less. Creatures not native to the plane occupied by the spell caster are not affected by the dust devil. It is automatically dispelled if it contacts any creature with innate magic resistance - but not until after it gets a chance to hit and do damage."
    ),
    Spell('Enthrall','C',2,
        cast=tp(1,R),
        duration=tp(1,VA),
        sourcebook=U,
        desc="A cleric who uses this spell can bind and enthrall an audience that can fully understand his or her language. Listeners of the same race as the cleric are allowed a saving throw versus spell; those of a different race which is generally unfriendly to the cleric's race save at +4. It is impossible to enthrall a character or creature with more than 4 levels or hit dice, or one with a wisdom score greater than 15. To effect the spell, the caster must speak without interruption for a full round. Thereafter, the enchantment lasts for as long as the cleric keeps speaking, to a maximum of 6 turns. Those who fail their saving throw will view the cleric as if he or she had a charisma of 21 (loyalty base +70%, reaction adjustment +50%). They will stand and listen to the cleric's words, but will not act on them as if a suggestion had been cast. When the cleric stops talking, the spell is broken and the listeners regain control of their own minds. Any form of attack (i.e. a successful hit or the casting of a spell) against the cleric will instantly cancel the enthrall spell, as will any attempt by the cleric to cast a different spell or perform some other action. Members of the audience who make a successful saving throw will view the cleric as having a charisma of 3; they may (50% chance) hoot and jeer, allowing a new saving throw for others listening. If the cleric tries to take undue advantage of the spell by preaching about a religion or alignment opposed to that to which the members of the audience subscribe, each \"offended\" listener is allowed a new saving throw at +5."
    ),
    Spell('Find Traps','C',2,
        cast=tp(5,S),
        duration=tp(3,T),
        sourcebook=V,
        desc="When a cleric casts a find traps spell, all traps - concealed normally or magically - of magical or mechanical nature become visible to him or her. Note that this spell is directional. and the caster must face the desired direction in order to determine if a trap is laid in that particular direction."
    ),
    Spell('Hold Person','C',2,
        cast=tp(5,S),
        duration=tp(4,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell holds immobile, and freezes in places, from 1-3 humans or humanoid creatures (see below) for 5 or more melee rounds. The level of the cleric casting the Hold Person spell dictates the length of time the effect will last. The basic duration is 5 melee rounds at 1st level, 6 rounds at 2nd level, 7 rounds at 3rd level, etc. If the spell is cast at three persons, each gets a saving throw at the normal score; if only two persons are being enspelled, each makes their saving throw at -1 on their die; if the spell is cast at but one person, the saving throw die is at -2. Persons making their saving throws are totally unaffected by the spell. Creatures affected by a Hold Person spell are: brownies, dryads, dwarves, elves, gnolls, gnomes, goblins, half-elves, halflings, half-orcs, hobgoblins, humans, kobolds, lizard men, nixies, orcs, pixies, sprites, and troglodytes. The spell caster needs a small, straight piece of iron as the material component of this spell."
    ),
    Spell('Holy Symbol','C',2,
        cast=tp(1,T),
        duration=tp(1,P),
        sourcebook=U,
        desc="This spell is used to prepare a cleric's holy symbol, or to create a new symbol to replace a lost or damaged one. The new symbol-to-be, which is the spell's material component (and obviously is not consumed in the casting), must be crafted of appropriate material depending on the religion/deity in question, and must be of the proper shape and design - a cleric cannot pick up just any item and make it into a holy symbol. A cleric may posess two holy symbols at one time, and this spell can be used to create a second one as a spare. No cleric can create a holy symbol related to a religion or deity other than the one that he or she worships. The holy symbol of a good or evil cleric will radiate a faint aura of good or evil, but it is not a magical item per se. The holy symbol of a cleric who is of neutral morals (with respect to good and evil) will have no such aura."
    ),
    Spell('Know Allignment','C',2,
        cast=tp(1,R),
        duration=tp(1,T),
        sourcebook=V,
        desc="A Know Alignment spell enables the cleric to exactly read the aura of a person - human, semi-human, or non-human. This will reveal the exact alignment of the person. Up to 10 persons can be examined with this spell. The reverse totally obscures alignment, even from this spell, of a single person for 1 turn, two persons for 5 rounds, etc. Certain magical devices will negate the ability to Know Alignment."
    ),
    Spell('Messenger','C',2,
        cast=tp(1,R),
        duration_lvl=tp(1,H),
        sourcebook=U,
        desc="This spell enables the cleric to call upon a small (size S) creature of at least animal intelligence to act as his or her messenger. The spell does not affect creatures that are \"giant\" types, and it will not work on creatures with an intelligence score of 4 or higher, or with a rating of low intelligence or better (whichever applies). If the creature is already within range, the cleric, using some type of food desirable to the animal as a lure, can call the animal to come. The animal is allowed a saving throw versus spell, and if this succeeds the spell fails. If the saving throw is failed, the animal will advance toward the cleric and await his or her bidding. The cleric can communicate with the animal in a crude fashion, telling it to go to a certain place, but directions must be simple. The spell caster can attach some small item or note to the animal. If so instructed, the animal will then wait at that location until the duration of the spell expires. (Note that unless the intended recipient of a message is expecting a messenger in the form of a small animal or bird, the carrier may be ignored.) When the spell's duration expires, the animal or bird will return to its normal activities. The intended reciever of a message gains no communication ability."
    ),
    Spell('Resist Fire','C',2,
        cast=tp(5,S),
        duration=tp(0),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="When this spell is placed upon a creature by a cleric, the creature's body is toughened to withstand heat, and boiling temperature is comfortable. The recipient of the resist tire spell can even stand in the midst of very hot or magical fires such as those produced by red-hot charcoal, a large amount of burning oil, flaming swords, fire storms, fire balls, meteor swarms. or red dragon's breath - but these will affect the creature, to some extent. The recipient of the spell gains a bonus of +3 an saving throws against such attack forms, and all damage sustained is reduced by 50%; therefore, if the saving throw is not made, the creature sustains one-half damage, and if the saving throw is mode only one-quarter damage is sustained, Resistance to fire lasts for 1 turn for each level of experience of the cleric placing the spell. The caster needs a drop of mercury as the material component of this spell."
    ),
    Spell('Silence 15\' Radius','C',2,
        cast=tp(5,S),
        duration=tp(0),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="Upon casting this spell, complete silence prevails in the area of its effect. All sound is stopped, so all conversation is impossible, spells cannot be cast and no noise whatsoever issues forth, The spell can be cast into the air or upon an object. The spell of Silence lasts for 2 rounds for each level of experience of the cleric, i.e. 2 rounds at 1st level, 4 at 2nd, 6 at 3rd, 8 at 4th and so forth. The spell can be cast upon a creature, and the effect will then radiate from the creature and move as it moves. If the creature is unwilling, it saves against the spell, and if the saving throw is made, the spell effect locates about one foot behind the target creature."
    ),
    Spell('Slow Poison','C',2,
        cast=tp(1,S),
        duration=tp(0),
        duration_lvl=tp(6,T),
        sourcebook=V,
        desc="When this spell is placed upon a poisoned individual it greatly slows the effects of any venom, even causing a supposedly dead individual to have life restored if it is cast upon the victim within a number of turns less than or equal to the level of experience of the cleric after the poisoning was suffered. i.e. a victim poisoned up to 10 turns previously could be temporarily saved by a 10th or higher level cleric who cast Slow Poison upon the victim. While this spell does not neutralize the venom, it does prevent it from substantially harming the individual for the duration of its magic, but each turn the poisoned creature will lose 1 hit point from the effect of the venom (although the victim will never go below 1 hit point while the Slow Poison spell's duration lasts). Thus, in the example above, the victim poisoned 10 turns previously has only 10 hit points, so when the 10th level cleric casts the spell, the victim remains with 1 hit point until the spell duration expires, and hopefully during that period a full cure can be accomplished. The material components of this spell are the cleric's holy/unholy symbol and a bud of garlic which must be crushed and smeared on the victim's bare feet."
    ),
    Spell('Snake Charm','C',2,
        cast=tp(5,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="When this spell is cast, a hypnotic pattern is set up which causes one or more snakes to cease all activity except a semi-erect postured swaying movement. If the snakes are charmed while in a torpor, the duration of the spell is 3 to 6 turns (d4 + 2); if the snakes are not torpid, but are not aroused and angry, the charm lasts 1 to 3 turns; if the snakes are angry and/or attacking, the snake charm spell will last from 5 to 8 melee rounds (d4+4). The cleric casting the spell can charm snakes whose hit points are less than or equal to those of the cleric. On the average, a 1st level cleric could charm snakes with a total of 4 or 5 hit points; a 2nd level cleric 9 hit points, a 3rd level 13 or 14 hit points, etc. The hit points can represent a single snake or several of the reptiles, but the total hit points cannot exceed those of the cleric casting the spell."
    ),
    Spell('Speak With Animals','C',2,
        cast=tp(5,S),
        duration=tp(0),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="By employing this spell, the cleric is empowered to comprehend and communicate with any warm or cold-blooded animal which is not mindless (such as an amoeba). The cleric is able to ask questions, receive answers, and generally be on amicable terms with the animal. This ability lasts for 2 melee rounds for each level of experience of the cleric employing the spell. Even if the bent of the animal is opposite to that of the cleric (evil/good, good/evil), it and any others of the same kind with it will not attack while the spell lasts. If the animal is neutral or of the some general bent as the cleric (evil/evil, good/good), there is a possibility that the animal, and its like associates, will do some favour or service for the cleric. This possibility will be determined by the referee by consulting a special reaction chart, using the charisma of the cleric and his actions as the major determinants. Note that this spell differs from speak with monsters (q.v.), for it allows conversation only with basically normal, non-fantastic creatures such as apes, bears, cats, dogs, elephants, and so on."
    ),
    Spell('Spiritual Hammer','C',2,
        cast=tp(5,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="By calling upon his or her deity, the cleric casting a Spiritual Hammer spell brings into existence a field of force which is shaped vaguely like a hammer. This area of force is hammer-sized, and as long as the cleric who invoked it concentrates upon the hammer, it will strike at any opponent within its range as desired by the cleric. The force area strikes as a magical weapon equal to one plus per 3 levels of experience of the spell caster for purposes of being able to strike creatures, although it has no magical plusses whatsoever \"to hit\", and the damage it causes when it scores a hit is exactly the same as a normal war hammer, i.e. 1-6 versus opponents of man-sire or smaller, 1-4 upon larger opponents. Furthermore, the hammer strikes at exactly the same level as the cleric controlling it, just as if the cleric was personally wielding the weapon. As soon as the cleric ceases concentration, the Spiritual Hammer is dispelled. Note: If the cleric is behind an opponent, the force can strike from this position, thus gaining all bonuses for such an attack and negating defensive protections such as shield and dexterity. The material component of this spell is a normal war hammer which the cleric must hurl towards opponents whilst uttering a plea to his or her deity. The hammer disappears when the spell is cast."
    ),
    Spell('Withdraw','C',2,
        cast=tp(3,S),
        duration=tp(1,VA),
        sourcebook=U,
        desc="By means of a withdraw spell, the cleric effectively alters the flow of time with regard to himself or herself. While but 1 segment of time passes for those not affected by the spell, the cleric is able to spend 1 round of time in contemplation. The base spell duration is 2 segments (2 rounds, from the cleric's point of view), and the cleric adds 1 additional increment of time for each level of experience he or she possesses. Thus, at 5th level of experience, the spell caster could spend up to 6 rounds cogitating on some matter while but 6 segments of time passed for all others. (The DM must allow the spell caster 1 minute of real time per segment to ponder some problem or question. No discussion with non-affected characters is permitted.) Note that while affected by a withdraw spell, the cleric can perform only these particular acts: the casting of an augury spell, any curing or healing spells, or any informational spells - and all such spells can only be cast upon the cleric himself or herself. The casting of any of these spells in a different fashion (e.g. a Cure Light Wounds bestowed upon a companion) will cause the magic of the withdraw spell to cease. Similarly, the cleric who is affected by the withdraw spell cannot walk or run, become invisible, or otherwise engage in actions othen than thinking, reading, and the like. The withdrawn cleric can be affected by the actions of the others while under the influence of this spell, and any attack upon the cleric which succeeds will break the spell."
    ),
    Spell('Wyvern Watch','C',2,
        cast=tp(5,S),
        duration=tp(8,H),
        sourcebook=U,
        desc="This spell is known as wyvern watch because of the insubstantial haze brought forth by its casting, which vaguely resembles a wyvern. It is typically used to guard some area against intrusion. Any creature that approaches within 1\" of the area in question is subject to attack from the spell force. The \"wyvern\" will strike, and any creature so attacked must make its saving throw versus spell or else stand paralyzed for 1 round per level of the caster, or until freed by the spell caster, by a dispel magic spell, or by a remove paralysis spell. A successful saving throw indicates that the target creature was missed by the attack of the wyvern-form and the spell remains in place. As soon as a target creature is successfully struck by the wyvern-form, the paralysis takes effect and the force of the spell itself is dissipated. The spell force will likewise dissipate if no intruder is struck by the wyvern-form for 8 hours after the spell is cast. Any creature approaching the space being guarded by the wyvern-form may be able to detect its presence before coming close enough to be attacked; this chance of detection is 90% in bright light, 30% in twilight conditions, and 0% in darkness. The material component is the cleric's holy/unholy symbol."
    ),
    Spell('Animate Dead','C',3,
        cast=tp(1,R),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell creates the lowest of the undead monsters, skeletons or zombies, from the bones or bodies of dead humans. The effect is to cause these remains to become animated and obey the commands of the cleric casting the spell. The skeletons or zombies will follow, remain in an area and attack any creature (or just a specific type of creature) entering the place, etc. The spell will animate the monsters until they are destroyed or until the magic is dispelled. (See Dispel Magic spell). The cleric is able to animate 1 skeleton or 1 zombie for each level of experience he or she has attained. Thus, a 2nd level cleric can animate 2 of these monsters, a 3rd level 3, etc. The act of animating dead is not basically a good one, and it must be used with careful consideration and good reason by clerics of good alignment. It requires a drop of blood, a piece of human flesh, and a pinch of bone powder or a bone shard to complete the spell."
    ),
    Spell('Cloudburst','C',3,
        cast=tp(5,S),
        duration=tp(1,R),
        sourcebook=U
    ),
    Spell('Continual Light','C',3,
        cast=tp(6,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell is similar to a Light spell, except that it lasts until negated (by a Continual Darkness or Dispel Magic spell) and its brightness is very great, being nearly as illuminating as full daylight. It can be cast into air, onto an object, or at a creature, In the third case, the Continual Light affects the space about one foot behind the creature if the latter makes its saving throw. Note that this spell will blind a creature if it is successfully cast upon the visual organs, for example. Its reverse causes complete absence of light."
    ),
    Spell('Create Food & Water','C',3,
        cast=tp(1,T),
        duration=tp(1,P),
        sourcebook=V,
        desc="When this spell is cast, the cleric causes food and/or water to appear. The food thus created is highly nourishing, and each cubic foot of the material will sustain three human-sized creatures or one horse-sized creature for a full day. For each level of experience the cleric has attained, 1 cubic foot of food and/or water is created by the spell, i.e. 2 cubic feet of food are created by a 2nd level cleric, 3 by a 3rd, 4 by a 4th, and so on; or the 2nd level cleric could create 1 cubic foot of food and 1 cubic foot of water, etc."
    ),
    Spell('Cure Blindness','C',3,
        cast=tp(1,R),
        duration=tp(1,P),
        sourcebook=V,
        desc="By touching the creature afflicted, the cleric employing the spell can permanently cure most forms of blindness. Its reverse, Cause Blindness, requires a successful touch upon the victim, and if the victim then makes the saving throw, the effect is negated."
    ),
    Spell('Cure Disease','C',3,
        cast=tp(1,T),
        duration=tp(1,P),
        sourcebook=V,
        desc="The cleric cures most diseases - including those of a parasitic, bacterial, or viral nature - by placing his or her hand upon the diseased creature. The affliction rapidly disappears thereafter, making the cured creature whole and well in from 1 turn to 1 week, depending on the kind of disease and the state of its advancement when the cure took place. The reverse of the Cure Disease spell is Cause Disease. To be effective. the cleric must touch the intended victim, and the victim must fail the saving throw. The disease caused will begin to affect the victim in 16 turns, causing the afflicted creature to lose 1 hit point per turn, and 1 point of strength per hour, until the creature is at 10% of original hit points and strength, at which time the afflicted is weak and virtually helpless."
    ),
    Spell('Death\'s Door','C',3,
        cast=tp(5,S),
        duration_lvl=tp(1,H),
        sourcebook=U,
        desc="When a cleric employs this spell, he or she touches a human or demi-human who is unconscious and \"at death's door\" (-1 to -9 hit points). The spell immediately brings the individual to 0 hit points. While the individual remains unconscious, bleeding and deterioration are stopped for the duration of the death's door spell. The subject, because of being treated by the spell and now being at 0 hit points, can be brought to consciousness, and have hit points restored, by means of Cure Light Wounds, Cure Serious Wounds, etc., potions such as healing or extra-healing, or clerical or other items which magically restore lost hit points. The material components of the spell are the cleric's holy/unholy symbol, a bit of white linen, and any form of unguent."
    ),
    Spell('Dispel Magic','C',3,
        cast=tp(6,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="When a cleric casts this spell, it neutralizes or negates the magic it comes in contact with as follows: A Dispel Magic will not affect a specially enchanted item such as a scroll, magic ring, wand, rod, staff, miscellaneous magic item, magic weapon, magic shield, or magic armour. It will destroy magic potions (they are treated as 12th level for purposes of this spell), remove spells cast upon persons or objects, or counter the casting of spells in the area of effect. The base chance for success of a Dispel Magic spell is 50%. For every level of experience of the character casting the Dispel Magic above that of the creature whose magic is to be dispelled (or above the efficiency level of the object from which the magic is issuing), the base chance increases by 5%, so that if there are 10 levels of difference, there is a 100% chance. For every level below the experience/efficiency level of the creature/object, the base chance is reduced by 2%. Note that this spell can be very effective when used upon charmed and similarly beguiled creatures. It is automatic in negating the spell caster's own magic."
    ),
    Spell('Feign Death','C',3,
        cast=tp(2,S),
        duration=tp(1,T),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the third level magic-user spell, Feign Death (q.v.). Note that a character of any level may be affected by the cleric casting this spell, and that the material components are a pinch of graveyard dirt and the cleric's holy/unholy symbol."
    ),
    Spell('Flame Walk','C',3,
        cast=tp(5,S),
        duration=tp(1,T),
        duration_lvl=tp(1,T),
        sourcebook=U,
        desc="By means of this spell the caster is able to empower himself or herself, or another creature of man-size and comparable mass, to withstand non-magical fires up to temperatures of 2,000°F. It also confers a +2 bonus to saving throws against magical fires. For every level of experience above the minimum required to create the dweomer (5th), the caster can affect an additional man-sized creature. This growing power enables multiple individuals, or one or more of greater than man-size and mass, to be affected by the flame walk spell. For instance, an 11th-level caster could empower both himself or herself and a steed such as a horse to move in molten lava. (Consider a horse to be equivalent to 6 humans for purposes of this spell; conversely, halfling-sized creatures count as ½ human apiece, and pixie-sized creatures are considered equivalent to ¼ human each.) The material componenets of the spell are at least 500 gp of powdered ruby and the cleric's holy/unholy symbol."
    ),
    Spell('Glyph of Warding','C',3,
        cast=tp(1,VA),
        duration=tp(1,P),
        sourcebook=V,
        desc="A Glyph of Warding is a powerful inscription magically drawn to prevent unauthorized or hostile creatures from passing, entering, or opening. It can be used to guard a small bridge, ward an entry, or as a trap on a chest or box. When the spell is cast, the cleric weaves a tracery of faintly glowing lines around the warding sigil. For every square foot of area to be protected, 1 segment of time is required to trace the warding lines from the glyph, plus the initial segment during which the sigil itself is traced. A maximum of a 5' X 5' area per level can be warded. When the spell is completed, the glyph and tracery become invisible, but any creature touching the protected area without first speaking the name of the glyph the cleric has used to serve as a ward will be subject to the magic it stores. Saving throws apply, and will either reduce effects by one-half or negate them according to the glyph employed. The cleric must use incense to trace this spell, and then sprinkle the area with powdered diamond (at least 2,000 g.p. worth) if it exceeds 50 square feet. Typical glyphs shock for 2 points of electrical damage per level of the spell caster, explode for a like amount of fire damage, paralyze, blind, or even drain a life energy level (if the cleric is of high enough level to cast this glyph)."
    ),
    Spell('Locate Object','C',3,
        cast=tp(1,T),
        duration=tp(0),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell aids in location of a known or familiar object. The cleric casts the spell, slowly turns, and knows when he or she is facing in the direction of the object to be located, provided the object is within range, i.e. 7\" for 1st level clerics, 8\" for 2nd, 9\" for 3rd, etc, The casting requires the use of a piece of lodestone, The spell will locate such objects as apparel, jewellery, furniture, tools, weapons, or even a ladder or stairway. By reversal (obscure object), the cleric is able to hide an object from location by spell, crystal ball, or similar means. Neither application of the spell will affect a living creature."
    ),
    Spell('Magical Vestment','C',3,
        cast=tp(1,R),
        duration_lvl=tp(6,R),
        sourcebook=U,
        desc="This spell enchants the caster's vestment, providing protection equivalent to armor. It will only function while the cleric is on ground consecrated to his or her deity (cf. 1st-level Ceremony spell). If any armor or protective device is worn during the spell duration, the vestment protects as if normal chain mail armor. If no other protection is worn, the vestment also gains a +1 enchantment for each four levels of the cleric, to a maximum effect of chain mail +4 (base AC 1). The magic lasts for 6 rounds per level of the caster, or until the caster loses consciousness or leaves the consecrated area. The material components are the vestment to be enchanted and the cleric's holy symbol."
    ),
    Spell('Meld Into Stone','C',3,
        cast=tp(7,S),
        duration=tp(1,VA),
        sourcebook=U,
        desc="The magic of this spell, when properly cast, allows the cleric to meld his or her body and possessions worn or carried into a large stone. To effect the spell, the cleric stands next to the stone to be melded into (which must be large enough to accomodate the cleric's body in all three dimensions) while holding a small sample of the same type of stone. When casting is complete, the cleric and up to 100 pounds of his or her non-living gear blend into the stone. Magical artifacts and relics are not affected by the spell. If the dimensions of the stone are not sufficient, or if the cleric is wearing and carrying more than 100 pounds of gear, the spell will fail and be wasted. The magic lasts for 9-16 (1d8 + 8) rounds, the variable part of the duration rolled secretly by the DM. At any time before the duration expires, the cleric can step out of the stone along the same surface that he or she used to enter it (i.e., the spell does not allow movement through the stone such as would a Passwall or Phase Door spell). If the duration runs out before the cleric exits the stone, then he or she will be expelled from the stone and take 4-32 (4d8) points of damage — and each piece of gear affected must save versus petrification or turn to stone. While in the stone, the cleric is aware of the passage of time; however, he or she cannot see or hear anything that may be going on around the stone. The following spells will harm the cleric if cast upon the stone that he or she is occupying: Stone to Flesh will expel the cleric and inflict 4-32 points of damage, but items carried need not save. Stone Shape will cause 4-16 (4d4) points of damage, but will not expel the cleric. Transmute Rock to Mud expels the cleric and will slay the victim instantly unless he or she makes a succussful saving throw versus spell."
    ),
    Spell('Negative Plane Protection','C',3,
        cast=tp(1,R),
        duration_lvl=tp(1,T),
        sourcebook=U,
        desc="This spell enables the caster or any other eligible creature touched to be partially protected from an undead monster that has an existence on the Negative Material Plane (such as a shadow, wight, wraith, spectre, or vampire). The dweomer of the spell opens a channel to the Positive Material Plane, the energy from which helps to offset the effect of the undead creature's attack. The recipient is allowed a saving throw versus death magic if he or she is touched (attacked) by an undead creature. Success indicates that the recipient takes normal hit-point damage from the attack, but does not suffer the drain of experience that would otherwise take place. In addition, the undead creature takes 2-12 (2d6) hit points of damage from the Positive Plane energy. The magic is only proof against one such attack, and dissipates after that attack whether or not the saving throw is successful. If the saving throw versus death magic is failed, the recipient of the spell takes double the usual physical damage in addition to the loss of experience that normally occurs. The spell will also protect the recipient from the effect of a magic-user's Energy Drain spell, but in such a case the magic-user is not affected. The contact between the Positive and Negative Planes that this spell brings about will cause a bright flash of light and sound like that of a thunderclap, but these phenomena do not cause damage in any event. The protection will last for 1 turn per level of the cleric casting the spell, or until the recipient is successfully attacked by an undead monster. This spell cannot be cast on the Negative Material Plane."
    ),
    Spell('Prayer','C',3,
        cast=tp(6,S),
        duration=tp(0),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell exactly duplicates the effects of a Chant with regard to bonuses of +1 for friendly attacks and saving throws and -1 on like enemy dice. However, once the Prayer is uttered, the cleric can do other things, unlike a Chant which he or she must continue to make the spell effective. The cleric needs a silver holy symbol, prayer beads, or a similar device as the material component of this spell."
    ),
    Spell('Remove Curse','C',3,
        cast=tp(6,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="Upon casting this spell, the cleric is usually able to remove a curse - whether it be on an object, a person, or in the form of some undesired sending or evil presence. Note that the Remove Curse spell will not affect a cursed shield, weapon or suit of armour, for example, although the spell will typically enable the person afflicted with any such cursed item to be rid of it. The reverse of the spell is not permanent; the Bestow Curse lasts for 1 turn for every level of experience of the cleric using the spell. It will lower one ability of the victim to 3 (your DM will determine which by random selection) 50% of the time; reduce the victim's \"to hit\" and saving throw probabilities by -4 25% of the time; or make the victim 50% likely per turn to drop whatever he, she, or it is holding (or simply do nothing in the case of creatures not using tools) 25% of the time. It is possible for a cleric to devise his or her own curse, and it should be similar in power to those shown. Consult your referee. The target of a Bestow Curse spell must be touched. If the victim is touched, a saving throw is still applicable; and if it is successful, the effect is negated."
    ),
    Spell('Remove Paralysis','C',3,
        cast=tp(6,S),
        duration=tp(1,P),
        duration_lvl=tp(0),
        sourcebook=U,
        desc=("By the use of this spell, the cleric can free the subject creature(s) from the effects of paralyzation or similar forces (such as a Hold spell). By casting this spell and then pointing his or her finger in the proper direction, the cleric can remove paralysis from as many as 4 creatures that are within range and within the area of affect. There must be no physical or magical barrier between the caster and the creature(s) to be affected, or else the spell will fail and be wasted. Each target of the spell obtains a new saving throw versus paralyzation, at a +3 bonus if only one creature is involved, +2 if two creatures are to be affected, and +1 if three or four reatures are the target.\n\n"
            "The reverse of the spell, Cause Paralysis, can affect only one target, which must be touched by the cleric (successful roll \"to hit\") using his or her holy/unholy symbol. If the victim fails a saving throw versus spell, paralyzation will set in for a duration of 1-6 rounds plus 1 round per level of the caster. Clerics of good alignment should be very discerning in their use of cause paralysis, and this spell might actually be prohibited to clerics belonging to certain good-aligned orders."
        )
    ),
    Spell('Speak With Dead','C',3,
        cast=tp(1,T),
        duration=tp(1,VA),
        sourcebook=V
    ),
    Spell('Water Walk','C',3,
        cast=tp(7,S),
        duration=tp(1,T),
        duration_lvl=tp(1,T),
        sourcebook=U,
        desc="By means of this spell, the caster is able to empower himself or herself or another creature of man-size and comparable mass to tread upon water as if it were firm, grassy ground (cf. ring of water walking). For every level of the caster above the minimum required to create the dweomer (5th level), he or she can affect an additional man-sized creature. This growing power enables multiple individuals, or one or more of greater size and mass, to be affected by the water walk spell. For instance, an 11th-level caster could additionally affect a horse, so that he or she could move atop the waves while mounted. (Consider a horse to be equivalent to 6 humans for purposes of this spell.) The material components for this spell are a piece of cork and the cleric's holy/unholy symbol."
    ),
    Spell('Abjure','C',4,
        cast=tp(1,R),
        duration=tp(1,P),
        sourcebook=U,
        desc=("When a cleric employs a spell of this sort, he or she is attempting to return a creature from another plane of existence to its own plane. The exact name of the type of creature to be affected by the abjure spell must be known. If the creature also has a specific (proper) name, then that too must be known and used. The naming cleric then compares his or her level against the level or hit dice of the creature under abjuration, in the same way that the success of a Dispel Magic spell is determined (base 50% chance of success, plus or minus the level/HD difference between the caster and the creature to be affected). The percent chance for success is then compared to a percentile dice roll. If the roll is equal to or less than the chance to abjure, the creature is instantly sent back to its own plane. In all other cases the spell fails. (The creature might not wish to remain on the caster's plane, and in such a case it could be appreciative of the cleric's attempt to return it to its home.)\n\n"
            "The reverse of the spell, Implore, entreats some like-aligned creature from another plane to come to the cleric casting the spell. Success must be determined just as if abjure had been cast. In like vein, the spell caster must know the exact name of the type of creature as well as its given name, if any. If the implore spell succeeds, the cleric has absolutely no guarantee that the creature summoned from another plane will be favorably disposed to him or her. Neither version of the spell will function upon deities, but might affect servants or minions thereof.\n\n"
            "The material components for an abjure spell are a holy/unholy symbol, holy or unholy water, and often some material inimical to the creature. In reversed form, the material components are the same except for the last, which must be something that the implored creature craves or respects."
        )
    ),
    Spell('Cloak of Fear','C',4,
        cast=tp(6,S),
        duration_lvl=tp(1,T),
        sourcebook=U,
        desc=("The casting of this spell empowers the cleric to radiate a personal aura of fear out to a 3' radius. Any character or creature that intrudes upon this aura must save versus spell or run away in fear for 6 rounds (cf. 3rd-level magic-user spell Fear). The spell will only remain in effect until one creature fails to save, whereupon the dweomer of the spell is dissipated. The spell has no effect upon creatures that themselves radiate fear, or upon undead creatures of any sort, and it is not dissipated upon contact by such creatures. It likewise remains in effect if an intruder makes a successful saving throw, but will expire after a duration of 1 turn per level of the cleric if not brought down earlier. Note that members of the cleric's party are not immune to the effects of the spell. The cleric may cancel the aura at any time before the duration ends if desired.\n\n"
            "The reverse of the spell, Cloak of Bravery, can be cast upon the cleric or upon another creature which is a willing recipient. A character or creature protected by a cloak of bravery gains a +3 bonus to the saving throw against any form of magical fear encountered. The magic of the cloak of bravery works only once and only upon a single figure, and is dispelled whether or not the recipient succeeds on his or her saving throw. The magic does not negate or otherwise affect the innate ability of a creature (such as a devil) to radiate fear, so that the creature can still affect others in the vicinity.\n\n"
            "The material components for a cloak of fear are a miniature quiver and a chicken feather; for a cloak of bravery, the necessary items are a drop of alcohol and the brain of a newt."
        )
    ),
    Spell('Cure Serious Wounds','C',4,
        cast=tp(7,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell is a more potent version of the Cure Light Wounds spell (q.v.). Upon laying his or her hand upon a creature, the cleric causes from 3 to 17 (2d8+1) hit points of wound or other injury damage to the creature's body to be healed. This healing will affect only those creatures listed in the Cure Light Wounds spell explanation. Cause Serious Wounds, the reverse of the spell, operates similarly to the Cause Light Wounds spell, the victim having to be touched first, and if the touch is successful, it will inflict 3 to 17 hit points."
    ),
    Spell('Detect Lie','C',4,
        cast=tp(7,S),
        duration=tp(0),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="When the cleric employs this spell, the recipient is immediately able to determine if truth is being spoken. The spell lasts one round for each level of experience of the cleric casting the Detect Lie. Gold dust is necessary for this spell. Its reverse, Undetectable Lie, makes bald-face untruths seem reasonable, or simply counters the Detect Lie spell powers. The reverse spell requires brass dust as its material component."
    ),
    Spell('Divination','C',4,
        cast=tp(1,T),
        duration=tp(0,R),
        sourcebook=V,
        desc="Similar to an Augury spell, a Divination spell is used to determine information regarding an area. The area can be a small woods, large building, or section of a dungeon level. In any case, its location must be known. The spell gives information regarding the relative strength of creatures in the area: whether a rich, moderate or poor treasure is there; and the relative chances for incurring the wrath of evil or good supernatural, super powerful beings if the area is invaded and attacked. The base chance for correct divination is 60%, plus 1% for each level of experience of the cleric casting the spell, i.e. 65% at 5th level, 66% at 6th, etc. The Dungeon Master will make adjustments to this base chance considering the facts regarding actual area being divined. If the result is not correct, inaccurate information will be obtained. The material components of the Divination are a sacrificial creature, incense, and the holy symbol of the cleric. If an unusually potent Divination is attempted, sacrifice of particularly valuable gems or jewellery and/or magic items may be required."
    ),
    Spell('Exorcise','C',4,
        cast=tp(1,VA),
        duration=tp(1,P),
        sourcebook=V,
        desc="The spell of Exorcism will negate possession of a creature or an object by any outside or supernatural force. This includes control of a creature by some force in an object, possession by Magic Jar (q.v.) spell, demonic possession, curse and even charm, for the Exorcise spell is similar to a Dispel Magic spell. Furthermore, it will affect a magical item if such is the object of the exorcism. Thus a soul object of any sort which comes under successful Exorcism will make the life force of the creature concerned wholly inhabit its nearest material body, wholly and completely. (Cf. ADVANCED DUNGEONS & DRAGONS, MONSTER MANUAL, Demon.) The Exorcise spell, once begun. cannot be interrupted, or else it is spoiled and useless. The base chance for success is a random 1% to 100%. Each turn of Exorcism the dice are rolled, and if the base chance number, or less, is rolled, the spell is successful. Base chance of success is modified by -1% for each level of difference between the cleric's level of experience and the level of the possessor or possessing magic, where the smaller number is the cleric's level. In the obverse, a +1% cumulative is added. The referee can determine base chance according to the existing circumstances if he or she so desires. Material components for this spell are the holy object of the cleric and holy water (or unholy, in the case of evil clerics, with respect to object and water). A religious artifact or relic can increase the chance of success by from 1% to 50%, according to the power of the artifact or relic."
    ),
    Spell('Giant Insect','C',4,
        cast=tp(1,VA),
        duration_lvl=tp(2,R),
        sourcebook=U,
        desc=("By means of this spell, the cleric can turn one or more normal-sized insects into larger forms which resemble the \"giant\" forms of such creatures as described in the Monster Manual books or the FIEND FOLIO® Tome. The number of insects that can be affected is dependent upon the cleric's level: one at 7th-9th level, two at 10th or 11th level, three at 12th or 13th level, and four at 14th or higher level. The magic only works upon one type of insect at one time; i.e., a cleric cannot use the same casting of the spell to affect both an ant and a fly. The casting time for a giant insect spell is one round per hit die of the resulting giant creature(s); if the casting is interrupted for any reason, the subject insect(s) will die and the spell will be ruined. A monster created by this spell will have as many attacks per round as its namesake, but will not do full damage unless the created form has as many hit dice as the usual giant version of the same insect. Although it may have more hit dice than a standard giant form, the created insect can never exceed the damage figures given in the books. Example: A cleric of 14th level can use the giant insect spell to enlarge a normal wasp to one having 6 HD (instead of the usual 4 HD for a giant wasp; see Monster Manual), but the creature would still do damage of 2-8/1-4. Conversely, a 7th-level cleric can use this spell to create a giant wasp of 3 HD, and such a creature would have reduced damage figures of 2-6/1-3 — three-fourths of the damage potential of a \"real\" giant wasp, since it only has three-fourths of the usual number of hit dice for such a creature.\n\n"
            "The spell will only work on actual insects. Arachnids, crustaceans, and other types of small creatures are not affected. The giant insects created will not have any special attacks or defenses possessed by the standard giant forms; however, armor class, movement rate, and other physical characteristics are as described in the creature's book listing. Any giant insects created by this spell will not attempt to harm the cleric, but the cleric's control of such creatures is limited. He or she could give them simple commands such as \"attack\", \"defend\", \"guard\", and so forth, but could not instruct them to attack a certain creature or guard against a particular occurence. Unless commanded to do otherwise, the giant insects will attemp to attack whomever or whatever is near them.\n\n"
            "The reverse of the spell, shrink insect, will reduce the size of standard giant insects as well as those created by the unreversed form of the spell. The shrinking will be at a rate of 1 HD for every 4 levels of the casting cleric, with a maximum of 6 HD of reduction (to a minimum of ⅛ HD, or 1 hp). Special attacks possessed by a standard giant insect will be retained, but at a weaker level which allows a bonus to the saving throw versus the attack. For instance, a 9th-level cleric could cast shrink insect upon a standard giant wasp to reduce it form 4 HD to 1 HD. The resulting insect would still be able to use its poison string, but the saving throw against such an attack would be at a +3 bonus (or perhaps higher), and the hit-point damage from its normal attacks would be reduced to 1-2 for a bite and 1 point for a sting — one-fourth of the usual amounts, since the creature is only one-fourth of its original size. The material component for either version of the spell is the cleric's holy/unholy symbol."
        )
    ),
    Spell('Imbue With Spell Ability','C',4,
        cast=tp(1,T),
        duration=tp(1,VA),
        sourcebook=U,
        desc=("By the use of this spell, the cleric can bestow the ability to cast a particular spell upon a character normally unable to cast spells. The magic is only effective on thieves, fighters, cavaliers, assassins, monks, rangers (of under 8th level), and paladins (of under 9th level) — it will not work on a member of any other character class or sub-class, nor will it function upon a monster or any individual with less than one full hit die. The spell or spells to be imbued in the subject must be ones the cleric presently carries (i.e., has prayed for), and they can only be spells of an informational or defensive nature, or a cure light wounds spell. An attempt to transfer any other sort of spell will cause the magic to fail, and then no spells will be imbued in the recipient even if other allowable spells were also chosen. As many as three separate spells can be imbued, including one 2nd-level spell and one or two 1st-level spells. In order to recieve any spell, the subject character must have a wisdom score of 9 or higher. A single 1st-level spell can be imbued in any eligible recipient, but the recipient must be at least 3rd level to recieve two 1st-level spells, and must be at least 5th level to recieve a 2nd-level spell. If a transferred spell's characteristics (range, duration, area of effect, etc.) are variable according to the level of the caster, then the recipient will cast them at his or her own level. All other spell details (e.g., casting time, components, etc.) apply normally.\n\n"
            "When a cleric casts imbue with spell ability upon another character, the cleric loses that particular spell from his or her repertoire and cannot memorize more spells until the recipient uses all of the spells that were transferred. The material components for this spell are the cleric's holy/unholy symbol, plus some minor item \"borrowed\" from the intended recipient which is symbolic of his or her profession (a lockpick for a thief, a dagger for an assassin, etc.). The \"borrowed\" item is consumed in the casting of the spell."
        )
    ),
    Spell('Lower Water','C',4,
        cast=tp(1,T),
        duration=tp(0),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="The cleric casting a lower water spell causes water or similar fluid in the area of effect to sink away. Lowering is 5% of original effect for every level of experience of the cleric, i.e. 40% at 8th level, 45% at 9th, 50% at 10th, etc. The effect of the spell lasts for 1 turn for each level of experience of the cleric casting it. Likewise, the area of effect increases by level of experience, an 8th level cleric affecting an area of 8\" x 8\", a 9th level an area of 9\" x 9\", and so forth. Material components of this spell are the cleric's religious symbol and a pinch of dust. The reverse of the spell causes the water or similar fluid to return to its normal highest level, plus one foot for every level of experience of the cleric casting it."
    ),
    Spell('Neutralize Poison','C',4,
        cast=tp(7,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="By means of a Neutralize Poison spell, the cleric detoxifies any sort of venom in the creature or substance touched. Note that an opponent, such as a poisonous reptile or snake (or even an envenomed weapon of an opponent) unwilling to be so touched requires the cleric to score a hit in melee combat. Effects of the spell are permanent only with respect to poison existing in the touched creature at the time of the touch, i.e. creatures (or objects) which generate new poison will not be permanently detoxified. The reversed spell, Poison, likewise requires an attack (a \"to hit\" touch which succeeds), and the victim is allowed a saving throw versus poison. If the latter is unsuccessful, the victim is killed by the poison."
    ),
    Spell('Protection From Evil 10\' Radius','C',4,
        cast=tp(7,S),
        duration=tp(0,R),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="The globe of protection of this spell is identical in all respects to a Protection From Evil (q.v.) spell except that it encompasses a much larger area and the duration of the Protection From Evil, 10' Radius spell is greater. To complete this spell, the cleric must trace a circle 20' in diameter using holy water or blood, incense or smouldering dung as according to the Protection From Evil spell."
    ),
    Spell('Speak With Plants','C',4,
        cast=tp(1,T),
        duration=tp(0),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="When cast, a Speak With Plants spell enables the cleric to converse, in very rudimentary terms, with all sorts of living vegetables. Thus, the cleric can question plants as to whether or not creatures have passed through them, cause thickets to part to enable easy passage, require vines to entangle pursuers, and similar things. The spell does not enable the cleric to animate non-ambulatory vegetation. The power of the spell lasts for 1 melee round for each level of experience of the cleric who cast it. All vegetation within the area of effect are under command of the spell. The material components for this spell are a drop of water, a pinch of dung, and a flame."
    ),
    Spell('Spell Immunity','C',4,
        cast=tp(1,R),
        duration_lvl=tp(1,T),
        sourcebook=U,
        desc="By means of this spell, the cleric or any creature touched is made immune to the effects of a specified spell of 4th level or lower that the cleric has directly experienced. For instance, if the cleric has been hit by a fireball spell at some time, then this spell can be used to protect someone from the effect of a fireball. This spell cannot affect an intended recipient who is already magically protected by a spell or another temporary effect. The magic of this spell will only protect against actual cast spells, not against effects of magic items or a creature's innate spell-like abilities, but immunity lasts for the full duration of the spell. Only one spell immunity can be in effect upon a single creature at one time; any applications subsequent to the first have no effect until the first duration ends. The spell immunity does not extend to items carried by the recipient, which must still make saving throws (if applicable) to avoid damage. Only a particular spell can be protected against, not a certain class of spells or a group of spells which are similar in effect; thus, someone given immunity from lightning bolt spells would still be vulnerable to a shocking grasp. The material component for spell immunity is the same (if any) as for the spell to be protected against."
    ),
    Spell('Spike Growth','C',4,
        cast=tp(7,S),
        duration=tp(1,VA),
        duration_lvl=tp(1,T),
        sourcebook=U,
        desc="Wherever any sort of plant growth of moderate size or density is found, this spell is of service. It enables the caster to cause ground-covering vegetation and/or roots and rootlets to become very hard and sharply pointed. In effect the groud cover, while appearing to be unchanged, acts as if the area were strewn with caltrops. In areas of bare ground or earthen pits, roots and rootlets will act in the same way. Without the use of a spell such as true seeing, similar magical aids, or some other special means of detection (such as detect traps), an area affected by spike growth is absolutely undetectable as such until a victim enters the area and takes damage. Even then, the creature will not be able to determine the extent of the perilous area unless some means of magical detection is used. For each 1\" of movement through the area, a victim will incur 2 \"attacks\" from the spike growth. Hit probability is as if the caster of the spell were making an attack, and any successful hit causes 1-4 points of damage. Spells which control or harm vegetation, or a dispel magic spell, will negate the area of the dweomer. The components for this spell are the cleric's holy symbol plus either seven sharp thorns or seven small twigs, each sharpened to a point."
    ),
    Spell('Sticks to Snakes','C',4,
        cast=tp(7,S),
        duration=tp(0),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="By means of this spell the cleric is able to change 1 stick to a snake for each level of experience he or she has attained, i.e. a 9th level cleric can change 9 sticks into 9 snakes. These snakes will attack as commanded by the cleric. There must, of course, be sticks or similar pieces of wood (such as torches, spears, etc.) to turn into snakes. Note that magical items such as staves and spears which are enchanted are not affected by the spell. Only sticks within the area of effect will be changed. The probability of a snake thus changed being venomous is 5% per level of experience of the spell caster, so that there is a 55% probability of any given snake created by the spell being poisonous when sticks are turned to snakes by an 11th level cleric, 60% at 12th level, etc. The effect lasts for 2 melee rounds for each level of experience of the spell caster. The material components of the spell are a small piece of bark and several snake scales. The reverse changes snakes to sticks for the duration appropriate, or it negates the Sticks To Snakes spell according to the level of the cleric countering the spell, i.e. a 10th level cleric casting the reverse spell can turn only 10 snakes back to sticks."
    ),
    Spell('Tongues','C',4,
        cast=tp(7,S),
        duration=tp(1,T),
        sourcebook=V,
        desc="This spell enables the cleric to speak the language of any creature inside the spell area, whether it is a racial tongue or an alignment language. The reverse of the spell cancels the effect of the Tongues spell or confuses verbal communication of any sort within the area of effect."
    ),
    Spell('Air Walk','C',5,
        cast=tp(1,S),
        duration=tp(6,T),
        duration_lvl=tp(1,T),
        sourcebook=U,
        desc="The spell enables the cleric to tread upon air just as if it were solid ground. Moving upward is similar to walking up a hill, and the more steep the ascent, the slower the rate of movement: Ascending at a 45° angle is done at one-half normal movement, a 60° angle reduces movement to one-fourth of normal, and traveling straight upward can be done at one-eighth the normal rate. Similarly, rapid descent is possible, almost as if the cleric were running downhill; invert the above proportions, so that traveling straight downward can be done at eight times the normal movement rate (or, of course, at any slower rate the traveller desires). An air walking creature is always in control of his or her own movement rate; someone traveling straight down at a rapid rate can \"stop on a copper piece\" to avoid crashing into the ground or some other solid object. Someone attempting to air walk while a gust of wind spell is in effect in the same area will move at one-half the usual rate if going into the gust, or twice the usual rate if traveling in the same direction. The spell can be placed upon any creature touched, up to and including one of giant size. For example, the caster could place the spell upon a trained horse and ride it through the air. Of course, an animal not accustomed to such movement would panic, so the steed would certainly need careful and lengthy training. The material components for the spell are the cleric's holy/unholy symbol and a bit of thistledown."
    ),
    Spell('Animate Dead Monsters','C',5,
        cast=tp(7,S),
        duration=tp(1,P),
        sourcebook=U,
        desc="This spell enables the caster to animate 1 humanoid or semi-humanoid skeleton or corpse for every 2 levels of experience which he or she has attained. The dweomer animates the remains and empoweres the caster to give commands. Direct commands or instructions of up to about 12 words in length will be obeyed by the skeletons or zombies animated (cf. animate dead spell). Monster types which can be animated by this spell include but are not limited to: apes (carnivorous and giant), bugbears, ettins, giants (all varieties), ogres, and trolls (all varieties). In general, the remains must be of bipedal monsters of more than 3 hit dice and with endoskeletons similar to those of humans, except in size (which must be greater than 7' height). Corpses animated by this spell are treated either as monster zombies (see Monster Manual II), or else as normal (living) creatures of the same form if that creature type normally has less than 6 hit dice. Skeletons animated by this spell are treated as monsters of half the hit dice (rounded up) of the normal sort. Animated monsters of either type receive their normal physical attacks, but have no special attacks or defenses other than those typically possessed by monster zombies or skeletons. The material components for the spell are the cleric's holy/unholy symbol and a small specimen of the type of creature which is to be animated."
    ),
    Spell('Atonement','C',5,
        cast=tp(1,T),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell is used by the cleric to remove the onus of unwilling or unknown deeds from the person who is the subject of the Atonement The spell will remove the effects of magical alignment change as well. The person for whom Atonement is being made must be either truly repentant or not in command of his or her own will so as to be able to be repentant. Your referee will judge this spell in this regard, noting any past instances of its use upon the person. Deliberate misdeeds and acts of knowing and wilful nature cannot be atoned for with this spell. The material components of this spell are the cleric's religious symbol, prayer beads or wheel or book, and burning incense."
    ),
    Spell('Commune','C',5,
        cast=tp(1,T),
        duration=tp(0),
        sourcebook=V,
        desc="By use of a Commune spell the cleric is able to contact his or her divinity - or agents thereof - and request information in the form of questions which can be answered by a simple \"yes\" or \"no\". The cleric is allowed one such question for every level of experience he or she has attained. The answers given will be correct. It is probable that the referee will limit the use of Commune spells to one per adventure, one per week, or even one per month, for the \"gods\" dislike frequent interruptions. The material components necessary to a Commune spell are the cleric's religious symbol, holy/unholy water, and incense."
    ),
    Spell('Cure Critical Wounds','C',5,
        cast=tp(8,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="The Cure Critical Wounds spell is a very potent version of the Cure Light Wounds spell (q.v.). The cleric lays his or her hand upon a creature and heals from 6 to 27 (3d8+3) hit points of damage from wounds or other damage. The spell does not affect creatures excluded in the Cure Light Wounds spell explanation. Its reverse, Cause Critical Wounds, operates in the same fashion as other Cause Wounds spells, requiring a successful touch to inflict the 6-27 hit points of damage. Caused wounds heal as do wounds of other sorts."
    ),
    Spell('Dispel Evil','C',5,
        cast=tp(8,S),
        duration=tp(1,R),
        sourcebook=V,
        desc="The cleric using this spell causes summoned creatures of evil nature, or monsters enchanted and caused to perform evil deeds, to return to their own plane or place. Examples of such creatures are: aerial servants, demons, devils, djinn, efreet, elementals, and invisible stalkers. Note that this spell lasts for 1 melee round for each level of experience of the caster, and while the spell is in effect all creatures which could be affected by it attack at a -7 penalty' on their \"to hit\" dice when engaging the spell caster. The reverse of the spell, Dispel Good, functions against summoned or enchanted creatures of good alignment or sent to aid the cause of good. The material components for this spell are the cleric's religious object and holy/unholy water."
    ),
    Spell('Flame Strike','C',5,
        cast=tp(8,S),
        duration=tp(1,S),
        sourcebook=V,
        desc="When the cleric calls down a Flame Strike spell, a column of fire roars downward in the exact location called for by the caster. If any creature is within the area of effect of a Flame Strike, it must make a saving throw. Failure to make the save means the creature has sustained 6-48 (6d8) hit points of damage; otherwise, 3-24 (3d8) hit points of damage are taken. The material component of this spell is a pinch of sulphur."
    ),
    Spell('Golem','C',5,
        cast=tp(8,S),
        duration=tp(1,VA),
        sourcebook=U,
        desc=("In order for this spell to operate, the cleric must first construct the form of the golem to be made. The cleric must do this personally and then place a prayer spell upon the construction. All golems must be man-shaped and approximately man-sized, although they can be as small as 3' or as large as 7' tall. The sort of golem that can be created depends on the material used and the level of the cleric:\n\n"
            "At 9th or higher level, the cleric can create a straw golem. Construction time is 1 hour, duration thereafter is 1 hour per level. The golem has AC 10, MV 12\", HD 2+4, hp 20, #AT 2, D 1-2/1-2, SD immune to piercing weapons, half damage from blunt weapons. Carrying capacity is 30 pounds. The golem is highly susceptible to flame (taking double normal damage).\n\n"
            "At 11th and higher level, the cleric can create a rope golem. Construction time is 3 hours, duration thereafter is 3 hours per level. The golem has AC 8, MV 9\", HD 3+6, hp 30, #AT 1, D 1-6 plus strangulation (6 points per round after scoring a hit until destroyed or caused to release its grip), SD immune to blunt weapons, half damage from piercing weapons. Carrying capacity is 40 pounds.\n\n"
            "At 13th and higher level, the cleric can create a leather golem. Construction time is 9 hours, duration thereafter is 6 hours per level. The golem has AC 6, MV 6\", HD 4+8, hp 40, #AT 2, D 1-6/1-6, SD +1 or better magic weapon to hit, half damage from blunt weapons. Carrying capacity is 50 pounds.\n\n"
            "At 15th or higher level, the cleric can create a wood golem. Construction time is 27 hours, duration thereafter is 12 hours per level. The golem has AC 4, MV 3\", HD 5+10, hp 50, #AT 1, D 3-12, SD +1 or better magic weapon to hit, immune to blunt and piercing weapons. Carrying capacity is 60 pounds.\n\n"
            "These creations are collectively known as lesser golems to distinguish them from the golems described in the Monster Manual. Similar to their namesakes, these golems have no minds, so spells such as charm, fear, hold, sleep, and the like have no effect on them. The dweomer of the lesser golem enables it to save as if it were a cleric of the same experience level as the one who created it. These golems cannot speak, but they can comprehend and carry out simple instructions involving no more than a dozen words."
        )
    ),
    Spell('Insect Plague','C',5,
        cast=tp(1,T),
        duration=tp(0),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="When this spell is cast by the cleric, a horde of creeping, hopping, and flying insects swarm in a thick cloud. These insects obscure vision, limiting it to 3\". Creatures within the insect plague sustain 1 hit point of damage for each melee round they remain in it due to the bites and stings of the insects, regardless of armour class. The referee will cause all creatures with fewer than five hit dice to check morale. Creatures with two or fewer hit dice will automatically move at their fastest possible speed in a straight line in a random direction until they are not less than 24\" distant from the cloud of insects. Creatures with fewer than five hit dice which fail their morale check will behave likewise. Heavy smoke will drive off insects within its bounds. Fire will also drive insects away; a Wall of Fire in a ring shape will keep the Insect Plague outside its confines, but a Fireball will simply clear insects from its blast area for 1 turn. Lightning and cold/ice act likewise. The plague lasts for 1 turn for each level of experience of the cleric casting the spell, and thereafter the insects disperse. The insects swarm in an area which centres around a summoning point determined by the spell caster, which point can be up to 36\" distant from the cleric. The Insect Plague does not move thereafter for as long as it lasts. Note that the spell can be countered by casting a Dispel Magic upon the summoning point. A cube of force (a special magic item) would keep insects away from a character seeking the centre of the swarm, but invisibility would afford no protection. The material components of this spell area few grains of sugar, some kernels of grain, and a smear of fat."
    ),
    Spell('Magic Font','C',5,
        cast=tp(5,T),
        duration=tp(1,VA),
        sourcebook=U,
        desc="This spell causes a holy/unholy water font to serve as a scrying device. The spell will not function unless the cleric is in good standing with his or her deity. The basin of holy/unholy water becomes similar to a crystal ball (see Dungeon Masters Guide, Miscellaneous Magic Treasure section, under crystal ball). For each vial of capacity of the basin of the font, the cleric may scry for 1 round; thus, the duration of the magic font spell is directly related to the size of the holy/unholy water receptacle. For the chances of a character being able to detect scrying, see the crystal ball description in the Dungeon Masters Guide and the text for the magic-user spell magic mirror herein. The material components for this spell, the cleric's holy/unholy symbol and the font and its trappings, are not exhausted by the use of the spell."
    ),
    Spell('Plane Shift','C',5,
        cast=tp(8,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="When the Plane Shift spell is cast, the cleric moves himself or herself or some other creature to another plane of existence. The recipient of the spell will remain in the new plane until sent forth by some like means. If several persons link hands in a circle, up to seven can be affected by the Plane Shift at the same time. The material component of this spell is a small, forked metal rod - the exact size and metal type dictating to which plane of existence the spell will send the affected creature(s) to. (Your referee will determine specifics regarding how and what planes are reached.) An unwilling victim must be touched in order to be sent thusly: and in addition, the creature also is allowed a saving throw, and if the latter is successful the effect of the spell is negated."
    ),
    Spell('Quest','C',5,
        cast=tp(8,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="The Quest is a spell by means of which the cleric requires the affected creature to perform a service and return to the cleric with proof that the deed was accomplished. The Quest can, for example, require the location and return of some important or valuable object, the rescue of a notable person, the release of some creature, the capture of a stronghold, the slaying of a person, the delivery of some item, and so forth. If the Quest is not properly followed due to disregard, delay, or perversion, the creature affected by the spell loses 1 from its saving throw dice for each day of such action, and this penalty will not be removed until the Quest is properly discharged or the cleric cancels it. (There are certain circumstances which will temporarily suspend a Quest, and other which will discharge or cancel it; your Dungeon Master will give you appropriate information as the need to know arises.) The material component of this spell is the cleric's religious symbol."
    ),
    Spell('Rainbow','C',5,
        cast=tp(7,S),
        duration_lvl=tp(1,R),
        sourcebook=U,
        desc=("In order to effect this spell, the cleric must be in sight of a rainbow of any sort, or have a special component (see below). The rainbow spell has four applications, and the cleric is able to decide which one is desired at the time of casting. These applications are:\n\n"
            "Bow: The spell creates a shimmering, multi-layered bow of rainbow hues. It is light and easy to pull, so that anyone with a strength of 6 or better can use it. It is magic, each of its missiles being equal to a +3 weapon, and there is no non-proficiency penalty for its use. However, it can only be employed by a member of a character class permitted to use a bow. The bow will fire 7 missiles before disappearing. It fires once or twice per round, according to the user's desire. Each time a missile is fired, one hue leaves the bow, corresponding to the color of arrow that is released. Each color of arrow has the ability to cause double damage to certain creatures, as follows:\n"
            "Red — fire dwellers/users\n"
            "Orange — earth elementals\n"
            "Yellow — vegetable targets (including fungus creatures, shambling mounds, treants, etc.)\n"
            "Green — aquatic creatures and water elementals\n"
            "Blue — aerial creatures, electricity-using creatures, and air elementals\n"
            "Indigo — acid-usigng or poison-using creatures\n"
            "Violet — metallic or regenerating creatures\n"
            "When the bow is drawn, an arrow of the appropriate color magically appears, nocked and ready. If no color is requested, or a color that has already been used is asked for, then the next arrow (in the order of the spectrum) will appear.\n\n"
            "Bridge: The caster causes the rainbow to form a seven-hued bridge. The bridge is as many feet wide as the cleric has levels of experience, and it can bear as much weight, in hundreds of pounds, as the cleric has levels of experience. It will be at least 20' long and can be as long as 120', according to the desire of the caster. If the bridge's weight limit is exceeded at any time, the bridge will simply disappear into nothingness; otherwise it will last for the length of the spell duration or until ordered out of existence by the caster.\n\n"
            "Elevator: When desired, the caster can cause the rainbow to life his or her person, and all those within a 10' radius, skyward. The effect is to carry the cleric and others, if any, in a path arching upward to as high an altitude as the cleric desires, and then down again if desired. Care must be taken to reach a place of safety before the spell duration expires, or the rainbow elevator will disappear, leaving those treading upon it with no means of support. Movement along the rainbow elevator is at a rate of 12\", and the arc of the rainbow trails out 12\" behind those traveling upon it.\n\n"
            "Flagon: When used in this form, the rainbow swirls and condenses into a seven-colored vessel which contains seven measures of pure water. Each time a measure of the water is poured out, one of the hues of the container mixes with it to produce a magical draught. Any measures of the liquid that remain unused at the expiration of the spell duration will disappear, along with the container itself, whether the contents have been poured from the flagon or not. The draughts and their effects are:\n"
            "Red — cure light wounds\n"
            "Orange — resist fire\n"
            "Yellow — cure blindness\n"
            "Green — slow poison\n"
            "Blue — cure disease\n"
            "Indigo — resist cold\n"
            "Violet — remove paralysis\n"
            "The effects of each draught consumed will be as if the appropriate spell had been cast by a cleric of 12th level, and these effects will persist after the duration of the spell expires.\n\n"
            "The components for this spell are the cleric's holy/unholy symbol and a vial of holy/unholy water. If no rainbow is in the vicinity, the cleric can substitute a diamond of not less than 1,000 gp value, specifically prepared by him or her when in sight of a rainbow by the casting of bless and prayer spells upon the gem. Only the holy symbol remains after the spell is cast."
        )
    ),
    Spell('Raise Dead','C',5,
        cast=tp(1,R),
        duration=tp(1,P),
        sourcebook=V,
        desc="When the cleric casts a raise dead spell, he or she can restore life to a dwarf, gnome, half-elf, halfling, or human. The length of time which the person has been dead is of importance, as the cleric can raise dead persons only up to a certain point, the limit being 1 day for each level of experience of the cleric, i.e. a 9th level cleric can raise a person dead for up to 9 days. Note that the body of the person must be whole, or otherwise missing parts will still be missing when the person is brought back to life. Also, the resurrected person must make a special saving throw to survive the ordeal (see CHARACTER ABILITIES, Constitution). Furthermore, the raised person is weak and helpless in any event, and he or she will need one full day of rest in bed for each day he or she was dead. The somatic component of the spell is a pointed finger. The reverse of the spell, Slay L living, allows the victim a saving throw, and if it is successful, the victim sustains damage equal only to that caused by a Cause Serious Wounds spell. i.e. 3-17 hit points. An evil cleric can freely use the reverse spell; a good cleric must exercise extreme caution in its employment, being absolutely certain that the victim of the Slay Living spell is evil and that his or her death is a matter of great necessity and for good, otherwise the alignment of the cleric will be sharply changed. Note that newly made undead, excluding skeletons, which fall within the days of being dead limit are affected by Raise Dead spells cast upon them. The effect of the spell is to cause them to become resurrected dead, providing the constitution permits survival; otherwise, they are simply dead."
    ),
    Spell('Spike Stones','C',5,
        cast=tp(6,S),
        duration=tp(1,VA),
        duration_lvl=tp(1,T),
        sourcebook=U,
        desc="The spike stones spell causes rock to shape itself into long, sharp points which tend to blend into the background. It is effective on both natural rock and worked stone. The spike stones serve to impede progress through an area or actually inflict damage. If an area is carefully observed, each observer is 25% likely to notice the sharp points of rock. Otherwise, those entering the area of effect of the spell will suffer 1-4 points of damage from each spike stone that hits, success of such attacks determined as if the caster of the spell were actually engaging in combat. Those entering the area are subject to attack immediately upon setting foot in the area and upon each step taken therein afterward. The initial step will be sufficient to allow the individual to become aware of some problem only if the initial attack succeeds; otherwise movement will continue and the spike stones will remain unnoticed until damage occurs. Charging or running victims will suffer 2 attacks per 1\" of movement rate over the area of effect after initial damage is taken before being able to halt. Others will suffer but 1 additional attack-like check. Those falling into pits so affected by spike stones will suffer 6 such attack-like checks, each made at +2 probability \"to hit\" for each 10' of distance fallen, and +2 on damage inflicted per 10' distance fallen, spike damage being in addition to falling damage. The material component of this spell is four tiny stalactites."
    ),
    Spell('True Seeing','C',5,
        cast=tp(8,S),
        duration=tp(0),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="When the cleric employs this spell, all things within the area of the True Seeing effect appear as they actually are. Secret doors become plain. The exact location of displaced things is obvious. Invisible things and those which are astral or ethereal become quite visible. Illusions and apparitions are seen through. Polymorphed, changed, or magicked things are apparent. Even the aura projected by creatures becomes visible, so that the cleric is able to know whether they are good or evil or between. The spell requires an ointment for the eyes. The ointment is made from very rare mushroom powder, saffron, and fat. The reverse of the spell, False Seeing, causes the person to see things as they are not, rich being poor, rough smooth, beautiful ugly. The ointment for the reverse spell is concocted of oil, poppy dust, and pink orchid essence. For both spells, the ointment must be aged for 1-6 months."
    ),
    Spell('Aerial Servant','C',6,
        cast=tp(9,S),
        duration=tp(0),
        duration_lvl=tp(1,D),
        sourcebook=V,
        desc="This spell summons an invisible Aerial Servant (see ADVANCED DUNGEONS & DRAGONS, MONSTER MANUAL) to do the bidding of the cleric who conjured it. The creature does not fight, but it obeys the command of the cleric with respect to finding and returning with whatever object or creature that is described to it. Of course, the object or creature must be such as to allow the aerial servant to physically bring it to the cleric or his or her assign. The spell caster should keep in mind the consequences of having an aerial servant prevented, for any reason, from completion of the assigned duty. The spell lasts for a maximum of 1 day for each level of experience of the cleric who cast it. The aerial servant returns to its own plane whenever the spell lapses, its duty is fulfilled, it is dispelled, the cleric releases it, or the cleric is slain. The cleric must have a Protection From Evil spell, or be within a magic circle, thaumaturgic triangle, or pentagram when summoning an aerial servant unless the cleric has his or her religious symbol or a religious artifact or relic to use to control the creature. Otherwise, the creature will slay its summoner and return from whence it came. The aerial servant will always attack by complete surprise when sent on a mission, and gain the benefit of 4 free melee rounds unless the creature involved is able to detect invisible objects, in which case a six-sided die is rolled, and 1 = 1 free round, 2 = 2 free rounds, 3 = 3 free rounds, 4 = 4 free rounds, and 5 or 6 = 0 free rounds (the opponent is not surprised at all). Each round the aerial servant must dice to score a hit, and when a hit is scored, it means the aerial servant has grabbed the item or creature it was sent to take and bring back to the cleric. If a creature is involved, the aerial servant's strength is compared to the strength of the creature to be brought. If the creature in question does not have a strength rating, roll the appropriate number of the correct type of hit dice for the aerial servant and for the creature it has grabbed. The higher total is the stronger."
    ),
    Spell('Animate Object','C',6,
        cast=tp(9,S),
        duration=tp(0),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This powerful spell enables the cleric casting it to imbue inanimate objects with mobility and a semblance of life. The animated object, or objects, then attack whomever or whatever the cleric first designates. The object can be of any material whatsoever - wood, metal, stone, fabric, leather, ceramic, glass, etc. The speed of movement of the object is dependent upon its means of propulsion and its weight. A large wooden table would be rather heavy, but its legs would give it speed. A rug could only slither along. A jar would roll. Thus a large stone pedestal would rock forward at 1\" per round, a stone statue would move at 4\" per round, a wooden statue 8\" per round, an ivory stool of light weight would move at 12\". Slithering movement is about 1\" to 2\" per round, rolling 3\" to 6\" per round. The damage caused by the attack of an animated object is dependent upon its form and composition. Light, supple objects can only obscure vision, obstruct movement, bind, trip. smother, etc. Light, hard objects can fall upon or otherwise strike for 1-2 hit points of damage or possibly obstruct and trip as do light, supple objects. Hard, medium weight objects can crush or strike for 2-8 hit points of damage, those larger and heavier doing 3-12, 4-16, or even 5-20 hit points of damage. The frequency of attack of animated objects is dependent upon their method of locomotion, appendages, and method of attack. This varies from as seldom as once every five melee rounds to as frequently as once per melee round. The armour class of the object animated is basically a function of material and movement ability with regard to hitting. Damage is dependent upon the type of weapon and the object struck. A sharp cutting weapon is effective against fabric, leather, wood and like substances. Heavy smashing and crushing weapons are useful against wood, stone, and metal objects. Your referee will determine all of these factors, as well as how much damage the animated object can sustain before being destroyed. The cleric can animate 1 cubic foot of material for each level of experience he or she has attained. Thus, a 14th level cleric could animate one or more objects whose solid volume did not exceed 14 cubic feet, i.e. a large statue, two rugs, three chairs, or a dozen average crocks."
    ),
    Spell('Blade Barrier','C',6,
        cast=tp(9,S),
        duration=tp(0),
        duration_lvl=tp(3,R),
        sourcebook=V,
        desc="The cleric employs this spell to set up a wall of circling, razor-sharp blades. These whirl and flash in endless movement around an immobile point. Any creature which attempts to pass through the Blade Barrier suffers 8-64 (8d8) hit points of damage in doing so. The barrier remains for 3 melee rounds for every level of experience of the cleric casting it. The barrier can cover any area from as small as 5' square to as large as 2\" square, i.e. 20'x20' under ground, 60'x60' outdoors."
    ),
    Spell('Conjure Animals','C',6,
        cast=tp(9,S),
        duration=tp(0),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="The Conjure Animals spell enables the cleric to summon a mammal, or several of them, to his locale in order that the creature(s) can attack the cleric's opponents. The conjured animal(s) remain in the cleric's locale for 2 melee rounds for each level of experience of the cleric conjuring it (them), or until slain. The spell caster can, by means of his incantation, call up one or more mammals with hit dice whose total does not exceed his or her level. Thus, a cleric of 12th level could conjure one mammal with 12 hit dice, two with 6 hit dice each, three with 4 hit dice each, 4 with a hit dice each, six with 2 hit dice each, or 12 with 1 hit die each. For every +1 (hit point) of a creature's hit dice, count 1/4 of a hit die, i.e. a creature with 4+3 hit dice equals a 4¾ hit dice creature. The creature(s) summoned by the spell will unfailingly attack the opponent(s) of the cleric by whom the spell was cast."
    ),
    Spell('Find The Path','C',6,
        cast=tp(3,R),
        duration=tp(0),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="By use of this spell, the cleric is enabled to find the shortest, most direct route that he or she is seeking, be it the way to or from or out of a locale. The locale can be outdoors or underground, a trap or even a maze spell. The spell will enable the cleric to select the correct direction which will eventually lead him or her to egress, the exact path to follow (or actions to take), and this knowledge will persist as long as the spell lasts, i.e. 1 turn for each level of experience of the cleric casting find the path. The spell frees the cleric, and those with him or her from a Maze spell in a single melee round and will continue to do so as long as the spell lasts. The material component of this spell is a set of divination counters of the sort favoured by the cleric - bones, ivory counters, sticks, carved runes, or whatever. The reverse, Lose The Path, makes the creature touched totally lost and unable to find its way for the duration of the spell, although it can be led, of course."
    ),
    Spell('Forbiddance','C',6,
        cast=tp(6,R),
        duration=tp(1,P),
        sourcebook=U,
        desc=("This spell can be used only to secure a consecrated area (cf. ceremony spell). The effect on the enchanted area is based on the ethics (law/chaos) and morals (good/evil) of those trying to enter it, relative to the caster's.\n\n"
            "Identical morals and ethics: Cannot enter area unless password is known (no saving throw).\n\n"
            "Different ethics: Save versus spell to enter the area; if failed, take 2-12 points of damage.\n\n"
            "Different morals: Save versus spell to enter the area; if failed, take 4-24 points of damage.\n\n"
            "Once a saving throw is failed, a intruder can never enter the forbidden area until the dweomer ceases. Effects are cumulative, and multiple required saving throws are certainly possible. The caster is immune to the spell's effect. Intruders who enter by making saving throws will feel uneasy and tense, despite their success. In addition to the cleric's holy/unholy symbols, components include holy/unholy water, silver/dung, and iron/sulfur."

        )
    ),
    Spell('Heal','C',6,
        cast=tp(1,R),
        duration=tp(1,P),
        sourcebook=V,
        desc="The very potent Heal spell enables the cleric to wipe away disease and injury in the creature who receives the benefits of the spell. It will completely cure any and all diseases and/or blindness of the recipient and heal all hit points of damage suffered due to wounds or injury, save 1 to 4 (d4). It dispels a Feeblemind spell. Naturally, the effects can be negated by later wounds, injuries, and diseases. The reverse, Harm, infects the victim with a disease and causes loss of all hit points, as damage, save 1 to 4 (d4), if a successful touch is inflicted. For creatures not affected by the Heal (or Harm) spell, see Cure Light Wounds."
    ),
    Spell('Heroes\' Feast','C',6,
        cast=tp(1,T),
        duration=tp(1,H),
        sourcebook=U,
        desc="This special dweomer enables the cleric to bring forth a great feast which will serve as many creatures as the cleric has levels of experience. The spell creates a magnificent table, chairs, service, and all the necessary food and drink. Those partaking of the feast are cured of all diseases, are immune to poison for 12 hours, and healed of 5-8 points of damage after imbibing the nectar-like beverage which is part of the feast. The ambrosia-like food that is consumed is equal to a bless spell that lasts for 12 hours. Also, during this period, the persons who consumed the feast are immune to fear, hopelessness, and panic. The feast takes one full hour to consume, and the beneficial effects do not set in until after this hour is over. If the feast is interrupted for any reason, the spell is ruined and all effects of the dweomer are negated. The material components of the spell are the cleric's holy/unholy symbol and specially fermented honey taken from the cells of bee larvae destined for royal status."
    ),
    Spell('Part Water','C',6,
        cast=tp(1,T),
        duration=tp(0),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="By employing a Part Water spell, the cleric is able to cause water or similar liquid to move apart. thus forming a trough. The depth and length of the trough created by the spell is dependent upon the level of the cleric, and a trough 3' deep by 1' by 1\" (10' or 10 yards) is created per level, i.e. at 12th level the cleric would part water 36' deep by 12' wide by 24\" (240' or 240 yards) long. The trough will remain as long as the spell lasts or until the cleric who cast it opts to end its effects (cf. Dispel Magic). The material component of this spell is the cleric's religious symbol."
    ),
    Spell('Speak With Monsters','C',6,
        cast=tp(9,S),
        duration=tp(0),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="When cast, the Speak With Monsters spell allows the cleric to converse with any type of creature which has any form of communicative ability. That is, the monster will understand the intent of what is said to it by the cleric. The creature or creatures thus spoken to will be checked by your referee in order to determine reaction. All creatures of the same type as that chosen by the cleric to speak to can likewise understand if they are within range. The spell lasts for 1 melee round per level of experience of the cleric casting it. and during its duration conversation can take place as the monster is able and desires."
    ),
    Spell('Stone Tell','C',6,
        cast=tp(1,T),
        duration=tp(1,T),
        sourcebook=V,
        desc="When the cleric casts a Stone Tell upon an area, the very stones will speak and relate to the caster who or what has touched them as well as telling what is covered, concealed, or simply behind the place they are. The stones will relate complete descriptions as required. The material components for this spell area drop of mercury and a bit of clay."
    ),
    Spell('Word of Recall','C',6,
        cast=tp(1,S),
        duration=tp(0),
        sourcebook=V,
        desc="The Word Of Recall spell takes the cleric instantly back to his or her sanctuary when the word is uttered. The sanctuary must be specifically designated in advance by the cleric. It must be a well known place, but it can be any distance from the cleric, above or below ground. Transportation by the Word Of Recall spell is infallibly safe. The cleric is able to transport, in addition to himself or herself, 250 gold pieces weight cumulative per level of experience. Thus, a 15th level cleric could transport his or her person and 3,750 (375 pounds) gold pieces weight in addition; this extra matter can be equipment, treasure, or living material such as another person."
    ),
    Spell('Astral Spell','C',7,
        cast=tp(3,T),
        duration=tp(0),
        sourcebook=V,
        desc="By means of the Astral Spell a cleric is able to project his or her astral body into the Astral Plane, leaving his or her physical body and material possessions behind on the Prime Material Plane, (the plane on which the entire universe and all of its parallels have existence). Only certain magic items which have multi-planed existence can be brought into the Astral Plane. As the Astral Plane touches upon all of the first levels of the Outer Planes, the cleric can travel astrally to any of these Outer Planes as he or she wills. The cleric then leaves the Astral Plane, forming a body on the plane of existence he or she has chosen to enter. It is also possible to travel astrally anywhere in the Prime Material Plane by means of the Astral Spell, but a second body cannot be formed on the Prime Material Plane. As a general rule, a person astrally projected can be seen only by creatures on the Astral Plane. At all times the astral body is connected to the material by a silvery cord. If the cord is broken, the affected person is killed, astrally and materially, but generally only the psychic wind can normally cause the cord to break. When a second body is formed on a different plane. the silvery cord remains invisibly attached to the new body, and the cord simply returns to the latter where it rests on the Prime Material Plane, reviving it from its state of suspended animation. Although astrally projected persons are able to function on the Astral Plane, their actions do not affect creatures not existing on the Astral Plane. The spell lasts until the cleric desires to end it, or until it is terminated by some outside means (Dispel Magic or destruction of the cleric's body on the Prime Material Plane). The cleric can take up to five other creatures with him or her by means of the Astral Spell, providing the creatures are linked in a circle with the cleric. These fellow travellers are dependent upon the cleric and can be stranded. Travel in the Astral Plane can be slow or fast according to the cleric's desire. The ultimate destination arrived at is subject to the conceptualization of the cleric. (See APPENDIX IV, THE KNOWN PLANES OF EXISTENCE, for further information on the Astral Plane and astral projection.)"
    ),
    Spell('Control Weather','C',7,
        cast=tp(1,T),
        duration=tp(1,VA),
        sourcebook=V
    ),
    Spell('Earthquake','C',7,
        cast=tp(1,T),
        duration=tp(1,R),
        sourcebook=V
    ),
    Spell('Exaction','C',7,
        cast=tp(1,R),
        duration=tp(1,VA),
        sourcebook=U,
        desc="When this spell is employed, the cleric confronts some powerful creature from another plane (including devas and powerful \"name\" demons, for instance, but not demigods or deities of any sort) and requires of it some duty or quest. The creature may not be one ethically or morally opposed to the cleric (i.e. not evil if the cleric is good, not chaotic if the cleric is lawful). Note that an absolute (true) neutral creature is in effect greatly opposed to both good and evil, and both law and chaos. The spell caster must know something about the creature to exact service from it, or else he or she must offer some fair trade in return for the service. That is, if the cleric is aware that the creature has received some favor from someone of the cleric's alignment, then the exaction can name this as cause; if no balancing reason for service is known, then some valuable gift or service must be pledged in return for the exaction. The service exacted must be reasonable with respect to the past or promised favor or reward. The spell then acts as a quest upon the creature which is to perform the required service. Immediately upon completion of the service, the subject creature is transported to the vicinity of the cleric, and the cleric must then and there return the promised reward, whether it is irrevocable cancellation of a past debt or the giving of some service or other material reward. Upon so doing, the creature is instantly freed to return to its own plane. Failure to fulfill the promise to the letter results in the cleric being subject to exaction by the subject creature or by its master, liege, etc., at the very least. At worst, the creature may attack the reneging cleric without fear of any of his or her spells affecting it, for the failure to live up to the bargain gives the creature total immunity from the spell powers of the cleric so doing. The material components of this spell are the cleric's holy/unholy symbol, some matter or substance from the plane of the creature from whom an exaction is to be expected, and knowledge of the creature's nature and/or actions which is written out on a parchment leaf that is burned to seal the bargain."
    ),
    Spell('Gate','C',7,
        cast=tp(5,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="The casting of a Gate spell has two effects: first, it causes an ultra-dimensional connection between the plane of existence the cleric is an and that plane on which dwells a specific being of great power, the result enabling the being to merely step through the gate or portal, from its plane to that of the cleric; second, the utterance of the spell attracts the attention of the dweller on the other plane. When casting the spell, the cleric must name the demon, devil, demi-god, god, or similar being he or she desires to make use of the Gate and come to the cleric's aid. There is a 100% certainty that something will step through the gate. The actions of the being which comes through will depend on many factors, including the alignment of the cleric, the nature of those in company with him or her, and who or what opposes or threatens the cleric. Your Dungeon Master will have a sure method of dealing with the variables of the situation. The being gated in will either return immediately (very unlikely) or remain to take action."
    ),
    Spell('Holy (Unholy) Word','C',7,
        cast=tp(1,S),
        duration=tp(1,VA),
        sourcebook=V
    ),
    Spell('Regenerate','C',7,
        cast=tp(3,R),
        duration=tp(1,P),
        sourcebook=V,
        desc="When a Regenerate spell is cast, body members (fingers, toes, hands, feet, arms, legs, tails, or even the heads of multi-headed creatures), bones, or organs will grow back. The process of regeneration requires but 1 round if the member(s) severed is (are) present and touching the creature, 2-8 turns otherwise. The reverse, Wither, causes the member or organ touched to shrivel and cease functioning in 1 round, dropping off into dust in 2-8 turns. As is usual, creatures must be touched in order to have harmful effect occur. The material components of this spell are a prayer device and holy/unholy water."
    ),
    Spell('Restoration','C',7,
        cast=tp(3,R),
        duration=tp(1,P),
        sourcebook=V,
        desc="When this spell is cast, the life energy level of the recipient creature is raised upwards by one. This subsumes previous life energy level drain of the creature by some force or monster. Thus, if a 10th level character had been struck by a wight and drained to 9th level, the Restoration spell would bring the character up to exactly the number of experience points necessary to restore him or her to 10th level once again. and restoring additional hit dice (or hit points) and level functions accordingly. Restoration is only effective if the spell is cast within 1 day/level of experience of the cleric casting it of the recipient's loss of life energy. The reverse, Energy Drain, draws away a life energy level (cf. such \"undead\" as spectre, wight, vampire). The Energy Drain requires the victim to be touched. A Restoration spell will restore the intelligence of a creature affected by a Feeblemind spell (q.v.)."
    ),
    Spell('Resurrection','C',7,
        cast=tp(1,T),
        duration=tp(1,P),
        sourcebook=V,
        desc="The cleric employing this spell is able to restore life and complete strength to the person he/she bestows the Resurrection upon. The person can have been dead up to 10 years cumulative per level of the cleric casting the spell, i.e. a 19th level cleric can resurrect the bones of a person dead up to 190 years. See raise dead for limitations on what persons can be raised. The reverse, Destruction, causes the victim of the spell to be instantly dead and turned to dust. Destruction requires a touch, either in combat or otherwise. The material components of the spell are the cleric's religious symbol and holy/unholy water. Employment of this spell makes it impossible for the cleric to cast further spells or engage in combat until he or she has had one day of bed rest for each level of experience of the person brought back to life or destroyed."
    ),
    Spell('Succor','C',7,
        cast=tp(1,D),
        duration=tp(1,VA),
        sourcebook=U,
        desc=("By casting this spell, the cleric creates a powerful dweomer in some specially prepared object — a string of prayer beads, a small clay tablet, an ivory baton, etc. This object will radiate magic, for it contains the power to instantaneously transport its possessor to the sanctuary of the cleric who created its dweomer. Once the item is magicked, the cleric must give it willingly to an individual, at the same time informing him or her of a command word to be spoken when the item is to be used. To make use of the item, the recipient must speak the command word at the same time that he or she rends or breaks the item. When this is done, the individual and all that he or she is wearing and carrying will be instantly transported to the sanctuary of the cleric just as if the individual were capable of speaking a word of recall spell. No other creatures can be affected.\n\n"
        "The reversed application of the spell enables the cleric to be transported to the vicinity of the possessor of the dweomered item when it is broken and the command word said. The cleric can choose not to be affected by this \"summons\" by making that decision at the instant when the transportation is to take place, but if he or she so chooses, then the opportunity is gone forever and the spell is wasted. The cost of preparing the special item (for either version of the spell) varies from 2,000 to 5,000 gold pieces."
        )
    ),
    Spell('Symbol','C',7,
        cast=tp(3,S),
        duration=tp(0),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc=("The cleric casting this spell inscribes a symbol in the air or upon any surface, according to his or her wish. The symbol glows for 1 turn for each level of experience of the cleric casting it. The particular symbol used can be selected by the cleric at the time of casting, selection being limited to:\n"
            "HOPELESSNESS	- Creatures seeing it must turn back in dejection and/or surrender to capture or attack unless they save versus magic. Its effects last for 3 to 12 turns.\n"
            "PAIN	- Creatures affected suffer -4 on \"to hit\" dice and -2 on dexterity ability score due to wracking pains. The effects last for 2-20 turns.\n"
            "PERSUASION	- Creatures seeing the symbol become of the same alignment as and friendly to the cleric who scribed the symbol for from 1 to 20 turns unless a saving throw versus magic is made.\n"
            "The material components of this spell are mercury and phosphorus. (cf. eighth level magic-user symbol spell."
        )
    ),
    Spell('Wind Walk','C',7,
        cast=tp(1,R),
        duration_lvl=tp(6,T),
        sourcebook=V,
        desc="This spell enables the cleric, and possibly one or two other persons. to alter the substance of his or her body to cloud-like vapours. A magical wind then wafts the cleric along at a speed of up to 60\" per turn, or as slow as 6\" per turn, as the spell caster wills. The Wind Walk spell lasts as long as the cleric desires, up to a maximum duration o 6 turns (one hour) per level of experience of the caster. For every 8 levels of experience the cleric has attained, up to 24, he or she is able to touch another and carry that person. or those two persons, along with the Wind Walk. Persons wind walking are not invisible but appear misty and are transparent. If fully clothed in white they are 80% likely to be mistaken for clouds, fog, vapours, etc. The material components of this spell are fire and holy/unholy water."
    )
]

druid_spells = [
    Spell('Animal Friendship','D',1,
        cast=tp(6,T),
        duration=tp(1,P),
        sourcebook=V,
        desc="By means of this spell the druid is able to show any animal which is of at least animal intelligence (but not above semi-intelligent rating) that the druid is disposed to be its friend. If the animal does not make its saving throw versus magic immediately when the spell is begun, it will stand quietly while the druid finishes the spell. Thereafter, it will follow the druid about, and he or she can teach it 3 specific \"tricks\" or tasks for each point of intelligence it possesses. (Typical tasks are those taught a dog or similar pet, i.e. they cannot be complex.) Training for each such \"trick\" must be done over a period of 1 week, and all must be done within 3 months of acquiring the creature. During the training period the animal will not harm the druid, but if the creature is left alone for more than 3 days it will revert to its natural state and act accordingly. The druid may use this spell to attract up to 2 hit dice of animal(s) per level of experience he or she possesses. This also means that the druid can never have more hit dice of animals so attracted and trained than are equal to or less than twice his or her levels of experience. Only neutral animals can be attracted, befriended, and trained. The material components of this spell ore mistletoe and a piece of food attractive to the animal subject."
    ),
    Spell('Ceremony','D',1,
        cast=tp(1,H),
        duration=tp(1,P),
        sourcebook=U,
        desc=("The druidic ceremony spell is similar to the clerical spell of the same name. It has a number of applications within the hierarchy of druids. The effect of a ceremony spell does not leave behind an aura of magic, although a know alignment spell or similar magic might reveal the force of true neutrality involved in the magic. Druidic ceremonies include the following, which can be cast by a druid of the indicated or higher level:\n\n"
            "1st-level druid: coming of age, rest eternal, marriage\n"
            "3rd-level druid: dedication, investiture\n"
            "7th-level druid: initiation, special vows\n"
            "9th-level druid: hallowed ground\n"
            "12th-level druid: cast out\n\n"
            "The characteristics of the various types of druidic ceremony spells are as follows:\n\n"
            "Coming of age is performed upon young people in druidic societies, usually when they reach the age of 14, and is symbolic of the young man's or young woman's entrance into adulthood. Effects of the spell are the same as for the clerical version (+1 bonus to a single saving throw); see the cleric text for other details.\n\n"
            "Rest eternal is cast upon the body of a deceased being, by means of which the soul/spirit of the creature is hastened in its journey to its final resting place. The spells raise dead and resurrection will not restore life to a character who has been the object of this spell, although a wish spell would serve that purpose.\n\n"
            "Marriage is essentially identical to the clerical ceremony of the same name.\n\n"
            "Dedication allows the recipient of the spell to be taken into the ranks of the druid's followers/worshipers, provided that the character is true neutral in alignment. A recipient of this spell is charged, as are druids, with the responsibility to preserve and protect nature and the balance of forces in the world. In other respects it is similar to the clerical ceremony of the same name.\n\n"
            "Investiture is a rite that must be performed upon a character before he or she can become an Aspirant (1st-level druid). It conveys no other benefit.\n\n"
            "Initiation imbues the druid with the shape-changing and immunity to woodland charm powers that become available to the character upon attaining 7th level. This ceremony must be performed upon a druid immediately after he or she begins to advance upward through the 7th level of experience; if cast earlier than this, it will not work, and the druid will not have the benefit of the above-mentioned special powers until receiving initiation. Usually a druid must seek out another druid of 7th or higher level to perform the rite, but in unusual cases a druid may cast it upon himself or herself.\n\n"
            "Special vows is a ceremony that operates in the same fashion as the clerical rite of the same name. It does not work upon paladins, but will function upon cavaliers of any alignment.\n\n"
            "Hallowed ground is cast by the druid on his or her permanent grove. This ceremony ensorcels the trees of the grove so that they will never be affected by disease or natural disasters. The ground remains hallowed for as long as the druid maintains this grove as his or her permanent base.\n\n"
            "Cast out is a form of excommunication or punishment that can be performed by a druid upon someone who has committed sacrilege upon the natural environment or in some other way violated the principles and standards of druidism. Its effects may be lessened at a later date by the casting of the reversed version of this ceremony, either by the same druid or another one of at least as high a level as the original caster, but the casting out can never be completely neutralized except by a Hierophant Druid of any level. A character who has been cast out exudes a powerful negative aura, causing any natural creature encountered to react negatively to the character. This includes all normal (non-magical) animals, monsters native to the woodlands, domesticated beasts such as horses and dogs, and all druids and their followers.\n\n"
            "Casting out is a very powerful form of punishment, and can only be performed by a druid who has received permission from his or her Archdruid to do so. Similarly, an Archdruid must get permission from the Great Druid, and the Great Druid from the Grand Druid. The Grand Druid does not need to obtain permission, but his or her actions may be reversed by a Hierophant Druid at any time.\n\n"
            "This ceremony is usually only used on occasions where the severity of an offense warrants an extreme punishment; a druid who asks for and is denied permission to perform it, or one who later has his or her actions offset by another druid, may be subject to punishment by higher-ranking members of the hierarchy. An intended recipient of this ceremony who is unwilling recieves a saving throw versus spell, at -4, to negate its effects.\n\n"
            "The components of a ceremony spell always include mistletoe, and the rite (of any sort) must be performed in a druid grove or some other natural, healthy patch of forest. Such ceremonies are normally conducted either at dawn or dusk, the times when night and day are in balance."
        )
    ),
    Spell('Detect Balance','D',1,
        cast=tp(1,S),
        duration_lvl=tp(1,R),
        sourcebook=U,
        desc=("This spell allows the druid to determine if non-neutral forces and alignments are at work in the area of effect (upon or in the object or creature being scanned). An alignment that is partly neutral (such as that of a neutral good cleric) will radiate a mild aura, while an alignment that has no neutral component (such as that of a chaotic good fighter) will give off a strong aura. The spell does not determine exact alignment, but only tells the druid if the object or creature being examined is something other than true neutral; a paladin and a chaotic evil thief, for instance, will radiate the same aura at the same strength.\n\n"
            "The spell will not function upon non-living items that do not have a natural aura (such as a vial of poison), but will work upon an object such as an aligned magical sword. Creatures that are under the effect of an unknowable alignment spell or similar magic will not radiate any aura when this spell is used upon them. If the magic is used upon something or someone that exudes a true neutral alignment (such as another druid), it will produce a smooth, well-balanced aura identifiable as one of neutrality."
        )
    ),
    Spell('Detect Magic','D',1,
        cast=tp(3,S),
        duration=tp(12,R),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the first level cleric spell of the same name."
    ),
    Spell('Detect Poison','D',1,
        cast=tp(1,R),
        duration_lvl=tp(1,R),
        sourcebook=U,
        desc=("By means of this spell the druid is able to determine if some object, creature, or area contains poison or has been poisoned. In general, the area which can be perused by the dweomer of the spell is 1 cubic yard of space. Therefore, the druid cannot determine if an entire pond is poisoned, but he or she could tell if a portion — or something within the portion — scanned during the round contain poison. There is also a 5% chance per level of experience of the caster that the type of poison used or contained in the area scanned will also be discovered by the spell, i.e., contact poison (insinuative), ingestive, or respirative (gas).\n\n"
            "While more than one area can be scanned with a detect poison spell during the duration of the spell, it is almost fruitless to attempt to determine poison type for all of those areas; any single failure on the \"5% chance per level\" roll to detect poison type makes this spell useless for this purpose for the remainder of the duration of that particular casting. In addition to mistletoe, the druid needs a yew leaf as a material component for this spell. The latter item will turn brown if poison is present, so that several will possibly be needed to fully utilize the entire spell duration."
        )
    ),
    Spell('Detect Snares & Pits','D',1,
        cast=tp(3,S),
        duration=tp(0),
        duration_lvl=tp(4,R),
        sourcebook=V,
        desc='Upon casting this spell, the druid is able to detect snares & pits along the 1" wide by 4" long area of effect path and thus avoid such deadfalls. Note that in the underground only simple pits, not all forms of traps, would be detected by means of this spell. Outdoors, the spell detects all forms of traps - deadfalls, missile trips, snares, etc. The spell lasts 4 melee rounds for each level of experience of the druid casting it, i.e. 4 rounds at the 1st level, 8 at the 2nd, 12 (1 turn plus 2 rounds) at the 3rd, etc.'
    ),
    Spell('Entangle','D',1,
        cast=tp(3,S),
        duration=tp(1,T),
        sourcebook=V,
        desc="By means of this spell the druid is able to cause plants in the area of effect to entangle creatures within the area. The grasses, weeds, bushes, and even trees wrap, twist, and entwine about creatures, thus holding them fast for the duration of the spell. If any creature in the area of effect makes its saving throw, the effect of the spell is to slow its movement by 50% for the spell duration."
    ),
    Spell('Faerie Fire','D',1,
        cast=tp(3,S),
        duration=tp(0),
        duration_lvl=tp(4,R),
        sourcebook=V,
        desc="When the druid casts this spell, he or she outlines an object or creature with a pale glowing light. The completeness of the lining is dependent upon the number of linear feet the druid is able to affect, about 12' per level (i.e. one 6' man or two 3' kobolds). If there is sufficient power, several objects or creatures can be covered by the faerie fire, but one must be fully outlined before the next is begun, and all must be within the area of effect. Outlined objects or creatures (including those otherwise invisible) are visible at 8\" in the dark, 4\" if the viewer is near a bright light source. Outlined creatures are easier to strike, thus opponents gain +2 on \"to hit\" dice. The faerie fire can be blue, green, or violet according to the word of the druid at the time he or she casts the spell. The faerie fire does not itself cause any harm to the object or creature lined."
    ),
    Spell('Invisibility to Animals','D',1,
        cast=tp(4,S),
        duration=tp(1,T),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="When an Invisibility To Animals spell is cast by a druid, the recipient of the magic becomes totally undetectable with respect to normal animals with intelligence under 6. Normal animals includes giant-sized varieties, but it excludes any with magical abilities or powers. The magicked individual is able to walk amongst animals or pass through them as if he or she did not exist. For example, this individual could stand before the hungriest of lions or a tyrannosaurus rex and not be molested or even noticed. However, a nightmare, hell hound, or winter wolf would certainly be aware of the individual. The material component of this spell is holly rubbed over the individual."
    ),
    Spell('Locate Animals','D',1,
        cast=tp(1,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc='The druid with a Locate Animals spell is able to determine the direction and distance of any of the desired animals within the area of effect. The sought after animal can be of any sort, but the druid must concentrate on the sort desired. The cleric faces in a direction, thinks of the animal desired, and he or she then knows if any such animal is within spell range. During a round of spell effect duration, the druid must face in only one direction, i.e., only a 2" wide path can be known. The spell lasts 1 round per level of experience of the druid, while the length of the path is 2" per level of experience.'
    ),
    Spell('Pass Without Trace','D',1,
        cast=tp(1,R),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="When this spell is cast, the recipient can move through any type of terrain - mud, snow, dust, etc. - and leave neither footprint nor scent. Thus, tracking a person or other creature covered by this dweomer is impossible. The material components of this spell are a leaf of mistletoe (which must be burned thereafter and the ashes powdered and scattered) and a sprig of pine or evergreen. Note: The area which is passed over will radiate a dweomer for 6-36 turns after the affected creature passes."
    ),
    Spell('Precipitation','D',1,
        cast=tp(3,S),
        duration_lvl=tp(1,S),
        sourcebook=U,
        desc="This spell is identical to the 1st-level clerical spell of the same name, except that the druid needs mistletoe as an additional material component."
    ),
    Spell('Predict Weather','D',1,
        cast=tp(1,R),
        duration_lvl=tp(2,H),
        sourcebook=V,
        desc="When a Predict Weather spell is cast by a druid, he or she gains 100% accurate knowledge of the weather (sky, temperature, precipitation) in a nine square mile area centring on the druid. For each level of experience of the druid casting the spell, two hours advance weather can be forecast. Thus, at 1st level the druid knows what the weather will be for two hours; at second level he or she knows the weather for 4 hours in advance, etc."
    ),
    Spell('Purify Water','D',1,
        cast=tp(1,R),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell makes dirty, contaminated water clean and pure, suitable for consumption. Up to one cubic foot per level of the druid casting the spell can be thus purified. The reverse of the spell, Contaminate Water, works in exactly the same manner, and even holy/unholy water can be spoiled by its effects."
    ),
    Spell('Shillelagh','D',1,
        cast=tp(1,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell enables the druid to change his own oaken cudgel into a magical weapon which is +1 to hit and inflicts 2-8 hit points of damage on opponents up to man-sized, 2-5 hit points of damage on larger opponents. The druid must wield the shillelagh, of course. The material components of this spell are an oaken club, any mistletoe, and a shamrock leaf."
    ),
    Spell('Speak With Animals','D',1,
        cast=tp(3,S),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the second level cleric spell of the same name."
    ),
    Spell('Barkskin','D',2,
        cast=tp(3,S),
        duration=tp(4,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="When the druid casts the Barkskin spell upon a creature, its armour class improves 1 place because the creature's skin becomes as tough as bark. In addition, saving throws versus all attack forms except magic increase by +1. This spell can be placed on the druid casting it or on any other creature he or she touches. In addition to mistletoe. the caster must have a handful of bark from an oak as the material component of the spell."
    ),
    Spell('Charm Person Or Mammal','D',2,
        cast=tp(4,S),
        duration=tp(1,VA),
        sourcebook=V
    ),
    Spell('Create Water','D',2,
        cast=tp(1,T),
        duration=tp(1,P),
        sourcebook=V,
        desc="The druid can create pure, drinkable water by means of a Create Water spell. He or she creates 1 cubic foot of water for each level of experience attained. The water can be created at a maximum distance of 1\" from the druid."
    ),
    Spell('Cure Light Wounds','D',2,
        cast=tp(4,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="With the exception of the fact that the druid must have mistletoe (of any sort) to effect this spell, it is the same as the first level cleric Cure Light Wounds spell."
    ),
    Spell('Feign Death','D',2,
        cast=tp(3,S),
        duration=tp(4,R),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the third level magic-user Feign Death spell (q.v.). The material component is a piece of dead oak leaf (in addition to mistletoe, of course)."
    ),
    Spell('Fire Trap','D',2,
        cast=tp(1,T),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell is the same as the fourth level magic-user Fire Trap spell (q.v.) except as shown above and for the fact that the material components are holly berries and a stick of charcoal to trace the outline of the closure."
    ),
    Spell('Flame Blade','D',2,
        cast=tp(3,S),
        duration_lvl=tp(1,R),
        sourcebook=U,
        desc="When a druid casts this spell, he or she causes a ray of red-hot fire to spring forth from his or her hand. This blade-like ray is actually wielded as if it were a scimitar, and if the druid scores a successful hit while employing the flame blade, the creature struck will take 5-8 points of damage — with a damage bonus of +2 if the creature is of the undead class or is especially vulnerable to fire, or a -2 penalty to damage if the creature is protected from fire. No damage can be inflicted upon a creature which is a fire-dweller or which uses fire as an attack form. The flame blade will ignite combustible materials such as parchment, straw, dry sticks, cloth, etc. However, it is not a magical weapon in the normal sense of the term except with respect to undead monsters, so creatures that can be struck only by magical weapons are not harmed by this spell unless they are of the undead class. In addition to mistletoe, the druid must have a leaf of sumac in order to cast the spell."
    ),
    Spell('Goodberry','D',2,
        cast=tp(5,S),
        duration=tp(1,R),
        sourcebook=U,
        desc="When a druid casts a goodberry spell upon a handful or freshly picked berries, from 2 to 8 of them will become magical. The druid casting the spell (as well as any other druid of 3rd or higher level) will be able to immediately discern which berries were affected. A detect magic spell will discover this also. Berries with the dweomer will either enable a hungry creature of approximately man-size to eat one and be as well-nourished as if a full normal meal were eaten, or else the berry will cure 1 point of physical damage due to wounds or other similar causes, subject to a maximum of 8 points of such curing in any 24-hour period. The reverse of the spell, badberry, causes rotten berries to appear wholesome but each actually delivers 1 point of poison damage (no saving throw) if ingested. The material component of the spell is mistletoe passed over the freshly picked, edible berries to be enspelled (blueberries, blackberries, rapberries, currants, gooseberries, etc.)."
    ),
    Spell('Heat Metal','D',2,
        cast=tp(4,S),
        duration=tp(7,R),
        sourcebook=V
    ),
    Spell('Locate Plants','D',2,
        cast=tp(1,R),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="When this spell is used by a druid, he or she is able to locate any desired type of plant within the area of effect. Note: the plant type must be singular and concentrated upon. The spell's area of effect centres on, and moves with, the druid."
    ),
    Spell('Obscurement','D',2,
        cast=tp(4,S),
        duration_lvl=tp(4,R),
        sourcebook=V,
        desc="This spell causes a misty vapour to arise around the druid. It persists in this locale for 4 rounds per level of experience of the druid casting the spell, and it reduces visibility of any sort (including infravision) to 2' to 8' (2d4). The area of effect is a cubic progression based on the druid's level of experience, a 1\" cube at 1st level, a 2\" cube at 2nd level, a 3\" cube at 3rd level, and so on. Underground, the height of the vapour is restricted to 1\", although the length and breadth of the cloud is not so limited. A strong wind will cut the duration of an Obscurement spell by 75%."
    ),
    Spell('Produce Flame','D',2,
        cast=tp(4,S),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="A bright flame, equal in brightness to a torch, springs forth from the druid's palm when he or she casts a Produce Flame spell. This magical flame lasts for 2 melee rounds for each level of the druid casting the spell. The flame does not harm the druid's person. but it is hot, and it will cause combustion of inflammable materials (paper, cloth, dry wood, oil, etc.). The druid is capable of hurling the magical flame as a missile, with a range of 4\". The flame will flash on impact, igniting combustibles within a 3' diameter of its centre of impact. and then extinguish itself. The druid can cause it to go out any time he or she desires, but fire caused by the flame cannot be so extinguished."
    ),
    Spell('Reflecting Pool','D',2,
        cast=tp(2,H),
        duration_lvl=tp(1,R),
        sourcebook=U,
        desc=("This spell enables the druid to cause a pool of normal water found in a natural setting to act as a scrying device. The pool can be no greater diameter than 2 feet per level of the spell caster. The effect is to create a scrying device similar to a crystal ball, in much the same fashion as the magic-user spell magic mirror and the clerical spell magic font, both described elsewhere in this text. The scrying can extend only to those planes of existence which are coexistent with or border upon the Prime Material Plane, i.e. the Inner Planes (including the Para-elemental Planes, Plane of Shadow, et al.). Penalties for attempting to scry beyond the druid's own plane, as given in the description for crystal ball (see Dungeon Masters Guide) are applicable.\n\n"
            "The following spells can be cast through a reflecting pool, with a 5% per level chance of operating correctly: detect magic, detect snares and pits, detect poison. Infravision and ultravision will operate normally through the reflecting pool, as will the spells starshine and moonbeam (see hereafter). The druid must use both mistletoe and the oil extracted from such nuts as the hickory and the walnut, refined, and dropped in three measures upon the surface of the pool. (A measure need be no more than a single ounce of oil.)"
        )
    ),
    Spell('Slow Poison','D',2,
        cast=tp(0),
        duration=tp(0),
        duration_lvl=tp(0),
        sourcebook=U,
        desc=("This spell is identical to the 2nd-level clerical spell slow poison, except that if the druid is able to determine that the poison was one made from some living plant, he or she has a 5% chance per level of knowing an herbal antidote which will neutralize the poison. (If the actual type of poison is not given by the Dungeon Master, a successful casting of detect poison [type] indicates an organic poison which can be countered.) A dice roll equal to or less than the druid's chance to find an antidote indicates neutralization.\n\n"
            "The druid uses mistletoe as a material component for this spell, and crushed garlic must be rubbed on the recipient's feet. Antidotes must be obtained from green vegetables outdoors, or from an herbalist or similar source of supply."
        )
    ),
    Spell('Trip','D',2,
        cast=tp(4,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="The spell caster must use a length of vine, a stick, pole, rope, or similar object to cast this magic upon. The Trip spell causes the object to rise slightly off the ground or floor it is resting on and trip creatures crossing it if they fail to make their saving throw versus magic. Note that only as many creatures can be tripped as are actually stepping across the magicked object, i.e. a 3' long piece of rope could trip only 1 man-sized creature. Creatures moving at a very rapid pace (running) when tripped will take 1-6 (d6) hit points of damage and be stunned for 2-5 (d4+1) rounds if the surface they full upon is very hard, but if it is turf or non-hard they will merely be stunned for 2-5 segments. Very large creatures such as elephants will not be at all affected by a Trip. The object magicked will continue to trip all creatures passing over it, including the spell caster, for as long as the spell duration lasts. Creatures aware of the object and its potential add +4 to their saving throw when crossing it. The object is 80% undetectable without magical means of detection."
    ),
    Spell('Warp Wood','D',2,
        cast=tp(4,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="When this spell is cast the druid causes a volume of wood to bend and warp, permanently destroying its straightness, form and strength. The range of a Warp Wood spell is 1\" for each level of experience of the druid casting it. It affects approximately a fifteen inch shaft of wood of up to one inch diameter per level of the druid. Thus, at 1st level, a druid might be able to warp a hand axe handle, or four crossbow bolts, at 5th level he or she could warp the shaft of a typical magic spear. Note that boards or planks can also be affected, causing a door to be sprung or a boat or ship to leak."
    ),
    Spell('Call Lightning','D',3,
        cast=tp(1,T),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="When a Call Lightning spell is cast, there must be a storm of some sort in the area - a rain shower, clouds and wind, hot and cloudy conditions, or even a tornado. The druid is then able to call down belts of lightning from sky to ground. Each bolt will cause damage equal to 2 eight-sided dice (2d8) plus 1 like die (d8) for each level of experience of the druid casting the spell. Thus, a 4th level druid calls down a six-die (6d8) bolt. The bolt of lightning flashes down in a perpendicular stroke at whatever distance the spell caster decides, up to the 36\" radial distance maximum. Any creature within a 1\" radius of the path or the point where the lightning strikes will take full damage, unless a saving throw is made, in which case only one-half damage is taken. Full/half damage refers to the number of hit dice of the lightning bolt, i.e. if it is of eight dice strength, the victim will take either eight dice (8d8) or four dice (4d8), if the saving throw is made, of damage. The druid is able to call one bolt of lightning every 10 melee rounds (1 turn), to a maximum number of turns equal to the level of experience he or she has attained, i.e. 1 bolt/turn for each level of experience. Note: This spell is normally usable outdoors only."
    ),
    Spell('Cloudburst','D',3,
        cast=tp(5,S),
        duration=tp(1,R),
        sourcebook=U,
        desc="This spell is essentially the same as the 3rd-level clerical spell of the same name, with only the following special notations and additions: Lightning cannot be called by the use of a cloudburst spell, and a call lightning spell cannot be used in the same area at the same time. Also, the druid must use mistletoe as an additional material component."
    ),
    Spell('Cure Disease','D',3,
        cast=tp(1,R),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell is the same as the 3rd level cleric Cure Disease spell (q.v.), with the exception that the druid must have mistletoe to effect it. It is reversible to Cause Disease also."
    ),
    Spell('Hold Animal','D',3,
        cast=tp(5,S),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="By means of this spell the druid holds one to four animals rigid. Animals affected are normal or giant-sized mammals, birds, or reptiles, but not monsters such as centaurs, gorgons, harpies, naga, etc. That is, apes, bears, crocodiles, dogs, eagles, foxes, giant beavers, and similar animals are subject to this spell. The hold lasts for 2 melee rounds per level of experience of the druid casting it. It is up to the druid as to how many animals he or she wishes to hold with the spell, but the greater the number, the better chance each will have of not being affected by the spell. Note that a maximum body weight of 400 pounds (100 pounds with respect to non-mammals)/animal/level of experience of the druid can be affected, i.e. an 8th level druid can affect up to four 3,200 pound mammals or a like number of 800 pound non-mammals such as birds or reptiles. Each animal gets a saving throw: if only 1 is the subject of the spell, it has a penalty of -4 on its die roll to save; if 2 are subject, they each receive a penalty of -2 on their die rolls; if 3 are subject, they each receive a penalty of -1 on their die rolls; if 4 are subject, each makes a normal saving throw."
    ),
    Spell('Know Alignment','D',3,
        cast=tp(5,S),
        duration=tp(5,R),
        sourcebook=U,
        desc="This spell is essentially the same as the 2nd-level clerical spell of the same name, except as noted above, and with the following additional difference. Because of the shorter duration, only five creatures (maximum) can be examined by this spell, and it cannot be reversed."
    ),
    Spell('Neutralize Poison','D',3,
        cast=tp(5,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell is the same as the 4th level cleric Neutralize Poison spell (q.v.)."
    ),
    Spell('Plant Growth','D',3,
        cast=tp(1,R),
        duration=tp(1,P),
        sourcebook=V,
        desc="When a Plant Growth spell is cast by the druid, he or she causes normal vegetation a grow, entwine, and entangle to form a thicket or jungle which creatures must hack or force a way through at a movement rate of 1\" per, or 2\" per with respect to larger than man-sized creatures. Note that the area must have brush and trees in it in order to allow this spell to go into effect. Briars, bushes, creepers, lianas, roots, saplings, thistles, thorn, trees, vines, and weeds become so thick and overgrown in the area of effect as to form a barrier. The area of effect is 2\" x 2\" square per level of experience of the druid, in any square or rectangular shape that the druid decides upon at the time of the spell casting. Thus an 8th level druid can affect a maximum area of 16\" x 16\" square, a 32\" x 8\" rectangle, a 64\" X 4\" rectangle, 128\" x 2\" rectangle, etc. The spell's effects persist in the area until it is cleared by labour, fire, or such magical means as a Dispel Magic spell (q.v.)"
    ),
    Spell('Protection From Fire','D',3,
        cast=tp(5,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="The effect of a Protection From Fire spell differs according to the recipient of the magic - the druid or some other creature. If the spell is cast upon the druid, it confers complete invulnerability to normal fires (torches, bonfires, oil fires, and the like) and to exposure to magical fires such as demon fire, burning hands, fiery dragon breath, Fireball, Fire Seeds, Fire Storm, Flame Strike, hell hound breath, Meteor Swarm, pyrohydra breath, etc. until an accumulation of 12 hit points of potential damage per level of experience of the druid has been absorbed by the Protection From Fire spell, at which time the spell is negated. Otherwise the spell lasts for 1 turn per level of experience of the druid. If the spell is cast upon another creature, it gives invulnerability to normal fire, gives a bonus of +4 on saving throw die rolls made versus fire attacks, and reduces damage sustained from magical fires by 50%."
    ),
    Spell('Pyrotechnics','D',3,
        cast=tp(5,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="A Pyrotechnics spell can have either of two effects. It produces a flashing and fiery burst of glowing, coloured aerial fireworks which lasts 1 segment per experience level of the druid casting the spell and temporarily blinds those creatures in the area of effect or under it or within 12\" of the area (and in any event in unobstructed line of sight); or it causes a thick writhing stream of smoke to arise from the fire source of the spell and form a choking cloud which lasts for 1 round per experience level of the druid casting it, covering a roughly globular area from the ground or floor up (or conforming to the shape of a confined area), which totally obscures vision beyond 2'. The spell requires a fire of some sort in range. The area of Pyrotechnics effect is 10 times the volume of the fire source with respect to fireworks, 100 times with respect to smoke. In either case, the fire source is immediately extinguished by the employment of the spell."
    ),
    Spell('Snare','D',3,
        cast=tp(3,R),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell enables the druid to make a snare which is 90% undetectable without magical aid. The snare can be made from any supple vine, a thong, or a rope. When the Snare spell is cast upon it, the cordlike object blends with the background of its location. One end of the snare is tied in a loop which will contract about 1 or more of the limbs of any creature stepping inside the circle (note that the head of a worm or snake could also be thus ensnared). If a strong and supple tree is nearby, the snare will be fastened to it, and the dweomer of the spell will cause it to bend and then straighten when the loop is triggered, thus causing 1-6 hit points of damage to the creature trapped, and lifting off the ground by the trapped member(s) (or strangling it if the head/neck triggered the snare). If no such sapling or tree is available, the cord-like object will tighten upon the member(s) and then enwrap the entire creature, doing no damage, but tightly binding it. The snare is magical, so for 1 hour it is breakable only by storm giant or greater strength (23); each hour thereafter, the snare material loses magic so as to become 1 point more breakable per hour - 22 after 2 hours, 21 after 3, 20 after 4 - until 6 full hours have elapsed. At that time, 18 strength will break the bonds. After 12 hours have elapsed, the materials of the snare lose all of the magical properties, and the loop opens, freeing anything it had held. The druid must have a snake skin and a piece of sinew from a strong animal to weave into the cord-like object from which he or she will make the snare. Only mistletoe is otherwise needed."
    ),
    Spell('Spike Growth','D',3,
        cast=tp(3,S),
        duration=tp(1,VA),
        duration_lvl=tp(1,T),
        sourcebook=U,
        desc="This spell is essentially the same as the 4th-level clerical spell of the same name, except as noted above, and with the following additional differences: The affected area will radiate an aura of magic, and a detect snares and pits spell will reveal the location of the spike growth. The druid must use mistletoe as a material component (in place of the cleric's holy symbol) in addition to the seven small twigs or thorns."
    ),
    Spell('Starshine','D',3,
        cast=tp(5,S),
        duration_lvl=tp(1,T),
        sourcebook=U,
        desc="A starshine spell enables the druid to softly illuminate an area as if it were exposed to a clear night sky filled with stars. Regardless of the height of the open area in which the spell is cast, the area immediately beneath it will be lit by starshine. Vision will be clear at up to 30', indistinct out to 60', and beyond that only gleams and glitters will be discernible. The starshine allows shadows. It enhances ultravision to its full potential but does not affect infravision. The spell makes the area of effect actually appear to be a night sky, but disbelief of the illusion merely allows the disbeliever to note that the \"stars\" are actually evoked lights. The material components are several stalks from an amaryllis (especially Hypoxis) and several holly berries."
    ),
    Spell('Stone Shape','D',3,
        cast=tp(1,R),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell is exactly the same as the fifth level magic-user spell, Stone Shape (q.v.), except as noted above and for the requirement of mistletoe as an additional component to enable a druid to cast the spell."
    ),
    Spell('Summon Insects','D',3,
        cast=tp(1,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="When a Summon Insects spell is cast by a druid, he or she attracts flying insects 70% of the time. The exact insects called will be bees, biting flies, hornets, or wasps if flying insects are indicated, or biting ants or pinching beetles if non-flying insects are determined. A cloud of the flying type, or a swarm of the crawling sort, will appear after the spell is cast. They will attack any creature the druid points to. The attacked creature will sustain 2 hit points of damage per melee round, and it can do nothing but attempt to fend off these insects during the time it is so attacked. The summoned insects can be caused to attack another opponent. but there will be at least a 1 round delay while they leave the former recipient and attack the new victim, and crawling insects can travel only about 12' per round (maximum speed over smooth ground). It is possible in underground situations that the druid could summon 1-4 giant ants by means of the spell, but the possibility is only 30% unless giant ants are nearby. The materials needed for this spell are mistletoe, a flower and a bit of mud or wet clay."
    ),
    Spell('Tree','D',3,
        cast=tp(5,S),
        duration=tp(6,T),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="By means of this spell the druid is able to assume the form of a small living tree or shrub or that of a large dead tree trunk with but a few limbs. Although the closest inspection will not reveal that this plant is actually a druid, and for all normal tests he or she is, in fact, a tree or shrub, the druid is able to observe all that goes on around his or her person just as if he or she were in human form. The spell caster may remove the dweomer at any time he or she desires, instantly changing from plant to human form, and having full capability of undertaking any action normally possible to the druid. Note that all clothing and gear worn/carried change with the druid. The material components of this spell are mistletoe and a twig from a tree."
    ),
    Spell('Water Breathing','D',3,
        cast=tp(5,S),
        duration_lvl=tp(6,T),
        sourcebook=V,
        desc="The recipient of a Water Breathing spell is able to freely breathe underwater for the duration of the spell, i.e. 6 turns for each level of experience of the druid casting the spell. The reverse, Air Breathing, allows water breathing creatures to comfortably survive in the atmosphere for an equal duration."
    ),
    Spell('Animal Summoning I','D',4,
        cast=tp(6,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="By means of this spell, the druid calls up to eight animals of whatever sort the druid names when the summoning is made, if such type are within spell range. These animals can have no more than four hit dice each. The animals summoned will aid the druid by whatever means they possess, staying until a fight is over, a specific mission is finished, the druid is safe, he or she sends them away, etc. The druid may try three times to summon three different sorts of animals, i.e. suppose that wild dogs are first summoned to no avail, then hawks are unsuccessfully called, and finally the druid calls for wild horses which may or may not be within summoning range. Your referee will determine probabilities if the presence of a summoned animal type is not known. Other than various sorts of giant animals, fantastic animals or monsters cannot be summoned lay this spell, i.e. no chimerae, dragons, gorgons, manticores, etc."
    ),
    Spell('Call Woodland Beings','D',4,
        cast=tp(2,T),
        duration=tp(1,P),
        sourcebook=V,
    ),
    Spell('Control Temperature','D',4,
        cast=tp(6,S),
        duration=tp(4,T),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="When this spell is cast by the druid, the temperature surrounding the druid can be altered by 9 degrees Fahrenheit (5ºC) per level of experience of the spell caster, either upwards or downwards. Thus, a 10th level druid could raise the surrounding temperature from 1 to 90 degrees (1-50ºC) or lower it by from 1 to 90 degrees (1-50ºC). The spell lasts for a number of turns equal to 4 plus the level of experience of the druid, i.e. when cast by a 10th level druid the spell persists for 14 turns."
    ),
    Spell('Cure Serious Wounds','D',4,
        cast=tp(6,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell is the same as the 4th level cleric Cure Serious Wounds spell (q.v.), with the exception of the fact that the spell requires the use of any sort of mistletoe."
    ),
    Spell('Dispel Magic','D',4,
        cast=tp(6,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the 3rd level cleric Dispel Magic spell (q.v.)."
    ),
    Spell('Hallucinatory Forest','D',4,
        cast=tp(6,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="By casting this spell the druid causes the appearance of an Hallucinatory Forest to come into existence. The Illusionary forest appears to be perfectly natural and is indistinguishable from a real forest. Other druids - as well as such creatures as centaurs, dryads, green dragons, nymphs, satyrs, and treants - will recognize the forest for what it is. All other creatures will believe it is there, and movement and order of march will be affected accordingly. The Hallucinatory Forest will remain until it is magically dispelled by a reverse of the spell or a Dispel Magic. The area shape is either rectangular or square, in general, at least 4\" deep, and in whatever location the druid casting the spell desires. The forest can be of less than maximum area if the druid wishes. One of its edges will appear up to 8\" away from the druid, according to the desire of the spell caster."
    ),
    Spell('Hold Plant','D',4,
        cast=tp(6,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="The Hold Plant spell affects vegetable matter as follows: 1) it causes ambulatory vegetation to cease moving; 2) it prevents vegetable matter from entwining, grasping, closing. or growing; 3) it prevents vegetable matter from making any sound or movement which is not caused by wind. The spell effects apply to all forms of vegetation, including parasitic and fungoid types, and those magically animated or otherwise magically empowered. It affects such monsters as green slime, moulds of any sort, shambling mounds. shriekers, treants, etc. The duration of a Hold Plant spell is 1 melee round per level of experience of the druid casting the spell. It affects from 1 to 4 plants - or from 4 to 16 square yards of small ground growth such as grass or mould. If but one plant (or 4 square yards) is chosen as the target for the spell by the druid, the saving throw of the plant (or area of plant growth) is made at a -4 on the die; if two plants (or 8 square yards) are the target, saving throws are at -2; if three plants (or 12 square yards) are the target, saving throws are at -1; and if the maximum of 4 plants (or 16 square yards of area) are the target, saving throws are normal."
    ),
    Spell('Plant Door','D',4,
        cast=tp(6,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="The Plant Door spell opens a magical portal or passageway through trees, undergrowth, thickets, or any similar growth - even growth of a magical nature. The Plant Door is open only to the druid who cast the spell, druids of a higher level, or dryads. The door even enables the druid to enter into a solid tree trunk and remain hidden there until the spell ends. If the tree is cut down or burned, the druid must leave before the tree falls or is consumed, or else he or she is killed also. The duration of the spell is 1 turn per level of experience of the druid casting it. If the druid opts to stay within an oak, the spell lasts 9 times longer, if an ash tree it lasts 2 times as long. The path created by the spell is up to 4' wide, 8' high and 12'/level of experience of the druid long."
    ),
    Spell('Produce Fire','D',4,
        cast=tp(6,S),
        duration=tp(1,R),
        sourcebook=V,
        desc="By means of this spell the druid causes a common-type fire of up to 12' per side in area boundary. While it lasts but a single round, the fire produced by the spell will cause 1-4 hit points of damage on creatures within its area; and it will ignite combustible materials such as cloth, oil, paper, parchment, wood and the like so as to cause continued burning. The reverse, Quench Fire will extinguish any normal fire (coals, oil, tallow, wax, wood, etc.) within the area of effect."
    ),
    Spell('Protection From Lightning','D',4,
        cast=tp(6,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="This spell is exactly the same as the 3rd level Protection From Fire spell (q.v.) except that it applies to electrical/lightning attacks."
    ),
    Spell('Repel Insects','D',4,
        cast=tp(1,R),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="When this spell is cast the druid creates an invisible barrier to all sorts of insects, and normal sorts will not approach within 10' of the druid while the spell is in effect although any giant insects with 2 or more hit dice will do so if they make a saving throw versus magic, and even those which do so will sustain 1-6 hit points of damage from the passing of the magical barrier. Note that the spell does not in any way affect arachnids, myriapods, and similar creatures - it affects only true insects. The material components of the Repel Insects spell are mistletoe and one of the following: several crushed marigold flowers, a whole crushed leek, 7 crushed stinging nettle leaves or a small lump of resin from a camphor tree."
    ),
    Spell('Speak With Plants','D',4,
        cast=tp(1,T),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="Except as noted above, and that the material component is that typically druidic (mistletoe, eta).), the spell is the same as the 4th level cleric spell Speak With Plants."
    ),
    Spell('Animal Growth','D',5,
        cast=tp(7,S),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="When this spell is cast, the druid causes all animals, up to a maximum of 8, within a 2\" square area to grow to twice their normal size. The effects of this growth are doubled hit dice (with resultant improvement in attack potential) and doubled damage in combat. The spell lasts for 2 melee rounds for each level of experience of the druid casting the spell. Note that the spell is particularly useful in conjunction with a Charm Person or Mammal or a Speak With Animals spell. The reverse reduces animal size by one half, and likewise reduces hit dice, attack damage, etc."
    ),
    Spell('Animal Summoning II','D',5,
        cast=tp(7,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell is the same in duration and effect as the 4th level Animal Summoning I spell, except that up to six animals of no more than eight hit dice each can be called, or 12 animals of no more than four hit dice each can be called."
    ),
    Spell('Anti-Plant Shell','D',5,
        cast=tp(7,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="The Anti-Plant Shell spell creates an invisible barrier which keeps out all creatures or missiles of living vegetable material. Thus, the druid (and any creatures within the shell) is protected from attacking plants or vegetable creatures such as shambling mounds or treants. The spell lasts for one turn per level of experience of the druid."
    ),
    Spell('Commune With Nature','D',5,
        cast=tp(1,T),
        duration=tp(0),
        sourcebook=V,
        desc="This spell enables the druid to become one with nature in the area, thus being empowered with knowledge of the surrounding territory. For each level of experience of the druid, he or she may \"know\" one fact, i.e. the ground ahead, left or right, the plants ahead, left or right, the minerals ahead, left or right, the water courses/bodies of water ahead, left or right, the people dwelling ahead, left or right, etc. The spell is effective only in outdoors settings, and operates in a radius of one half mile for each level of experience of the druid casting the Commune With Nature spell."
    ),
    Spell('Control Winds','D',5,
        cast=tp(7,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="By means of a Control Winds spell the druid is able to alter wind force in the area of effect. For every level of his or her experience, the druid is able to increase or decrease wind force by 3 miles per hour. Winds in excess of 30 miles per hour drive small flying creatures (those eagle-sized and under) from the skies and severely inhibit missile discharge. Winds in excess of 45 miles per hour drive even man-sized flying creatures from the skies. Winds in excess of 60 miles per hour drive all flying creatures from the skies and uproot trees of small size, knock down wooden structures, tear off roofs, etc. Winds in excess of 75 miles per hour are of hurricane force and cause devastation to all save the strongest stone constructions. A wind above 30 miles per hour makes sailing difficult, above 45 miles per hour causes minor ship damage, above 60 miles per hour endangers ships, and above 75 miles per hour sinks ships. There is an \"eye\" of 4\" radius around the druid where the wind is calm. A higher level druid can use a Control Winds spell to counter the effects of a like spell cast by a lower level druid (cf. control weather). The spell remains in force for 1 turn for each level of experience of the druid casting it. Once the spell is cast, the wind force increases by 3 miles per hour per round until maximum speed is attained. When the spell is exhausted, the force of the wind diminishes at the same rate. Note that while the spell can be used in underground places, the \"eye\" will shrink in direct proportion to any confinement of the wind effect, i.e. if the area of effect is a 48\" radius, and the confined space allows only a 46\" radius, the \"eye\" will be 2\" radius; and any space under 44\" radius will completely eliminate the \"eye\" and subject the spell caster to the effects of the wind."
    ),
    Spell('Insect Plague','D',5,
        cast=tp(1,T),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="Except as noted above, and other than the fact that the material component needed for the spell is mistletoe or the holly or oak leaves substitute, the spell is the same as the 5th level cleric Insect Plague spell (q.v.)."
    ),
    Spell('Moonbeam','D',5,
        cast=tp(7,S),
        duration_lvl=tp(1,R),
        sourcebook=U,
        desc="By means of this spell the druid is able to cause a beam of soft, pale light to strike downward from overhead and illuminate whatever area he or she is pointing at. The light is exactly the same as moonlight, so that colors other than shades of black, gray, or white will not be determinable. The spell caster can easily cause the moonbeam to move to any area that he or she can see and point to. This makes the spell an effective way to spotlight something, for example an opponent. While the moonbeam allows shadows, a creature centered in a moonbeam spell is most certainly under observation. The reflected light from this spell allows dim visual perception 1\" beyond the area of affect. The light does not adversely affect infravision, and enhances ultravision to its greatest potential. The material components are several seeds of any moonseed plant and a piece of opalescent feldspar (moonstone)."
    ),
    Spell('Pass Plant','D',5,
        cast=tp(7,S),
        duration_lvl=tp(1,R),
        sourcebook=V
    ),
    Spell('Spike Stones','D',5,
        cast=tp(6,S),
        duration=tp(1,VA),
        duration_lvl=tp(1,R),
        sourcebook=U,
        desc="This spell is the same as the 5th-level clerical spell of the same name."
    ),
    Spell('Sticks To Snakes','D',5,
        cast=tp(7,S),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="Except as noted above, and for the fact that the material component of the spell is typical for druids, this is the same as the 4th level cleric Sticks To Snakes spell (q.v.)."
    ),
    Spell('Transmute Rock To Mud','D',5,
        cast=tp(7,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell turns natural rock of any sort into an equal volume of mud. The depth of the mud can never exceed one-half its length and/or breadth. If it is cast upon a rock, for example, the rock affected will collapse into mud. Creatures unable to levitate, fly, or otherwise free themselves from the mud will sink and suffocate, save for lightweight creatures which could normally pass across such ground. The mud will remain until a dispel magic spell or a reverse of this spell, Mud To Rock, restores its substance - but not necessarily its form. Evaporation will turn the mud to normal dirt, from 1 to 6 days per cubic 1\" being required. The exact time depends on exposure to sun, wind and normal drainage. The Mud To Rock reverse will harden normal mud into soft stone (sandstone or similar mineral) permanently unless magically changed."
    ),
    Spell('Wall of Fire','D',5,
        cast=tp(7,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="The Wall Of Fire spell brings forth a blazing curtain of magical fire of shimmering colour - yellow-green or amber in case of druidical magic. The Wall Of Fire inflicts 4 to 16 hit points of damage, plus 1 hit point of damage per level of the spell caster, upon any creature passing through it. Creatures within 1\" of the wall take 2-8 hit points of damage, those within 2\", take 1-4 hit points of damage. Creatures especially subject to fire may take additional damage, and undead always take twice normal damage. Only the side of the wall away from the spell caster will inflict damage. The opaque Wall Of Fire lasts for as long as the druid concentrates on maintaining it, or 1 round per level of experience of the druid in the event he or she does not wish to concentrate upon it. The spell creates a sheet of flame up to 2\" square per level of the spell caster, or as a ring with a radius of up to ½\" per level of experience from the druid to its flames, and a height of 2\". The former is stationary, while the latter moves as the druid moves."
    ),
    Spell('Animal Summoning III','D',6,
        cast=tp(8,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell is the same in duration and effect as the 4th level Animal Summoning I spell except that up to 4 animals of no more than 16 hit dice each can be summoned, or eight of no more than 8 hit dice, or 16 creatures of no more than 4 hit dice each can be summoned."
    ),
    Spell('Anti-Animal Shell','D',6,
        cast=tp(1,R),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="By casting this spell the druid brings into being a hemispherical force field which prevents the entrance of any sort of animal matter of normal (not magical) nature. Thus, a giant would be kept out, but undead could pass through the shell of force, as could such monsters as aerial servants, demons, devils, etc. The Anti-Animal Shell lasts for 1 turn for each level of experience the druid has attained."
    ),
    Spell('Conjure Fire Elemental','D',6,
        cast=tp(6,R),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="Upon casting a Conjure Fire Elemental spell, the druid opens a special gate to the Elemental Plane of Fire, and a strong fire elemental (see ADVANCED DUNGEONS & DRAGONS, MONSTER MANUAL) is summoned to the vicinity of the spell caster. It is 85% likely that a 16 die elemental will appear, 9% likely that 2 to 4 salamanders (q.v.) will come, a 4% chance exists that an efreeti (q.v.) will come, and a 2% chance exists that a huge fire elemental of 21 to 24 hit dice (d4 + 20) will appear. Because of the relationship of druids to natural and elemental forces, the conjuring druid need not fear that the elemental force summoned will turn on him or her, so concentration upon the activities of the fire elemental (or other creature, summoned) or the protection of a magic circle is not necessary. The elemental summoned will help the druid however possible, including attacking opponents of the druid. The fire elemental or other creature summoned remains for a maximum of 1 turn per level of the druid casting the spell - or until it is sent back by attack, a Dispel Magic spell or the reverse of the spell (Dismiss Fire Elemental). Only a druid can dismiss summoned salamanders, efreeti, or ultra-powerful elemental."
    ),
    Spell('Cure Critical Wounds','D',6,
        cast=tp(8,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell is the same as the 5th level cleric Cure Critical Wounds spell (q.v.), with the exception of the fact that the spell requires the use of any sort of mistletoe."
    ),
    Spell('Feeblemind','D',6,
        cast=tp(8,S),
        duration=tp(1,P),
        sourcebook=V
    ),
    Spell('Fire Seeds','D',6,
        cast=tp(1,VA),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="The spell of Fire Seeds creates special missiles or timed incendiaries which burn with great heat. The druid may hurl these seeds up to 4\" or place them to ignite upon a command word. Acorns become fire seed missiles, while holly berries are used as the timed incendiaries. The spell creates up to four acorn fire seeds or eight holly berry fire seeds. The acorns burst upon striking their target, causing 2 to 16 hit points (2d8) of damage and igniting any combustible materials within a 1\" diameter of the point of impact. Although the holly berries are too light to make effective missiles, they can be placed, or tossed up to 6' away, to burst into flame upon a word of command. The berries ignite causing 1 to 8 hit points (d8) of damage to any creature in a ½\" diameter burst area, and their fire ignites combustibles in the burst area. The command range for holly berry fire seeds is 4\". All fire seeds lose their power after the expiration of 1 turn per level of experience of the druid casting the spell, i.e. a 13th level druid has fire seeds which will remain potent for a maximum of 13 turns after their creation. Targets of acorn fire seeds must be struck by the missile. If a saving throw is made, creatures within the burst area take only one-half damage, but creatures struck directly always take full damage. Note that no mistletoe or other material components beyond acorns or holly berries are needed for this spell."
    ),
    Spell('Liveoak','D',6,
        cast=tp(1,T),
        duration_lvl=tp(1,D),
        sourcebook=U,
        desc="This spell enables the druid to select a healthy oak tree and cast a dweomer upon it so as to cause it to serve as a protector. The spell can be cast on but a single tree at a time, and while a liveoak cast by a particular druid is in effect, he or she cannot cast another such spell. The tree upon which the dweomer is cast must be within 10 feet of the druid's dwelling place, within a place sacred to the druid, or within 10' of something the druid wishes to guard or protect. The liveoak spell can be cast upon a healthy tree of small, medium, or large size according to desire and availability. A \"triggering\" phrase of up to a maximum of one word per level of the spell caster is then placed upon the dweomered oak; for instance \"Attack any persons who come near without first saying 'sacred mistletoe'\" is an 11-word trigger phrase that could be used by a druid of 11th or higher level casting the spell. The liveoak triggers the tree into becoming a treant of appropriate size and attack capability, matching the specifications of the Monster Manual description, but with only a 3\" movement rate. An oak enchanted by this spell will radiate a magic aura, and can be returned to normal by a successful casting of dispel magic or upon the desire of the druid who enchanted it. The druid needs mistletoe to cast this spell."
    ),
    Spell('Transmute Water To Dust','D',6,
        cast=tp(8,S),
        duration=tp(1,P),
        sourcebook=U,
        desc=("When this spell is cast, the subject area instantly undergoes a change from liquid to powdery dust. Note that if the water is already muddy, the area of effect will be expanded to double normal, while if wet mud is concerned the area of effect will be quadrupled. If water remains in contact with the transmuted dust, the former will quickly permeate the latter, turning dust into silty mud if a sufficient quantity of water exists to do so, otherwise soaking or dampening the dust accordingly."
            "Only liquid actually existing in the area of effect at the moment of spell casting is affected. Liquids which are only partially water will be affected insofar as the actual water is concerned, except that potions which contain water as a component part will be rendered useless. Living creatures are unaffected, except for those native to the Elemental Plane of Water. Such creatures receive a saving throw versus spell to escape the effect, and only one such creature can be affected by any single casting of this spell, regardless of the creature's size or the size of the spell's area of effect. The reverse of the spell is simple a very high-powered create water spell which requires a pinch of normal dust as an additional material component. For either usage of the spell, other components required are diamond dust of at least 500 gp value, a bit of seashell, and the druid's mistletoe."
        )
    ),

    Spell('Transport Via Plants','D',6,
        cast=tp(3,S),
        duration=tp(1,D),
        sourcebook=V,
        desc="By means of this spell, the druid is able to enter any large plant and pass any distance to a plant of the same species in o single round regardless of the distance separating the two. The entry plant must be alive. The destination plant need not be familiar to the druid, but it also must be alive. If the druid is uncertain of the destination plant, he or she need merely determines direction and distance, and the Transport Via Plants spell will move him or her as near as possible to the desired location. There is a basic 20% chance, reduced 1% per level of experience of the druid, that the transport will deliver the druid to an allied species of plant from 1 to 100 miles removed from the desired destination plant. If a particular destination plant is desired, but the plant is not living, the spell fails, and the druid must come forth from the entrance plant within 24 hours. Harm to a plant housing a druid can affect the druid (cf. Plant Door)."
    ),
    Spell('Turn Wood','D',6,
        cast=tp(8,S),
        duration_lvl=tp(4,R),
        sourcebook=V,
        desc="When this spell is cast, waves of force roll forth from the druid, moving in the direction he or she faces, and causing all wooden objects in the path of the spell to be pushed away from the druid to the limit of the area of effect. Wooden objects above three inches diameter which are fixed firmly will not be affected, but loose objects (movable mantlets, siege towers, etc.) will move back. Objects under 3 inches diameter which are fixed will splinter and break and the pieces will move with the wave of force. Thus, objects such as wooden shields, spears, wooden weapon shafts and hafts, and arrows and bolts will be pushed back, dragging those carrying them with them; and if a spear is planted in order to prevent this forced movement, it will splinter. The Turn Wood spell lasts for 4 rounds per level of experience of the druid casting it, and the waves of force will continue to sweep down the set path for this period. The wooden objects in the area of effect are pushed back at a rate of 4\" per melee round. The length of the path is 2\" per level of the druid, i.e. a 14th level druid casts a Turn Wood spell with an area of effect 12\" wide by 28\" long, and the spell would last for 56 rounds (5.6 turns). As usual, the above assumes the druid is using greater mistletoe when casting the spell. Note that after casting the spell the path is set, and the druid may then do other things or go elsewhere without affecting the spell's power."
    ),
    Spell('Wall of Thorns','D',6,
        cast=tp(8,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="The Wall Of Thorns spell creates a barrier of very tough, pliable green angled brush bearing needle-sharp thorns as long as a person's finger. Any creature breaking through (or merely impacting upon) the Wall Of Thorns takes 8 hit points of damage plus an additional amount of hit points equal to the creature's armour class, i.e. 10 or fewer additional hit points of damage, with negative armour classes subtracting from the base 8 hit points of damage. Any creature within the area of effect of the spell when it is cast is considered to have impacted on the wall of thorns and in addition must break through to gain movement space. The damage is based on each 1\" thickness of the barrier. If the Wall Of Thorns is chopped at, it will take at least 4 turns to cut a path through a 1\" thickness. Normal fire will not harm the barrier, but magical fires will burn away the barrier in 2 turns with the effect of creating a wall of fire while doing so (see Wall Of Fire spell.) The nearest edge of the Wall Of Thorns appears up to 8\" distant from the druid, as he or she desires. The spell lasts for 1 turn for each level of experience of the druid casting it, and covers an area of ten cubic inches per level of the caster in whatever form the caster desires. Thus a 14th level druid could create a Wall Of Thorns 7\" long by 2\" high (or deep) by)\" deep (or high), a 1\" high by 1\" wide by 14\" long wall to block a dungeon passage, or any other sort of shape that suited his or her needs."
    ),
    Spell('Weather Summoning','D',6,
        cast=tp(1,T),
        duration=tp(1,VA),
        sourcebook=V,
        desc="The druidic Weather Summoning spell is similar to the Control Weather spell (q.v.) of clerical nature. By casting the spell, the druid calls forth weather commensurate with the climate and season of the area he or she is in at the time, Thus, in spring a tornado, thunderstorm, cold, sleet storm, or hot weather could be summoned. In summer a torrential rain, heat wave, hail storm, etc. can be called for. In autumn, hot or cold weather, fog, sleet, etc. could be summoned. Winter allows great cold, blizzard, or thaw conditions to be summoned. Hurricane-force winds can be summoned near coastal regions in the late winter or early spring. The summoned weather is not under the control of the druid. It might last but a single turn in the case of a tornado, or for hours or even days in other cases. The area of effect likewise varies from about 1 square mile to 100 or more square miles. Note that several druids can act in concert to greatly affect weather, controlling winds and/or working jointly to summon very extreme weather conditions. Within 4 turns after the spell is cast, the trend of the weather to come will be apparent, i.e., clearing skies, gusts of warm or hot air, a chill breeze, overcast skies, etc. Summoned weather will arrive 6 to 17 turns (d12 + 5) after the spell is cast. Anything less than greater mistletoe as the material component will sharply curtail the weather extremes desired."
    ),
    Spell('Animate Rock','D',7,
        cast=tp(9,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="By employing an Animate Rock spell, the druid causes a lithic object of a size up to that indicated to move (see Animate Object, the sixth level cleric spell.) The animated stone object must be separate, i.e. not a piece of a huge boulder or the like. It will follow the desire of the druid casting the spell - attacking, breaking objects, blocking - while the magic lasts. It has no intelligence nor volition of its own, but it follows instructions exactly as spoken. Note that only one set of instructions for one single action (the whole being simply worded and very brief - 12 words or so), can be given to the rock animated. The rock remains animated for 1 melee round per level of experience of the spell caster, and the volume of rock which can be animated is also based on the experience level of the druid - 2 cubic feet of stone per level, i.e. 24 cubic feet at the 12th level."
    ),
    Spell('Changestaff','D',7,
        cast=tp(3,S),
        duration_lvl=tp(1,T),
        sourcebook=U,
        desc=("By means of this spell, the druid is able to change his or her staff from a pole of dead wood into a treant of largest size. In order to cast the dweomer, the druid must first have located a tree struck by lightning within the past 24 hours (1%-5% chance for any given tree, depending on the severity of the storm). He or she must then select a sound limb, remove it from the tree, and prepare a specially cured section. This section must be shaped and carved so as to be ready to accept the magic which the druid will then place upon it. The staff must be of ash, oak, or yew wood. Curing by sun drying and special smoke requires 28 days. Shaping, carving, smoothing, and polishing require another 28 days. The druid cannot adventure or engage in other strenuous activity during either of these periods. The finished staff, engraved with scenes of woodland life, is then rubbed with the juice of holly berries, and the end of it is thrust into the earth of the druid's grove while he or she speaks with plants, calling upon the staff to assist in time of need. The item is then charged with a dweomer which will last for many changes from staff to treant and back again.\n\n"
            "While the staff/treant will initially be of largest size and greatest number of hit points, each 8 points of damage it accumulates actually reduces it by 1 hit die. The staff begins at 12 hit dice and 96 hit points, goes to 11 and 88, 10 and 80, 9 and 72, etc. As it loses hit dice, it becomes smaller in size, thus losing attack power as well. If and when the staff/treant is brought below 7 hit dice, the thing crumbles to sawdust-like powder and is lost. The staff cannot ever be brought upwards in hit dice or hit points, except by a wish (which restores it completely). Of course, a new staff can always be sought out, seasoned, as so forth, to begin the process anew.\n\n"
            "When the druid plants the end of the staff in the ground and speaks a special command prayer and invocation, the staff turns into a treant. It can and will defend the druid, or obey him or her in any way. However, it is by no means a true treant, and it cannot converse with actual treants. The transformation lasts for as many turns as the druid has levels of experience, until the druid commands the thing to return to its true form, or until the thing is destroyed, whichever first occurs. In order to cast a changestaff spell, the druid must have either mistletoe or leaves (ash, oak, or yew) of the same sort as the staff."
        )
    ),
    Spell('Chariot of Sustarre','D',7,
        cast=tp(1,T),
        duration=tp(6,T),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="When this spell is cast by a druid, it brings forth a large flaming chariot pulled by two fiery horses which appear in a clap of thunder amidst cloud-like smoke. This vehicle moves at 24\" on the ground, 48\" flying, and it can carry the druid and up to 8 other man-sized creatures whom he or she first touches so as to enable these creatures to be able to ride aboard this burning transport. Creatures other than the druid and his or her designated passengers will sustain damage equal to that of a Wall Of Fire spell if they are within 5' of the horses or chariot, voluntarily or involuntarily. The druid controls the chariot by verbal command, causing the flaming steeds to stop or go, walk, trot, run or fly, turning left or right as he or she desires. Note that the Chariot Of Sustarre is a physical manifestation, and can sustain damage. The vehicle and steeds are struck only by magical weapons or by water one quart of which will cause 1 hit point of damage), they are armour class 2, and each requires 30 hit points of damage to dispel. Naturally, fire has absolutely no effect upon either the vehicle or its steeds, but magical fires will affect the riders if they are exposed to them (other than those of the chariot itself). In addition to mistletoe, the druid casting this spell must have a small piece of wood, 2 holly berries, and a fire source at least equal too torch."
    ),
    Spell('Confusion','D',7,
        cast=tp(9,S),
        duration_lvl=tp(1,R),
        sourcebook=V
    ),
    Spell('Conjure Earth Elemental','D',7,
        cast=tp(1,T),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="When a druid casts a Conjure Earth Elemental spell, he or she summons an earth elemental of 16 hit dice to do the druid's bidding. Furthermore, the druid need but command it, and then do as he or she desires, for the elemental does not regard the druid who conjured it with enmity. The elemental remains until destroyed, dispelled, or sent away by dismissal (cf. Conjure Fire Elemental)."
    ),
    Spell('Control Weather','D',7,
        cast=tp(1,T),
        duration=tp(1,VA),
        sourcebook=V,
        desc="The druidic Control Weather spell is more powerful than the clerical spell of the same name (q.v.). The spell caster is able to change weather by two places from the prevailing conditions if greater mistletoe is used. It otherwise is the same as the 7th level cleric Control Weather spell."
    ),
    Spell('Creeping Doom','D',7,
        cast=tp(9,S),
        duration_lvl=tp(4,R),
        sourcebook=V,
        desc="When the druid utters the spell of Creeping Doom, he or she calls forth a mass of from 500 to 1000 (d6 + 4) venomous, biting and stinging arachnids, insects and myriapods. This carpet-like mass will swarm in an area of 2\" square, and upon command from the druid will creep forth at 1\" per round towards any prey within 8\", moving in the direction in which the druid commanded. The Creeping Doom will slay any creature subject to normal attacks, each of the small horrors inflicting 1 hit point of damage (each then dies after their attack), to that up to 1,000 hit points of damage can be inflicted on creatures within the path of the Creeping Doom. If the Creeping Doom goes beyond 8\" of the summoner, it loses 50 of its number for each 1\" beyond 8\", i.e. at 10\" its number has shrunk by 100. There are a number of ways to thwart or destroy the creatures forming the swarm, all of which methods should be obvious."
    ),
    Spell('Finger of Death','D',7,
        cast=tp(5,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="The Finger Of Death spell causes the victim's heart to stop. The druid utters the incantation, points his or her index finger at the creature to be slain, and unless the victim succeeds in making the appropriate saving throw, death occurs. A successful saving throw negates the spell."
    ),
    Spell('Fire Storm','D',7,
        cast=tp(9,S),
        duration=tp(1,R),
        sourcebook=V,
        desc="When a Fire Storm spell is cast by a druid, a whole area is shot through with sheets of roaring flame which are equal to a Wall Of Fire (q.v.) in effect. Creatures within the area of fire and 1\" or less from the edge of the affected area receive 2 to 16 hit points of damage plus additional hit points equal to the number of levels of experience of the druid unless they make a saving throw, in which case they take only one-half damage. The area of effect is equal to 2 cubic\" per level of the druid, i.e. a 13th level druid can cast a Fire Storm which measures 13\" by 2\" by 1\". The height of the storm is 1\" or 2\"; the balance of its area must be in length and width. The reverse spell, Fire Quench, smothers double the area of effect of a Fire Storm with respect to normal fires, and with respect to magical fires it has a 5% chance per level of the caster of extinguishing a magical fire (such as a Fire Storm) of proportions up to the normal area of effect of the non-reversed spell."
    ),
    Spell('Reincarnate','D',7,
        cast=tp(1,T),
        duration=tp(1,P),
        sourcebook=V
    ),
    Spell('Sunray','D',7,
        cast=tp(3,S),
        duration=tp(1,R),
        sourcebook=U,
        desc=("When a sunray spell is cast, the druid evokes a burning beam of light which is similar to a ray of actual sunlight in all important aspects. It inflicts blindness for 1-3 rounds upon all creatures within its area of effect unless a successful saving throw versus spell is made. Creatures using ultravision at the time may be blinded for 2-8 rounds, while those to whom sunlight is harmful or unnatural will suffer permanent blindness unless the save is made, in which case blindness lasts for 2-12 rounds. Those within its area of effect, as well as creatures within 2\" of its perimeter, will have no infravisual capabilites for 2-5 rounds.\n\n"
            "Undead (including vampires) caught within its main area of effect must save versus spell, taking 8-48 points of damage or half damage if a save is made. Those within the secondary area of effect (up to 2\" from the perimeter) take 3-18 points of damage or no damage if save is made. The ultraviolet light generated by the spell will inflict damage on fungoid creatures and subterranean fungi just as if they were undead, but no saving throw is possible. The material components are an aster seed and a piece of aventurine feldspar (sunstone)."
        )
    ),
    Spell('Transmute Metal To Wood','D',7,
        cast=tp(9,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="The Transmute Metal To Wood spell allows the druid casting it to change an object from metal to wood. The volume of metal is equal to a maximum weight of 80 gold pieces per level of experience. Magical objects of metal are only 10% likely to be affected by the spell. Note that even a Dispel Magic spell will not reverse the spell effects. Thus, a metal door changed to wood would be forevermore a wooden door."
    ),
]

mu_spells = [
    Spell('Affect Normal Fires','M',1,
        cast=tp(1,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell enables the magic-user to cause small fires - from as small as a torch or lantern to as large as a normal bonfire of 3' maximum diameter - to reduce in size and light to become match-like or increase in light so as to become as bright as a light spell. Reducing the fire will cut fuel consumption to half normal, and increasing the fire will double consumption. Note that heat output is not altered in either case!"
    ),
    Spell('Alarm','M',1,
        cast=tp(1,R),
        duration=tp(1,VA),
        duration_lvl=tp(1,T),
        sourcebook=U,
    ),
    Spell('Armor','M',1,
        cast=tp(1,R),
        duration=tp(1,P),
        sourcebook=U,
    ),
    Spell('Burning Hands','M',1,
        cast=tp(1,S),
        duration=tp(1,R),
        sourcebook=V,
        desc="When the magic-user casts this spell, jets of searing flame shoot from his or her fingertips. Hands can only be held so as to send forth a fan-like sheet of flames, as the magic-user's thumbs must touch each other and fingers must be spread. The burning hands send out flame jets of 3' length in a horizontal arc of about 120° in front of the magic-user. Any creature in the area of flames takes 1 hit point of damage for each level of experience of the spellcaster, and no saving throw is possible. Inflammable materials touched by the fire will burn, i.e. cloth, paper, parchment, thin wood, etc."
    ),
    Spell('Charm Person','M',1,
        cast=tp(1,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="Except as shown above, this spell is the same as the second level druid spell, Charm Person Or Mammal (q.v.), but the magic-user can charm only persons, i.e. brownies, dwarves, elves, gnolls, gnomes, goblins, half-elves, halflings, half-orcs, hobgoblins, humans, kobolds, lizard men, nixies, orcs, pixies, sprites, and troglodytes. All other comments regarding spell effects apply with respect to persons."
    ),
    Spell('Comprehend Languages','M',1,
        cast=tp(1,R),
        duration_lvl=tp(5,R),
        sourcebook=V,
        desc="When this spell is cast, the magic-user is able to read an otherwise incomprehensible written message such as a treasure map (but not a magical writing, other than to know it is \"magic\") or understand the language of a speaking creature. In either case, the magic-user must touch the object to be read or the creature to be understood, and the spell does not enable the spell caster to write or speak the language. The material components of this spell are a pinch of soot and a few grains of salt. The reverse, Confuse Languages, prevents comprehension or cancels a Comprehend Languages spell."
    ),
    Spell('Dancing Lights','M',1,
        cast=tp(1,S),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="When a dancing lights spell is cast, the magic-user creates, at his or her option, from 1 to 4 lights which resemble either A) torches and/or lanterns (and cast that amount of light), B) glowing spheres of light (such as evidenced by will-o-wisps), or C) one faintly glowing, vaguely man-like shape, somewhat similar to that of a creature from the Elemental Plane of Fire. The Dancing Lights move as the spell caster desires, forward or back, straight or turning corners, without concentration upon such movement by the magic-user. The spell will wink out if the range or duration is exceeded. Range is a base of 4\" plus 1\" for each level of the magic-user who cast the spell. Duration is 2 melee rounds per level of the spell caster . The material component of this spell is either a bit of phosphorus or wytchwood or a glowworm."
    ),
    Spell('Detect Magic','M',1,
        cast=tp(1,S),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="The only differences between this spell and the first level cleric Detect Magic spell are noted above (duration, area of effect, and no material component)."
    ),
    Spell('Enlarge','M',1,
        cast=tp(1,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="This spell causes instant growth of a creature or object. Enlargement causes increase in both size and weight. It can be cast upon only a single creature or object. Spell range is ½\" for each level of experience of the magic-user, and its duration is 1 turn per level of power experience of the spell caster . The effect of the enlargement spell is to increase the size of a living creature (or a symbiotic or community entity) by 20% per level of experience of the magic-user, with a maximum additional growth of 200%. The effect on objects is one-half that of creatures, i.e. 10% per level to a 100% maximum additional enlargement. The creature or object must be seen in order to effect the spell. The maximum volume of living material which can be initially affected is 10 cubic feet - for non-living matter, 5 cubic feet - per level of the magic-user. While magical properties are not increased by this spell - a huge +1 sword is still only +1, a staff-sized wand is still only capable of its normal functions, a giant-sized potion merely requires a greater fluid intake to make its magical effects operate, etc. - weight, mass and strength are. Thus, a table blocking a door would be heavier and more effective; a hurled stone would have more mass (and be more hurtful providing enlargement took place just prior to impact): chains would be more massive; doors thicker; a thin line turned to a sizable, longer rope; and so on. Likewise, a person 12' tall would be as an ogre, while an 18' tall person would actually be a giant for the duration of the spell. The reverse spell, Reduce, will negate the effects or actually make creatures or objects smaller in the tame ratios as the regular spell application functions. Unwilling victims of the spell. or its reverse, are entitled to a saving throw, which, if successful, indicates the magic does not function, and the spell is wasted. The material component of this spell is a pinch of powdered iron. "
    ),
    Spell('Erase','M',1,
        cast=tp(1,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="The Erase spell removes writings of either magical or mundane nature from a scroll or one or two pages or sheets of paper, parchment or similar surfaces. It will not remove Explosive Runes or a Symbol (see these spells hereafter), however. There is a basic chance of 50%, plus 2% per level of experience of the spell caster with respect to magical writings, plus 4% per level for mundane writing, that the spell will take effect. This represents the saving throw, and any percentile dice score in excess of the adjusted percentage chance means the spell fails."
    ),
    Spell('Feather Fall','M',1,
        cast=tp(Decimal(0.1),S),
        duration_lvl=tp(1,S),
        sourcebook=V,
        desc="When this spell is cast, the creature(s) or object(s) affected immediately assumes the mass of a feathery piece of down. Rate of falling is thus instantly changed to a mere constant 2' per second or 12' per segment, and no damage is incurred when landing when the spell is in effect. However, when the spell duration ceases, normal rate of fall occurs. The spell can be cast upon the magic-user or some other creature or object up to the maximum range of 1\" per level of experience of the spell caster. it lasts for 1 segment for each level of the magic-user. The Feather Fall affects an area of 1 cubic inch, and the maximum weight of creatures and/or objects cannot exceed a combined total equal to a base 2,000 gold pieces weight plus 2,000 gold pieces weight per level of the spell caster. Example: a 2nd level magic-user has a range of 2\", a duration of 2 segments, a weight maximum of 6,000 gold pieces (600 pounds) when employing the spell. The spell works only upon free-falling or propelled objects. It will not affect a sword blow or a charging creature, but it will affect a missile. The material component is a small feather or a piece of down somewhere on the person of the spell caster."
    ),
    Spell('Find Familiar','M',1,
        cast=tp(1,VA),
        duration=tp(1,P),
        sourcebook=V
    ),
    Spell('Firewater','M',1,
        cast=tp(1,S),
        duration=tp(1,R),
        sourcebook=U,
    ),
    Spell('Friends','M',1,
        cast=tp(1,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="A Friends spell causes the magic-user to gain a temporary increase of 2-8 points in charisma - or a temporary lowering of charisma by 1-4 points - depending on whether creatures within the area of effect of the spell make - or fail - their saving throw versus magic. Those that fail their saving throw will be very impressed with the spell caster and desire greatly to be his or her friend and help. Those that do not fail will be uneasy in the spell caster's presence and tend to find him or her irritating. Note that this spell has absolutely no effect on creatures of animal intelligence or lower. The components for this spell are chalk (or white flour), lampblack (or soot), and vermilion applied to the face before casting the spell."
    ),
    Spell('Grease','M',1,
        cast=tp(1,S),
        duration=tp(1,P),
        sourcebook=U,
    ),
    Spell('Hold Portal','M',1,
        cast=tp(1,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell magically bars a door, gate or valve of wood, metal or stone. The magical closure holds the portal fast just as if it were securely stopped and locked. The range of the spell is 2' per level of experience of the caster, and it lasts for 1 round per level. Note that any extra-dimensional creature (demon, devil, elemental, etc.) will shatter such a held portal. A magic-user of four or more experience levels higher than the spell caster can open the held portal at will. A Knock spell (q.v.) or Dispel Magic spell (q.v.) will negate the Hold Portal. Held portals can be broken or battered down."
    ),
    Spell('Identify','M',1,
        cast=tp(1,T),
        duration_lvl=tp(1,S),
        sourcebook=V,
        desc="When an Identify spell is cast, one item may be touched and handled by the magic-user in order that he or she may possibly find what dweomer it possesses. The item in question must be held or worn as would be normal for any such object. i.e. a bracelet must be placed on the spell caster's wrist, a helm on his or her head, boots on the feet, a cloak worn, a dagger held, and so on. Note that any consequences of this use of the item fall fully upon the magic-user, although any saving throw normally allowed is still the privilege of the magic-user. For each segment the spell is in force, it is 15% + 5% per level of the magic-user probable that 1 property of the object touched can become known - possibly that the item has no properties and is merely a ruse (the presence of Nystul's Magic Aura or a Magic Mouth being detected). Each time a property can be known, the referee will secretly roll to see if the magic-user made his or her saving throw versus magic. If the save was successful, the property is known; if it is 1 point short, a false power will be revealed; and if it is lower than 1 under the required score no information will be gained. The item will never reveal its exact plusses to hit or its damage bonuses, although the fact that it has few or many such plusses can be discovered. If it has charges, the object will never reveal the exact number, but it will give information which is +/-25% of actual i.e. a wand with 40 charges could feel as if it had 30, or 50, or any number in between. The item to be identified must be examined by the magic-user within 1 hour per level of experience of the examiner after it has been discovered, or all readable impressions will have been blended into those of the characters who have possessed it since. After casting the spell and determining what can be learned from it, the magic-user loses 8 points of constitution. He or she must rest for 6 turns per 1 point in order to regain them. If the 8 point loss drops the spell caster below a constitution of 3, he or she will fall unconscious, and consciousness will not be regained until full constitution is restored 24 hours later. The material components of this spell are a pearl (of at least 100g.p. value) and an owl feather steeped in wine, with the infusion drunk and a live miniature carp swallowed whole prior to spell casting. If a luckstone is powdered and added to the infusion, probability increases 25% and all saving throws are made at +4."
    ),
    Spell('Jump','M',1,
        cast=tp(1,S),
        duration=tp(1,T),
        sourcebook=V,
        desc="When this spell is cast, the individual is empowered to leap up to 30' forward or 10' backward or straight upward. Horizontal leaps forward or backward are in only a slight arc - about 2'/10' of distance travelled. The Jump spell does not insure any safety in landing or grasping at the end of the leap. For every 3 additional levels of experience of the magic-user beyond the 1st, he or she is able to empower 1 additional leap, so a 4th level magic-user can cast a Jump spell which enables the recipient to make 2 leaps, 3 leaps at 7th level, etc. All leaps must be completed within 1 turn after the spell is cast, for after that period has elapsed the spell wears off. The material component of this spell is a grasshopper's hind leg, one for each leap, to be broken when the leap is made."
    ),
    Spell('Light','M',1,
        cast=tp(1,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="With the exceptions noted above, this spell is the same as the first level cleric Light spell (q.v.)."
    ),
    Spell('Magic Missile','M',1,
        cast=tp(1,S),
        duration=tp(0),
        sourcebook=V,
        desc="Use of the Magic Missile spell creates one or more magical missiles which dart forth from the magic-user's fingertip and unerringly strike their target. Each missile does 2 to 5 hit points (d4+1) of damage. If the magic-user has multiple missile capability, he or she can have them strike a single target creature or several creatures, as desired. For each level of experience of the magic-user, the range of his or her Magic Missile extends 1\" beyond the 6\" base range. For every 2 levels of experience, the magic-user gains an additional missile, i.e. 2 at 3rd level, 3 at 5th level, 4 at 7th level, etc."
    ),
    Spell('Melt','M',1,
        cast=tp(1,S),
        duration_lvl=tp(1,R),
        sourcebook=U,
    ),
    Spell('Mending','M',1,
        cast=tp(1,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell repairs small breaks in objects. It will weld a broken ring, chain link, medallion or slender dagger, providing but one break exists. Ceramic or wooden objects with multiple breaks can be invisibly rejoined to be as strong as new. A hole in a leather sack or wineskin is completely healed over by a mending spell. This spell will not repair magic items of any kind. The material components of this spell are two small magnets of any type (lodestone in all likelihood) or two burrs."
    ),
    Spell('Message','M',1,
        cast=tp(1,S),
        duration=tp(5,S),
        duration_lvl=tp(1,S),
        sourcebook=V,
        desc="When this spell is cast, the magic-user can whisper a message and secretly, or openly, point his or her finger while so doing, and the whispered message will travel in a straight line and be audible to the creature pointed at. The message must fit spell duration, and if there is time remaining, the creature who received the message can whisper a reply and be heard by the spell caster. Note that there must be an open and unobstructed path between the spell caster and the recipient of the spell. The material component of the spell is a short piece of copper drawn fine."
    ),
    Spell('Mount','M',1,
        cast=tp(1,R),
        duration=tp(12,T),
        duration_lvl=tp(6,T),
        sourcebook=U,
    ),
    Spell('Nystul\'s Magic Aura','M',1,
        cast=tp(1,R),
        duration_lvl=tp(1,D),
        sourcebook=V,
        desc="By means of this spell any one item of a weight of 50 g.p. per level of experience of the spell caster can be given an aura which will be noticed if detection of magic is exercised upon the object. If the object bearing the Nystul's Magic Aura is actually held by the creature detecting for a dweomer, he, she or it is entitled to a saving throw versus magic, and if this throw is successful, the creature knows that the aura has been placed to mislead the unwary. Otherwise, the aura is simply magical, but no amount of testing will reveal what the magic is. The component for this spell is a small square of silk which must be passed over the object to bear the aura."
    ),
    Spell('Precipitation','M',1,
        cast=tp(1,S),
        duration_lvl=tp(1,S),
        sourcebook=U,
    ),
    Spell('Protection From Evil','M',1,
        cast=tp(1,S),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="With the differences shown above, and the requirement of powdered iron and silver as the material components for tracing the magic circle for Protection From Evil, the spell is the same as the first level cleric Protection From Evil spell (q.v.). "
    ),
    Spell('Push','M',1,
        cast=tp(1,S),
        duration=tp(0),
        sourcebook=V,
        desc="Upon pronouncing the syllables of this spell, the magic-user causes an invisible force to strike against whatever object he or she is pointing at. The force of the Push is not great, being 1 foot- pound per level of the magic-user casting the spell, but it can move small objects up to 1' in a direction directly away from the caster, topple an object under the proper conditions, or cause a creature to lose its balance. An example of the latter use is causing a creature attacking to lose its balance when it is attacking, for if the creature fails its saving throw, it will not be able to attack that round. Of course, the mass of the creature attacking cannot exceed the force of the Push by more than a factor of 50, i.e. a 1st level magic-user cannot effectively push a creature weighing more than 50 pounds. A Push spell employed against an object held by a creature will cause it to subtract the force of the spell in foot- pounds (1,2,3, etc.) from its chance to hit or add to opponent saving throws as applicable if the creature fails to make its saving throw against magic when the spell is cast. The material component of this spell is a small pinch of powdered brass which must be blown from the palm prior to pointing at the object of the spell."
    ),
    Spell('Read Magic','M',1,
        cast=tp(1,R),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="By means of a Read Magic spell, the magic-user is able to read magical inscriptions on objects - books, scrolls weapons and the like - which would otherwise be totally unintelligible to him or her. (The personal books of the magic-user, and works already magically read, are intelligible.) This deciphering does not normally invoke the magic contained in the writing, although it may do so in the case of a curse scroll. Furthermore, once the spell is cast and the magic-user has read the magical inscription, he or she is thereafter able to read that particular writing without recourse to the use of the Read Magic spell. The duration of the spell is 2 rounds per level of experience of the spell caster. The material component for the spell is a clear crystal or mineral prism. Note that the material is not expended by use. The reverse of the spell, Unreadable Magic, makes such writing completely unreadable to any creature, even with the aid of a Read Magic, until the spell wears off or the magic is dispelled. The material components for the reverse spell are a pinch of dirt and a drop of water."
    ),
    Spell('Run','M',1,
        cast=tp(1,R),
        duration=tp(1,VA),
        sourcebook=U,
    ),
    Spell('Shield','M',1,
        cast=tp(1,S),
        duration_lvl=tp(5,R),
        sourcebook=V,
        desc="When this spell is cast, an invisible barrier before the front of the magic-user comes into being. This Shield will totally negate magic missile attacks. It provides the equivalent protection of armour class 2 against hand hurled missiles (axes, darts, javelins, spears, etc.), armour class 3 against small device-propelled missiles (arrows, bolts, bullets, manticore spikes, sling stones, etc.), and armour class 4 against all other forms of attack. The Shield also adds +1 to the magic-user's saving throw dice vs. attacks which are basically frontal. Note that all benefits of the spell accrue only to attacks originating from the front facing the magic-user, where the Shield can move to interpose itself properly."
    ),
    Spell('Shocking Grasp','M',1,
        cast=tp(1,S),
        duration=tp(0),
        sourcebook=V,
        desc="When the magic-user casts this spell, he or she develops a powerful electrical charge which gives a jolt to the creature touched. The Shocking Grasp delivers from 1 to 8 hit points damage (d8), plus 1 hit point per level of the magic-user, i.e. a 2nd level magic-user would discharge a shock causing 3 to 10 hit points of damage. While the magic-user must only come close enough to his or her opponent to lay a hand on the opponent's body or upon an electrical conductor which touches the opponent's body, a like touch from the opponent does not discharge the spell."
    ),
    Spell('Sleep','M',1,
        cast=tp(1,S),
        duration_lvl=tp(5,R),
        sourcebook=V
    ),
    Spell('Spider Climb','M',1,
        cast=tp(1,S),
        duration=tp(1,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="A Spider Climb spell enables the recipient to climb and travel upon vertical surfaces just as a giant spider is able to do, i.e. at 3\" movement rate, or even hang upside down from ceilings. Note that the affected creature must have bare hands and feet in order to climb in this manner. During the course of the spell the recipient cannot handle objects which weigh less than 50 g.p., for such objects will stick to the creature's hands/feet, so a magic-user will find it virtually impossible to cast spells if under a Spider Climb dweomer. The material components of this spell are a drop of bitumen and a live spider, both of which must be eaten by the spell recipient."
    ),
    Spell('Taunt','M',1,
        cast=tp(1,R),
        duration=tp(0),
        sourcebook=U,
    ),
    Spell('Tenser\'s Floating Disc','M',1,
        cast=tp(1,S),
        duration=tp(3,T),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="With this spell, the caster creates the circular plane of null-gravity known as Tenser's Floating Disc after the famed wizard of that appellation (whose ability to locate treasure and his greed to recover every copper found are well known). The disc is concave, 3' in diameter, and holds 1,000 g.p. weight per level of the magic-user casting the spell. The disc floats at approximately 3' above the ground at all times and remains level likewise. It maintains a constant interval of 6' between itself and the magic-user if unbidden. It will otherwise move within its range, as well as along with him at a rate of 6\", at the command of the magic-user. If the spell caster moves beyond range, or if the spell duration expires, the floating disc winks out of existence and whatever it was supporting is precipitated to the surface beneath it. The material component of the spell is a drop of mercury."
    ),
    Spell('Unseen Servant','M',1,
        cast=tp(1,S),
        duration=tp(6,T),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="The Unseen Servant is a non-visible valet, a butler to step and fetch, open doors and hold chairs, as well as to clean and mend. The spell creates a force which is not strong, but which obeys the command of the magic-user. It can carry only light-weight items - a maximum of 200 gold pieces weight suspended, twice that amount moving across a relatively friction-free surface such as a smooth stone or wood floor. It can only open normal doors, drawers, lids, etc. The Unseen Servant cannot fight nor can it be killed, as it is a force rather than a creature. It can be magically dispelled, or eliminated after taking 6 hit points of magical damage. The material components of the spell are a piece of string and a bit of wood."
    ),
    Spell('Ventriloquism','M',1,
        cast=tp(1,S),
        duration=tp(2,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell enables the magic-user to make it sound as if his or her voice - or someone's voice or similar sound - is issuing from someplace else, such as from another creature, a statue, from behind a door, down a passage, etc. The spell caster is able to make his or her voice sound as if a different creature were speaking or making the noise; of course, in a language known by him or her, or a sound which the caster can normally make. With respect to such voices and sounds, there is a 10% chance per point of intelligence above 12 of the hearer that the ruse will be recognized. The material component of the spell is a small cone of parchment."
    ),
    Spell('Wizard Mark','M',1,
        cast=tp(1,S),
        duration=tp(1,P),
        sourcebook=U,
    ),
    Spell('Write','M',1,
        cast=tp(1,R),
        duration_lvl=tp(1,H),
        sourcebook=V,
        desc="By means of this spell a magic-user might be able to inscribe a spell to make a magical scroll he or she cannot understand at the time (due to level or lack of sufficient intelligence) into the tome or other compilation he or she employs to maintain a library of spells. The magic-user must make a saving throw versus magic to attempt the writing of any spell, +2 if it is only up to 1 level greater than he or she currently uses, 0 at 2 levels higher, and -1 per level from 3 levels higher onwards. If this throw fails, the magic user is subject to 1d4 of damage for every level of the spell he or she was attempting to transcribe into his or her magic book, and furthermore be knocked unconscious for a like number of turns. This damage, if not fatal, can only be healed at the rate of 1-4 points per day, as it is damage to psyche and body. Furthermore, a spell will take 1 hour per level to transcribe in this fashion, and during this period, the magic-user is in a trance state and can always be surprised by any foe. In addition to the writing surface upon which the spell is to be transcribed, the spell caster needs a fine ink composed of rare substances (minimum cost 200 g.p. per bottle, if available at all without manufacture by the magic user)."
    ),
    Spell('Audible Glamer','M',2,
        cast=tp(2,S),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="When the Audible Glamour spell is cast, the magic-user causes a volume of sound to arise, at whatever distance he or she desires (within range), and seeming to recede, close, or remain in a fixed place as desired. The volume of sound caused, however, is directly related to the level of the spell caster. The relative noise is based upon the lowest level at which the spell can be cast, 3rd level. The noise of the Audible Glamour at this level is that of 4 men, maximum. Each additional experience level adds a like volume, so at 4th level the magic-user can have the spell cause sound equal to that of 8 men, maximum. Thus, talking, singing, or shouting, and/or walking, marching or running sounds can be caused. The auditory illusion created by an Audible Glamour spell can be virtually any type of sound, but the relative volume must be commensurate with the level of the magic-user casting the spell. A horde of rats running and squeaking is about the some volume as 8 men running and shouting. A roaring lion is equal to the noise volume of 16 men, while a roaring dragon is equal to the noise volume of no fewer than 24 men. If a character states that he or she does not believe the sound, a saving throw is made, and if it succeeds, the character then hears nothing, or possibly just a faint sound. Note that this spell is particularly effective when cast in conjunction with Phantasmal Force (see below). The material component of the spell is a bit of wool or a small lump of wax."
    ),
    Spell('Bind','M',2,
        cast=tp(2,S),
        duration_lvl=tp(1,R),
        sourcebook=U,
    ),
    Spell('Continual Light','M',2,
        cast=tp(2,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell is the same as the second level cleric spell Continual Light except that the range is only 6\", not 12\", and it cannot be reversed by the caster."
    ),
    Spell('Darkness 15\' Radius','M',2,
        cast=tp(2,S),
        duration=tp(1,T),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell causes total, impenetrable darkness in the area of its effect. Infravision or ultravision are useless. Neither normal nor magical light will work unless a Light or Continual Light spell is used. In the former event, the darkness spell is negated by the Light spell and vice versa. The material components of this spell area bit of bat fur and either a drop of pitch or a piece of coal."
    ),
    Spell('Deeppockets','M',2,
        cast=tp(1,T),
        duration=tp(24,T),
        duration_lvl=tp(6,T),
        sourcebook=U,
    ),
    Spell('Detect Evil','M',2,
        cast=tp(2,S),
        duration_lvl=tp(5,R),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the first level cleric Detect Evil (q.v.)."
    ),
    Spell('Detect Invisibility','M',2,
        cast=tp(2,S),
        duration_lvl=tp(5,R),
        sourcebook=V,
        desc="When the magic-user casts a Detect Invisibility spell, he or she is able to clearly see any objects which are invisible, as well as astral, ethereal, hidden, invisible or out of phase creatures. Detection is in the magic-user's line of sight along a 1\" wide path to the range limit. The material components of this spell are a pinch of talc and a small sprinkling of powdered silver."
    ),
    Spell('ESP','M',2,
        cast=tp(2,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="When an ESP spell is used, the caster is able to detect the surface thoughts of any creatures in range - except creatures with no mind (as we know it), such as all of the undead. The ESP is stopped by 2 or more feet of rock, 2 or more inches of any metal other than lead, or a thin sheet of lead foil. The magic-user employing the spell is able to probe the surface thoughts of 1 creature per turn, getting simple instinctual thoughts from lower order creatures. Probes can continue on the same creature from round to round. The caster can use the spell to help determine if some creature lurks behind a door, for example, but the ESP will not always reveal what sort of creature it is. The material component of this spell is a copper piece."
    ),
    Spell('Flaming Sphere','M',2,
        cast=tp(2,S),
        duration_lvl=tp(1,R),
        sourcebook=U,
    ),
    Spell('Fools Gold','M',2,
        cast=tp(1,R),
        duration_lvl=tp(6,T),
        sourcebook=V,
        desc="Copper coins can temporarily be changed to gold pieces, or brass items turned to solid gold for the spell duration by means of this dweomer. Note that a huge amount of copper or brass can be turned to gold by the spell - assume 4,000 g.p. are equal to a cubic foot for purposes of this spell. Any creature viewing Fools Gold is entitled to a saving throw which must be equal to or less than its intelligence score, but for every level of the magic-user the creature must add 1 to his dice score, so it becomes unlikely that Fools Gold will be detected if it was created by a high level caster. If the \"gold\" is struck hard by an object of cold-wrought iron, there is a slight chance it will revert to its natural state, depending on the material component used to create the \"gold\": if a 50 g.p. citrine is powdered and sprinkled over the metal to be changed, the chance that cold iron will return it to its true nature is 30%; if a 100 g.p. amber stone is powdered, there is a 25% chance that iron will dispel the dweomer; if a 500 g.p. topaz is powdered, the chance drops to 10%; and if a 1,000 g.p. oriental (corundum) topaz is powdered, there is only a 1% chance that the cold iron will reveal that it is Fools Gold."
    ),
    Spell('Forget','M',2,
        cast=tp(2,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="By means of this dweomer the spell caster causes creatures within the area of effect to forget the events of the previous round (1 minute of time from the utterance of the spell back). For every 3 levels of experience of the spell caster another minute of past time is forgotten. Naturally, Forget in no way negates any Charm, Suggestions, Geases, Quests, or similar spells, but it is possible that the creature who caused such magic to be placed upon the victim of a Forget spell could be forgotten by this means. From 1-4 individual creatures can be affected by the spell, at the discretion of the caster. If only 1 is to be affected, the recipient saves versus magic at -2 on the dice; if 2 are spell objects, they save at -1; and if 3 or 4 are to be made to forget by this dweomer, they save normally. A clerical Heal or Restoration spell, specially cast for this purpose, will restore the lost memories, as will a Wish, but other means will not serve to do so."
    ),
    Spell('Invisibility','M',2,
        cast=tp(2,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell causes the recipient to vanish from sight and not be detectable by normal vision or even infravision. Of course, the invisible creature is not magically silenced with respect to noises normal to it. The spell remains In effect until it is magically broken or dispelled, or the magic-user or the other recipient cancels it or until he, she or it attacks any creature. Thus, the spell caster or recipient could open doors, talk, eat, climb stairs, etc., but if any form of attack is made, the invisible creature immediately becomes visible, although this will allow the first attack by the creature because of the former invisibility. Even the allies of the spell recipient cannot see the invisible creature, or his, her or its gear, unless these allies can normally see invisible things or employ magic to do so. Note that all highly intelligent creatures with 10 or more hit dice, or levels of experience, or the equivalent in intelligence/dice/levels have a chance to automatically detect invisible objects. The material components of the Invisibility spell are an eyelash and a bit of gum arabic, the former encased in the latter."
    ),
    Spell('Irritation','M',2,
        cast=tp(2,S),
        duration=tp(1,VA),
        sourcebook=U,
    ),
    Spell('Knock','M',2,
        cast=tp(1,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="The Knock spell will open stuck or held or wizard-locked doors. It will also open barred or otherwise locked doors. It causes secret doors to open. The Knock spell will also open locked or trick-opening boxes or chests. It will loose shackles or chains as well. If it is used to open a wizard-locked door, the Knock does not remove the former spell, but it simply suspends its functioning for 1 turn. In all other cases, the Knock will permanently open locks or welds - although the former could be closed and locked again thereafter. It will not raise bars or similar impediments (such as a portcullis). The spell will perform two functions, but if a door is locked, barred, and held, opening it will require two Knock spells."
    ),
    Spell('Know Alignment','M',2,
        cast=tp(1,R),
        duration_lvl=tp(1,R),
        sourcebook=U,
    ),
    Spell('Leomund\'s Trap','M',2,
        cast=tp(3,R),
        duration=tp(1,P),
        sourcebook=V,
        desc="This false trap is designed to fool the dwarf and/or thief attempting to pilfer or otherwise steal the spell caster's goods. It enables the magic-user to place a dweomer upon any small mechanism or device such as a lock, hinge, hasp, screw-on cap, ratchet, etc. Any examination by a character able to detect traps will be 100% likely to note the Leomund's Trap and believe it to be real. This probability reduces by 4% for each level of experience of the examiner beyond the first. If the supposed \"trap\" is then to be removed, it is only 20% likely that the creature attempting it will believe he or she has succeeded, +4% probability per level of experience of the remover. Of course, the spell is illusory, nothing will happen if the trap is ignored, and its primary purpose is to frighten away thieves or make them waste precious time. The material component of the spell is a piece of iron pyrite touched to the object to be \"trapped\". Only one Leomund's Trap may be placed within a 50' by 50' area"
    ),
    Spell('Levitate','M',2,
        cast=tp(2,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="When a Levitate spell is cast, the magic-user can place it upon his or her person, or upon some other creature, subject to a maximum weight limit of 1,000 gold pieces equivalence per level of experience, i.e., a third level magic user can Levitate up to 300 pounds (3,000 g.p.) maximum. If the spell is cast upon the person of the magic-user, he or she can move vertically at a rate of 20' per round. If cast upon another creature, the magic-user can levitate it at a maximum vertical movement of 10' per round. Horizontal movement is not empowered by this spell, but the recipient could push along the face of a cliff, far example, to move laterally. The spell caster can cancel the spell as desired. If the recipient of the spell is unwilling, that creature is entitled to a saving throw to determine if the Levitate spell affects it. The material component of this spell is either a small leather loop or a piece of golden wire bent into a cup shape with a long shank on one end."
    ),
    Spell('Locate Object','M',2,
        cast=tp(2,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell is the same as the third level cleric Locate Object (q.v.) except that its range differs."
    ),
    Spell('Magic Mouth','M',2,
        cast=tp(2,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="When this spell is cast, the magic-user empowers the chosen object with an enchanted mouth which suddenly appears and speaks the message which the spell caster imparted upon the occurrence of a specified event. The Magic Mouth can speak any message of 25 words or less in a language known by the spell caster, over a 1 turn period from start to finish. It cannot speak magic spells. The mouth moves to the words articulated, so if it is placed upon a statue, for example, the mouth of the statue would actually move and appear to speak. Of course, the Magic Mouth can be placed upon a tree, rock, door or any other object excluding intelligent members of the animal or vegetable kingdoms. The spell will function upon specific occurrence according to the command of the spell caster, i.e. speak to the first creature that touches you - or to the first creature that passes within 30'. Command can be as general or specific and detailed as desired, such as the following: \"Speak only when an octogenerian female human carrying a sack of great clusters sits cross legged within 1'.\" Command range is 1½\" per level of the magic-user, so a 6th level magic-user can command the Magic Mouth to speak at a maximum encounter range of 3\", i.e. \"Speak when a winged creature comes within 3\" \". Until the speak command can be fulfilled, the Magic Mouth will remain in effect, thus spell duration is variable. A Magic Mouth cannot distinguish invisible creatures, alignments, level or hit dice, nor class, except by external garb. The material component of this spell is a small bit of honeycomb."
    ),
    Spell('Melf\'s Acid Arrow','M',2,
        cast=tp(4,S),
        duration=tp(1,VA),
        sourcebook=U,
    ),
    Spell('Mirror Image','M',2,
        cast=tp(2,S),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="When a Mirror Image spell is invoked, the spell caster causes from 1 to 4 exact duplicates of himself or herself to come into being around his or her person. These images do exactly what the magic-user does, and as the spell causes a blurring and slight distortion when it is effected, it is impossible for opponents to be certain which are the phantasms and which is the actual magic-user. When an image is struck by a weapon, magical or otherwise, it disappears. but any other existing images remain intact until struck. The images seem to shift from round to round, so that if the actual magic-user is struck during one round, he or she cannot be picked out from amongst his or her images the next. To determine the number of images which appear, roll percentile dice, and add 1 to the resulting score for each level of experience of the magic-user: 25 or less = 1 mirror image, 26-50 = 2, 51-75 = 3, 75 or more = 4. At the expiration of the spell duration all images wink out."
    ),
    Spell('Preserve','M',2,
        cast=tp(2,R),
        duration=tp(1,P),
        sourcebook=U,
    ),
    Spell('Protection From Cantrips','M',2,
        cast=tp(2,S),
        duration_lvl=tp(1,D),
        sourcebook=U
    ),
    Spell('Pyrotechnics','M',2,
        cast=tp(2,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="With the exception of the differences noted above, this spell is the same as the third level druid spell Pyrotechnics (q.v.)."
    ),
    Spell('Ray of Enfeeblement','M',2,
        cast=tp(2,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="By means of a Ray Of Enfeeblement, a magic-user weakens an opponent, reducing strength - and attacks which rely upon it by 25% or more. For every level of experience beyond the third of the magic-user casting the spell, there is an additional 2% strength reduction, so that at 4th level, strength loss is 27%. Range and duration of the spell are also dependent upon the level of experience of the spell caster. For example, if a creature is struck by a Ray Of Enfeeblement it will lose the appropriate percentage of hit points of damage it scores on physical attacks (missiles, thrusting/cutting/crushing weapons, biting, clawing, goring, kicking, constriction, etc.). Your referee will determine any other reductions appropriate to the affected creature. If the target creature makes its saving throw, the spell has no effect."
    ),
    Spell('Rope Trick','M',2,
        cast=tp(2,S),
        duration_lvl=tp(2,T),
        sourcebook=V,
        desc="When this spell is cast upon a piece of rope from 5' to 30' in length, one end of the rope rises into the air until the whole is hanging perpendicular, as if affixed at the upper end. The upper end is, in fact, fastened in an extra-dimensional space, and the spell caster and up to five others can climb up the rope and disappear into this place of safety where no creature can find them. The rope cannot be taken into the extra-dimensional space if six persons have climbed it, but otherwise it can be pulled up. Otherwise, the rope simply hangs in air, and will stay there unless removed by some creature. The persons in the extra-dimensional space must climb down the rope prior to the expiration of the spell duration, or else they are dropped from the height to which they originally climbed when the effect of the spell wears out. The rope can be climbed by only one person at a time. Note that the Rope Trick spell allows climbers to reach a normal place if they do not climb all the way to the rope's upper end, which is in an extra-dimensional space. The material components of this spell are powdered corn extract and a twisted loop of parchment."
    ),
    Spell('Scare','M',2,
        cast=tp(2,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="When this spell is directed at any creature with fewer than 6 levels of experience/hit dice, it must save versus magic or fall into a fit of trembling and shaking. The frightened creature will not drop any items held unless it is encumbered. If cornered, the spell recipient will fight, but at -1 on \"to hit\" and damage dice rolls and all saving throws as well. Note that this spell does not have any effect on elves, half-elves, the undead (skeletons, zombies, ghouls, shadows, ghosts, wights, wraiths), larvae, lemures, manes, or clerics of any sort. The material component used for this spell is a bit of bone from an undead skeleton, zombie, ghoul, ghost or mummy."
    ),
    Spell('Shatter','M',2,
        cast=tp(2,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="The Shatter spell affects non-magical objects of crystal, glass, ceramic, or porcelain such as vials, bottles, flasks, jugs, windows, mirrors, etc. Such objects are shivered into dozens of pieces by the spell. Objects above 100 gold pieces weight equivalence per level of the spell caster are not affected, but all other objects of the appropriate composition must save versus a \"crushing blow\" or be shattered. The material component of this spell is a chip of mica."
    ),
    Spell('Stinking Cloud','M',2,
        cast=tp(2,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="When a Stinking Cloud is cast, the magic-user causes a billowing mass of nauseous vapours to come into being up to 3\" distant from his or her position. Any creature caught within the cloud must save versus poison or be helpless due to nausea from 2 to 5 turns (d4 + 1). Those which make successful saving throws are helpless only for as long as they remain within the cloud, and for the round after they emerge, because of its irritating effects on visual and olfactory organs. The material component of the spell is a rotten egg or several skunk cabbage leaves."
    ),
    Spell('Strength','M',2,
        cast=tp(1,T),
        duration_lvl=tp(6,T),
        sourcebook=V
    ),
    Spell('Tasha\'s Uncontrollable Hideous Laughter','M',2,
        cast=tp(2,S),
        duration=tp(1,R),
        sourcebook=U
    ),
    Spell('Vocalize','M',2,
        cast=tp(1,R),
        duration=tp(5,R),
        sourcebook=U
    ),
    Spell('Web','M',2,
        cast=tp(2,S),
        duration_lvl=tp(2,T),
        sourcebook=V,
        desc="A Web spell creates a many-layered mass of strong, sticky strands similar to spider webs, but far larger and tougher. These masses must be anchored to two or more points - floor and ceiling, opposite walls, etc. - diametrically opposed. The Web spell covers a maximum area of 8 cubic inches, and the webs must be at least 1\" thick, so a mass 4\" high, 2\" wide, and 1\" deep may be cast. Creatures caught within webs, or simply touching them, become stuck amongst the gluey fibres. Creatures with less than 13 strength must remain fast until freed by another or until the spell wears off. For every full turn entrapped by a Web, a creature has a 5% cumulative chance of suffocating to death. Creatures with strength between 13 and 17 can break through 1' of webs per turn. Creatures with 18 or greater strength break through 1' of webs per round. (N.B. Sufficient mass equates to great strength in this case, and great mass will hardly notice webs.) Strong and huge creatures will break through 1' of webs per segment. It is important to note that the strands of a Web spell are flammable. A magic flaming sword will slash them away as easily as a hand brushes away cobwebs. Any fire - torch, flaming oil, flaming sword, etc. - will set them alight and burn them away in a single round. All creatures within the webs will take 2-8 hit points of damage from the flames, but those freed of the strands will not be harmed. Saving throw is made at -2. If the saving throw versus Web is made, two results may have occurred. If the creature has room to escape then he is assumed to have jumped free. If there is no room to escape then the webs are only ½ strength. The material component of this spell is a bit of spider web."
    ),
    Spell('Whip','M',2,
        cast=tp(2,S),
        duration_lvl=tp(1,R),
        sourcebook=U
    ),
    Spell('Wizard Lock','M',2,
        cast=tp(2,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="When a Wizard Lock spell is cast upon a door, chest or portal, it magically locks it, The wizard-locked door or object can be opened only by breaking, a Dispel Magic, a Knock spell (qq.v.}, or by a magic-user 4 or more levels higher than the one casting the spell, Note that the last two methods do not remove the Wizard Lock, they only negate it for a brief duration. Creatures of extra-dimensional nature do not affect a Wizard Lock as they do a held portal (see Hold Portal)."
    ),
    Spell('Zephyr','M',2,
        cast=tp(2,S),
        duration=tp(1,S),
        sourcebook=U
    ),
    Spell('Blink','M',3,
        cast=tp(1,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="By means of this spell, the magic-user causes his or her material form to \"blink\" out and back to this plane once again in random period and direction during the duration at each minute the spell is in effect. (Cf. ADVANCED DUNGEONS & DRAGONS, MONSTER MANUAL, Blink Dog.) The segment of the round that the spell caster \"blinks out\" is determined by random roll with 2d4, and during this same segment he or she will appear again 2' distant from his or her previous position. (Direction is determined by roll of d8: 1 = right ahead, 2 = right, 3 = right behind, 4 = behind, 5 = left behind, 6 = left, 7 = left ahead, 8 = ahead.) If some object is already occupying the space where the spell caster is indicated as \"blinking\" into, his or her form is displaced in a direction away from original (round starting) position for any distance necessary to appear in empty space, but never in excess of an additional 10'. If that extra distance still dictates the magic-user and another solid object are to occupy the same space, the spell caster is then trapped on the ethereal plane. During and after the blink segment of a round, the spell caster can be attacked only by opponents able to strike both locations at once, e.g. a breath weapon, Fireball, and similar wide area attack forms. Those not so able can only strike the magic-user if they managed to attack prior to the \"blink\" segment. The spell caster is only 75% likely to be able to perform any acts other than physical attack with a hand-held stabbing or striking weapon during the course of this spell. That is, use of any spell, device, or item might not be accomplished or accomplished in an incorrect manner or in the wrong direction. Your referee will determine success/failure and the results thereof according to the particular action being performed."
    ),
    Spell('Clairaudience','M',3,
        cast=tp(3,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="The Clairaudience spell enables the magic-user to concentrate upon some locale and hear in his or her mind whatever noise is within a 6\" radius of his or her determined Clairaudience locale centre. Distance is not a factor, but the locale must be known, i.e. a place familiar to the spell caster or an obvious one (such as behind a door, around a corner, in a copse of woods, etc.). Only sounds which are normally detectable by the magic-user can be heard by use of this spell. Only metal sheeting or magical protections will prevent the operation of the spell. Note that it will function only on the plane of existence an which the magic-user is at the time of casting. The material component of the spell is a small silver horn of at least 100 g.p. value, and casting the spell causes it to disappear."
    ),
    Spell('Clairvoyance','M',3,
        cast=tp(3,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="Similar to the Clairaudience spell, the Clairvoyance spell empowers the magic-user to see in his or her mind whatever is within sight range from the spell locale chosen. Distance is not a factor, but the locale must be known - familiar or obvious. Furthermore, light is a factor whether or not the spell caster has the ability to see into the infrared or ultraviolet spectrums. If the area is dark, only a 1\" radius from the centre of the locale of the spell's area of effect can be clairvoyed; otherwise, the seeing extends to normal vision range. Metal sheeting or magical protections will foil a Clairvoyance spell. The spell functions only on the plane on which the magic-user is at the time of casting. The material component of the spell is a pinch of powdered pineal gland from a human or humanoid creature."
    ),
    Spell('Cloudburst','M',3,
        cast=tp(3,S),
        duration=tp(1,R),
        sourcebook=U
    ),
    Spell('Detect Illusion','M',3,
        cast=tp(3,S),
        duration=tp(2,R),
        duration_lvl=tp(1,R),
        sourcebook=U
    ),
    Spell('Dispel Magic','M',3,
        cast=tp(3,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the third level cleric spell Dispel Magic (q.v.)."
    ),
    Spell('Explosive Runes','M',3,
        cast=tp(3,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="By tracing the mystic runes upon a book, map, scroll, or similar instrument bearing written information, the magic-user prevents unauthorized reading of such. The explosive runes are difficult to detect, 5% per level of magic use experience of the reader, thieves having only a 5% chance in any event, When read, the Explosive Runes detonate, delivering a full 12 to 30 (6d4 + 6) hit points of damage upon the reader, who gets no saving throw, and either a like amount, or half that if saving throws are made, on creatures within the blast radius. The magic-user who cast the spell, as well as any other magic-users he or she instructs, can use the instrument without triggering the runes. Likewise, the magic-user can totally remove them whenever desired. They can otherwise be removed only by a Dispel Magic spell, and the Explosive Runes last until the spell is triggered. The instrument upon which the runes are placed will be destroyed when the explosion takes place unless it is not normally subject to destruction by magical fire."
    ),
    Spell('Feign Death','M',3,
        cast=tp(1,S),
        duration=tp(6,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="By means of this spell, the caster or any other creature whose levels of experience/hit dice do not exceed the magic-user's own level can be put into a cataleptic state which is impossible to distinguish from actual death. Although the person/creature affected by the Feign Death spell can smell, hear, and know what is going on, no feeling or sight of any sort is possible; thus, any wounding or mistreatment of the body will not be felt and no reaction will occur and damage will be only one-half normal. In addition, paralysis, poison, or energy level drain will not affect the individual/creature under the influence of this spell, but poison injected or otherwise introduced into the body will become effective when the spell recipient is no longer under the influence of this spell, although a saving throw is permitted. Note that only a willing individual can be affected by Feign Death. The spell caster is able to end the spell effects at any time desired, but it requires 1 full round for bodily functions to begin again."
    ),
    Spell('Fireball','M',3,
        cast=tp(3,S),
        duration=tp(0),
        sourcebook=V,
        desc="A Fireball is an explosive burst of flame, which detonates with a low roar, and delivers damage proportionate to the level of the magic-user who cast it, i.e. 1 six-sided die (d6) for each level of experience of the spell caster. Exception: magic Fireball wands deliver 6 die fireballs (6d6), magic staves with this capability deliver 8 die Fireballs, and scroll spells of this type deliver a Fireball of from 5 to 10 dice (d6 + 4) of damage. The burst of the Fireball does not expend a considerable amount of pressure, and the burst will generally conform to the shape of the area in which it occurs, thus covering an area equal to its normal spherical volume. [The area which is covered by the Fireball is a total volume of roughly 33,000 cubic feet (or yards)]. Besides causing damage to creatures, the Fireball ignites all combustible materials within its burst radius, and the heat of the Fireball will melt soft metals such as gold, copper, silver, etc. Items exposed to the spell's effects must be rolled for to determine if they are affected. Items with a creature which makes its saving throw are considered as unaffected. The magic-user points his or her finger and speaks the range (distance and height) at which the Fireball is to burst. A streak flashes from the pointing digit and, unless it impacts upon a material body prior to attaining the prescribed range, flowers into the Fireball. If creatures fail their saving throws, they all take full hit point damage from the blast. Those who make saving throws manage to dodge, fall flat or roll aside, taking ½ the full hit point damage - each and every one within the blast area. The material component of this spell is a tiny ball composed of bat guano and sulphur."
    ),
    Spell('Flame Arrow','M',3,
        cast=tp(3,S),
        duration=tp(0),
        duration_lvl=tp(1,S),
        sourcebook=V,
        desc="Once the magic-user has cast this spell. he or she is able to touch one arrow or crossbow bolt (quarrel) per segment for the duration of the Flame Arrow. Each such missile so touched becomes magic, although it gains no bonuses \"to hit\". Each such missile must be discharged within 1 round, for after that period flame consumes it entirely, and the magic is lost. Fiery missiles will certainly have normal probabilities of causing combustion. and any creature subject to additional fire damage will suffer +1 hit point of damage from any flame arrow which hits it. The material components for this spell are a drop of oil and a small piece of flint."
    ),
    Spell('Fly','M',3,
        cast=tp(3,S),
        duration=tp(1,VA),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="This spell enables the magic-user to bestow the power of magical flight. The creature affected is able to move vertically and/or horizontally at a rate of 12\" per move (half that if ascending, twice that if descending in a dive). The exact duration of the spell is always unknown to the spell caster, as the 1-6 turns variable addition is determined by the Dungeon Master secretly. The material component of the Fly spell is a wing feather of any bird."
    ),
    Spell('Gust of Wind','M',3,
        cast=tp(3,S),
        duration=tp(1,S),
        sourcebook=V,
        desc="When this spell is cast, a strong puff of air originates from the magic-user and moves in the direction he or she is facing. The force of this Gust Of Wind is sufficient to extinguish candles, torches, and similar unprotected flames. It will cause protected -flames such as those of lanterns to wildly dance and has a 5% chance per level of experience of the spell caster to extinguish even such lights. It will also fan large fires outwards 1' to 6' in the direction of the wind's movement. It will force back small flying creatures 1\" to 6\" and cause man-sized ones to be held motionless if attempting to move into its force, and similarly slow large flying creatures by 50% for 1 round. It will blow over light objects. Its path is 1\" wide by 1\" of length per level of experience of the magic-user casting the Gust Of Wind spell i.e. an 8th level magic-user causes a Gust Of Wind which travels 8\". The material component of the spell is a legume seed."
    ),
    Spell('Haste','M',3,
        cast=tp(3,S),
        duration=tp(3,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="When this spell is cast, affected creatures function at double their normal movement and attack rates. Thus, a creature moving at 6\" and attacking 1 time per round would move at 12\" and attack 2 times per round. Spell casting is not more rapid. The number of creatures which can be affected is equal to the level of experience of the magic-user, those creatures closest to the spell caster being affected in preference to those farther away, and all affected by Haste must be in the designated area of effect. Note that this spell negates the effects of a Slow spell (see hereafter). Additionally, this spell ages the recipients due to speeded metabolic processes. Its material component is a shaving of liquorice root."
    ),
    Spell('Hold Person','M',3,
        cast=tp(3,S),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="Similar to the second level cleric Hold Person (q.v.). this spell immobilizes creatures, within range, as designated by the magic-user. If three or four persons are attacked, their saving throws are normal; but if two are attacked, their saving throws are made at -1 and if only one creature is attacked, the saving throw versus the Hold Person spell is made at -3 on the die. Partial negation of a Hold Person spell, such as would be possible by a ring of spell turning, causes the spell to function as a Slow spell (q.v.) unless the saving throw is successful. Creatures affected by the spell are: brownies, dryads, dwarves, elves, gnolls, gnomes, goblins, half-elves, halflings, half-orcs, hobgoblins, humans, kobolds, lizard men, nixies, orcs, pixies, sprites, and troglodytes."
    ),
    Spell('Infravision','M',3,
        cast=tp(1,R),
        duration=tp(12,R),
        duration_lvl=tp(6,T),
        sourcebook=V,
        desc="By means of this spell the magic-user enables the recipient of Infravision to see light in the infrared spectrum. Thus, differences in heat wave radiations can be seen up to 6\". Note that strong sources of infrared radiation (fire, lanterns, torches, etc.) tend to blind or cast \"shadows\" just as such light does with respect to normal vision, so the infravision is affected and does not function efficiently in the presence of such heat sources. (Invisible creatures are not usually detectable by infravision, as the infrared light waves are affected by invisibility, just as those of the ultraviolet and normal spectrums are.) The material component of this spell is either a pinch of dried carrot or an agate."
    ),
    Spell('Invisibility 10\' Radius','M',3,
        cast=tp(3,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell is essentially the same as Invisibility (q.v.). Those affected by it cannot see each other. Those affected creatures which attack negate the invisibility only with respect to themselves, not others made invisible, unless the spell recipient causes the spell to be broken."
    ),
    Spell('Item','M',3,
        cast=tp(3,S),
        duration_lvl=tp(6,T),
        sourcebook=U
    ),
    Spell('Leomund\'s Tiny Hut','M',3,
        cast=tp(3,S),
        duration_lvl=tp(6,T),
        sourcebook=V,
        desc="When this spell is cast, the magic-user causes an opaque sphere of force to come into being around his or her person, half of the sphere projecting above the ground or floor surface, the lower hemisphere passing through the surface. This field causes the interior of the sphere to maintain at 70°F. temperature in cold to 0°F., and heat up to 105°F. Cold below 0° lowers inside temperature on a 1° for 1° basis, heat above 105° raises the inside temperature likewise. The Tiny Hut will withstand winds up to 50 m.p.h. without being harmed, but wind force greater than that will destroy it. The interior of the Tiny Hut is a hemisphere, and the spell caster can illuminate it dimly upon command, or extinguish the light as desired. Note that although the force field is opaque from positions outside, it is transparent from within. In no way will Leomund's Tiny Hut provide protection from missiles, weapons, spells, and the like. Up to 6 other man-sized creatures can fit into the field with its creator, and these others can freely pass in and out of the Tiny Hut without harming it, but if the spell caster removes himself from it, the spell will dissipate. The material component for this spell is a small crystal bead which will shatter when spell duration expires or the hut is otherwise dispelled."
    ),
    Spell('Lightning Bolt','M',3,
        cast=tp(3,S),
        duration=tp(0),
        sourcebook=V,
        desc="Upon casting this spell, the magic user releases a powerful stroke of electrical energy which causes damage equal to 1 six-sided die (d6) for each level of experience of the spell caster to creatures within its area of effect, or 50% of such damage to such creatures which successfully save versus the attack form. The range of the bolt is the location of the commencement of the stroke, i.e. if shot to 6\", the bolt would extend from this point to n inches further distance. The Lightning Bolt will set fire to combustibles, sunder wooden doors, splinter up to 1' thickness of stone, and melt metals with a low melting point (lead, gold, copper, silver, bronze). Saving throws must be made for objects which withstand the full force of a stroke (cf. fireball). The area of the Lightning Bolt's effect is determined by the spell caster, just as its distance is. The stroke can be either a forking bolt 1\" wide and 4\" long. or a single bolt ½\" wide and 8\" long. If a 12th level magic-user cast the spell at its maximum range, 16\" in this case, the stroke would begin at 16\" and flash outward from there, as a forked bolt ending at 20\" or a single one ending at 24\". If the full length of the stroke is not possible due to the interposition of a non-conducting barrier (such as a stone wall), the Lightning Bolt will double and rebound towards its caster, its length being the normal total from beginning to end of stroke, damage caused to interposing barriers notwithstanding. Example: An 8\" stroke is begun at a range of 4\", but the possible space in the desired direction is only 3½\"; so the bolt begins at the 3½\" maximum, and it rebounds 8\" in the direction of its creator. The material components of the spell are a bit of fur and an amber, crystal or glass rod."
    ),
    Spell('Material','M',3,
        cast=tp(1,R),
        duration=tp(1,P),
        sourcebook=U
    ),
    Spell('Melf\'s Minute Meteors','M',3,
        cast=tp(5,S),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Monster Summoning I','M',3,
        cast=tp(3,S),
        duration=tp(2,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="Within 1-4 rounds of casting this spell, the magic-user will cause the appearance of from 2-8 first level monsters (selected at random by the referee, but whose number may be either randomly determined or selected personally by the referee, according to the strength of the monster randomly determined). These monsters will appear in the spot, within spell range, desired by the magic-user, and they will attack the spell user's opponents to the best of their ability until he or she commands that attack cease, or the spell duration expires, or the monsters ore slain. Note that if no opponent exists to fight, summoned monsters can, if communication is possible, and if they are physically capable, perform other services for the summoning magic-user. The material components of this spell are a tiny bag and a small (not necessarily lit) candle."
    ),
    Spell('Phantasmal Force','M',3,
        cast=tp(3,S),
        duration=tp(0),
        sourcebook=V,
        desc="When this spell is cast, the magic-user creates a visual illusion which will affect all believing creatures which view the Phantasmal Force, even to the extent of suffering damage from phantasmal missiles or from falling into an illusory pit full of sharp spikes. Note that audial illusion is not a component of the spell. The illusion lasts until struck by an opponent - unless the spell caster causes the illusion to react appropriately - or until the magic-user ceases concentration upon the spell (due to desire, moving, or successful attack which causes damage). Creatures which disbelieve the Phantasmal Force gain a saving throw versus the spell, and if they succeed, they see it for what it is and add +4 to associates' saving throws if this knowledge can be communicated effectively. Creatures not observing the spell effect are immune until they view it. The spell can create the illusion of any object, or creature, or force, as long as it is within the boundaries of the spell's area of effect. This area can move within the limits of the range. The material component of the spell is a bit of fleece."
    ),
    Spell('Protection From Evil 10\' Radius','M',3,
        cast=tp(3,S),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="This spell is the same as the first level Protection From Evil spell except with respect to its area of effect. See also the first level cleric Protection From Evil spell for general information."
    ),
    Spell('Protection From Normal Missiles','M',3,
        cast=tp(3,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="By means of this spell, the magic-user bestows total invulnerability to hurled and projected missiles such as arrows, axes, bolts, javelins, small stones and spears. Furthermore, it causes a reduction of 1 from each die of damage inflicted by large and/or magical missiles such as ballista missiles, catapult stones, and magical arrows, bolts, javelins, etc. Note, however that this spell does not convey any protection from such magical attacks as Fireballs, Lightning Bolts, or Magic Missiles. The material component of this spell is a piece of tortoise or turtle shell."
    ),
    Spell('Secret Page','M',3,
        cast=tp(1,T),
        duration=tp(1,P),
        sourcebook=U
    ),
    Spell('Sepia Snake Sigil','M',3,
        cast=tp(3,S),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Slow','M',3,
        cast=tp(3,S),
        duration=tp(3,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="A Slow spell causes affected creatures to move and attack at one half of the normal or current rate. Thus, it negates a Haste spell (q.v.), has cumulative effect if cast upon creatures already slowed, and otherwise affects magically speeded or slowed creatures. The magic will affect as many creatures as the spell caster has levels of experience, providing these creatures are within the area of effect determined by the magic-user, i.e. the 4\" x 4\" area which centres in the direction and at the range called for by the caster. The material component of this spell is a drop of treacle."
    ),
    Spell('Suggestion','M',3,
        cast=tp(3,S),
        duration=tp(6,T),
        duration_lvl=tp(6,T),
        sourcebook=V,
        desc="When this spell is cast by the magic-user, he or she influences the actions of the chosen recipient by utterance of a few words - phrases, or a sentence or two - suggesting a course of action desirable to the spell caster. The creature to be influenced must, of course, be able to understand the magic-user's suggestion, i.e., it must be spoken in a language which the spell recipient understands. The suggestion must be worded in such a manner as to make the action sound reasonable; a request asking the creature to stab itself, throw itself onto a spear, immolate itself, or do some other obviously harmful act will automatically negate the effect of the spell. However, a suggestion that a pool of acid was actually pure water, and a quick dip would be refreshing, is another matter; or the urging that a cessation of attack upon the magic-user's party would benefit a red dragon, for the group could loot a rich treasure elsewhere through co-operative action, is likewise a reasonable use of the spell's power. The course of action of a Suggestion can continue in effect for a considerable duration, such as in the case of the red dragon mentioned above. If the recipient creature makes its saving throw, the spell has no effect. Note that a very reasonable suggestion will cause the saving throw to be made at a penalty (such as -1, -2, etc.) at the discretion of your Dungeon Master. Undead are not subject to Suggestion. The material components of this spell are a snake's tongue and either a bit of honeycomb or a drop of sweet oil."
    ),
    Spell('Tongues','M',3,
        cast=tp(3,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the fourth level cleric spell, Tongues (q.v.). Also, the material component is a small clay model of a ziggurat, which shatters when the spell is pronounced."
    ),
    Spell('Water Breathing','M',3,
        cast=tp(3,S),
        duration_lvl=tp(3,T),
        sourcebook=V,
        desc="Except as noted above, and that the material component of the spell is a short reed or piece of straw, this is the same as the third level druid spell, Water Breathing (q.v.)."
    ),
    Spell('Wind Wall','M',3,
        cast=tp(3,S),
        duration_lvl=tp(1,R),
        sourcebook=U
    ),
    Spell('Charm Monster','M',4,
        cast=tp(4,S),
        duration=tp(1,VA),
        sourcebook=V
    ),
    Spell('Confusion','M',4,
        cast=tp(4,S),
        duration=tp(2,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="Except as noted above, this spell is identical to the seventh level druid spell, Confusion (q.v.). However, it affects a basic 2-16 creatures. Its material component is a set of three nut shells."
    ),
    Spell('Dig','M',4,
        cast=tp(4,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="A Dig spell enables the caster to excavate 125 cubic feet of earth, sand, or mud per round. The hole thus dug is a cube 5' per side. The material thrown from the excavation scatters evenly around the pit. If the magic-user continues downward beyond 5', there is a chance that the pit will collapse: 15%/additional 5' in depth in earth, 35%/additional 5' depth in sand, and 55%/additional 5' depth in mud. Any creature at the edge (1') such a pit uses its dexterity score as a saving throw to avoid falling into the hole with a score equal to or less than the dexterity meaning that a fall was avoided. Any creature moving rapidly towards a pit area will fall in unless it saves versus magic. Any creature caught in the centre of a pit just dug will always fall in. The spell caster uses a miniature shovel and tiny bucket to activate a Dig spell and must continue to hold these material components while each pit is excavated."
    ),
    Spell('Dimension Door','M',4,
        cast=tp(1,S),
        duration=tp(0),
        sourcebook=V,
        desc="By means of a Dimension Door spell, the magic-user instantly transfers himself or herself up to 3\" distance per level of experience of the spell caster. This special form of teleportation allows for no error, and the magic-user always arrives at exactly the spot desired whether by simply visualizing the area (within spell transfer distance, of course) or by stating direction such as \"30 inches straight downwards,\" or \"upwards to the northwest, 45 degree angle, 42 inches.\" If the magic-user arrives in a place which is already occupied by a solid body, he or she remains in the Astral Plane until located by some helpful creature willing to cast a Dispel Magic upon the person, for he or she is stunned and cannot successfully perform any spell casting. If distances are stated and the spell caster arrives with no support below his or her feet (i.e. in mid-air), falling and damage will result unless further magical means are employed. All that the magic-user wears or carries, subject to a maximum weight equal to 5,000 gold pieces of non-living matter, or half that amount of living matter, is transferred with the spell caster. Recovery from use of a Dimension Door spell requires 7 segments."
    ),
    Spell('Dispel Illusion','M',4,
        cast=tp(4,S),
        duration=tp(1,P),
        sourcebook=U
    ),
    Spell('Enchanted Weapon','M',4,
        cast=tp(1,T),
        duration_lvl=tp(5,R),
        sourcebook=V,
        desc="This spell turns an ordinary weapon into a magical one, The weapon is the equivalent of a +1 weapon but has no bonuses whatsoever. Thus, arrows, axes, bolts, bows, daggers, hammers, maces, spears, swords, etc. can be made into enchanted weapons. Two small (arrows. bolts, daggers, etc.) or one large (axe, bow, hammer, mace, etc.) weapon can be affected by the spell. Note that successful hits by enchanted missile weapons cause the spell to be broken, but that otherwise the spell duration lasts until the time limit based on the level of experience of the magic-user casting it expires, i.e. 40 rounds (4 turns) in the case of an 8th level magic-user. The material components of this spell are powdered lime and carbon."
    ),
    Spell('Evard\'s Black Tentacles','M',4,
        cast=tp(8,S),
        duration=tp(1,R),
        sourcebook=U
    ),
    Spell('Extension I','M',4,
        cast=tp(2,S),
        duration=tp(0),
        sourcebook=V,
        desc="By use of an Extension I spell the magic-user prolongs the duration of a previously cast first, second, or third level spell by 50%. Thus, a Levitation spell can be made to function 1½ turns/level, a Hold Person spell made to work for 3 rounds/level, etc. Naturally, the spell has effect only on such spells where duration is meaningful."
    ),
    Spell('Fear','M',4,
        cast=tp(4,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="When a Fear spell is cast, the magic-user sends forth an invisible ray which causes creatures within its area of effect to turn away from the spell caster and flee in panic. Affected creatures are likely to drop whatever they are holding when struck by the spell; the base chance of this is 60% at 1st level (or at 1 hit die), and each level (or hit die) above this reduces the probability by 5%, i.e. at 10th level there is only a 15% chance, and at 13th level 0% chance. Creatures affected by fear flee at their fastest rate for the number of melee rounds equal to the level of experience of the spell caster. The panic takes effect on the melee round following the spell casting, but dropping of items in hand will take place immediately. Of course, creatures which make their saving throws versus the spell are not affected. The material component of this spell is either the heart of a hen or a white feather."
    ),
    Spell('Fire Charm','M',4,
        cast=tp(4,S),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="By means of this spell the magic-user causes a normal fire source such as a brazier, flambeau, or bonfire to serve as a magical agent, for from this source he or she causes a gossamer veil of multi-hued flame to circle the fire at 5' distance. Any creatures observing the fire or the dancing circle of flame around it must save versus magic or be charmed into remaining motionless and gazing, transfixed at the flames. While so charmed, creatures are subject to Suggestion spells of 12 or fewer words, saving against their influence at -3. The Fire Charm is broken by any physical attack upon the charmed creature, if a solid object is interposed between the creature and the veil of flames so as to obstruct vision, or when the duration of the spell is at an end. Note that the veil of flame is not a magical fire, and passing through it incurs the same type and amount of damage as would be sustained from passing through its original fire source. The material component for this spell is a small piece of multicoloured silk of exceptional thinness which the dweomercraefter must throw into the fire source."
    ),
    Spell('Fire Shield','M',4,
        cast=tp(4,S),
        duration=tp(2,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc=("By casting this spell the magic-user appears to immolate himself or herself, but the flames are thin and wispy shedding light equal only to half that of a normal torch (15' radius of dim light), and coloured blue or green if variation A is cast, violet or blue if variation B is employed. Any creature striking the spell caster with body or hand-held weapons will inflict normal damage upon the magic-user, but the attacker will take double the amount of damage so inflicted! The other spell powers depend on the variation of the spell used:\n"
            "A)	The flames are hot, and any cold-based attacks will be saved against at +2 on the dice, and either half normal damage or no damage will be sustained, fire-based attacks are normal, but if the magic-user fails to make the required saving throw (if any) against them, he or she will sustain double normal damage. The material component for this variation is a bit of phosphorous.\n"
            "B)	The flames are cold, and any fire-based attack will be saved against at +2 on the dice, and either half normal damage or no damage will be sustained; cold-based attacks are normal, but if the magic-user fails to make the required saving throw (if any) against them, he or she will sustain double normal damage. The material component for this variation is a live firefly or glow worm or the tail portions of 4 dead ones.")
    ),
    Spell('Fire Trap','M',4,
        cast=tp(3,R),
        duration=tp(1,P),
        sourcebook=V,
        desc="Any closable item (book, box, bottle. chest, coffer, coffin, door, drawer, and so forth) is affected by a Fire Trap spell, but the item so trapped cannot have a second spell such as Hold Portal or Wizard Lock placed upon it except as follows: if a Fire Trap/Hold Portal is attempted, only the spell first cast will work, and the other will be negated (both negated if cast simultaneously). If a Fire Trap is cast after a Wizard Lock, the former is negated, if both are cast simultaneously both are negated, and if a Wizard Lock is cast after placement of a Fire Trap there is a 50% chance that both spells will be negated. A Knock spell will not affect a Fire Trap in any way - as soon as the offending party enters/touches, the trap will discharge. The caster can use the trapped object without discharging it. When the trap is discharged there will be an explosion of 5' radius, and all creatures within this area must make saving throws versus magic. Damage is 1-4 hit points plus 1 hit point per level of the magic-user who cast the spell, or one-half the total amount for creatures successfully saving versus magic. The item trapped is NOT harmed by this explosion. There is only 50% of the normal chance to detect a Fire Trap, and failure to remove it when such action is attempted detonates it immediately. To place this spell, the caster must trace the outline of the closure with a bit of sulphur or saltpetre."
    ),
    Spell('Fumble','M',4,
        cast=tp(4,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="When a Fumble spell is cast, the magic-user causes the recipient of the magic to suddenly become clumsy and awkward. Running creatures will trip and fall, those reaching for an item will fumble and drop it, those employing weapons will likewise awkwardly drop them. Recovery from a fall or of a fumbled object will typically require the whole of the next melee round. Note that breakable items might suffer damage when dropped. If the victim makes his or her saving throw, the Fumble will simply make him or her effectively operate at one-half normal efficiency (cf. slow spell). The material component of this spell is a dab of solidified milk fat."
    ),
    Spell('Hallucinatory Terrain','M',4,
        cast=tp(1,T),
        duration=tp(1,P),
        sourcebook=V,
        desc="By means of this spell the magic-user causes an illusion which hides the actual terrain within the area of the spell's effect. Thus, open fields or a road can be made to look as if a swamp or hill or crevasse or same other difficult or impassable terrain existed there. Also, a pond can be made to appear as a grassy meadow, a precipice look as if it were a gentle slope, or a rock-strewn gully made to look as if it were a wide and smooth road. The Hallucinatory Terrain persists until a Dispel Magic spell is cast upon the area or until it is contacted by an intelligent creature. Each level of experience of the magic-user enables him or her to affect a larger area. At 10th level, a magic-user can affect an area up to 10\" x 10\" square, while at 12th level the spell caster affects a 12\" x 12\" square area. The material components of this spell area stone, a twig, and a bit of green plant - leaf or grass blade."
    ),
    Spell('Ice Storm','M',4,
        cast=tp(4,S),
        duration=tp(1,R),
        sourcebook=V,
        desc="When this spell is cast, the magic-user causes either great hail stones to pound down in an area of 4\" diameter and inflict from 3 to 30 (3d10) hit points of damage on any creatures within the area of effect; or the Ice Storm can be made to cause driving sleet to fall in an area of 8\" diameter and both blind creatures within its area of effect for the duration of the spell and cause the ground in the area to be icy, thus slowing movement within by 50% and making it 50% probable that a moving creature will slip and fall when trying to move. The material components for this spell are a pinch of dust and a few drops of water. (Note that this spell will negate a Heat Metal spell (q.v.), but its first application will also cause damage in the process)."
    ),
    Spell('Leomund\'s Secure Shelter','M',4,
        cast=tp(4,T),
        duration_lvl=tp(6,T),
        sourcebook=U
    ),
    Spell('Magic Mirror','M',4,
        cast=tp(1,H),
        duration_lvl=tp(1,R),
        sourcebook=U
    ),
    Spell('Massmorph','M',4,
        cast=tp(1,T),
        duration=tp(1,P),
        sourcebook=V,
        desc="When this spell is cast upon willing creatures of man-size or smaller, up to 10 such creatures per level of experience of the magic-user can be made to appear as normal trees of any sort. Thus, a company of creatures can be made to appear as a copse, grove, or orchard. Furthermore, these massmorphed creatures can be passed through - and even touched - by other creatures without revealing the Illusion. Note, however, that blows to the creature-trees will reveal their nature, as damage will be sustained by the creatures struck and blood will be seen. Creatures massmorphed must be within the spell's area of effect. Unwilling creatures are not affected. The spell persists until the caster commands it to cease or until a dispel magic is cast upon the creatures. The material component of this spell is a handful of bark chips."
    ),
    Spell('Minor Globe of Invulnerability','M',4,
        cast=tp(4,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell creates a magical sphere around the caster which prevents any first, second or third level spells from penetrating, i.e. the area of effect of any such spells does not include the area of the Minor Globe Of Invulnerability. However, any sort of spells can be cast out of the magical sphere, and they pass from the caster of the globe, through its area of effect, and to their target without effect upon the Minor Globe Of Invulnerability. Fourth and higher level spells are not affected by the globe. It can be brought down by a Dispel Magic spell. The material component of the spell is a glass or crystal bead."
    ),
    Spell('Monster Summoning II','M',4,
        cast=tp(4,S),
        duration=tp(3,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell is similar to the third level Monster Summoning I spell (q.v.). Its major difference is that 1-6 second level monsters are conjured up. The material components are the same as those of the lesser spell. There is also a 1-4 round delay."
    ),
    Spell('Otiluke\'s Resilient Sphere','M',4,
        cast=tp(4,S),
        duration_lvl=tp(1,R),
        sourcebook=U
    ),
    Spell('Plant Growth','M',4,
        cast=tp(4,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as a third level druid spell, Plant Growth (q.v.)."
    ),
    Spell('Polymorph Other','M',4,
        cast=tp(4,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="The Polymorph Other spell is a powerful magic which completely alters the form and ability, and possibly the personality and mentality, of the recipient. Of course, creatures with a lower intelligence cannot be polymorphed into something with a higher intelligence, but the reverse is possible. The creature polymorphed must make a \"system shock\" (cf. CONSTITUTION) roll to see if it survives the change. If it is successful, it then acquires all of the form and abilities of the creature it has been polymorphed into. There is a base 100% chance that this change will also change its personality and mentality into that of the creature whose form it now possesses. For each 1 point of intelligence of the creature polymorphed, subtract 5% from the base chance. Additionally, for every hit die of difference between the original form and the form it is changed into by the spell, the polymorphed creature must adjust the base chance percentage by +/-5% per hit die below or above its own number (or level in the case of characters). The chance for assumption of the personality and mentality of the new form must be checked daily until the change takes place. (Note that all creatures generally prefer their own form and will not willingly stand the risk of being subjected to this spell) If a one hit die orc of 8 intelligence is polymorphed into a white dragon with 6 hit dice, for example, it is 85% (100% - [5% x 8 intelligence + [(6 - 1) x ( 5%] = 85%) likely to actually become one in all respects, but in any case it will have the dragon's physical and mental capabilities; and if it does not assume the personality and mentality of a white dragon, it will know what it formerly knew as well. Another example: an 8th level fighter successfully polymorphed into a blue dragon would know combat with weapons and be able to employ them with prehensile dragon forepaws if the fighter did not take on dragon personality and mentality. However, the new form of the polymorphed creature may be stronger than it looks, i.e. a mummy changed to a puppy dog would be very tough, or a brontosaurus changed to an ant would be impossible to squash merely from being stepped on by a small creature or even a man-sized one. The magic-user must use a dispel magic spell to change the polymorphed creature back to its original form, and this too requires a \"system shock\" saving throw. The material component of this spell is a caterpillar cocoon."
    ),
    Spell('Polymorph Self','M',4,
        cast=tp(3,S),
        duration_lvl=tp(2,T),
        sourcebook=V,
        desc="When this spell is cast, the magic-user is able to assume the form of any creature - from as small as a wren to as large as a hippopotamus - and its form of locomotion as well. The spell does not give the other abilities (attack, magic. etc.), nor does it run the risk of changing personality and mentality. No \"system shock\" check is required. Thus, a magic-user changed to an owl could fly, but his or her vision would be human; a change to a black pudding would enable movement under doors or along halls and ceilings. but not the pudding's offensive or defensive capabilities. Naturally, the strength of the new form must be sufficient to allow normal movement. The spell caster can change his or her form as often as desired, the change requiring only 5 segments. Damage to the polymorphed form is computed as if it were inflicted upon the magic-user, but when the magic-user returns to his or her own form, from 1 to 12 (d12) points of damage are restored."
    ),
    Spell('Rary\'s Mnemonic Enhancer','M',4,
        cast=tp(1,T),
        duration=tp(1,D),
        sourcebook=V,
        desc="By means of this spell the magic-user is able to memorize, or retain the memory of, three additional spell levels, i.e. three spells of the first level, or one first and one second, or one third level spell. The magic-user can elect to immediately memorize additional spells or he or she may opt to retain memory of a spell cast by means of the Enhancer. The material components of the spell are a piece of string, an ivory plaque of at least 100 g.p. value, and an ink composed of squid secretion and either black dragon's blood or giant slug digestive juice. All components disappear when the spell is cast."
    ),
    Spell('Remove Curse','M',4,
        cast=tp(4,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the third level cleric spell, Remove Curse (q.v.)."
    ),
    Spell('Shout','M',4,
        cast=tp(1,S),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Stoneskin','M',4,
        cast=tp(1,S),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Ultravision','M',4,
        cast=tp(4,S),
        duration=tp(6,T),
        duration_lvl=tp(6,T),
        sourcebook=U
    ),
    Spell('Wall of Fire','M',4,
        cast=tp(4,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="This spell differs from the fifth level druid spell, Wall Of Fire (q.v.) only as indicated above and as stated below: the flame colour is either violet or reddish blue, base damage is 2-12 hit points (plus 1 hit point per level), the radius of the ring-shaped wall of fire is 1\" + 1/4\" per level of experience of the magic user casting it, and the material component of the spell is phosphorus. "
    ),
    Spell('Wall of Ice','M',4,
        cast=tp(4,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="When this spell is cast, a sheet of strong, flexible ice is created. The wall is primarily defensive, stopping pursuers and the like. The wall is one inch thick per level of experience of the magic-user. It covers a 1\" square area per level, i.e. a 10th level magic-user would cause a Wall Of Ice up to 10\" long and 1\" high, or 5\" long and 2\" high, and so forth. Any creature breaking through the ice will suffer 2 hit points of damage per inch of thickness of the wall, fire-using creatures will suffer 3 hit points, cold-using creatures only 1 hit point when breaking through. If this spell is cast to form a horizontal sheet to fall upon opponents, it has the same effect as an Ice Storm's (q.v.) hail stones in the area over which it falls. Magical fires such as Fireballs and fiery dragon breath will melt a Wall Of Ice in 1 round, though they will cause a great cloud of steamy fog which will last 1 turn, but normal fires or lesser magical ones will not hasten its melting. The material component of this spell is a small piece of quartz or similar rock crystal."
    ),
    Spell('Wizard Eye','M',4,
        cast=tp(1,T),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="When this spell is employed, the magic-user creates an invisible sensory organ which sends visual information to him or her. The Wizard Eye travels at 3\" per round, viewing an area ahead as a human would or 1\" per round examining the ceiling and walls as well as the floor ahead and casually viewing the walls ahead. The Wizard Eye can \"see\" with infravision at 10', or it \"sees\" up to 60' distant in brightly lit areas. The Wizard Eye can travel in any direction as long as the spell lasts. The material component of the spell is a bit of bat fur."
    ),
    Spell('Airy Water','M',5,
        cast=tp(5,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="The Airy Water spell turns normal liquid such as water or water based infusions or solutions to a less dense, breathable substance. Thus, if the magic-user were desirous of entering an underwater place, he or she would step into the water, cast the spell and sink downwards in a globe of bubbling water which he or she and any companions in the spell's area of effect could move freely in and breathe just as if it were air rather than water. The globe will move with the spell caster, Note that water breathing creatures will avoid a sphere (or hemisphere) of airy water, although intelligent ones can enter it if they are able to move by means other than swimming, but no water-breathers will be able to breathe in an area affected by this spell. There is only one word which needs to be spoken to actuate the magic, and the material component of the spell is a small handful of alkaline or bromine salts."
    ),
    Spell('Animal Growth','M',5,
        cast=tp(5,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="Except as noted above, and for the fact that the material component of the spell is a pinch of powdered bone, this is the same as the fifth level druid spell Animal Growth (q.v.)."
    ),
    Spell('Animate Dead','M',5,
        cast=tp(5,R),
        duration=tp(1,P),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the third level cleric spell Animate Dead (q.v.)."
    ),
    Spell('Avoidance','M',5,
        cast=tp(3,S),
        duration=tp(1,P),
        sourcebook=U
    ),
    Spell('Bigby\'s Interposing Hand','M',5,
        cast=tp(5,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="Bigby's Interposing Hand is a large to huge-sized magic member which appears and places itself between the spell caster and his or her chosen opponent. This disembodied hand then remains between the two, regardless of what the spell caster does subsequently or how the opponent tries to get around it. The size of the Hand is determined by the magic-user, and it can be human-sized all the way up to titan-sized. It takes as many hit points of damage to destroy as the magic-user who cast it. Any creature weighing less than 2,000 pounds trying to push past it will be slowed to one-half normal movement. The material component of the spell is a glove."
    ),
    Spell('Cloudkill','M',5,
        cast=tp(5,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell generates a billowing cloud of ghastly yellowish green vapours which is so toxic as to slay any creature with fewer than 4 + 1 hit dice, cause creatures with 4 + 1 to 5 + 1 hit dice to save versus poison at -4 on the dice roll, and creatures up to 6 hit dice (inclusive) to save versus poison normally or be slain by the cloud. The Cloudkill moves away from the spell caster at 1\" per round, rolling along the surface of the ground. A wind will cause it to alter course, but it will not move back towards its caster. A strong wind will break it up in 4 rounds, and a greater wind force prevents the use of the spell. Very thick vegetation will disperse the cloud in two rounds, i.e. moving through such vegetation for 2\". As the vapours ore heavier than air, they will sink to the lowest level of the land, even pour down den or sinkhole openings; thus, it is ideal for slaying nests of giant ants, for example."
    ),
    Spell('Conjure Elemental','M',5,
        cast=tp(1,T),
        duration_lvl=tp(1,T),
        sourcebook=V
    ),
    Spell('Cone of Cold','M',5,
        cast=tp(5,S),
        duration=tp(0),
        sourcebook=V,
        desc="When this spell is cast, it causes a cone-shaped area originating at the magic-user's hand and extending outwards in a cone ½\" long per level of the caster. It drains heat and causes 1 four-sided die, plus 1 hit point of damage (1d4 +1), per level of experience of the magic-user. For example, a 10th level magic-user would cast a Cone Of Cold causing 10d4 + 10 hit points of damage. Its material component is a crystal or glass cone of very small size."
    ),
    Spell('Contact Other Plane','M',5,
        cast=tp(1,T),
        duration=tp(1,VA),
        sourcebook=V
    ),
    Spell('Dismissal','M',5,
        cast=tp(1,R),
        duration=tp(1,P),
        sourcebook=U
    ),
    Spell('Distance Distortion','M',5,
        cast=tp(6,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="This spell can only be cast when the magic-user has an earth elemental conjured up, but the elemental will not react hostilely to co-operation with the spell caster when he or she announces that his or her intent is to cast a Distance Distortion spell. The magic places the earth elemental in the area of effect, and the elemental then causes the area's dimensions to be distorted in either of two ways: 1) the area will effectively be one-half the distance to those travelling over it, or 2) the area will be twice the distance to those travelling across it. Thus a 10' X 100' corridor could seem as if it was but 5' wide and 50' long, or it could appear to be 20' wide and 200' long. When the spell duration has elapsed, the elemental returns to its own plane. The true nature of an area affected by Distance Distortion is absolutely undetectable to any creatures travelling along it, although the area will radiate a dim dweomer, and a True Seeing spell will reveal that an earth elemental is spread within the area. Material needed for this spell is a small lump of soft clay."
    ),
    Spell('Dolor','M',5,
        cast=tp(5,S),
        duration=tp(2,R),
        sourcebook=U
    ),
    Spell('Extension II','M',5,
        cast=tp(4,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="This spell is the same as the fourth level Extension I spell, except it extends the duration of first through fourth level spells by 50%."
    ),
    Spell('Fabricate','M',5,
        cast=tp(1,VA),
        duration=tp(1,P),
        sourcebook=U
    ),
    Spell('Feeblemind','M',5,
        cast=tp(5,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the sixth level druid spell, Feeblemind (q.v.). The material component of this spell is a handful of small clay, crystal, glass or mineral spheres."
    ),
    Spell('Hold Monster','M',5,
        cast=tp(5,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell immobilizes from one to four creatures of any type within spell range and in sight of the spell caster. He or she can opt to hold one, two, three or four monsters. If three or four are attacked, each saving throw is a normal; if two are attacked, each saving throw is at -1 on the die; and if but one is attacked, the saving throw is at -3 on the die. (Partially-negated Hold Monster spell effects equal those of a Slow spell.) The material component for this spell is one hard metal bar or rod for each monster to be held. The bar or rod can be small, i.e. the size of a three-penny nail."
    ),
    Spell('Leomund\'s Lamentable Belabourment','M',5,
        cast=tp(5,S),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Leomund\'s Secret Chest','M',5,
        cast=tp(1,T),
        duration=tp(60,D),
        sourcebook=V,
        desc="In order to cast this spell the magic-user must have an exceptionally well-crafted and expensive chest constructed for him by master craftsmen. If made principally of wood, it must be of ebony, rosewood, sandalwood, teak or the like, and all of its corner fittings, nails, and hardware must be of platinum. If constructed of ivory. the metal fittings of the chest may be of gold; and if the chest is fashioned from bronze, copper, or silver, its fittings may be of electrum or silver. The cost of such a chest will never be less than 5,000 g.p. Once constructed, the magic-user must have a tiny replica (of the same materials and perfect in every detail) made, so that the miniature of the chest appears to be a perfect copy. One magic-user can have but one pair of these chests at any given time, and even wish spells will not allow exceptions. While touching the chest and holding the tiny replica, the caster chants the spell. This will cause the large chest to vanish into the ethereal plane. The chest can contain one cubic foot of material per level of the magic-user no matter what its apparent size. Living matter makes it 75% likely that the spell will fail, so the chest is typically used for securing valuable spell books, magic items, gems, etc. As long as the spell caster has the small duplicate of the magic chest, he or she can recall the large one from the ethereal plane to the locale he or she is in when the chest is desired. If the miniature of the chest is lost or destroyed, there is no way, including a wish, that the large chest will return. While on the ethereal plane, there is a 1% cumulative chance per week that some creature/being will find the chest. If this occurs there is 10% likelihood that the chest will be ignored, 10% possibility that something will be added to the contents, 30% possibility that the contents will be exchanged for something else, 30% chance that something will be stolen from it, and 20% probability that it will be emptied. In addition, when the secret chest is brought back to the Prime Material Plane, an ethereal window is opened and remains open for 5 hours, slowly diminishing in size. As this hole opens between the planes there is a 5% chance that some ethereal monster will be drawn through, with a 1% cumulative reduction in probability each hour thereafter until the window is gone. However, no creature on the Prime Material Plane can locate the chest even with a gem of seeing, true seeing, etc. If Leomund's Secret Chest is not retrieved before spell duration lapses, there is a cumulative chance of 5% per day that the chest will be lost forever, i.e. 5% chance for loss at 61 days, 10% at 62 days, and so forth."
    ),
    Spell('Magic Jar','M',5,
        cast=tp(1,R),
        duration=tp(1,VA),
        sourcebook=V
    ),
    Spell('Monster Summoning III','M',5,
        cast=tp(5,S),
        duration=tp(4,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="When this spell is cast, 1-4 third level monsters are summoned, coming within 1-4 rounds. See Monster Summoning I for other details."
    ),
    Spell('Mordenkainen\'s Faithful Hound','M',5,
        cast=tp(5,S),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="By means of this spell the magic-user summons up a phantom watchdog which only he or she can see, He or she may then command it to perform as guardian of a passage, room, door, or similar space or portal. The phantom watchdog will immediately commence a loud barking if any creature larger than a cat approaches the place it guards. As the Faithful Hound is able to detect invisible, astral, ethereal, out of phase, duo-dimensional, or similarly non-visible creatures, it is an excellent guardian. In addition, if the intruding creature or creatures allow their backs to be exposed to the phantom watchdog, it will deliver a vicious attack as if it were a 10 hit dice monster, striking for 3-18 hit points of damage, and being able to hit opponents of all sorts, even those normally subject only to magical weapons of +3 or greater. The Faithful Hound cannot be attacked, but it can be dispelled. Note, however, that the spell caster can never be more than 3\" distant from the area that the phantom watchdog is guarding, or the magic is automatically dispelled. The material components of this spell are a tiny silver whistle, a piece of bone, and a thread."
    ),
    Spell('Passwall','M',5,
        cast=tp(5,S),
        duration=tp(6,T),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="A Passwall enables the spell caster to open a passage through wooden, plaster, or stone walls; thus he or she and any associates can simply walk through. The spell causes a 5' wide by 8' high by 10' deep opening. Note several of these spells will form a continuing passage so that very thick walls can be pierced. The material component a this spell is a pinch of sesame seeds."
    ),
    Spell('Sending','M',5,
        cast=tp(1,T),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Stone Shape','M',5,
        cast=tp(1,R),
        duration=tp(1,P),
        sourcebook=V,
        desc="By means of this spell the magic-user can form an existing piece of stone into a shape which will suit his or her purposes. For example, a stone weapon can be made, a special trapdoor fashioned, or an idol sculpted. By the same token, it would allow the spell caster to reshape a stone door, perhaps, so as to escape imprisonment providing the volume of stone involved was within the limits of the area of effect. While stone coffers can be thus formed, secret doors made, etc., the fineness of detail is not great. The material component of this spell is soft clay which must be worked into roughly the desired shape of the stone object and then touched to the stone when the spell is uttered."
    ),
    Spell('Telekinesis','M',5,
        cast=tp(5,S),
        duration=tp(2,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="By means of this spell the magic-user is able to move objects by will force, by concentrating on moving them mentally. The Telekinesis spell causes the desired object to move vertically or horizontally. Movement is 2\" the first round, 4\" the second, 8\" the third, 16\" the fourth, and so on, doubling each round until a maximum telekinetic movement of 1,024\" per round is reached. (Heavy objects travelling at high speed can be deadly weapons!) Note that Telekinesis can be used to move opponents who fall within the weight capacity of the spell, but if they are able to employ as simple a counter-measure as an Enlarge spell, for example (thus making the body weight go over the maximum spell limit), it is easily countered. Likewise, ambulation or some other form of motive power if the recipient of the spell is not able to ambulate, counters the effect of Telekinesis, provided the velocity has not reached 16\" per round. The various Bigby's Hand spells will also counter this spell, as will many other magics."
    ),
    Spell('Teleport','M',5,
        cast=tp(2,S),
        duration=tp(0),
        sourcebook=V
    ),
    Spell('Transmute Rock To Mud','M',5,
        cast=tp(5,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="Except as noted above, and that the material components for the spell are clay and water (or sand, lime and water for the reverse), this spell is the same as the fifth level druid spell, Transmute Rock To Mud."
    ),
    Spell('Wall of Force','M',5,
        cast=tp(5,S),
        duration=tp(1,T),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="A Wall Of Force spell creates an invisible barrier in the locale desired by the caster, up to the spell's range. The Wall Of Force will not move and is totally unaffected by any other spells, including Dispel Magic, save a Disintegrate spell, which will immediately destroy it. Likewise, the Wall Of Force is not affected by blows, missiles, cold, heat electricity, or any similar things. Spells or breath weapons will not pass through it in either direction. The magic-user can, if desired, shape the wall to a hemispherical or spherical shape with an area equal to his or her ability, maximum of 20 square feet per level of experience. The material component for this spell is a pinch of powdered diamond."
    ),
    Spell('Wall of Iron','M',5,
        cast=tp(5,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="When this spell is cast, the magic-user causes a vertical iron wall to spring into being. Typically, this wall is used to seal off a passage or close a breach, for the wall inserts itself into any surrounding material if its area is sufficient to do so. The Wall Of Iron is one quarter of an inch thick per level of experience of the spell caster. The magic-user is able to evoke an area of iron wall 15 square feet for each of his or her experience levels, so at 12th level a Wall Of Iron 180 square feet in area can be created. If the wall is created in a location where it is not supported, it will fall and crush any creature beneath it. The wall is permanent, unless attacked by a Dispel Magic spell, but subject to all forces a normal iron wall is subject to. i.e. rust, perforation, etc. The material component of this spell is a small piece of sheet iron."
    ),
    Spell('Wall of Stone','M',5,
        cast=tp(5,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell creates a wall of granite rock which merges into adjoining rock surfaces if the area is sufficient to allow it. It is typically employed to close passages, portals, and breaches against opponents. The wall of stone is ¼' thick and 20' square in area per level of experience of the magic-user casting the spell. Thus, a 12th level magic-user creates a wall of stone 3' thick and 240 square feet in surface area (a 12' wide and 20' high wall, for example, to completely close a 10' x 16' passage). The wall created need not be vertical nor rest upon any firm foundation (cf. wall of iron); however, it must merge with an existing stone formation. It can be used to bridge a chasm, for instance, or as a ramp. The wall is permanent unless destroyed by a Dispel Magic spell or by normal means such as breaking, chipping or a Disintegrate spell The material component is a small block of granite."
    ),
    Spell('Anti-Magic Shell','M',6,
        cast=tp(1,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="By means of an Anti-Magic Shell, the magic-user causes an invisible barrier to surround his or her person. and this moves with the spell caster. This barrier is totally impervious to all magic and magic spell effects (this includes such attack forms as breath weapons, gaze weapons, and voice weapons). It thus prevents the entrance of spells or their effects, and it likewise prevents the function of any magical items or spells within its confines. It prevents the entrance of charmed, summoned, and conjured creatures. However, normal creatures (assume a normal troll rather than one conjured up, for instance) can pass through the shell, as can normal missiles. While a magic sword would not function magically within the shell, it would still be a sword."
    ),
    Spell('Bigby\'s Forceful Hand','M',6,
        cast=tp(6,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="Bigby's Forceful Hand is a more powerful version of Bigby's Interposing Hand (q.v.). It exerts a force in addition to interposing itself, and this force is sufficient to push a creature away from the spell caster if the creature weighs 500 pounds or less, to push so as to slow movement to 1\" per round if the creature weighs between 500 and 2,000 pounds, and to slow movement by 50% of creatures weighing up to 8,000 pounds. It takes as many hit points to destroy as its creator has. Its material component is a glove."
    ),
    Spell('Chain Lightning','M',6,
        cast=tp(6,S),
        duration=tp(0),
        sourcebook=U
    ),
    Spell('Contingency','M',6,
        cast=tp(1,T),
        duration_lvl=tp(1,D),
        sourcebook=U
    ),
    Spell('Control Weather','M',6,
        cast=tp(1,T),
        duration=tp(1,VA),
        sourcebook=V,
        desc="Except as noted above, and for the differing material components, this spell is the same as the seventh level cleric Control Weather spell (q.v.). The material components of this spell are burning incense, and bits of earth and wood mixed in water."
    ),
    Spell('Death Spell','M',6,
        cast=tp(6,S),
        duration=tp(0),
        sourcebook=V
    ),
    Spell('Disintegrate','M',6,
        cast=tp(6,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell causes matter to vanish. It will affect even matter (or energy) of a magical nature, such as Bigby's Forceful Hand, but not a Globe Of Invulnerability or an Anti-Magic Shell. Disintegration is instantaneous, and its effects are permanent. Any living thing can be affected, even undead, and non-living matter up to 1\" cubic volume can be obliterated by the spell. Creatures, and magical material with a saving throw, which successfully save versus the spell are not affected. Only 1 creature or object can be the target of the spell. Its material components are a lodestone and a pinch of dust."
    ),
    Spell('Enchant An Item','M',6,
        cast=tp(1,VA),
        duration=tp(1,VA),
        sourcebook=V,
        desc="This is a spell which must be used by a magic-user planning to create a magic item. The Enchant An Item spell prepares the object to accept the magic to be placed upon or within it. The item to be magicked must meet the following tests: 1) it must be in sound and undamaged condition; 2) the item must be the finest possible, considering its nature, i.e. crafted of the highest quality material and with the finest workmanship; and 3) its cost or value must reflect the second test, and in most cases the item must have a raw materials cost in excess of 100 g.p. With respect to requirement 3), it is not possible to apply this test to items such as ropes, leather goods, cloth, and pottery not normally embroidered, bejeweled, tooled, carved, and/or engraved; however, if such work or materials can be added to on item without weakening or harming its normal functions, these are required for the item to be magicked. The item to be prepared must be touched manually by the spell caster. This touching must be constant and continual during the casting time which is a base 16 hours plus an additional 8-64 hours (as the magic-user may never work over 8 hours per day, and haste or any other spells will not alter time required in any way, this effectively means that Casting Time for this spell is 2 days + 1-8 days). All work must be uninterrupted, and during rest periods the item being enchanted must never be more than 1' distant from the spell caster, for if it is, the whole spell is spoiled and must be begun again. (Note that during rest periods absolutely no other form of magic may be performed, and the magic-user must remain quiet and in isolation.) At the end of the spell, the caster will \"know\" that the item is ready for the final test. He or she will then pronounce the final magical syllable, and if the item makes a saving throw (which is exactly the same as that of the magic-user who magicked it) versus magic, the spell is completed. (Note that the spell caster's saving throw bonuses also apply to the item, up to but not exceeding +3.) A result of 1 on the die (d20) always results in failure, regardless of modifications. Once the spell is finished, the magic-user may begin to place the desired dweomer upon the item, and the spell he or she plans to place on or within the item must be cast within 24 hours or the preparatory spell fades, and the item must again be enchanted. Each spell subsequently cast upon an object bearing an enchant an item spell requires 4 hours + 4-8 additional hours per spell level of the magic being cast. Again, during casting the item must be touched by the magic-user, and during rest periods it must always be within 1' of his or her person. This procedure holds true for any additional spells placed upon the item, and each successive dweomer must be begun within 24 hours of the last, even if any prior spell failed. No magic placed on or into an item is permanent unless a Permanency spell is used as a finishing touch, and this always runs a risk of draining a point of constitution from the magic-user casting the spell. It is also necessary to point out that while it is possible to tell when the basic (Enchant An Item) spell succeeds, it is not possible to tell if successive castings actually take, for each must make the same sort of saving throw as the item itself made. Naturally, items that are charged - rods, staves, wands, javelins of lightning, ring of wishes, etc. - can never be made permanent. Scrolls or magic devices can never be used to enchant an item or cast magic upon an object so prepared. The material component(s) for this spell vary according to both the nature of the item being magicked and successive magicks to be cast upon it. For example, a cloak of displacement might require the hides of 1 or more displacer beasts, a sword meant to slay dragons could require the blood and some other part of the type(s) of dragon(s) it will be effective against, and a ring of shooting stars might require pieces of meteorites and the horn of a ki-rin. These specifics, as well as other information pertaining to this spell, are known by your Dungeon Master."
    ),
    Spell('Ensnarement','M',6,
        cast=tp(1,T),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Extension III','M',6,
        cast=tp(5,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="This spell is the same as the fourth level Extension I except that it will extend first through third level spells to double duration and will extend the duration of fourth or fifth level spells by 50% of the indicated duration."
    ),
    Spell('Eyebite','M',6,
        cast=tp(1,S),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Geas','M',6,
        cast=tp(4,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="A Geas spell places a magical command upon the creature (usually human or humanoid) to carry out some service, or refrain from same action or course of activity, as desired by the spell caster. The creature must be intelligent, conscious, and under its own volition. While a Geas cannot compel a creature to kill itself, or to perform acts which are likely to result in certain death, it can cause almost any other course of action. The spell causes the geased creature to follow the instructions until the Geas is completed. Failure to do so will cause the creature to grow sick and die within 1 to 4 weeks. Deviation from or twisting of the instructions causes corresponding loss of strength points until the deviation ceases. A Geas can be done away with by a Wish spell, but a Dispel Magic or Remove Curse will not negate it. Your referee will instruct you as to any additional details of a geas, for its casting and fulfilment are tricky. and an improperly cast Geas is null and void immediately (cf. Wish)."
    ),
    Spell('Glassee','M',6,
        cast=tp(1,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="By means of this spell the magic-user is able to make a section of metal, stone or wood as transparent as glass to his gaze, or even make it into transparent material as explained hereafter. Normally, up to four inches of metal can be seen through, stone up to 6' thick can be made transparent, and 20' of wood can be affected by the Glassee spell. The spell will not work on lead, gold or platinum. The magic-user can opt to make the Glassee apply to himself or herself only, and apply it up to once per round while spell duration lasts; or the caster can actually make a transparent area, a one-way window, in the material affected. Either case gives a viewing area 3' wide by 2' high. The material component of the spell is a small piece of crystal or glass."
    ),
    Spell('Globe of Invulnerability','M',6,
        cast=tp(1,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell is the same as the fourth level Minor Globe Of Invulnerability (q.v.), except as regards casting time and for the fact that it prevents the functioning of first through fourth level spell, affecting the magic-user within the globe, while he or she can cast spells through it, of course."
    ),
    Spell('Guards and Wards','M',6,
        cast=tp(3,T),
        duration_lvl=tp(6,T),
        sourcebook=V
    ),
    Spell('Invisible Stalker','M',6,
        cast=tp(1,R),
        duration=tp(1,VA),
        sourcebook=V,
        desc="This spell summons an invisible stalker from the Elemental Plane of Air. This 8 hit die monster will obey and serve the spell caster in performance at whatever tasks are set before it. However, the creature is bound to serve; it does not do so from loyalty or desire. Therefore, ii will resent prolonged missions or complex tasks, and it will attempt to pervert instructions accordingly (for complete details of the invisible stalker, consult ADVANCED DUNGEONS & DRAGONS, MONSTER MANUAL). The invisible stalker will follow instructions even at hundreds or thousands of miles distance. The material components of this spell are burning incense and a piece of horn carved into a crescent shape."
    ),
    Spell('Legend Lore','M',6,
        cast=tp(1,VA),
        duration=tp(0),
        sourcebook=V,
        desc="The Legend Lore spell is used to determine information available regarding a known person. place or thing. If the person or thing is at hand, or if the magic-user is in the place in question, the likelihood of the spell producing results is far greater and the casting time is only 1 to 4 turns. If detailed information on the person, place or thing is known, casting time is 1 to 10 days. If only rumours are known, casting time is 2 to 12 weeks. During the casting, the magic-user cannot engage in other activities other than routine: eating, sleeping, etc. When completed, the divination will reveal if legendary material is available. It will often reveal where this material is - by place name, rhyme, or riddle. It will sometimes give certain information regarding the person, place or thing (when the object of the Legend Lore is at hand), but this data will always be in some cryptic form (rhyme, riddle, anagram, cipher, sign, etc.). The spell is cast with incense and strips of ivory formed into a rectangle, but some item must be sacrificed in addition - a potion, magic scroll, magic item, creature, etc. Naturally, Legend Lore will reveal information only if the person, place or thing is noteworthy or legendary."
    ),
    Spell('Lower Water','M',6,
        cast=tp(1,T),
        duration_lvl=tp(5,R),
        sourcebook=V,
        desc="Except as noted above, and for the facts that the reverse spell raises water only ½'/level of experience of the spell caster, and the material components for the spell are a small vial of water and a small vial of dust, it is the same as the fourth level cleric spell, Lower Water (q.v.)."
    ),
    Spell('Monster Summoning IV','M',6,
        cast=tp(6,S),
        duration=tp(5,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell summons 1 to 3 fourth level monsters, and they appear within 1 to 3 rounds. See Monster Summoning I for other details."
    ),
    Spell('Mordenkainen\'s Lucubration','M',6,
        cast=tp(1,S),
        duration=tp(0),
        sourcebook=U
    ),
    Spell('Move Earth','M',6,
        cast=tp(1,VA),
        duration=tp(1,P),
        sourcebook=V,
        desc="When cast the Move Earth spell moves dirt (clay, loam, sand) and its other components. Thus, embankments can be collapsed, hillocks moved, dunes shifted, etc. The area to be affected will dictate the casting time; for every 4\" square area, 1 turn of casting time is required. If terrain features are to be moved - as compared to simply caving in banks or walls of earth - it is necessary that an earth elemental be subsequently summoned to assist. All spell casting and/or summoning must be completed before any effects occur. In no event can rock prominences be collapsed or moved. The material components for this spell are a mixture of soils (clay, loam, sand) in a small bag, and an iron blade."
    ),
    Spell('Otiluke\'s Freezing Sphere','M',6,
        cast=tp(6,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="Otiluke's Freezing Sphere is a multi-purpose dweomer of considerable power. If the caster opts, he or she may create a globe of matter at absolute zero temperature which spreads upon contact with water or liquid which is principally composed of water, so as to freeze it to a depth of 6 inches over an area equal to 100 square feet per level of the magic-user casting the spell. The ice so formed lasts for 1 round per level of the caster. The spell can also be used as a thin ray of cold which springs from the caster's hand to a distance of 1\" per level of the magic-user; this ray will inflict 4 hit points of damage per level of the caster upon the creature struck, with a saving throw versus magic applicable, and all damage negated if it is successful (as the ray is so narrow a save indicates it missed), but the path of the ray being plotted to its full distance, as anything else in its path must save (if applicable) or take appropriate damage. Finally, Otiluke's Freezing Sphere can be cast so as to create a small globe about the size of a sling stone, cool to the touch, but not harmful. This globe can be cast, and it will shatter upon impact, inflicting 4-24 hit points of cold damage upon all creatures within a 10' radius (one-half damage if saving throw versus magic is made). Note that if the globe is not thrown or slung within a time period equal to 1 round times the level of the spell caster, it automatically shatters and causes cold damage as stated above. This timed effect can be employed against pursuers, although it can also prove hazardous to the spell caster and/or his or her associates as well. The material components of the spell depend upon in which form it is to be cast. A thin sheet of crystal about an inch square is needed for the first application of the spell, a white sapphire of not less than 1,000 g.p. value for the second application of the spell, and a 1,000 g.p. diamond is minimum for the third application of the spell. All components are lost when the spell is cast."
    ),
    Spell('Part Water','M',6,
        cast=tp(1,T),
        duration_lvl=tp(5,R),
        sourcebook=V,
        desc="Except as shown above, and also that the material components for this spell are two small sheets of crystal or glass, this spell is the same as the sixth level cleric spell, Part Water (q.v.)."
    ),
    Spell('Project Image','M',6,
        cast=tp(6,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="By means of this spell, the magic-user creates a non-material duplicate of himself or herself, projecting it to any spot within spell range which is desired. This image performs actions identical to the magic-user - walking, speaking, spell-casting - as the magic-user determines. A special channel exists between the image of the magic-user and the actual magic-user, so spells cast actually originate from the image. The image can be dispelled only by means of a Dispel Magic spell (or upon command from the spell caster), and attacks do not affect it. The image must be within view of the magic-user projecting it at all times, and if his or her sight is obstructed, the spell is broken. The material component of this spell is a small replica (doll) of the magic-user."
    ),
    Spell('Reincarnation','M',6,
        cast=tp(1,T),
        duration=tp(1,P),
        sourcebook=V
    ),
    Spell('Repulsion','M',6,
        cast=tp(6,S),
        duration_lvl=tp(5,S),
        sourcebook=V,
        desc="When this spell is cast, the magic-user is able to cause all creatures in the path of the area of effect to move away from his or her person. Repulsion is at 3\" per round, or at the motive speed of the creature attempting to move towards the spell caster. The repelled creature will continue to move away for the balance of a complete move even though this takes it beyond spell range. The material component of this spell is a pair of small magnetized iron bars attached to two small canine statuettes, one ivory and one ebony."
    ),
    Spell('Spiritwrack','M',6,
        cast=tp(3,R),
        duration_lvl=tp(1,Y),
        sourcebook=V,
        desc="A Spiritwrack spell is a very strong protection/punishment spell against the powerful creatures of the nether planes (Abyssal, Hades, Hell, etc.), but to employ the magic, the spell caster must know the name of the being at whom he or she will direct the energy. Prior to actual utterance of a Spiritwrack spell the magic-user must prepare an illuminated sheet of vellum, carefully inscribed in special inks made from powdered rubies and the ichor of a slain demon of type I, II, or III and covered with gold leaf in a continuous border. The spell caster must personally prepare this document, including the being's name thereon. (This will require from 8-32 hours of time and cost 1,000 g.p. for vellum, special pens, gold leaf, and other miscellaneous materials alone; the cost of the powdered rubies is a minimum of 5,000 g.p. for each document.) If the demon, devil, or other powerful being from a nether outer plane is present in some form (and not possessing another creature's body instead), the magic-user can then begin actual spell incantation. Immediately upon beginning the reading of the document, the being named will be rooted to the spot unless it makes its magic resistance percentage (adjusted for the level of the magic-user) as a saving throw; and even if such a saving throw is made, the monster feels greatly uncomfortable, and if it has not been magically forced to the locale and so held there, it is 90% likely to retreat to its own (or another) plane, as the named being is powerless to attack the magic-user while he or she is reading the spell document. This first part of the document continues for 1 full round, with the discomfort to the named being becoming greater at the end. During the second minute of the incantation, the being named undergoes acute pain and loses 1 hit point per hit die it possesses. At the end of this round of reading, the being is in wracking pain. The third and final round of utterance of the condemnation will cause a loss to the being of 50% of its existing hit points, horrible pain, and at the end consign it to some confined space on its own plane - there to remain in torture for a number of years equal to the level of the magic-user who prepared the document. Obviously, the being so dealt with will be the sworn foe of the magic-user forever afterwards, so the magic-user will be loath to finish the spell but rather use it as a threat to force submission of the being. Each round of reading will cause the being forced to listen to be a cumulative 25% likely to concede even without any other offerings or payment."
    ),
    Spell('Stone To Flesh','M',6,
        cast=tp(6,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="The Stone To Flesh spell turns any sort of stone into flesh - if the recipient stone object was formerly living, it will restore life (and goods), although the survival of the creature is subject to the usual system shock survival dice roll. Any formerly living creature, regardless of size, can be thus returned to flesh. Ordinary stone can be likewise turned to flesh at a volume of 9 cubic feet per level of experience of the spell caster. The reverse will turn flesh of any sort to stone, just as the Stone To Flesh spell functions. All possessions on the person of the creature likewise turn to stone. This reverse of the spell will require a saving throw be allowed the intended victim. The material components of the spell are a pinch of earth and a drop of blood; lime and water and earth are used for the reverse."
    ),
    Spell('Tenser\'s Transformation','M',6,
        cast=tp(6,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="Tenser's Transformation is a sight guaranteed to astound any creature not aware of its power, for when the magic-user casts the dweomer, he or she undergoes a startling transformation. The size and strength of the magic-user increase to heroic proportions, so he or she becomes a formidable fighting machine, for the spell causes the caster to become a berserk fighter. The magic-user's hit points double, and all damage he or she sustains comes first from the magical points gained; so if damage does not exceed original hit points, none is actually taken, but if damage beyond the additional amount is sustained. each point counts as 2 (double damage). The armour class of the magic-user is a full 4 factors better than that he or she possessed prior to casting the spell (AC 10 goes to 6, AC 9 to 5, AC 8 to 4, etc.), all attacks are at a level equal to those of a fighter of the same level as the magic-user (i.e., the spell caster uses the combat table normally restricted to fighters), and although he or she can employ a dagger only in attacking, damage inflicted by the weapon is at +2 additional hit points, and 2 such attacks per round are made by the magic-user. However, it is worth noting that this spell must run its full course, and the magic-user will continue attacking until all opponents are slain, he or she is killed, the magic is dispelled, or the Transformation duration expires. The material component for casting this dweomer is a potion of heroism (or superheroism) which the magic-user must consume during the course of uttering the spell."
    ),
    Spell('Transmute Water To Dust','M',6,
        cast=tp(6,S),
        duration=tp(1,P),
        sourcebook=U
    ),
    Spell('Banishment','M',7,
        cast=tp(7,S),
        duration=tp(1,P),
        sourcebook=U
    ),
    Spell('Bigby\'s Grasping Hand','M',7,
        cast=tp(7,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="Bigby's Grasping Hand is a superior version of the sixth level Bigby's Forceful Hand spell (q.v.), being like it in many ways. The Grasping Hand can actually hold motionless a creature or object of up to 1,000 pounds weight, or move creatures as a double strength Forceful Hand. The material component is a leather glove."
    ),
    Spell('Cacodemon','M',7,
        cast=tp(1,VA),
        duration=tp(1,VA),
        sourcebook=V
    ),
    Spell('Charm Plants','M',7,
        cast=tp(1,T),
        duration=tp(1,P),
        sourcebook=V,
        desc="The Charm Plants spell allows the spell caster to bring under command vegetable life forms, communicate with them, and these plants will obey instructions to the best of their ability. The spell will charm plants in a 3\" x 1\" area. While the spell does not endow the vegetation with new abilities, it does allow the magic-user to command the plants to use whatever they have in order to fulfil his or her instructions, and if the plants in the area of effect do have special or unusual abilities, these will be used as commanded by the magic-user. The saving throw applies only to intelligent plants, and it is made at -4 on the die roll. The material components of the spell area pinch of humus, a drop of water and a twig or leaf."
    ),
    Spell('Delayed Blast Fireball','M',7,
        cast=tp(7,S),
        duration=tp(5,R),
        sourcebook=V,
        desc="This spell creates a fire ball with +1 on each of its dice of damage, and it will not release its blast for from 1 to 50 segments (1/10 to 5 rounds), according to the command upon casting by the magic-user. In other respects, the spell is the same as the third level Fireball spell (q.v.)."
    ),
    Spell('Drawmij\'s Instant Summons','M',7,
        cast=tp(1,S),
        duration=tp(0),
        sourcebook=V,
        desc="When this spell is cast, the magic-user teleports some desired item from virtually any location directly to his or her hand. The object must be singular, can be no larger than a sword is long, have no more mass and weight than a shield (about 75 g.p. weight), and it must be non-living. To prepare this spell, the magic-user must hold a gem of not less than 5,000 g.p. value in his or her hand and utter all but the final word of the conjuration. He or she then must have this same gem available to cast the spell. All that is then required is that the magic-user utter the final word while crushing the gem, and the desired item is transported instantly into the spell caster's right or left hand as he or she desires. The item must, of course, have been previously touched during the initial incantation and specifically named, and only that particular item will be summoned by the spell. If the item is in the possession of another creature, the spell will not work, but the caster will know who the possessor is and roughly where he, she, or it is located when the summons is cast. Items can be summoned from other planes of existence, but only if such items are not in the possession (not necessarily physical grasp) of another creature. For each level of experience above the 14th, the magic-user is able to summon a desired item from 1 plane further removed from the plane he or she is upon at the time the spell is cast, i.e. 1 plane at 14th level, but 2 at 15th, 3 at 16th. etc. Thus, a magic-user of 16th level could effect the spell even if the item desired was on the second layer of one of the outer planes, but at 14th level the magic-user would be able to summon the item only if it were on one of the Elemental Planes or the Astral or the Ethereal Plane."
    ),
    Spell('Duo-Dimension','M',7,
        cast=tp(7,S),
        duration=tp(3,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="A Duo-Dimension spell causes the caster to have only two dimensions, height and width but no depth. He or she is thus invisible when a sideways turn is made, and this invisibility can only be detected by means of a true seeing spell or similar means. In addition, the duo-dimensional magic-user can pass through the thinnest of spaces as long as they have the proper height according to his or her actual length - going through the space between a door and its frame is a simple matter. The magic-user can perform all actions on a normal basis. He or she can turn and become invisible, move in this state, and appear again next round and cast a spell, disappearing on the following round. Note that when turned the magic-user cannot be affected by any form of attack, but when visible he or she is subject to triple the amount of damage normal for an attack form, i.e. a dagger thrust would inflict 3-12 hit points of damage if it struck a duo-dimensional magic-user. Furthermore, the magic-user has a portion of his or her existence on the Astral Plane when the spell is in effect, and he or she is subject to possible notice from creatures thereupon. If noticed, it is 25% probable that the magic-user will be entirety brought to the Astral Plane by attack from the astral creature. The material components of this spell are a thin, flat ivory likeness of the spell caster (which must be of finest workmanship, gold filigreed, and enamelled and gem-studded at an average cost of 5,000 to 10,000 g.p.) and a strip of parchment. As the spell is uttered, the parchment is given a half twist and joined at the ends. The figurine is then passed through the parchment loop, and both disappear forever."
    ),
    Spell('Forcecage','M',7,
        cast=tp(1,VA),
        duration=tp(6,T),
        duration_lvl=tp(1,T),
        sourcebook=U
    ),
    Spell('Limited Wish','M',7,
        cast=tp(1,VA),
        duration=tp(1,VA),
        sourcebook=V,
        desc="A Limited Wish is a very potent but difficult spell. It will fulfil literally, but only partially or for a limited duration, the utterance of the spell caster. Thus, the actuality of the past, present or future might be altered (but possibly only for the magic-user unless the warding of the Limited Wish is most carefully stated) in some limited manner. The use of a Limited Wish will not substantially change major realities, nor will it bring wealth or experience merely by asking. The spell can, for example, restore some hit points (or all hit points for a limited duration) lost by the magic-user. It can reduce opponent hit probabilities or damage, it can increase duration of some magical effect, it can cause a creature to be favourably disposed to the spell caster, and so on (cf. Wish). The Limited Wish can possibly give a minor clue to some treasure or magic item. Greedy desires will usually end in disaster for the wisher. Casting time is the actual number of seconds - at six per segment - to phrase the Limited Wish."
    ),
    Spell('Mass Invisibility','M',7,
        cast=tp(7,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="This is the same as an Invisibility spell (q.v.) except that it can hide creatures in a 3\" x 3\" area, up to 300 to 400 man-sized creatures, 30 to 40 giants, or 6 to 8 large dragons."
    ),
    Spell('Monster Summoning V','M',7,
        cast=tp(6,S),
        duration=tp(6,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell summons 1-2 fifth level monsters, and they will appear in 1-3 rounds. See Monster Summoning I for other details."
    ),
    Spell('Mordenkainen\'s Magnificent Mansion','M',7,
        cast=tp(7,R),
        duration_lvl=tp(1,H),
        sourcebook=U
    ),
    Spell('Mordenkainen\'s Sword','M',7,
        cast=tp(7,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="Upon casting this spell, the magic-user brings into being a shimmering sword-like plane of force. The spell caster is able to mentally wield this weapon (to the exclusion of activities other than movement), causing it to move and strike as if it were being used by a fighter. The basic chance for Mordenkainen's Sword to hit is the same as the chance for a sword wielded by a fighter of one-half the level of the spell caster, i.e. if cast by a 12th level magic-user, the weapon has the same hit probability as a sword wielded by a 6th level fighter. The sword has no magical \"to hit\" bonuses, but it can hit any sort of opponent even those normally struck only by +3 weapons or astral, ethereal or out of phase; and it will hit any armour class on a roll of 19 or 20. It inflicts 5-20 hit points on opponents of man-size or smaller, and 5-30 on opponents larger than man-sized. It can be used to subdue. It lasts until the spell duration expires, a dispel magic is used successfully upon it, or its caster no longer desires it. The material component is a miniature platinum sword with a grip and pommel of copper and zinc which costs 500 g.p. to construct, and which disappears after the spell's completion."
    ),
    Spell('Phase Door','M',7,
        cast=tp(7,S),
        duration=tp(0),
        sourcebook=V,
        desc="When this spell is cast, the magic-user attunes he or her body, and a section of wall is affected as if by a Passwall spell (q.v.). The Phase Door is invisible to all creatures save the spell caster, and only he or she can use the space or passage the spell creates, disappearing when the Phase Door is entered, and appearing when it is exited. The Phase Door lasts for 1 usage for every 2 levels of experience of the spell caster. It can be dispelled only by a casting of Dispel Magic from a higher level magic-user, or by several lower level magic-users, casting in concert, whose combined levels of experience are more than double that of the magic-user who cast the spell."
    ),
    Spell('Power Word, Stun','M',7,
        cast=tp(1,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="When a Power Word, Stun is uttered, any creature of the magic-user's choice will be stunned - reeling and unable to think cogently or act for 2 to 8 (2d4) melee rounds. Of course, the magic-user must be facing the creature, and it must be within the spell caster's range or ½\" per level of experience. Creatures with 1 to 30 hit points will be stunned for 4-16 (4d4) rounds, those with 31 to 60 hit points will be stunned for 2 to (2d4) rounds, those with 61 to 90 hit points will be stunned for 1 to 4 (d4) rounds, and creatures with over 90 hit points will not be affected. Note that if a creature is weakened due to any cause so that its hit points are below the usual maximum, the current number of hit points possessed will be used."
    ),
    Spell('Reverse Gravity','M',7,
        cast=tp(7,S),
        duration=tp(1,S),
        sourcebook=V,
        desc="This spell reverses gravity in the area of effect, causing all unfixed objects and creatures within it to \"fall\" upwards. The Reverse Gavity lasts for 1 second (1/6 segment) during which time the objects and creatures will \"fall\" 16' up. If some solid object is encountered in this \"fall\", the object strikes it in the some manner as a normal downward fall. At the end of the spell duration, the affected objects and creatures fall downwards. As the spell affects an area, objects tens, hundreds or even thousands of feet in the air can be affected. The material components of this spell are a lodestone and iron filings."
    ),
    Spell('Sequester','M',7,
        cast=tp(1,R),
        duration=tp(7,D),
        duration_lvl=tp(1,D),
        sourcebook=U
    ),
    Spell('Simulacrum','M',7,
        cast=tp(1,VA),
        duration=tp(1,P),
        sourcebook=V,
        desc="By means of this spell the magic-user is able to create a duplicate of any creature. The duplicate appears exactly the same as the real. There are differences: the simulacrum will have only 51% to 60% (50% + 1% to 10%) of the hit points of the real creature, there will be personality differences, there will be areas of knowledge which the duplicate does not have, and a Detect Magic spell will instantly reveal it as a simulacrum, as will a True Seeing spell. At all times the simulacrum remains under the absolute command of the magic-user who created it, although no special telepathic link exists, so command must be exercised in the normal manner. The spell creates the form of the creature, but it is only a zombie-like creature. A Reincarnation spell must be used to give the duplicate a vital force, and a Limited Wish spell must be used to empower the duplicate with 40% to 65% (35% + 5% to 30%) of the knowledge and personality of the original. The level, if any, of the simulacrum, will be from 20% to 50% of the original creature. The duplicate creature is formed from ice or snow. The spell is cast over the rough form, and some piece of the creature to be duplicated must be placed inside the snow or ice. Additionally, the spell requires powdered ruby. The simulacrum has no ability to become more powerful, i.e. it cannot increase its levels or abilities."
    ),
    Spell('Statue','M',7,
        cast=tp(7,S),
        duration_lvl=tp(6,T),
        sourcebook=V,
        desc="When a Statue dweomer is cast, the magic-user or other creature is apparently turned to solid stone, along with any garments and equipment worn or carried. The initial transformation from flesh to stone requires 1 full round after the spell is cast. Thereafter the creature can withstand any inspection and appear to be a stone statue, although a faint magic will be detected from the stone if it is checked for. Despite being in this condition, the petrified individual can see, hear, and smell normally. Feeling is only as acute as that which will actually affect the granite-hard substance of the individual's body, i.e. chipping is equal to a slight wound, but breaking off one of the statue's arms is another matter. The individual under the magic of a Statue spell can return to normal state in 1/6 of a segment, and then return to statue state in the same period if he or she so desires, as long as the spell duration is in effect. During the initial transformation from flesh to stone, the creature must make a saving throw of 82% or less, with -1 deducted from the dice roll score for each point of his or her constitution score, so an 18 constitution indicates certain success. Failure indicates system shock and resultant death. The material components of this spell are lime, sand, and a drop of water stirred by an iron bar such as a nail or spike."
    ),
    Spell('Teleport Without Error','M',7,
        cast=tp(1,S),
        duration=tp(0),
        sourcebook=U
    ),
    Spell('Torment','M',7,
        cast=tp(1,R),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Truename','M',7,
        cast=tp(1,VA),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Vanish','M',7,
        cast=tp(2,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="When the magic-user employs this spell, he or she causes an object to vanish. The magic-user can cause the object to be teleported (see Teleport spell) if it weighs up to a maximum of 500 g.p. per level of experience of the spell caster, i.e. 14th level magic-user can vanish and cause to reappear at his or her desired location 7000 g.p. weight. Greater objects can be made to vanish, but they are simply placed into the ethereal plane and replaced with stone. Thus, a door can be made to disappear, and it will be replaced by a stone wall of 1' thickness, or equal in thickness to the door, whichever is greater. The maximum volume of material which can be affected is 3 cubic feet per level of experience. Thus, both weight and volume limit the spell. A Dispel Magic which is successful will bring back vanished items from the ethereal plane."
    ),
    Spell('Volley','M',7,
        cast=tp(1,S),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Antipathy/Sympathy','M',8,
        cast=tp(6,T),
        duration_lvl=tp(12,T),
        sourcebook=V
    ),
    Spell('Bigby\'s Clenched Fist','M',8,
        cast=tp(8,S),
        duration_lvl=tp(1,R),
        sourcebook=V
    ),
    Spell('Binding','M',8,
        cast=tp(1,VA),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Clone','M',8,
        cast=tp(1,T),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell creates a duplicate of a person. This clone is in all respects the duplicate of the individual, complete to the level of experience, memories, etc. However, the duplicate is the person, so that if the original and a duplicate exist at the same time, each knows of the other's existence; and the original person and the clone will each desire to do away with the other, for such an alter-ego is unbearable to both. If one cannot destroy the other, one (95%) will go insane (75% likely to be the clone) and destroy itself, or possibly (5%) both will become mad and commit suicide. These probabilities will occur within 1 week of the dual existence. The material component of the spell is a small piece of the flesh of the person to be duplicated. Note that the clone will become the person as he or she existed at the time at which the flesh was taken, and all subsequent knowledge, experience, etc. will be totally unknown to the clone. Also, the clone will be a physical duplicate, and possessions of the original are another matter entirely. Note that a clone takes from 2-8 months to grow, and only after that time is dual existence established."
    ),
    Spell('Demand','M',8,
        cast=tp(1,T),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Glassteel','M',8,
        cast=tp(8,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="The Glassteel spell turns crystal or glass into a transparent substance which has the tensile strength and unbreakability of actual steel. Only a relatively small volume of material can be affected, a maximum weight of 10 pounds per level of experience of the spell caster, and it must form one whole object. The material components of this spell area small piece of glass and a small piece of steel."
    ),
    Spell('Incendiary Cloud','M',8,
        cast=tp(2,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="An Incendiary Cloud spell exactly resembles the smoke effects of a Pyrotechnics spell (q.v.), except that its minimum dimensions are a cloud of 10' height by 20' length and breadth. This dense vapour cloud billows forth, and on the 3rd round of its existence it begins to flame, causing ½ hit point per level of the magic-user who cast it. On the 4th round it does 1 hit point of damage per level of the caster, and on the 5th round it again drops to ½ h.p. of damage per level of the magic-user as its flames burn out. Any successive rounds of existence are simply harmless smoke which obscures vision within its confines. Creatures within the cloud need make only 1 saving throw if it is successful, but if they fail the first, they roll again an the 4th and 5th rounds (if necessary) to attempt to reduce damage sustained by one-half. In order to cast this spell the magic-user must have an available fire source (just as with a Pyrotechnics spell), scrapings from beneath a dung pile, and a pinch of dust."
    ),
    Spell('Mass Charm','M',8,
        cast=tp(8,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="A Mass Charm spell affects either persons or monsters just as a Charm Person spell or a Charm Monster spell (qq.v.) does. The Mass Charm, however, will affect a number of creatures whose combined levels of experience and/or hit dice does not exceed twice the level of experience of the spell caster. All affected creatures must be within the spell range and within a maximum area of 3\" by 3\". Note that the creatures' saving throws are unaffected by the number of recipients (cf. Charm Person and Charm Monster), but all target creatures are subject to a penalty of -2 on the saving throw because of the efficiency and power of a Mass Charm spell."
    ),
    Spell('Maze','M',8,
        cast=tp(3,S),
        duration=tp(1,VA),
        sourcebook=V
    ),
    Spell('Mind Blank','M',8,
        cast=tp(1,S),
        duration=tp(1,D),
        sourcebook=V,
        desc="When the very powerful Mind Blank spell is cast, the recipient is totally protected from all devices and/or spells which detect, influence, or read emotions and/or thoughts. Protection includes Augury, Charm, Command, Confusion, Divination, empathy (all forms), ESP, Fear, Feeblemind, Mass Ssuggestion, Phantasmal Killer, possession, rulership, soul trapping, Suggestion, and telepathy. Cloaking protection also extends to prevention of discovery or information gathering by crystal balls or other scrying devices, Clairaudience, Clairvoyance, communing, contacting other planes. or Wsh-related methods (Wishing, Limited Wish, Alter Reality). Of course, exceedingly powerful deities would be able to penetrate the spell's powers. Note that this spell also protects from psionic-related detection and/or influence such as Domination (or Mass Domination), Hypnosis, Invisibility (the psionic sort is mind related), and Precognition, plus those powers which are already covered as spells."
    ),
    Spell('Monster Summoning VI','M',8,
        cast=tp(8,S),
        duration=tp(7,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell summons 1 or 2 sixth level monsters, the creature(s) appearing in 1 to 3 rounds. See Monster Summoning I for other details."
    ),
    Spell('Otiluke\'s Telekinetc Sphere','M',8,
        cast=tp(4,S),
        duration_lvl=tp(1,R),
        sourcebook=U
    ),
    Spell('Otto\'s Irresistible Dance','M',8,
        cast=tp(5,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="When Otto's Irresistible Dance is placed upon a creature, the spell causes the recipient to begin dancing, feet shuffling and tapping. This dance makes it impossible for the victim to do anything other than caper and prance, this cavorting lowering the armour class of the creature by -4, making saving throws impossible, and negating any consideration of a shield. Note that the creature must be touched - possibly as if melee combat were taking place and the spell caster were striking to do damage."
    ),
    Spell('Permanency','M',8,
        cast=tp(2,R),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell affects the duration of certain other spells, making the duration permanent. The spells upon which a personal Permanency will be effective are: Comprehend Languages, Detect Evil, Detect Invisibility, Detect Magic, Infravision, Protection From Evil, Protection From Normal Missiles, Read Magic, Tongues, Unseen Servant. The magic-user casts the desired spell and then follows with the Permanency spell. Each Permanency spell lowers the magic-users constitution by 1 point. The magic-user cannot cast these spells upon other creatures. In addition to personal use, the Permanency spell can be used to make the following object/creature or area effect spells lasting: Enlarge, Fear, Gust Of Wind, Invisibility, Magic Mouth, Prismatic Sphere, Stinking Cloud, Wall Of Fire, Wall Of Force, Web. The former application of Permanency can be dispelled only by a magic-user of greater level than the spell caster was when he or she initially cast it. The Permanency application to other spells allows it to be cast simultaneously with any of the latter when no living creature is the target, but the Permanency can be dispelled normally, and thus the entire spell negated."
    ),
    Spell('Polymorph Any Object','M',8,
        cast=tp(1,R),
        duration=tp(1,VA),
        sourcebook=V
    ),
    Spell('Power Word, Blind','M',8,
        cast=tp(1,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="When a Power Word, Blind is cast, one or more creatures within spell range and area of effect will become temporarily sightless. The spell affects up to 100 hit points of creatures, but the duration is dependent upon how many hit points of creatures are affected. If 50 or less points are affected, blindness lasts for 2 to 5 (d4+1) turns, if 51 or more hit points of creatures are affected, the spell duration is but 2 to 5 rounds. Note that the spell caster must indicate which creatures he or she desires to affect with the spell, noting one as target centre, prior to determining results. Creatures with over 100 hit points are not affected. Blindness can be removed by Cure Blindness or Dispel Magic."
    ),
    Spell('Serten\'s Spell Immunity','M',8,
        cast=tp(1,VA),
        duration_lvl=tp(1,T),
        sourcebook=V
    ),
    Spell('Sink','M',8,
        cast=tp(8,S),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Symbol','M',8,
        cast=tp(8,S),
        duration=tp(1,P),
        sourcebook=V
    ),
    Spell('Trap The Soul','M',8,
        cast=tp(1,VA),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell is similar to the Magic Jar, except that the Trap The Soul spell forces the subject creature's life force (and its material body, if any) into a special prison magicked by the spell caster. The subject of the spell must be seen by the caster, and the magic-user must know the subject's true name as well when the final word is uttered. Preparatory to the actual casting of the Trap The Soul the magic-user must prepare the soul prison, a gem of 1,000 g.p. value for every hit die or level of experience the creature whose soul is to be trapped possesses, i.e. it requires a gem of 10,000 g.p. value to trap a 10 hit dice (or 10th level) creature by placing an Enchant An Item spell upon it and then placing a Maze spell into the gem, thereby forming the prison for the soul to be trapped. There are 2 manners in which the soul of the victim can be imprisoned. The final word of the spell can be spoken when the creature is within spell range, but this entitles it to exercise its magic resistance (if any) and a saving throw versus magic as well, and if the latter is successful, the gem shatters. The second method of soul trapping is far more insidious, for it tricks the victim into accepting a trigger object inscribed with the final spell word which will automatically place the creature's soul into the trap. If this method is used, it will be necessary to name the triggering item when the prison gem is magicked. A Sympathy spell may be placed on the trigger item. As soon as the subject creature picks up or accepts the trigger item, its soul is automatically transferred to the gem. The gem prison will hold the soul trapped until time indefinite, or until it is broken and the soul is released, allowing the material body to reform. If the creature trapped is a powerful creature from another plane (and this could actually mean a character trapped by some inhabitant of another plane of existence when the character is not on the Prime Material Plane), it can be required to perform a service immediately upon being freed. Otherwise, the creature can go totally free once the gem imprisoning it is broken."
    ),
    Spell('Astral Spell','M',9,
        cast=tp(9,S),
        duration=tp(0),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the seventh level cleric spell, Astral Spell (q.v.)."
    ),
    Spell('Bigby\'s Crushing Hand','M',9,
        cast=tp(9,S),
        duration_lvl=tp(1,R),
        sourcebook=V
    ),
    Spell('Crystalbrittle','M',9,
        cast=tp(9,S),
        duration=tp(1,P),
        sourcebook=U
    ),
    Spell('Energy Drain','M',9,
        cast=tp(3,S),
        duration=tp(1,P),
        sourcebook=U
    ),
    Spell('Gate','M',9,
        cast=tp(9,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the seventh level cleric spell, Gate (q.v.)."
    ),
    Spell('Imprisonment','M',9,
        cast=tp(9,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="When on Imprisonment spell is cast and the victim is touched, the recipient is entombed in a state of suspended animation (cf. Temporal Stasis) in a small sphere far below the surface of the earth. The victim remains there unless a reverse of the spell, with the creature's name and background, is cast. Magical search by crystal ball, a Locate Objects spell or similar means will not reveal the fact that a creature is imprisoned. The reverse (Freedom) spell will cause the appearance of the victim at the spot he, she or it was entombed and sunk into the earth. There is a 10% chance that 1 to 100 other creatures will be freed from Imprisonment at the same time if the magic-user does not perfectly get the name and background of the creature to be freed. The spell only works if the name and background of the victim are known."
    ),
    Spell('Meteor Swarm','M',9,
        cast=tp(9,S),
        duration=tp(0),
        sourcebook=V,
        desc="A Meteor Swarm is a very powerful and spectacular spell which is similar to a Fireball in many aspects. When it is cast, either four spheres of 2' diameter or eight spheres of 1' diameter spring from the outstretched hand of the magic-user and streak in a straight line up to the distance demanded by the spell caster, up to the maximum range. Any creature in the straight line path of these missiles will receive the full effect of the missile, or missiles, without benefit of a saving throw. The \"meteor\" missiles leave a fiery trail of sparks, and each bursts as a Fireball (q.v.). The large spheres each do 10 to 40 hit points of damage, the four bursting in a diamond or box pattern. Each has a 3\" diameter area of effect, and each sphere will be 2\" apart, along the sides of the pattern, so that there are overlapping areas of effect, and the centre will be exposed to all four blasts. The eight small spheres have one-half diameter (1½\") and one-half the damage potential (5-20). They burst in a pattern of a box within a diamond or vice versa, each of the outer sides 2\" long. and the inner sides being 1\" long. Note that the centre will have 4 areas of overlapping effect, and there are numerous peripheral areas which have two overlapping areas of effect. A saving throw for each area of effect will indicate whether full hit points of damage, or half the indicated amount of damage, will be sustained by creatures within each area, except as already stated with regard to the missiles impacting."
    ),
    Spell('Monster Summoning VII','M',9,
        cast=tp(9,S),
        duration=tp(8,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell summons 1 or 2 seventh level monsters which appear 1 round after the spell is cast, or 1 8th level monster which will appear 2 rounds after the spell is cast. See Monster Summoning I for other details."
    ),
    Spell('Mordenkainen\'s Disjunction','M',9,
        cast=tp(9,S),
        duration=tp(1,P),
        sourcebook=U
    ),
    Spell('Power Word, Kill','M',9,
        cast=tp(1,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="When a Power Word, Kill is uttered, one or more creatures within the spell range and area of effect will be slain. The Power Word will destroy a creature with up to 60 hit points, or it will kill 2 or more creatures with 10 or fewer hit points, up to a maximum of 20 hit points. The option to attack a single creature, or multiple creatures, must be stated along with the spell range and area of effect centre."
    ),
    Spell('Prismatic Sphere','M',9,
        cast=tp(7,S),
        duration_lvl=tp(1,T),
        sourcebook=V
    ),
    Spell('Shape Change','M',9,
        cast=tp(9,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="With this spell, the magic-user is able to assume the form of any creature short of a demigod, greater devil, demon prince, singular dragon type, greater demon or the like. The spell caster becomes the creature he or she wishes, and has all of the abilities save those dependent upon intelligence, for the mind of the creature is that of the spell caster. Thus, he or she can change into a griffon, thence to an efreet, and then to a titan, etc. These creatures have whatever hit points the magic-user has at the time of the Shape Change. Each alteration in form requires 1 segment. No system shock is incurred. Example: A wizard is in combat and assumes the form of a will o' wisp, and when this form is no longer useful, the wizard changes into a stone golem and walks away. When pursued, the golem-shape is changed to that of a flea, which hides upon a horse until it can hop off and become a bush. If detected as the latter, the magic-user can become a dragon, pool of water, or just about anything else. The material component of the spell is a jade circlet worth no less than 5000 g.p. which will shatter at the expiration of the magic's duration. In the meantime it is left in the wake of the Shape Change, and premature shattering will cause the magic to be dispelled."
    ),
    Spell('Succor','M',9,
        cast=tp(1,VA),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Temporal Stasis','M',9,
        cast=tp(9,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="Upon casting this spell, the magic-user places the recipient creature into a state of suspended animation. This cessation of time means that the creature does not grow older. Its body functions virtually cease. This state persists until the magic is removed by a Dispel Magic spell or the reverse of the spell (Temporal Reinstatement) is uttered. Note that the reverse requires only a single word and no somatic or material components. The material component of a Temporal Stasis spell is a powder composed of diamond, emerald, ruby, and sapphire dust, one stone of each type being required."
    ),
    Spell('Time Stop','M',9,
        cast=tp(9,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="Upon casting a Time Stop spell, the magic-user causes the flow of time to stop in the area of effect, and outside this area the sphere simply seems to shimmer for an instant. During the period of spell duration, the magic-user can move and act freely within the area where time is stopped, but all other creatures there are frozen in their actions, for they are literally between ticks of the time clock, and the spell duration is subjective to the caster. No creature can enter the area of effect without being stopped in time also, and if the magic-user leaves it, he or she immediately negates the spell. When spell duration ceases, the magic-user will again be operating in normal time."
    ),
    Spell('Wish','M',9,
        cast=tp(1,VA),
        duration=tp(1,VA),
        sourcebook=V,
        desc="The Wish spell is a more potent version of a Limited Wish (q.v.). If it is used to alter reality with respect to hit points sustained by a party, to bring a dead character to life, or to escape from a difficult situation by lifting the spell caster (and his or her party) from one place to another, it will not cause the magic-user any disability. Other forms of wishes, however, will cause the spell caster to be weak (-3 on strength) and require 2 to 8 days of bed rest due to the stresses the wish places upon time, space, and his or her body. Regardless of what is wished for, the exact terminology of the Wish spell is likely to be carried through. (This discretionary power of the referee is necessary in order to maintain game balance. As wishing another character dead would be grossly unfair, for example, your DM might well advance the spell caster to a future period where the object is no longer alive, i.e. putting the wishing character out of the campaign.)"
    )
]

illusionist_spells = [
    Spell('Audible Glamer','I',1,
        cast=tp(5,S),
        duration_lvl=tp(3,R),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the second level magic-user spell, Audible Glamour (q.v.)."
    ),
    Spell('Change Self','I',1,
        cast=tp(1,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="This spell enables the Illusionist to alter the appearance of his or her form - including clothing and equipment - to appear 1' shorter or taller; thin, fat, or in between; human, humanoid, or any other generally man-shaped bipedal creature. The duration of the spell is 2 to 12 (2d6) rounds base plus 2 additional rounds per level of experience of the spell caster."
    ),
    Spell('Chromatic Orb','I',1,
        cast=tp(1,S),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Color Spray','I',1,
        cast=tp(1,S),
        duration=tp(1,S),
        sourcebook=V,
        desc="Upon casting this spell, the Illusionist causes a vivid fan-shaped spray of clashing colours to spring forth from his or her hand. From 1 to 6 creatures within the area of effect can be affected. The spell caster is able to affect 1 level or hit die of creatures for each of his or her levels of experience. Affected creatures are struck unconscious for 2 to 8 rounds if their level is less than or equal to that of the spell caster; they are blinded for 1 to 4 rounds if their level or number of hit dice is 1 or 2 greater than the Illusionist; and they are stunned (cf. power word, stun, seventh level magic-user spell) for 2 to 8 segments if their level or number of hit dice is 3 or more greater than the spell caster. All creatures above the level of the spell caster and all creatures of 6th level or 6 hit dice are entitled to a saving throw versus the colour spray spell. The material components of this spell area pinch each of powder or sand coloured red, yellow and blue."
    ),
    Spell('Dancing Lights','I',1,
        cast=tp(1,S),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="This spell is the same as the first level magic-user spell, Dancing Lights (q.v.)."
    ),
    Spell('Darkness','I',1,
        cast=tp(1,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the second level magic-user spell of Darkness (q.v.)."
    ),
    Spell('Detect Illusion','I',1,
        cast=tp(1,S),
        duration=tp(3,R),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="By means of this spell the Illusionist is able to see an Illusion and know it for exactly that. Note that it can be used to enable others to see Illusions as unreal if the spell caster touches the creature with both hands and the creature looks at the Illusion while so touched. The material component is a piece of yellow tinted crystal, glass, or mica."
    ),
    Spell('Detect Invisibility','I',1,
        cast=tp(1,S),
        duration_lvl=tp(5,R),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the second level magic-user spell, Detect Invisibility (q.v.)."
    ),
    Spell('Gaze Reflection','I',1,
        cast=tp(1,S),
        duration=tp(1,R),
        sourcebook=V,
        desc="The gaze reflection spell creates a mirror-like area of air before the Illusionist. Any gaze attack, such as that of a basilisk or a medusa, will be reflected back upon the gazer if it looks upon the spell caster."
    ),
    Spell('Hypnotism','I',1,
        cast=tp(1,S),
        duration=tp(1,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="The gestures of the Illusionist, along with his or her droning incantation, cause from 1 to 6 creatures to become susceptible to suggestion (see the third level magic-user suggestion spell). The suggestion must be given after the hypnotism spell is cast, and until that time the success of the spell is unknown. Note that the subsequent suggestion is not a spell, but simply a vocalized urging. Creatures which make their saving throw are not under hypnotic influence."
    ),
    Spell('Light','I',1,
        cast=tp(1,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="This spell is the same as the first level magic-user Light spell (q.v.) (cf. first level cleric Light spell.)"
    ),
    Spell('Phantasmal Force','I',1,
        cast=tp(1,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the third level magic-user spell, Phantasmal Force (q.v.)."
    ),
    Spell('Phantom Armor','I',1,
        cast=tp(1,R),
        duration=tp(1,P),
        sourcebook=U
    ),
    Spell('Read Illusionist Magic','I',1,
        cast=tp(1,S),
        duration_lvl=tp(2,R),
        sourcebook=U
    ),
    Spell('Spook','I',1,
        cast=tp(1,S),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Wall of Fog','I',1,
        cast=tp(1,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="By casting this spell. the Illusionist creates a wall of misty vapours in whatever area within the spell range he or she desires. The wall of fag obscures all sight normal and/or infravisual, beyond 2'. The area of effect is a cube of 2\" per side per level of experience of the spell caster. The misty vapours persist for 3 or more rounds unless blown away by a strong breeze (cf. gust of wind). The material component is a pinch of split dried peas."
    ),
    Spell('Alter Self','I',2,
        cast=tp(2,S),
        duration=tp(1,VA),
        duration_lvl=tp(2,R),
        sourcebook=U
    ),
    Spell('Blindness','I',2,
        cast=tp(2,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="The blindness spell causes the recipient creature to become blind and able to see only a greyness before its eyes. Various cure spells will not remove this effect, and only a dispel magic or the spell caster can do away with the blindness if the creature fails its initial saving throw versus the spell."
    ),
    Spell('Blur','I',2,
        cast=tp(2,S),
        duration=tp(3,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="When a blur spell is cast, the Illusionist causes the outline of his or her form to become blurred, shifting and wavery. This distortion causes all missile and melee combat attacks to be made at -4 on the first attempt and -2 on all successive attacks. It alto allows a +1 on the saving throw die roll for any direct magical attack."
    ),
    Spell('Deafness','I',2,
        cast=tp(2,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="The deafness spell causes the recipient creature to become totally deaf and unable to hear any sounds (cf. blindness). This deafness can be done away with only by means of a dispel magic or by the spell caster. The victim is allowed a saving throw. The material component of the spell is beeswax."
    ),
    Spell('Detect Magic','I',2,
        cast=tp(2,S),
        duration_lvl=tp(2,R),
        sourcebook=V,
        desc="This spell is similar to the first level cleric and the first level magic-user spell, Detect Magic (qq.v.)."
    ),
    Spell('Fascinate','I',2,
        cast=tp(2,S),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Fog Cloud','I',2,
        cast=tp(2,S),
        duration=tp(4,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="The fog cloud is a billowing mass of misty vapours which is of similar appearance to a Cloudkill (q.v.), the fog being greenish. The spell caster creates the fog cloud and it moves away from him or her at a 1\" per round rate. Although it behaves in most respects just as if it were a Cloudkill, the only effect of the fog is to obscure vision, just as a wall of fog does."
    ),
    Spell('Hypnotic Pattern','I',2,
        cast=tp(2,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="When this spell is cast the Illusionist creates a weaving, turning pattern of subtle colours in the air. This hypnotic pattern will cause any creature looking at it to become fascinated and stand gazing at it as long as the spell caster continues to maintain the shifting interplay of glowing lines. Note that the spell can captivate a maximum of 24 levels, or hit dice, of creatures, i.e. 24 creatures with 1 hit die each, 12 with 2 hit dice, etc. All creatures affected must be within the area of effect, and each is entitled to a saving throw. The Illusionist need not utter a sound. but he or she must gesture appropriately while holding a glowing stick of incense or a crystal rod filled with phosphorescent material."
    ),
    Spell('Improved Phantasmal Force','I',2,
        cast=tp(2,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="Except as noted above, and as detailed hereafter, this spell is the same as the third level magic-user Phantasmal Force spell (q.v.). The spell caster can maintain the illusion with minimal concentration. i.e. he or she can move at half normal speed (but not cast other spells). Some minor sounds are included in the effects of the spell, but not understandable speech. Also, by concentration on the form of the phantasm, the Improved Phantasmal Force will continue for 2 rounds after the Illusionist ceases to concentrate upon the spell."
    ),
    Spell('Invisibility','I',2,
        cast=tp(2,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the second level magic-user spell, Invisibility (q.v.)."
    ),
    Spell('Magic Mouth','I',2,
        cast=tp(2,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="This spell is the same as the second level magic-user Magic Mouth spell (q.v.)."
    ),
    Spell('Mirror Image','I',2,
        cast=tp(2,S),
        duration_lvl=tp(3,R),
        sourcebook=V,
        desc="Except as noted above, and except for the fact that there are 2-5 (d4 + 1) mirror images created, this spell is the same as the second level magic-user spell, Mirror Image (q.v.)."
    ),
    Spell('Misdirection','I',2,
        cast=tp(2,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="By means of this spell the Illusionist misdirects the information from a detection-type spell, i.e. detect charm, detect evil, detect invisibility, detect lie, detect magic and detect snares & pits. While the detection spell functions, the information it reveals will indicate the wrong area, creature. or the opposite of the truth with respect to detect evil or detect lie. The Illusionist directs the spell effect upon the creature or item which is the object of the detection spell. If the caster of the detection-type spell fails his or her saving throw, the misdirection takes place."
    ),
    Spell('Ultravision','I',2,
        cast=tp(2,S),
        duration=tp(6,T),
        duration_lvl=tp(1,T),
        sourcebook=U
    ),
    Spell('Ventriloquism','I',2,
        cast=tp(2,S),
        duration=tp(4,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the first level magic-user spell, Ventriloquism (q.v.)."
    ),
    Spell('Whispering Wind','I',2,
        cast=tp(2,S),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Continual Darkness','I',3,
        cast=tp(3,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="When this spell is cast, a globe of impenetrable darkness is created. The effects of this darkness, as well as the material component of the spell, are the same as the second level magic-user spell, Darkness, 15' Radius (cf. Continual Light)."
    ),
    Spell('Continual Light','I',3,
        cast=tp(3,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell is the same as the second level cleric Continual Light spell (q.v.), except as noted above."
    ),
    Spell('Delude','I',3,
        cast=tp(3,S),
        duration_lvl=tp(1,T),
        sourcebook=U
    ),
    Spell('Dispel Illusion','I',3,
        cast=tp(3,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="By means of this spell, the spell caster can dispel any phantasmal force - with or without audible glamour - cast by a non-illusionist; and the spell has the same chance of dispelling any illusion/phantasm spells at another Illusionist as a dispel magic spell (q.v.) does, i.e. 50% base chance adjusted by 2% downward, or 5% upward for each level of experience lesser/greater of the Illusionist casting the dispel illusion compared to the Illusionist casting the spell to be dispelled."
    ),
    Spell('Fear','I',3,
        cast=tp(3,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the fourth level magic-user spell, Fear (q.v.)."
    ),
    Spell('Hallucinatory Terrain','I',3,
        cast=tp(5,R),
        duration=tp(1,VA),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the fourth level magic-user Hallucinatory Terrain spell (q.v.)."
    ),
    Spell('Illusionary Script','I',3,
        cast=tp(1,VA),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell enables the Illusionist to write instructions or other information on parchment, paper, skin, etc. The Illusionary Script appears to be some form of foreign or magical writing. Only the person (or class of persons or whatever} whom the Illusionist desires to read the writing will be able to do so, although another Illusionist will recognize it for Illusionary Script. Others attempting to read it will become confused as from a confusion spell (q.v.) for 5 to 20 turns, minus 1 turn for each level of experience he or she has attained. The material component of the spell is a lead-based ink which requires special manufacture by an alchemist."
    ),
    Spell('Invisibility 10\' Radius','I',3,
        cast=tp(3,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the third level magic-user spell, Invisibility, 10' Radius (q.v.). See also the second level magic-user spell, Invisibility."
    ),
    Spell('Non-detection','I',3,
        cast=tp(3,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="By casting this spell, the Illusionist makes himself or herself invisible to divination spells such as clairaudience, clairvoyance, \"detects\", and ESP. It also prevents location by such magic items as crystal balls and ESP medallions. The material component of the spell is a pinch of diamond dust."
    ),
    Spell('Paralyzation','I',3,
        cast=tp(3,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="The paralyzation spell enables the spell caster to create illusionary muscle slowdown in creatures whose combined hit dice do not exceed twice the total level of experience of the Illusionist. If the recipient creatures fail their saving throws, they become paralyzed, and a dispel illusion or dispel magic spell must be used to remove the effect, or the Illusionist may dispel it at anytime he or she desires."
    ),
    Spell('Phantom Steed','I',3,
        cast=tp(1,T),
        duration_lvl=tp(6,T),
        sourcebook=U
    ),
    Spell('Phantom Wind','I',3,
        cast=tp(3,S),
        duration_lvl=tp(1,R),
        sourcebook=U
    ),
    Spell('Rope Trick','I',3,
        cast=tp(3,S),
        duration_lvl=tp(2,T),
        sourcebook=V,
        desc="This spell is the same as the second level magic-user spell, Rope Trick (q.v.)."
    ),
    Spell('Spectral Force','I',3,
        cast=tp(3,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="The spectral force spell creates an illusion in which sound, smell and thermal illusions are included. It is otherwise similar to the second level Improved Phantasmal Force spell (q.v.). The spell will last for 3 rounds after concentration."
    ),
    Spell('Suggestion','I',3,
        cast=tp(3,S),
        duration=tp(0),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the third level magic-user spell, Suggestion (q.v.)."
    ),
    Spell('Wraithform','I',3,
        cast=tp(1,S),
        duration_lvl=tp(2,R),
        sourcebook=U
    ),
    Spell('Confusion','I',4,
        cast=tp(4,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the fourth level magic-user Confusion spell (q.v.). See also the seventh level druid Confusion spell."
    ),
    Spell('Dispel Exhaustion','I',4,
        cast=tp(4,S),
        duration_lvl=tp(3,T),
        sourcebook=V,
        desc="By means of this spell, the Illusionist is able to restore 50% of lost hit points to all persons (humans, demi-humans and humanoids) he or she touches during the round it is cast, subject to a maximum of four persons. The spell gives the illusion to the person touched that he or she is fresh and well, stamina is renewed, but when the spell duration expires, the recipient drops back to their actual hit point strength. The spell will allow recipients to move at double speed for 1 round every turn (cf. haste spell)."
    ),
    Spell('Dispel Magic','I',4,
        cast=tp(4,S),
        duration=tp(1,P),
        sourcebook=U
    ),
    Spell('Emotion','I',4,
        cast=tp(4,S),
        duration=tp(1,VA),
        sourcebook=V
    ),
    Spell('Improved Invisibility','I',4,
        cast=tp(4,S),
        duration=tp(4,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell is similar to invisibility, but the recipient is able to attack, either by missile discharge, melee combat, or spell casting and remain unseen. Note, however, that there are sometimes telltale traces, a shimmering, so that an observant opponent can attack the invisible spell recipient. Such attacks are at -4 on the \"to hit\" dice, and all saving throws are made at +4."
    ),
    Spell('Massmorph','I',4,
        cast=tp(4,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="Except as noted above, this spell is the same as the fourth level magic-user spell, Massmorph (q.v.)."
    ),
    Spell('Minor Creation','I',4,
        cast=tp(1,T),
        duration_lvl=tp(6,T),
        sourcebook=V,
        desc="This spell enables the Illusionist to create an item of non-living, vegetable nature, i.e. soft goods, rope, wood, etc. The item created cannot exceed 1 cubic foot per level of the spell caster in volume., (Cf. ADVANCED DUNGEONS & DRAGONS, MONSTER MANUAL, Djinni.) Note the limits of the spell's duration, The spell caster must have at least a tiny piece of matter of the same type of item he or she plans to create by means of the minor creation spell, i.e. a bit of twisted hemp to create rope, a splinter of wood to create a door, and so forth."
    ),
    Spell('Phantasmal Killer','I',4,
        cast=tp(4,S),
        duration_lvl=tp(1,R),
        sourcebook=V
    ),
    Spell('Rainbow Pattern','I',4,
        cast=tp(4,S),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Shadow Monsters','I',4,
        cast=tp(4,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="The shadow monsters spell enables the Illusionist to create semi-real phantasms of one or more monsters. The total hit dice of the shadow monster or monsters thus created cannot exceed the level of experience of the Illusionist; thus a 10th level Illusionist can create one creature which has 10 hit dice (in normal circumstances), two which have 5 hit dice (normally), etc. All shadow monsters created by one spell must be of the same sort, i.e. hobgoblins, orcs, spectres, etc. They have 20% of the hit points they would normally have. To determine this, roll the appropriate hit dice and multiply by .20, any score less than .4 is dropped - in the case of monsters with one (or fewer) hit dice, this indicates the monster was not successfully created - and scores of .4 or greater are rounded up to one hit point. If the creature or creatures viewing the shadow monsters fail their saving throw and believe the illusion, the shadow monsters perform as normal with respect to armour class and attack forms. If the viewer or viewers make their saving throws, the shadow monsters are armour class 10 and do only 20% of normal melee damage (biting, clawing, weapon, etc.), dropping fractional damage less than .4 as done with hit points. Example: A shadow monster dragonne attacks a person knowing it is only quasi-real. The monster strikes with 2 claw attacks and 1 bite, hitting as a 9 die monster. All 3 attacks hit, and the normal damage dice are rolled: d8 scored 5, d8 scores 8, 3d6 scores 11 and each total is multiplied by .2 (.2 x 5 = 1, .2 x 8 = 1.6 = 2, 2 x 11 = 2.2 = 2) and 5 hit points of real damage are scored upon the victim."
    ),
    Spell('Solid Fog','I',4,
        cast=tp(4,S),
        duration=tp(1,VA),
        duration_lvl=tp(1,R),
        sourcebook=U
    ),
    Spell('Vacancy','I',4,
        cast=tp(4,S),
        duration_lvl=tp(1,T),
        sourcebook=U
    ),
    Spell('Advanced Illusion','I',5,
        cast=tp(5,S),
        duration_lvl=tp(1,R),
        sourcebook=U
    ),
    Spell('Chaos','I',5,
        cast=tp(5,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell is similar to the seventh level druid confusion spell (q.v.), but all creatures in the area of effect are confused for the duration of the spell. Only fighters other than paladins or rangers and Illusionists are able to combat the spell effects and are thus allowed a saving throw. Similarly, monsters which do not employ magic and have intelligences of 4 (semi-intelligent) or less are entitled to saving throws. The material component for this spell is a small disc of bronze and a small rod of iron."
    ),
    Spell('Demi-Shadow Monsters','I',5,
        cast=tp(5,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell is similar to the fourth level spell, shadow monsters, except that the monsters created are of 40% hit points. Damage potential is 40% of normal, and they are armour class 8."
    ),
    Spell('Dream','I',5,
        cast=tp(1,D),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Magic Mirror','I',5,
        cast=tp(1,H),
        duration_lvl=tp(1,R),
        sourcebook=U
    ),
    Spell('Major Creation','I',5,
        cast=tp(1,T),
        duration_lvl=tp(6,T),
        sourcebook=V,
        desc="This spell is comparable to a minor creation spell (q.v.) except that it allows the Illusionist to create mineral objects. If vegetable objects are created, they have a duration of 12 turns per level of experience of the spell caster."
    ),
    Spell('Maze','I',5,
        cast=tp(5,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="This spell, except as noted above, is the same as the eighth level magic-user Maze spell (q.v.)."
    ),
    Spell('Projected Image','I',5,
        cast=tp(5,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="Except as shown above, this spell is the same as the sixth level magic-user spell Project Image (q.v.)."
    ),
    Spell('Shadow Door','I',5,
        cast=tp(2,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="By means of this spell, the Illusionist creates the illusion of a door. The illusion also permits the Illusionist to appear to step through this \"door\" and disappear, when in reality he or she has darted aside, and can then flee totally invisible for the spell duration. Creatures viewing this are deluded into seeing/entering an empty 10' x 10' room if they open the \"door\". Only a true seeing spell, a gem of seeing, or similar magical means will discover the Illusionist."
    ),
    Spell('Shadow Magic','I',5,
        cast=tp(5,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="The shadow magic spell allows the Illusionist to cast a quasi-real magic-user spell. This spell can be magic missile, fireball, lightning bolt, or cone of cold and will have normal effects upon creatures in the area of effect if they fail to make their saving throws. If saving throws are made, the shadow magic spell will inflict but 1 hit point of damage per level of experience of the Illusionist casting it, regardless of which quasi-real spell was cast."
    ),
    Spell('Summon Shadow','I',5,
        cast=tp(5,S),
        duration=tp(1,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="When this spell is cast, the Illusionist conjures up 1 shadow (see ADVANCED DUNGEONS & DRAGONS. MONSTER MANUAL) for every three levels of experience he or she has attained. These monsters are under the control of the spell caster and will attack his or her enemies on command. The shadows will remain until slain or turned or the spell duration expires. The material component for this spell is a bit of smoky quartz."
    ),
    Spell('Tempus Fugit','I',5,
        cast=tp(5,S),
        duration_lvl=tp(5,T),
        sourcebook=U
    ),
    Spell('Conjure Animals','I',6,
        cast=tp(6,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="Except as shown above. this spell is the same as the sixth level cleric spell, Conjure Animals (q.v.)."
    ),
    Spell('Death Fog','I',6,
        cast=tp(6,S),
        duration=tp(1,VA),
        duration_lvl=tp(1,R),
        sourcebook=U
    ),
    Spell('Demi-Shadow Magic','I',6,
        cast=tp(6,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="This spell is similar to the fifth level Shadow Magic spell (q.v.), but in addition to the quasi-real spells listed thereunder it enables the Illusionist to cast a quasi-real Wall of Fire, Wall of Ice, or Cloudkill. If recognized as Demi-Shadow Magic (the victim makes its saving throw), the Magic Missile, Fireball, et al. do 2 hit points of damage per level of experience of the spell caster, the wall spells cause 1-4 hit points of damage per level, and the Cloudkill will slay only creatures with fewer than 2 hit dice."
    ),
    Spell('Mass Suggestion','I',6,
        cast=tp(6,S),
        duration=tp(4,T),
        duration_lvl=tp(4,T),
        sourcebook=V,
        desc="This spell is the same as the third level Suggestion spell, except that the Illusionist is able to cast the spell upon more than one subject, provided the prospective recipients of the suggestion are within the 3\" range. One creature per level of experience the spell caster has attained can be affected. If only one creature is the subject, its saving throw is at -2. The suggestion must be the same for all hearing it."
    ),
    Spell('Mirage Arcane','I',6,
        cast=tp(1,VA),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('Mislead','I',6,
        cast=tp(1,S),
        duration_lvl=tp(1,R),
        sourcebook=U
    ),
    Spell('Permanent Illusion','I',6,
        cast=tp(6,S),
        duration=tp(1,P),
        sourcebook=V,
        desc="This spell creates a lasting Spectral Force (q.v.) which requires no concentration. It is subject to Dispel Magic, of course."
    ),
    Spell('Phantasmagoria','I',6,
        cast=tp(6,S),
        duration_lvl=tp(1,R),
        sourcebook=U
    ),
    Spell('Programmed Illusion','I',6,
        cast=tp(6,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="By means of this spell, the Illusionist sets up a Spectral Forces spell (q.v.) which will activate upon command or when a specified condition occurs (cf. Magic Mouth). The illusion will last for a maximum of 1 round per level of the spell caster."
    ),
    Spell('Shades','I',6,
        cast=tp(6,S),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell is related to shadow monsters and demi-shadow monsters (qq.v.), but the monsters created are of 60% hit points and damage potential and are of armour class 6."
    ),
    Spell('True Sight','I',6,
        cast=tp(1,R),
        duration_lvl=tp(1,R),
        sourcebook=V,
        desc="This spell is very like the fifth level cleric spell, True Seeing (q.v.). However, while the true sight spell allows the Illusionist to see its actual or former form, it does not allow determination of alignment."
    ),
    Spell('Veil','I',6,
        cast=tp(3,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="The veil spell enables the Illusionist to instantly change the appearance of his or her surroundings and/or party or create Hallucinatory Terrain (q.v.) so as to fool even the most clever creatures unless they have true seeing/sight, a gem of seeing, or similar magical aid. The veil can make a sumptuous room seem a filthy den and even touch will conform to the visual illusion. If hallucinatory terrain is created, touch will not cause it to vanish."
    ),
    Spell('Alter Reality','I',7,
        cast=tp(1,VA),
        duration=tp(1,VA),
        sourcebook=V,
        desc="The Alter Reality spell is similar to the seventh level magic-user Limited Wish spell (q.v.). In order to effect the magic fully, the Illusionist must depict the enactment of the alteration of reality through the casting of a Phantasmal Force, as well as verbalization in a limited form, before the spell goes into action."
    ),
    Spell('Astral Spell','I',7,
        cast=tp(3,T),
        duration=tp(1,VA),
        sourcebook=V,
        desc="This spell is the same as the seventh level cleric spell, Astral Spell (q.v.)."
    ),
    Spell('Prismatic Spray','I',7,
        cast=tp(7,S),
        duration=tp(0),
        sourcebook=V,
        desc="When this spell is cast, the Illusionist causes 7 rays of the Prismatic Sphere spell (q.v.) to spring from his or her hand. Any creature in the area of effect will be touched by 1 or more of the rays. To determine which ray strikes the concerned creature, roll an eight-sided die: 1 = red 2 = orange 3 = yellow 4 = green 5 = blue 6 = indigo 7 = violet 8 = struck by 2 rays, roll again twice ignoring any 8's. Saving throws apply only with respect to those prismatic colour rays which call for such."
    ),
    Spell('Prismatic Wall','I',7,
        cast=tp(7,S),
        duration_lvl=tp(1,T),
        sourcebook=V,
        desc="The prismatic wall spell is similar to the Prismatic Sphere spell (q.v.). It differs only in that the spell creates a wall, or curtain, of scintillating colours. The wall is of maximum proportions of 4' wide per level of experience of the spell caster and 2' high per level of experience."
    ),
    Spell('Shadow Walk','I',7,
        cast=tp(1,S),
        duration_lvl=tp(6,T),
        sourcebook=U
    ),
    Spell('Vision','I',7,
        cast=tp(7,S),
        duration=tp(1,VA),
        sourcebook=V,
        desc="At such time as the Illusionist wishes to gain supernatural guidance, he or she casts a Vision spell, calling upon whatever power he or she desires aid from, and asking the question for which a vision is to be given to answer. Two six-sided dice are rolled. If they total 2 to 6, the power is annoyed and will cause the Illusionist, by ultra-powerful geas or quest to do some service, and no question will be answered. If the dice total 7 to 9, the power is indifferent, and some minor vision, possibly unrelated to the question, will be given. A score of 10 or better indicates the vision is granted. Note that the material component of the spell is the sacrifice of something valued by the spell caster and/or by the power supplicated. The more precious the sacrifice, the better he chance of spell success, for a very precious item will give a bonus of +1 on the dice, one that is extremely precious will add +2, and a priceless/nonesuch will add +3."
    ),
    Spell('Weird','I',7,
        cast=tp(7,S),
        duration=tp(1,VA),
        sourcebook=U
    ),
    Spell('First Level Magic-User Spells','I',7,
        cast=tp(1,VA),
        duration=tp(1,VA),
        sourcebook=V,
        desc="The Illusionist gains four of the following first level magic-user spells at the 14th level of experience and an additional one as each additional level of experience is gained. The spells are:  Affect Normal Fires, Burning Hands, Charm Person, Comprehend Languages, Enlarge, Erase, Feather Fall, Friends, Hold Portal, Magic Missile, Mending, Message, Nystul's Magic Aura, Protection from Evil, Read Magic, Shield, Shocking Grasp, Sleep, Tenser's Floating Disc, Unseen Servant. The Illusionist may learn any spell or spells from the preceding list. He or she must seek the spells in the same manner as a magic-user. If the Illusionist chooses to take this \"spell\", he or she actually takes four or more first level magic-user spells as a seventh level spell."
    )
]

all_spells = (cleric_spells + druid_spells
            + mu_spells + illusionist_spells)

def randomSpell():
    return choice(all_spells)

def randomIllusionistSpells(num=1,level=None):
    if not level:
        return sample(illusionist_spells, num)
    else:
        spells = [s for s in illusionist_spells if s.level == level]
        return sample(spells, num)


def test_module():
    print(cleric_spells[0].cast_time)
    print(cleric_spells[0].duration)
    print(cleric_spells[0].sourcebook.value)


if __name__ == '__main__':
    test_module()
