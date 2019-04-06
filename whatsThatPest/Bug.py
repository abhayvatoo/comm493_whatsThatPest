#class to represnt bug info
class Bug:
    #initialize the attributes
    def __init__(self, damage, description, pesticide):
        self.__damage = damage
        self.__description = description
        self.__pesticide = pesticide

    #getter for damage level
    def get_damage(self):
        return self.__damage
    #getter for description
    def get_description(self):
        return self.__description
    #getter for pesticide info
    def get_pesticide(self):
        return self.__pesticide

#creating objects of type Bug for each of the bug type supported by the application currently
#next: create a new object of type Bug which coressponds to new bug which the application will support
ladyBug = Bug(0, 'Coccinellidae is a widespread family of small beetles ranging in size from 0.8 to 18 mm. The family is commonly known as ladybugs in North America, and ladybirds in Britain and other parts of the English-speaking ', ['D-Fense SC','Cyper WSP'])
cricket = Bug(5, 'Crickets, of the family Gryllidae, are insects related to bush crickets, and, more distantly, to grasshoppers. The Gryllidae have mainly cylindrical bodies, round heads, and long antennae. Crickets mainly eat plants, plant debris, smaller insects, and other crickets. ', ['Talstar PL Granules','NiBan Granular', 'Merit WP', 'Temprid'])
fly = Bug(3, 'Flies are insects with a pair of functional wings for flight and a pair of vestigial hindwings called halteres for balance. They are classified as an order called Diptera. Some flies, attack and spoil citrus and other fruits.', ['Cynoff WP', 'Talstar One', 'Maxforce Granular Fly Bait'])
moth = Bug(5, 'Moth larvae feed on leaves, buds, flowers, seed pods, the green outer layer of the stems and occasionally the developing seeds within the older seed pods of canola and mustard. The amount of damage varies greatly, depending on plant growth stage, larval densities and size.', ['organophosphorus compounds', 'cartap methomy', 'fenvalerate'])
weevil = Bug(4, 'Weevils are certain beetles, namely the ones belonging to the superfamily Curculionoidea. They are usually small, less than 6 mm, and herbivorous. They damage leaves', ['permethrin', 'bifenthrin'])
#if the ibm service is not able to recognize a bug and the bellow information is displayed to the user
unknown = Bug(0, 'We do not recognize this picture yet. Please try with different pictures or contact us offline', ['N/A'])

#initializing the in-memory map to store all the information related to all the bugs supported
#next: add newly created Bug objects to the map
bug_info = {
    'ladybug': ladyBug,
    'cricket': cricket,
    'fly': fly,
    'moth': moth,
    'weevil': weevil,
    'unknown': unknown
}