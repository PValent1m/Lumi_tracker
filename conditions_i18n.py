#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
conditions_i18n.py
Bilingual condition mappings (English <-> Brazilian Portuguese) for
luminescent_encounters.json and parse_encounters.py.
Proper names of Pokémon, locations, items, rods, and moves remain in English
to match the Luminescent Platinum ROM.
"""

SHORT_CONDITIONS_PT_TO_EN = {
    "Nenhuma": "None",
    "Trophy Garden Diário": "Daily Trophy Garden",
    "Enxame Diário (Swarm)": "Daily Swarm",
    "Requer Surf (HM03)": "Requires Surf (HM03)",
    "Requer Incense Burner na água": "Requires Incense Burner on water",
    "Requer Incense Burner": "Requires Incense Burner",
    "Requer Poké Radar": "Requires Poké Radar",
    "Requer Old Rod": "Requires Old Rod",
    "Requer Good Rod": "Requires Good Rod",
    "Requer Super Rod": "Requires Super Rod",
    "Árvore de Mel": "Honey Tree",
    "Disponível apenas pela manhã (04:00 - 09:59)": "Available only in the morning (04:00 - 09:59)",
    "Disponível apenas durante o dia (10:00 - 19:59)": "Available only during the day (10:00 - 19:59)",
    "Disponível apenas à noite (20:00 - 03:59)": "Available only at night (20:00 - 03:59)",
    "Escolha de Pokémon inicial": "Starter Pokémon choice",
    "Encontro com Pokémon Lendário": "Legendary Pokémon encounter",
    "Troca in-game com NPC": "In-game trade with NPC",
    "Presente de NPC / Ovo recebido": "NPC Gift / Received Egg",
    "Encontro fixo no mapa / Interação única": "Static overworld encounter / One-time interaction",
}

SHORT_CONDITIONS_EN_TO_PT = {en: pt for pt, en in SHORT_CONDITIONS_PT_TO_EN.items()}

EVENT_CONDITIONS_EN_TO_PT = {
    (
        "A Shroomish is near the start of Route 203 near some flowers and trees. Talk to it with an Oran Berry in your inventory. "
        "It'll take it, transform into Mew and disappear. After seeing the Shroomish part, you'll find a Buneary on Route 209 above a muddy slope. "
        "Talk to it with a Sitrus Berry in your inventory. It'll take it, transform into Mew and disappear. After seeing the Buneary part, "
        "you'll find a Torchic in Pastoria City on the alcove above the lake. Talk to it with an Old Gateau in your inventory. "
        "It'll take it, transform into Mew and disappear. After seeing the Torchic part, you'll find a Pachirisu on Route 201. "
        "Talk to it and it'll transform into Mew, but stay in place. Talk to Mew to encounter it."
    ): (
        "Há um Shroomish perto do início da Route 203, próximo a flores e árvores. Fale com ele tendo uma Oran Berry no inventário; "
        "ele a pegará, se transformará em Mew e desaparecerá. Depois dessa etapa, você encontrará um Buneary na Route 209 acima de uma rampa de lama. "
        "Fale com ele tendo uma Sitrus Berry no inventário; ele a pegará, se transformará em Mew e desaparecerá. Depois da etapa do Buneary, "
        "você encontrará um Torchic em Pastoria City na área elevada acima do lago. Fale com ele tendo um Old Gateau no inventário; "
        "ele o pegará, se transformará em Mew e desaparecerá. Depois da etapa do Torchic, você encontrará um Pachirisu na Route 201. "
        "Fale com ele e ele se transformará em Mew, permanecendo no lugar. Fale com Mew para enfrentá-lo."
    ),
    (
        "After becoming Champion, do the Lugia quest as far as receiving the Silver Wing from Professor Oak. "
        "Place Raikou, Entei and Suicune in your active party. Ask Professor Oak in Eterna City about 'Quests' to get the Rainbow Wing. "
        "Go to the Lost Tower. On the top floor by a grave is Ho-Oh. Talk to Ho-Oh with the Rainbow Wing in your inventory to encounter it."
    ): (
        "Após se tornar Campeão, avance na missão do Lugia até receber a Silver Wing com Professor Oak. "
        "Coloque Raikou, Entei e Suicune na sua party ativa. Pergunte ao Professor Oak em Eterna City sobre 'Quests' para obter a Rainbow Wing. "
        "Vá até a Lost Tower. No último andar, perto de um túmulo, está Ho-Oh. Fale com Ho-Oh com a Rainbow Wing no inventário para enfrentá-lo."
    ),
    (
        "After becoming Champion, place Articuno, Zapdos and Moltres in your active party. "
        "Ask Professor Oak in Eterna City about 'Quests' to get the Silver Wing. Go to Route 220. "
        "At the bottom of the route is Lugia on a small island. Talk to Lugia with the Silver Wing in your inventory to encounter it."
    ): (
        "Após se tornar Campeão, coloque Articuno, Zapdos e Moltres na sua party ativa. "
        "Pergunte ao Professor Oak em Eterna City sobre 'Quests' para obter a Silver Wing. Vá até a Route 220. "
        "Na parte inferior da rota há uma pequena ilha com Lugia. Fale com Lugia com a Silver Wing no inventário para enfrentá-lo."
    ),
    (
        "After capturing Dialga, return to the cave above the waterfall in the room accessible from the summit. "
        "Collect the Lustrous Orb. Go to Spear Pillar with the Lustrous Orb in your inventory to find Palkia. Talk to Palkia to encounter it."
    ): (
        "Após capturar Dialga, retorne à caverna acima da cachoeira na sala acessível pelo topo. "
        "Pegue a Lustrous Orb. Vá até Spear Pillar com a Lustrous Orb no inventário para encontrar Palkia. Fale com Palkia para enfrentá-lo."
    ),
    (
        "After defeating Jupiter in Eterna Galactic HQ, Cynthia will approach and give you an Egg. Previously, this Egg contained a Togepi. "
        "It is now randomized between: Riolu, Budew, Happiny, Togepi. You can save before collecting the Egg and soft reset if you don't like the result. "
        "If you obtained any of these babies from the Jubilife Baby Egg, you will not get them again here."
    ): (
        "Após derrotar Jupiter no Eterna Galactic HQ, Cynthia se aproximará e entregará um Ovo. Antes, esse Ovo continha um Togepi; "
        "agora ele é sorteado entre: Riolu, Budew, Happiny e Togepi. Você pode salvar antes de pegar o Ovo e fazer soft reset se quiser outro resultado. "
        "Se você já obteve algum desses bebês no Jubilife Baby Egg, ele não sairá novamente aqui."
    ),
    (
        "After defeating Mars, the scientist will mention Drifloon reappearing. "
        "You may now encounter it once a day outside the Valley Windworks, instead of every Friday."
    ): (
        "Após derrotar Mars, o cientista comentará sobre o retorno de Drifloon. "
        "Agora você pode encontrá-lo uma vez por dia do lado de fora de Valley Windworks, em vez de apenas às sextas-feiras."
    ),
    (
        "After defeating Wake (or on your way to Canalave), speak with the NPCs in the back of Jubilife Poké Mart. "
        "Walk north of the city toward the Ravaged Path. Head inside the Ravaged Path and turn left. "
        "Surf down the waterway until you reach land, and pass into the cave system while defeating Graveler in the way. "
        "You will locate Crystal Onix in the very back."
    ): (
        "Após derrotar Wake (ou a caminho de Canalave), fale com os NPCs nos fundos do Jubilife Poké Mart. "
        "Siga ao norte da cidade em direção ao Ravaged Path. Entre no Ravaged Path e vire à esquerda. "
        "Use Surf pelo canal de água até alcançar terra firme e atravesse o sistema de cavernas derrotando os Graveler no caminho. "
        "Você encontrará o Crystal Onix bem no fundo."
    ),
    (
        "After proceeding through Iron Island with Riley and fighting the Team Galactic Grunts, he will offer you an egg. "
        "If you are going to reset for shininess, you must save before accepting the egg. Same as in Platinum, it contains a Riolu. "
        "Even if you obtained a Riolu from the Trainer School or Cynthia eggs, this one will still be Riolu."
    ): (
        "Após atravessar Iron Island com Riley e enfrentar os Team Galactic Grunts, ele oferecerá um Ovo. "
        "Se quiser tentar shiny, salve antes de aceitar o Ovo. Assim como em Platinum, ele contém um Riolu. "
        "Mesmo que você já tenha obtido um Riolu nos ovos da Trainer School ou da Cynthia, este continuará sendo Riolu."
    ),
    (
        "After the credits, go to Canalave and into the house next to the port. Talk to the young boy in the bed. "
        "Talk to the sailor outside to go to Fullmoon Island. Talk to Cresselia in the grove further in the island to encounter it."
    ): (
        "Após os créditos, vá a Canalave e entre na casa ao lado do porto. Fale com o garoto deitado na cama. "
        "Fale com o marinheiro do lado de fora para ir até Fullmoon Island. Fale com Cresselia na clareira mais adentro da ilha para enfrentá-la."
    ),
    (
        "After the credits, talk to any of the meteories in Veilstone City. You should receive a message about something getting angry. "
        "Enter the bottommost meteor pit that has two meteorites in it, past the steps. Go up the steps and exit the pit. "
        "Deoxys will appear behind you and initiate battle."
    ): (
        "Após os créditos, interaja com qualquer um dos meteoritos em Veilstone City; aparecerá uma mensagem dizendo que algo ficou furioso. "
        "Entre na cratera mais ao sul que contém dois meteoritos, passando pelos degraus. Suba os degraus e saia da cratera. "
        "Deoxys aparecerá atrás de você e iniciará a batalha."
    ),
    (
        "After the credits, talk to the Celestic elder at the big house in Celestic Town. Go to Mt. Coronet. "
        "Collect the Adamant Orb in the cave above the waterfall in the room accessible from the summit. "
        "Go to Spear Pillar with the Adamant Orb in your inventory to find Dialga. Talk to Dialga to encounter it."
    ): (
        "Após os créditos, fale com a anciã na casa grande em Celestic Town. Vá para Mt. Coronet. "
        "Pegue a Adamant Orb na caverna acima da cachoeira na sala acessível pelo topo. "
        "Vá até Spear Pillar com a Adamant Orb no inventário para encontrar Dialga. Fale com Dialga para enfrentá-lo."
    ),
    (
        "After the credits, talk to the old woman in the 'Foreign Building' in Hearthome City to make the Type Master trainers appear. "
        "You need to collect all seventeen Plate items. You can get the Plates by defeating the Type Master trainers. "
        "The Plates previously in the field and Underground have been removed. Type Master trainers must be challenged with only a single Pokémon on your team that shares the type they specialise in. "
        "Flame Plate: Route 226, just right of the Survival Area. Splash Plate: Route 219, just below Sandgem Town. Zap Plate: Sunyshore City, inside the lighthouse. "
        "Meadow Plate: Floaroma Meadow, just right of the house. Icicle Plate: Snowpoint City, to the right of the Gym. Fist Plate: Veilstone City, in the house just south of the Gym. "
        "Toxic Plate: Pastoria City, on the top floor of the Great Marsh lobby. Earth Plate: Oreburgh Gate, on the top floor north of the entrances. "
        "Sky Plate: The Pokémon League, looking out on the right outside the building. Mind Plate: Solaceon Ruins, just inside the entrance. "
        "Insect Plate: Route 202, just above the Sandgem Town entrance. Stone Plate: Route 207, just to the right of the muddy slope. "
        "Spooky Plate: The Lost Tower, on the top floor. Draco Plate: Celestic Town, inside the ruins. Dread Plate: Sendoff Spring, just after the entrance from Route 214. "
        "Iron Plate: Iron Island, just south of the entrance to the cave. Pixie Plate: The Contest Hall. "
        "With all seventeen Plates in your inventory, talk to the old woman in the 'Foreign Building' to receive the Azure Flute. "
        "Go to Spear Pillar and stand on the flute symbol just as you leave the cave. You'll be prompted to play the Azure Flute. "
        "Head up the stairs to battle Arceus. You can fight Arceus repeatedly by playing the Azure Flute on the symbol until you catch it."
    ): (
        "Após os créditos, fale com a senhora no 'Foreign Building' em Hearthome City para fazer os treinadores Type Master aparecerem. "
        "Você precisa coletar todas as dezessete Plates derrotando os treinadores Type Master (as Plates que ficavam no mapa e no Underground foram removidas). "
        "Os treinadores Type Master devem ser desafiados com apenas um único Pokémon no time que compartilhe o tipo em que eles se especializam. "
        "Flame Plate: Route 226, logo à direita da Survival Area. Splash Plate: Route 219, logo abaixo de Sandgem Town. Zap Plate: Sunyshore City, dentro do farol. "
        "Meadow Plate: Floaroma Meadow, logo à direita da casa. Icicle Plate: Snowpoint City, à direita do Gym. Fist Plate: Veilstone City, na casa logo ao sul do Gym. "
        "Toxic Plate: Pastoria City, no último andar do saguão do Great Marsh. Earth Plate: Oreburgh Gate, no andar superior ao norte das entradas. "
        "Sky Plate: The Pokémon League, olhando para fora à direita do prédio. Mind Plate: Solaceon Ruins, logo após a entrada. "
        "Insect Plate: Route 202, logo acima da entrada de Sandgem Town. Stone Plate: Route 207, logo à direita da rampa de lama. "
        "Spooky Plate: Lost Tower, no último andar. Draco Plate: Celestic Town, dentro das ruínas. Dread Plate: Sendoff Spring, logo após a entrada pela Route 214. "
        "Iron Plate: Iron Island, logo ao sul da entrada da caverna. Pixie Plate: Contest Hall. "
        "Com todas as dezessete Plates no inventário, fale com a senhora no 'Foreign Building' para receber a Azure Flute. "
        "Vá até Spear Pillar e pise no símbolo de flauta logo ao sair da caverna; você será convidado a tocar a Azure Flute. "
        "Suba as escadas para batalhar contra Arceus. Você pode enfrentá-lo repetidamente tocando a Azure Flute no símbolo até capturá-lo."
    ),
    (
        "After the story events at the Pokémon Mansion, you will be offered an Egg. If shiny-hunting, save before receiving the Egg. "
        "Accept the Egg, then hatch it to get Manaphy."
    ): (
        "Após os eventos da história na Pokémon Mansion, você receberá a oferta de um Ovo. Se estiver fazendo shiny hunt, salve antes de receber o Ovo. "
        "Aceite o Ovo e choque-o para obter Manaphy."
    ),
    (
        "Check the shrine in Celestic Town to get the GS Ball. After getting the GS Ball, return to Eterna Forest from the entrance on the Eterna City side. "
        "Walk forward and you should see a message saying the GS Ball is shaking, followed by several portals appearing around Eterna Forest. "
        "Celebi will come out of the portal in sight, see you, then dive back in. Go to each of the portals and talk to them to trigger a small Trainer fight. "
        "There are eight in all. After all eight portals have been cleared, Celebi will wait close to the center of the forest. Talk to Celebi to encounter it."
    ): (
        "Examine o santuário em Celestic Town para obter a GS Ball. Depois, volte à Eterna Forest pela entrada do lado de Eterna City. "
        "Caminhe para frente até ver uma mensagem dizendo que a GS Ball está tremendo, e vários portais surgirão pela Eterna Forest. "
        "Celebi sairá do portal visível, verá você e voltará para dentro. Vá até cada um dos portais e interaja com eles para iniciar pequenas batalhas contra Treinadores "
        "(são oito no total). Após concluir todos os oito portais, Celebi ficará esperando perto do centro da floresta. Fale com Celebi para enfrentá-lo."
    ),
    (
        "Complete the events as far as Rowan's Assistant telling you to speak to your mother. "
        "Speak to your mother and she'll suggest taking Eevee. Interact with the Eevee to receive it."
    ): (
        "Avance nos eventos até o Assistente de Rowan pedir que você fale com sua mãe. "
        "Fale com sua mãe e ela sugerirá levar Eevee. Interaja com o Eevee para recebê-lo."
    ),
    (
        "Complete the events in the story with Regigigas in the Snowpoint Temple. Become the Champion (ie see the credits). "
        "Go to the basement of the Snowpoint Temple with Regirock, Regice and Registeel in your party. "
        "Talk to Regigigas with Regirock, Regice and Registeel in your party to encounter it."
    ): (
        "Conclua os eventos da história envolvendo Regigigas no Snowpoint Temple e torne-se Campeão (veja os créditos). "
        "Vá ao subsolo do Snowpoint Temple com Regirock, Regice e Registeel na sua party. "
        "Fale com Regigigas com os três na party para enfrentá-lo."
    ),
    (
        "Defeat Dawn or Lucas at Route 224 as part of the storyline. After becoming Champion, Professor Oak will approach you in Twinleaf to give Oak's Letter. "
        "Head to Route 224 and go towards the top of the route. Marley will speak to you. Speak to Professor Oak, and enter in whatever you want on the stone tablet. "
        "The map will change and Shaymin will appear, then flee. Head up the Seabreak Path towards the Flower Paradise. "
        "Talk to Shaymin in the center of the Flower Paradise to encounter it."
    ): (
        "Derrote Dawn ou Lucas na Route 224 como parte da história. Após se tornar Campeão, Professor Oak aparecerá em Twinleaf para entregar a Oak's Letter. "
        "Vá para a Route 224 e siga até o topo da rota. Marley falará com você. Fale com Professor Oak e escreva o que quiser na tábua de pedra. "
        "O mapa mudará e Shaymin aparecerá antes de fugir. Suba pelo Seabreak Path em direção ao Flower Paradise. "
        "Fale com Shaymin no centro do Flower Paradise para enfrentá-lo."
    ),
    "Defeat Jupiter at the Eterna Galactic Building. Interact with the Poké Ball behind her to get Porygon.": (
        "Derrote Jupiter no Eterna Galactic Building. Interaja com a Poké Ball atrás dela para receber Porygon."
    ),
    "Defeat the Pokémon League and become Champion. Speak with the small girl in Snowpoint Pokémon Center. Take a Hard Stone to Snowpoint Temple. Interact with Regirock to wake and battle it.": (
        "Derrote a Pokémon League e torne-se Campeão. Fale com a garotinha no Snowpoint Pokémon Center. Leve uma Hard Stone ao Snowpoint Temple. Interaja com Regirock para despertá-lo e batalhar."
    ),
    "Defeat the Pokémon League and become Champion. Speak with the small girl in Snowpoint Pokémon Center. Take a Nevermeltice to Snowpoint Temple. Interact with Regice to wake and battle it.": (
        "Derrote a Pokémon League e torne-se Campeão. Fale com a garotinha no Snowpoint Pokémon Center. Leve um Nevermeltice ao Snowpoint Temple. Interaja com Regice para despertá-lo e batalhar."
    ),
    "Defeat the Pokémon League and become Champion. Speak with the small girl in Snowpoint Pokémon Center. Take an Iron Ball to Snowpoint Temple. Interact with Registeel to wake and battle it.": (
        "Derrote a Pokémon League e torne-se Campeão. Fale com a garotinha no Snowpoint Pokémon Center. Leve uma Iron Ball ao Snowpoint Temple. Interaja com Registeel para despertá-lo e batalhar."
    ),
    "During the course of [Mewtwo's event](/docs/special-events/legendaries#kanto-legendaries), you will fight four Clone Pokemon. You may fight them in any order and must catch them to proceed.": (
        "Durante o evento do Mewtwo (em Oreburgh Gate), você enfrentará quatro Clone Pokémon. Você pode enfrentá-los em qualquer ordem e precisa capturá-los para prosseguir."
    ),
    (
        "Enter Amity Square and proceed through the event by finding them around the park. Head near the top of the park and to the left of the lady standing in front of the poffin maker. "
        "Head up the stairs on the right of the park and then head up to get it to run out of the small houses at the top of the hill. "
        "Head to the left of the park and find the girl standing with her Happiny. Go back to the small houses at the top right of the park and talk to it there to catch it."
    ): (
        "Entre na Amity Square e avance no evento encontrando-o pelo parque. Vá para a parte superior do parque, à esquerda da senhora em frente à máquina de Poffin. "
        "Suba as escadas à direita do parque e siga para cima para fazê-lo sair das casinhas no topo da colina. "
        "Vá para a esquerda do parque e encontre a garota com seu Happiny. Volte às casinhas no canto superior direito do parque e fale com ele lá para capturá-lo."
    ),
    "Enter Lost Tower and proceed through the event. You will fight an uncatchable Chandelure. Afterward, a Litwick will approach to join your party.": (
        "Entre na Lost Tower e avance pelo evento. Você enfrentará um Chandelure incapturável. Depois disso, um Litwick se aproximará para entrar na sua party."
    ),
    "Enter Wayward Cave from the hidden entrance beneath the Cycling Road. Go through the basement and up the stairs to the small room. Walk forward and you'll encounter Gabite.": (
        "Entre na Wayward Cave pela entrada secreta sob a Cycling Road. Atravesse o subsolo e suba as escadas até a sala pequena. Caminhe para frente para encontrar Gabite."
    ),
    "Get the Odd Keystone from a man on Route 208, hidden in Twinleaf Town, or from the Underground. Talk to the broken stone tower to encounter Spiritomb. The Odd Keystone will only be consumed upon successful capture.": (
        "Pegue uma Odd Keystone com o homem na Route 208, escondida em Twinleaf Town ou no Underground. Interaja com a torre de pedra quebrada para enfrentar Spiritomb. A Odd Keystone só é consumida após a captura."
    ),
    (
        "Giratina is encountered in the Distortion World as part of the story. It cannot be captured in the Distortion World. Defeat it to proceed. "
        "You can find it in the final room of Turnback Cave after the credits at Level 85. Talk to Giratina to encounter it. The Griseous Orb will be on the shrine behind Giratina once captured."
    ): (
        "Giratina é enfrentado no Distortion World como parte da história e não pode ser capturado lá; derrote-o para prosseguir. "
        "Você pode encontrá-lo na sala final da Turnback Cave após os créditos no Nível 85. Fale com Giratina para enfrentá-lo. O Griseous Orb estará no santuário atrás dele após a captura."
    ),
    "Go inside the house near Oreburgh Mine. Talk to Steven and he'll offer you a Beldum.": (
        "Entre na casa perto da Oreburgh Mine. Fale com Steven e ele oferecerá um Beldum."
    ),
    "Go to Celestic Town with a Pichu in your party. If shiny-hunting, save before continuing. Interact with the shrine to obtain a special Pichu.": (
        "Vá até Celestic Town com um Pichu na sua party. Se estiver fazendo shiny hunt, salve antes de continuar. Interaja com o santuário para obter um Pichu especial."
    ),
    "Go to the Underground Man's house, near the Pokémon Center in Eterna City. Talk to the female scientist to receive fossils for all of these Pokémon. Take the fossils to the museum in Oreburgh City to revive them.": (
        "Vá à casa do Underground Man, perto do Pokémon Center em Eterna City. Fale com a cientista para receber os fósseis de todos esses Pokémon. Leve os fósseis ao museu em Oreburgh City para revivê-los."
    ),
    "In one of the houses is an old lady. Agree to listen to her story. She'll give you a Lapras after she finishes.": (
        "Em uma das casas há uma senhora idosa. Aceite ouvir a história dela e ela dará um Lapras quando terminar."
    ),
    (
        "Interact with the briefcase at the top right of Rowan's lab. Rowan will say a few words and then allow you to take out the Poké Balls inside. "
        "Interact with the briefcase again to receive the two Sinnoh starters that you didn't choose. "
        "Turtwig, Chimchar and Piplup will be given in that order, with the one you already selected not appearing."
    ): (
        "Interaja com a maleta no canto superior direito do laboratório do Prof. Rowan. Ele dirá algumas palavras e permitirá pegar as Poké Balls de dentro. "
        "Interaja novamente com a maleta para receber os dois iniciais de Sinnoh que você não escolheu. "
        "Turtwig, Chimchar e Piplup são entregues nessa ordem, omitindo o que você já escolheu."
    ),
    (
        "Obtain the Lunar Wing by capturing Cresselia on Fullmoon Island. Talk to the young boy in the house next to the port to heal him. "
        "Talk to the woman in the dark house on Route 217 to get the Member Card. Enter the top house in Canalave City to get warped to Newmoon Island. "
        "Talk to Darkrai in the grove further in the island to encounter it."
    ): (
        "Obtenha a Lunar Wing capturando Cresselia na Fullmoon Island e fale com o garoto na casa ao lado do porto para curá-lo. "
        "Fale com a mulher na casa escura da Route 217 para conseguir o Member Card. Entre na casa ao norte de Canalave City para ser teleportado à Newmoon Island. "
        "Fale com Darkrai na clareira mais adentro da ilha para enfrentá-lo."
    ),
    (
        "Once you gain access, meet with Dragonite in Resort Area to receive the Odd Invitation. Go to Oreburgh Gate. In the basement, head as far west as possible to find a Nurse. "
        "Talk to the Nurse with the Odd Invitation in your inventory to find Mewtwo. Capture all of its clones to fight it. After defeating its armored form, you will fight it again and may attempt to catch it. "
        "Once defeated, you will receive [Mewtwo's Armor] as a memento. You may change forms between Mk.I (original movie) and Mk.II (PokéGO armor) by speaking with the NPC on the second floor of the Resort Area Pokémon Center. Both forms are purely cosmetic."
    ): (
        "Assim que tiver acesso, encontre Dragonite na Resort Area para receber o Odd Invitation. Vá até Oreburgh Gate e, no subsolo, siga o máximo possível para o oeste até encontrar uma Nurse. "
        "Fale com ela tendo o Odd Invitation no inventário para encontrar Mewtwo. Capture todos os seus clones para enfrentá-lo; após derrotar sua forma com armadura, você batalhará novamente e poderá capturá-lo. "
        "Ao derrotá-lo, você receberá [Mewtwo's Armor] como lembrança. É possível alternar entre as formas Mk.I e Mk.II falando com o NPC no segundo andar do Resort Area Pokémon Center (apenas cosmético)."
    ),
    "Speak to Rowan after the Distortion World events. Go to Lake Acuity. Go to the island in the center and enter the cave. Talk to Uxie to encounter it.": (
        "Fale com Rowan após os eventos do Distortion World. Vá até Lake Acuity, siga para a ilha no centro e entre na caverna. Fale com Uxie para enfrentá-lo."
    ),
    "Speak to Rowan after the Distortion World events. Go to Lake Valor. Go to the island in the center and enter the cave. Talk to Azelf to encounter it.": (
        "Fale com Rowan após os eventos do Distortion World. Vá até Lake Valor, siga para a ilha no centro e entre na caverna. Fale com Azelf para enfrentá-lo."
    ),
    "Speak to Rowan after the Distortion World events. Go to Lake Verity. Go to the island in the center and enter the cave. Talk to Mesprit to encounter it.": (
        "Fale com Rowan após os eventos do Distortion World. Vá até Lake Verity, siga para a ilha no centro e entre na caverna. Fale com Mesprit para enfrentá-lo."
    ),
    "Speak to Rowan after the Distortion World events. Head to Route 208. On the platform on the left of the route accessible by Rock Climb is Raikou. Talk to Raikou to encounter it.": (
        "Fale com Rowan após os eventos do Distortion World. Vá para a Route 208; na plataforma à esquerda acessível com Rock Climb está Raikou. Fale com Raikou para enfrentá-lo."
    ),
    "Speak to Rowan after the Distortion World events. Head to Route 211 (East). On the platform on the top of the route accessible by Rock Climb is Entei. Talk to Entei to encounter it.": (
        "Fale com Rowan após os eventos do Distortion World. Vá para a Route 211 (East); na plataforma superior acessível com Rock Climb está Entei. Fale com Entei para enfrentá-lo."
    ),
    "Speak to Rowan after the Distortion World events. Head to Route 213. At the bottom of the platform in the middle of the route accessible by Rock Climb is Suicune. Talk to Suicune to encounter it.": (
        "Fale com Rowan após os eventos do Distortion World. Vá para a Route 213; na base da plataforma central acessível com Rock Climb está Suicune. Fale com Suicune para enfrentá-lo."
    ),
    "Speak to Rowan after the Distortion World events. Head to Valley Windworks. On an island behind the building is Zapdos. Talk to Zapdos to encounter it.": (
        "Fale com Rowan após os eventos do Distortion World. Vá para Valley Windworks; em uma ilha atrás do prédio está Zapdos. Fale com Zapdos para enfrentá-lo."
    ),
    "Speak to Rowan after the Distortion World events. Head to Victory Road. In a small room accessible from the last big area is Moltres. Talk to Moltres to encounter it.": (
        "Fale com Rowan após os eventos do Distortion World. Vá para Victory Road; em uma pequena sala acessível pela última grande área está Moltres. Fale com Moltres para enfrentá-lo."
    ),
    "Speak to Rowan after the Distortion World events. Head to the snowy parts of Mt. Coronet. Just above the spiralling paths entrance is Articuno. Talk to Articuno to encounter it.": (
        "Fale com Rowan após os eventos do Distortion World. Vá para a parte nevada de Mt. Coronet; logo acima da entrada dos caminhos em espiral está Articuno. Fale com Articuno para enfrentá-lo."
    ),
    (
        'Speak to Steven in Oreburgh City via the Quests option with the Magma Stone in your inventory to receive the Soul Dew. '
        'Catch Cresselia on Fullmoon Island to get a rock to appear in the clearing. Talk to the clearing from its bottom with the Soul Dew in your inventory to get a choice. Choose "Blue" to encounter Latios.'
    ): (
        'Fale com Steven em Oreburgh City pela opção Quests com a Magma Stone no inventário para receber a Soul Dew. '
        'Capture Cresselia na Fullmoon Island para fazer uma rocha aparecer na clareira. Interaja com a clareira por baixo tendo a Soul Dew no inventário e escolha "Blue" para enfrentar Latios.'
    ),
    (
        'Speak to Steven in Oreburgh City via the Quests option with the Magma Stone in your inventory to receive the Soul Dew. '
        'Catch Cresselia on Fullmoon Island to get a rock to appear in the clearing. Talk to the clearing from its bottom with the Soul Dew in your inventory to get a choice. Choose "Red" to encounter Latias.'
    ): (
        'Fale com Steven em Oreburgh City pela opção Quests com a Magma Stone no inventário para receber a Soul Dew. '
        'Capture Cresselia na Fullmoon Island para fazer uma rocha aparecer na clareira. Interaja com a clareira por baixo tendo a Soul Dew no inventário e escolha "Red" para enfrentar Latias.'
    ),
    "Steven must have received the Magma Stone and been shown Latias and Latios. Talk to Steven in Oreburgh City via the Quests option to receive the Blue Orb. Go to Route 213. Talk to Kyogre with the Blue Orb in your inventory to encounter it.": (
        "Steven precisa já ter recebido a Magma Stone e visto Latias e Latios. Fale com Steven em Oreburgh City pela opção Quests para receber a Blue Orb. Vá à Route 213 e fale com Kyogre com a Blue Orb no inventário para enfrentá-lo."
    ),
    "Steven must have received the Magma Stone and been shown Latias and Latios. Talk to Steven in Oreburgh City via the Quests option to receive the Jade Orb. Go to the Pokémon League part above Victory Road. Below the waterfall on a small bit of land jutting out is Rayquaza. Talk to Rayquaza with the Jade Orb in your inventory to encounter it.": (
        "Steven precisa já ter recebido a Magma Stone e visto Latias e Latios. Fale com Steven em Oreburgh City pela opção Quests para receber a Jade Orb. Vá para a área da Pokémon League acima da Victory Road; abaixo da cachoeira, em um pequeno trecho de terra saliente, está Rayquaza. Fale com Rayquaza com a Jade Orb no inventário para enfrentá-lo."
    ),
    "Steven must have received the Magma Stone and been shown Latias and Latios. Talk to Steven in Oreburgh City via the Quests option to receive the Red Orb. Go to the back room of Stark Mountain. Talk to Groudon with the Red Orb in your inventory to encounter it.": (
        "Steven precisa já ter recebido a Magma Stone e visto Latias e Latios. Fale com Steven em Oreburgh City pela opção Quests para receber a Red Orb. Vá até a sala dos fundos de Stark Mountain e fale com Groudon com a Red Orb no inventário para enfrentá-lo."
    ),
    (
        "Talk to the Cowgirl in the Jubilife School to receive an Egg. The Egg will hatch into one of the following Pokémon at random: "
        "Pichu, Cleffa, Igglybuff, Togepi, Tyrogue, Smoochum, Elekid, Magby, Azurill, Wynaut, Budew, Chingling, Bonsly, Mime Jr., Happiny, Munchlax, Riolu, Mantyke. "
        "You can save before collecting the Egg and soft reset if you don't like the result."
    ): (
        "Fale com a Cowgirl na Jubilife School para receber um Ovo. O Ovo chocará aleatoriamente um dos seguintes Pokémon: "
        "Pichu, Cleffa, Igglybuff, Togepi, Tyrogue, Smoochum, Elekid, Magby, Azurill, Wynaut, Budew, Chingling, Bonsly, Mime Jr., Happiny, Munchlax, Riolu ou Mantyke. "
        "Você pode salvar antes de pegar o Ovo e fazer soft reset se quiser outro resultado."
    ),
    "Talk to the Interviewer at the top left. Answer her questions correctly and win the battle. You may choose the order between Bulbasaur, Charmander and Squirtle, and can collect all three. If your party gets full before all three are given, she will send them to your box.": (
        "Fale com a Interviewer no canto superior esquerdo, responda às perguntas corretamente e vença a batalha. Você pode escolher a ordem entre Bulbasaur, Charmander e Squirtle e pegar todos os três; se sua party encher antes, ela os enviará para a Box."
    ),
    "Talk to the Interviewer at the top left. Answer her questions correctly and win the battle. You may choose the order between Chikorita, Cyndaquil and Totodile, and can collect all three. If your party gets full before all three are given, she will send them to your box.": (
        "Fale com a Interviewer no canto superior esquerdo, responda às perguntas corretamente e vença a batalha. Você pode escolher a ordem entre Chikorita, Cyndaquil e Totodile e pegar todos os três; se sua party encher antes, ela os enviará para a Box."
    ),
    "Talk to the Interviewer at the top left. Answer her questions correctly and win the battle. You may choose the order between Treecko, Torchic and Mudkip, and can collect all three. If your party gets full before all three are given, she will send them to your box.": (
        "Fale com a Interviewer no canto superior esquerdo, responda às perguntas corretamente e vença a batalha. Você pode escolher a ordem entre Treecko, Torchic e Mudkip e pegar todos os três; se sua party encher antes, ela os enviará para a Box."
    ),
    "Talk to the TV in one of the rooms at the back of the Old Chateau. The event is now repeatable and can be done at any time of day. The key you find can be used on Eterna's Galactic HQ first floor after defeating Jupiter.": (
        "Interaja com a TV em uma das salas nos fundos do Old Chateau. Agora o evento é repetível e pode ser feito a qualquer hora do dia. A chave encontrada pode ser usada no primeiro andar do Galactic HQ de Eterna após derrotar Jupiter."
    ),
    (
        "Talk to the girl in the Pokémon Center in Eterna City with a Dazzling Gleam TM in your inventory. "
        "Talk to the old woman in a house in Solaceon Town below the ledges with a Ponyta, Rapidash, Moltres, Quilava or Infernape in your party. "
        "Talk to the little boy outside the bottom house in Pastoria with a Gyarados, Carvanha or Sharpedo in your party. "
        "Talk to the Unown on the bottom floor of Solaceon Ruins. Talk to Jirachi with a Jigglypuff in your party. Select 'Yes' to sing to and encounter it."
    ): (
        "Fale com a garota no Pokémon Center de Eterna City tendo a TM Dazzling Gleam no inventário. "
        "Fale com a senhora em uma casa em Solaceon Town abaixo das elevações com Ponyta, Rapidash, Moltres, Quilava ou Infernape na party. "
        "Fale com o garotinho do lado de fora da casa inferior em Pastoria com Gyarados, Carvanha ou Sharpedo na party. "
        "Fale com o Unown no último andar das Solaceon Ruins. Fale com Jirachi com um Jigglypuff na party e selecione 'Yes' para cantar e enfrentá-lo."
    ),
    "Talk to the painting with the glowing red eyes in one of the rooms at the back of the Old Chateau. You will encounter a special, costumed Gengar. This Gengar is mechanically identical to a regular Gengar.": (
        "Interaja com o quadro de olhos vermelhos brilhantes em uma das salas nos fundos do Old Chateau. Você encontrará um Gengar especial fantasiado (mecanicamente idêntico a um Gengar normal)."
    ),
}


def normalize_bilingual_condition(raw_condition: str) -> tuple[str, str]:
    """
    Given a condition string (either legacy PT short label or EN text),
    return a tuple (conditions_en, conditions_pt).
    """
    if not raw_condition:
        return ("None", "Nenhuma")

    if raw_condition in SHORT_CONDITIONS_PT_TO_EN:
        en_val = SHORT_CONDITIONS_PT_TO_EN[raw_condition]
        return (en_val, raw_condition)

    if raw_condition in SHORT_CONDITIONS_EN_TO_PT:
        pt_val = SHORT_CONDITIONS_EN_TO_PT[raw_condition]
        return (raw_condition, pt_val)

    if raw_condition in EVENT_CONDITIONS_EN_TO_PT:
        return (raw_condition, EVENT_CONDITIONS_EN_TO_PT[raw_condition])

    return (raw_condition, raw_condition)
