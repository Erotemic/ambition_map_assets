"""The development blurb of each room of the History dimension: where and
when the room is, and one fact about it that can be checked.

`make_specs.py` writes each blurb as two `DebugLabel`s of category `Room`
at the top of its room, so that the author and the playtester can see at a
glance what a room is about. The blurbs use BCE and CE. A date of the last
50,000 years or so is a year; an older one is "years ago". A blurb states
evidence and its limits; it does not invent a certainty.
"""

#: Room id -> (where and when, a fact).
BLURB = {
    # ---- Africa ----
    "history_cradle": (
        "WHERE: the Great Rift Valley, East Africa. WHEN: about 300,000 years ago.",
        "FACT: the oldest known fossils of our species are about 300,000 years old (Jebel Irhoud, Morocco)."),
    "history_southern_coast": (
        "WHERE: the south coast of South Africa. WHEN: about 75,000 years ago.",
        "FACT: Blombos Cave has a piece of ochre with a cross-hatch cut in it, about 75,000 years old."),
    "history_green_sahara": (
        "WHERE: the Sahara (Chad, Niger, Libya). WHEN: about 7000 BCE.",
        "FACT: from about 9000 to 3500 BCE the Sahara had lakes and grass; rock art shows cattle where there is sand."),
    "history_nile_valley": (
        "WHERE: the Nile valley, Egypt. WHEN: about 3100-30 BCE.",
        "FACT: the Great Pyramid (about 2560 BCE) was the tallest building on Earth for about 3,800 years."),
    "history_aksum_and_kush": (
        "WHERE: Kush (Sudan) and Aksum (Ethiopia, Eritrea). WHEN: about 300 BCE-600 CE.",
        "FACT: Aksum made its own coins of gold, and its king Ezana became Christian in the 300s CE."),
    "history_timbuktu_coast": (
        "WHERE: Timbuktu (Mali) and the Swahili coast. WHEN: about 1300-1450 CE.",
        "FACT: Mansa Musa went to Mecca in 1324 CE with so much gold that its price in Cairo fell for years."),
    "history_benin_city": (
        "WHERE: Benin City, in today's Nigeria (not the country of Benin). WHEN: about 1200-1897 CE.",
        "FACT: in 1897 a British force burned the city and took thousands of brasses. Since 2022 a few have come back."),
    "history_ishango": (
        "WHERE: Ishango, on the Semliki river at Lake Edward, DR Congo. WHEN: about 20,000 years ago.",
        "FACT: the Ishango bone was dug up in 1950 by Jean de Heinzelin. People still argue over what its notches count."),
    "history_kongo": (
        "WHERE: Mbanza Kongo, now in northern Angola. WHEN: the kingdom of Kongo, about 1390-1665 CE; this room about 1526.",
        "FACT: Kongo's kings wrote to Lisbon and Rome for 150 years; dozens of their letters survive, in Portuguese."),
    "history_ndongo": (
        "WHERE: Ndongo and Matamba, the valley of the Kwanza, Angola. WHEN: Queen Nzinga's reign, 1624-1663 CE.",
        "FACT: Nzinga died in 1663, aged about 80, a queen still; Portugal had not beaten her."),
    "history_congo_free_state": (
        "WHERE: the Congo river, DR Congo. WHEN: the Congo Free State, 1885-1908 CE; this room about 1904.",
        "FACT: the campaign against Leopold's Congo was one of the first great human rights campaigns: photographs, lantern shows, petitions."),
    "history_door_of_no_return": (
        "WHERE: a castle of the Gold Coast (Ghana): a composite of forts such as Cape Coast and Elmina. WHEN: the 1700s CE.",
        "FACT: from about 1500 to 1866 CE about 12.5 million Africans were forced onto slave ships; about 10.7 million lived."),
    # ---- The Mediterranean and South-West Asia ----
    "history_levant": (
        "WHERE: the Levant (Israel, Lebanon, Syria, Jordan). WHEN: about 70,000-50,000 years ago.",
        "FACT: people met Neanderthals on the way out of Africa: most people outside Africa have 1-2% Neanderthal DNA."),
    "history_fertile_crescent": (
        "WHERE: the Fertile Crescent (Turkey, Syria, Iraq, Iran). WHEN: about 9500-7000 BCE.",
        "FACT: wheat, barley, lentils, sheep and goats were first farmed here. Gobekli Tepe is older than the farms."),
    "history_uruk": (
        "WHERE: Uruk, in the south of Iraq. WHEN: about 3500-3000 BCE.",
        "FACT: the oldest writing we know, cuneiform from about 3300 BCE, is mostly accounts: grain, beer and sheep."),
    "history_classical_shore": (
        "WHERE: the Mediterranean: Greece and Rome. WHEN: about 500 BCE-400 CE.",
        "FACT: Greek cities settled the whole coast: Marseille (about 600 BCE) and Naples began as Greek towns."),
    # ---- Europe ----
    "history_ice_age_europe": (
        "WHERE: Europe in the last Ice Age. WHEN: about 40,000-15,000 years ago.",
        "FACT: 20,000 years ago the sea was about 120 m lower, and you could walk from France to Britain."),
    "history_first_farmers_of_europe": (
        "WHERE: from Anatolia to the middle of Europe. WHEN: about 6500-5000 BCE.",
        "FACT: ancient DNA shows the first farmers of Europe came from Anatolia: the people came, not only the idea."),
    "history_megalith_builders": (
        "WHERE: Atlantic Europe: Stonehenge, Carnac, Newgrange. WHEN: about 4500-1500 BCE.",
        "FACT: Stonehenge lines up with the midsummer sunrise; its bluestones came about 225 km, from Wales."),
    "history_celtic_frontier": (
        "WHERE: Gaul and Britain, at the edge of Rome. WHEN: about 300 BCE-150 CE.",
        "FACT: most of what we read about the Celts was written by their enemies, Julius Caesar among them."),
    "history_viking_north": (
        "WHERE: Scandinavia and the North Atlantic. WHEN: about 793-1066 CE.",
        "FACT: Norse sailors were at L'Anse aux Meadows, Newfoundland, in 1021 CE (tree rings give the year)."),
    "history_age_of_sail": (
        "WHERE: the Atlantic and the oceans of the world. WHEN: about 1500-1850 CE.",
        "FACT: scurvy (no vitamin C) killed more sailors than battle did; the Royal Navy gave out lemon juice from 1795."),
    "history_industrial_age": (
        "WHERE: Britain, then the world. WHEN: about 1760-1900 CE.",
        "FACT: Britain's Factory Act of 1833 stopped children under 9 working in textile mills. Under 9."),
    # ---- South Asia ----
    "history_southern_route": (
        "WHERE: the coasts of Arabia and India. WHEN: about 70,000-50,000 years ago.",
        "FACT: people went along the coasts of southern Asia and were in Australia by at least 50,000 years ago."),
    "history_mehrgarh": (
        "WHERE: Mehrgarh, Balochistan, Pakistan. WHEN: about 7000-2500 BCE.",
        "FACT: teeth from Mehrgarh have holes drilled in them in life, 7,500-9,000 years ago: the oldest known dentistry."),
    "history_indus_cities": (
        "WHERE: the Indus valley (Pakistan, north-west India): Harappa, Mohenjo-daro. WHEN: about 2600-1900 BCE.",
        "FACT: the cities had planned streets and covered drains, and their script is still not read."),
    "history_dhaka_muslin": (
        "WHERE: Dhaka, on the Buriganga river, Bangladesh. WHEN: Mughal Bengal 1576-1757 CE; this room about 1700 CE.",
        "FACT: the finest Dhaka muslin was spun from phuti karpas, a cotton of the Meghna's banks that was lost in the 1800s."),
    "history_company_raj": (
        "WHERE: Calcutta (Kolkata), on the Hooghly, India. WHEN: Company rule in Bengal 1757-1858 CE.",
        "FACT: after the rising of 1857, the Government of India Act (1858) took India from the East India Company and gave it to the Crown."),
    "history_ekushey": (
        "WHERE: Dhaka, Bangladesh. WHEN: 1905-1971 CE; 21 February 1952.",
        "FACT: since 2000, 21 February, the day of 1952 (Ekushey, 'twenty-one'), is International Mother Language Day."),
    # ---- East Asia's coasts ----
    "history_jomon": (
        "WHERE: Sannai-Maruyama, Aomori, north Japan. WHEN: about 3900-2200 BCE.",
        "FACT: Jōmon pottery began about 14,500 BCE, among the oldest anywhere, made by people who did not farm."),
    "history_taiwan": (
        "WHERE: Taiwan. WHEN: about 4000-1500 BCE.",
        "FACT: of the ten first branches of the Austronesian language family, nine are spoken only on Taiwan."),
    "history_silla": (
        "WHERE: Gyeongju, South Korea. WHEN: Silla 57 BCE-935 CE; this room about 640 CE.",
        "FACT: Cheomseongdae, built in the reign of Queen Seondeok (632-647), is the oldest standing observatory in East Asia."),
    "history_song": (
        "WHERE: Hangzhou (then Lin'an), Zhejiang, China. WHEN: Southern Song 1127-1279 CE; this room about 1200 CE.",
        "FACT: the Song state printed paper money; the oldest known description of a compass with a needle is Shen Kuo's, of 1088."),
    "history_joseon": (
        "WHERE: Hanyang (now Seoul), South Korea. WHEN: Joseon 1392-1897 CE; this room 1446 CE.",
        "FACT: the Hunminjeongeum of 1446 gave Korean its own alphabet, now called Hangul (in the North, Chosŏn'gŭl)."),
    "history_heian": (
        "WHERE: Heian-kyō (now Kyoto), Japan. WHEN: the Heian period 794-1185 CE; this room about 1000 CE.",
        "FACT: The Tale of Genji (about 1008) and The Pillow Book (about 1002) were written by women of the court, in kana."),
    "history_kamakura": (
        "WHERE: Hakata Bay, Kyushu, Japan. WHEN: the Kamakura shogunate 1185-1333 CE; the invasions of 1274 and 1281.",
        "FACT: the fleet of 1281 was one of the largest before modern times: about 4,000 ships, from Korea and from south China."),
    "history_edo": (
        "WHERE: Edo (today's Tokyo), Japan. WHEN: the Tokugawa shogunate 1603-1868 CE; this room about 1830.",
        "FACT: for two centuries Japan let in almost no foreign ships; the Dutch could trade only from a small island at Nagasaki."),
    "history_meiji": (
        "WHERE: Tokyo, Japan. WHEN: the Meiji era 1868-1912 CE; this room 1872.",
        "FACT: in 1872 Japan changed to the Western calendar at a month's notice: 3 December became 1 January 1873."),
    # ---- Southeast Asia ----
    "history_sulawesi": (
        "WHERE: Maros-Pangkep, Sulawesi (Indonesia), in Wallacea. WHEN: about 51,000-40,000 years ago.",
        "FACT: at Leang Karampuang a pig and three human figures are painted, dated to at least 51,200 years ago."),
    "history_austronesian_islands": (
        "WHERE: the Philippines and the islands of Indonesia. WHEN: about 2200-1500 BCE.",
        "FACT: Austronesian languages, from Taiwan, came to be spoken from Madagascar to Rapa Nui, more than half the globe."),
    "history_dong_son": (
        "WHERE: the Red River valley, northern Vietnam. WHEN: about 600 BCE-43 CE.",
        "FACT: in 40 CE the Trưng sisters led a rising against Han China and ruled until 43 CE."),
    "history_srivijaya": (
        "WHERE: Palembang, Sumatra (Indonesia), on the Strait of Malacca. WHEN: about 650-1290 CE.",
        "FACT: the Kedukan Bukit stone of 682 CE, found at Palembang, is the oldest known writing in the Malay language."),
    "history_borobudur": (
        "WHERE: the Kedu plain, central Java (Indonesia). WHEN: built about 780-830 CE.",
        "FACT: Borobudur has 2,672 relief panels and 504 statues; it is the largest Buddhist monument in the world."),
    "history_angkor": (
        "WHERE: Angkor, north-west Cambodia. WHEN: 802-1431 CE; this room about 1150-1200 CE.",
        "FACT: Greater Angkor covered about 1,000 square km: by area, the largest city in the world before industry."),
    # ---- Oceania ----
    "history_sahul": (
        "WHERE: Sahul: Australia, New Guinea and Tasmania, one land when the sea was low. WHEN: 65,000-45,000 years ago.",
        "FACT: even at the lowest sea, Sahul was across open water from Asia: the first Australians came by boat."),
    "history_new_guinea_highlands": (
        "WHERE: the highlands of New Guinea (Kuk Swamp). WHEN: about 7000-4000 BCE.",
        "FACT: at Kuk people dug ditches to farm taro and bananas: farming began here on its own, as in the Crescent."),
    "history_lapita_voyagers": (
        "WHERE: from the Bismarck Islands to Tonga and Samoa. WHEN: about 1500-500 BCE.",
        "FACT: the Lapita, known by their stamped pots, sailed to islands where no person had ever lived."),
    "history_wayfinders": (
        "WHERE: Polynesia, the open Pacific. WHEN: about 1000-1300 CE.",
        "FACT: without instruments, Polynesian navigators found Hawaii, Rapa Nui and, about 1250-1300 CE, Aotearoa (New Zealand)."),
    "history_rapa_nui": (
        "WHERE: Rapa Nui (Easter Island). WHEN: about 1200-1862 CE.",
        "FACT: newer studies find no collapse before 1722; in 1862 slave raiders from Peru took about 1,500 people."),
    "history_tonga_samoa": (
        "WHERE: Tongatapu (Tonga) and Samoa. WHEN: the Tuʻi Tonga, about 950-1865 CE; this room about 1200.",
        "FACT: Tonga was never colonised; it is the only kingdom in the Pacific that never lost its independence."),
    "history_aotearoa": (
        "WHERE: Aotearoa (New Zealand), the North Island. WHEN: about 1280-1769 CE.",
        "FACT: Aotearoa was one of the last large lands on Earth that people settled; Cook arrived in 1769."),
    "history_waitangi": (
        "WHERE: Waitangi, Bay of Islands, New Zealand. WHEN: 6 February 1840 CE.",
        "FACT: more than 500 chiefs signed copies of the Treaty in 1840, almost all of them the Māori text."),
    "history_lake_mungo": (
        "WHERE: Lake Mungo, the Willandra Lakes, New South Wales, Australia. WHEN: about 42,000-20,000 years ago.",
        "FACT: the Willandra Lakes are the land of the Paakantyi, Mutthi Mutthi and Ngiyampaa, and a World Heritage site since 1981."),
    "history_budj_bim": (
        "WHERE: Budj Bim, Gunditjmara country, south-west Victoria, Australia. WHEN: about 4600 BCE-1840s CE.",
        "FACT: the kooyang (short-finned eel) swims about 3,000 km to the Coral Sea to spawn; its young swim all the way back."),
    "history_sydney_cove": (
        "WHERE: Warrane (Sydney Cove), the land of the Eora, Australia. WHEN: 1788-1802 CE.",
        "FACT: people have lived in Australia for at least 65,000 years; 1788 is less than half of one percent of that time ago."),
    # ---- East Asia ----
    "history_mammoth_steppe": (
        "WHERE: the mammoth steppe of northern Eurasia. WHEN: about 40,000-15,000 years ago.",
        "FACT: people made houses of mammoth bones (Mezhyrich, Ukraine, about 15,000 years ago)."),
    "history_yellow_river": (
        "WHERE: the Yellow River valley, northern China. WHEN: about 7000-2000 BCE.",
        "FACT: millet was farmed here by about 6000 BCE; rice was farmed to the south, on the Yangtze."),
    "history_shang_court": (
        "WHERE: Anyang, Henan, China. WHEN: about 1250-1046 BCE.",
        "FACT: Shang kings asked their ancestors questions on bones; the answers carved there are the oldest Chinese writing."),
    "history_silk_road": (
        "WHERE: the Silk Roads, from China to the Mediterranean. WHEN: about 130 BCE-1450 CE.",
        "FACT: the name \"Silk Road\" is from 1877 CE. There were many roads, and few traders went the whole way."),
    "history_mongol_steppe": (
        "WHERE: the Mongolian steppe. WHEN: about 1206-1368 CE.",
        "FACT: the Mongol Empire is the largest empire of joined land in history, about 24 million km2 in 1279 CE."),
    # ---- The Americas ----
    "history_beringia": (
        "WHERE: Beringia, the land between Siberia and Alaska. WHEN: about 25,000-15,000 years ago.",
        "FACT: footprints at White Sands, New Mexico, are about 21,000-23,000 years old: people came earlier than we thought."),
    "history_first_maize": (
        "WHERE: the Balsas valley, southern Mexico. WHEN: about 7000 BCE.",
        "FACT: maize was bred from a wild grass, teosinte, whose ear is a few hard seeds. Farmers did the rest."),
    "history_andean_highlands": (
        "WHERE: the Andes around Lake Titicaca (Peru, Bolivia). WHEN: about 8000-5000 BCE.",
        "FACT: the potato was first farmed here; the Andes still grow about 4,000 kinds of it."),
    "history_caral": (
        "WHERE: Caral, in the Supe valley, Peru. WHEN: about 3000-1800 BCE.",
        "FACT: Caral built pyramids in the same centuries as Egypt, and no signs of war have been found there."),
    "history_amazonia": (
        "WHERE: Marajó island and the Amazon basin, Brazil. WHEN: Marajoara culture about 400-1400 CE; this room about 1000 CE.",
        "FACT: lidar has found towns of platform mounds, causeways and reservoirs under the forest of Llanos de Mojos, Bolivia, from 500-1400 CE."),
    "history_palmares": (
        "WHERE: Serra da Barriga, Alagoas, Brazil. WHEN: the Quilombo dos Palmares 1605-1694 CE; this room about 1680 CE.",
        "FACT: since 2024, 20 November, the day Zumbi was killed in 1695, is a national holiday in Brazil: Black Consciousness Day."),
    "history_rio_1888": (
        "WHERE: Rio de Janeiro, Brazil. WHEN: 1881-1888 CE; the Golden Law, 13 May 1888.",
        "FACT: some four to five million enslaved Africans were brought to Brazil, more than to any other country in the Americas."),
    "history_olmec_heartland": (
        "WHERE: the Gulf coast of Mexico: San Lorenzo, La Venta. WHEN: about 1500-400 BCE.",
        "FACT: the Olmec carved at least 17 colossal heads of basalt, and made rubber balls from latex and morning glory."),
    "history_maya_city": (
        "WHERE: the Maya lowlands (Guatemala, Mexico, Belize). WHEN: about 250-900 CE.",
        "FACT: the Maya wrote a full script and used zero. A cycle of their calendar ended in 2012 CE, and nothing else did."),
    "history_taino_islands": (
        "WHERE: Boriken (Puerto Rico), Ayiti (Haiti and the Dominican Republic) and Cuba. WHEN: about 1000-1492 CE.",
        "FACT: hammock, canoe, hurricane, barbecue and tobacco are Taino words, by way of Spanish."),
    "history_haitian_revolution": (
        "WHERE: Saint-Domingue, the west of Ayiti: today's Haiti. WHEN: 1791-1804 CE.",
        "FACT: from 1825 Haiti paid France for its own freedom; with the loans, it paid until 1947."),
    # ---- The buildings ----
    "history_pyramid_tomb": (
        "WHERE: inside a pyramid, Egypt. WHEN: the Old Kingdom, about 2600-2500 BCE.",
        "FACT: robbers emptied almost every royal tomb long ago; Tutankhamun's, found in 1922, was still mostly whole."),
    "history_temple_granary": (
        "WHERE: a temple granary in Mesopotamia. WHEN: about 3000 BCE.",
        "FACT: workers were paid in barley and beer, and the lists of who got how much are some of the oldest writing."),
    "history_colosseum": (
        "WHERE: the Colosseum, Rome. WHEN: opened in 80 CE.",
        "FACT: it held about 50,000 people, and the opening games went on for 100 days."),
    "history_great_ger": (
        "WHERE: a ger (yurt) on the Mongolian steppe. WHEN: the 1200s CE.",
        "FACT: a family can take a ger down or put it up in a few hours. Its door faces south."),
    "history_timbuktu_library": (
        "WHERE: a family library in Timbuktu. WHEN: the 1400s-1500s CE.",
        "FACT: in 2012-2013 CE the librarians smuggled hundreds of thousands of manuscripts out, away from the fires."),
    "history_cotton_mill": (
        "WHERE: a cotton mill in Manchester. WHEN: about 1800-1850 CE.",
        "FACT: most of the cotton spun in Britain's mills was grown by enslaved people; by 1850, mostly in the American South."),
    "history_painted_cave": (
        "WHERE: a painted cave of France (Chauvet, Lascaux). WHEN: about 36,000-17,000 years ago.",
        "FACT: the paintings of Chauvet are about 36,000 years old; those of Lascaux, about 17,000."),
}
