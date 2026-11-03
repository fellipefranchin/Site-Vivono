#!/usr/bin/env python3
"""Reescreve a pagina das Bebidas a partir da carta de 2026.11.02.

As harmonizacoes da carta vem por prato; aqui sao invertidas para ficarem por
vinho, que e como o site sempre as mostrou.
"""
import re, unicodedata
from pathlib import Path

HTML = Path("/Users/fellipefranchin/dev/sites/vívono/index.html")

# ---------------------------------------------------------------- harmonizacoes
# prato -> vinhos (nome curto), tal como vem na carta
PARES = [
 ("Pão de Alho", "Garlic Bread", ["Dory Branco", "Muralhas", "Bolla Prosecco"]),
 ("Di Andria", "Di Andria", ["Arinto", "Muralhas", "Bolla Prosecco"]),
 ("Crostini", "Crostini", ["Arinto", "Bolla Prosecco"]),
 ("Insalata Vívono", "Insalata Vívono", ["Arinto", "Crasto Branco", "Anthilia"]),
 ("Brasiliana", "Brasiliana", ["Montado Rosé", "Mateus Rosé", "Bolla Prosecco"]),
 ("Porcellina", "Porcellina", ["Penedo do Lexim", "Peceguina"]),
 ("Brasiliana Più", "Brasiliana Più", ["Montado Rosé", "Contador de Estórias"]),
 ("Puttanesca", "Puttanesca", ["Muralhas", "Arinto", "Cecchi Chianti"]),
 ("Calabrese", "Calabrese", ["Dory Tinto", "Penedo do Lexim", "Cecchi Chianti"]),
 ("Piemontese", "Piemontese", ["Abanico", "Peceguina", "Barolo"]),
 ("Paulistana", "Paulistana", ["Penedo do Lexim", "Esteva", "Cecchi Chianti"]),
 ("Giardino", "Giardino", ["Dory Branco", "Crasto Branco", "Anthilia"]),
 ("Lusitana", "Lusitana", ["Penedo do Lexim", "Montado Rosé"]),
 ("Margherita", "Margherita", ["Montado Rosé", "Arinto", "Cecchi Chianti"]),
 ("Mineira", "Mineira", ["Esteva", "Montado Rosé"]),
 ("4 Formaggi", "4 Formaggi", ["Crasto Branco", "Peceguina", "Barolo"]),
 ("Vívono", "Vívono", ["Crasto Branco", "Dona Fátima", "Bolla Prosecco"]),
 ("5 Formaggi", "5 Formaggi", ["Contador de Estórias", "Peceguina"]),
 ("Parma Grana", "Parma Grana", ["Abanico", "Chianti Rufina", "Bolla Prosecco"]),
 ("Pepperoni", "Pepperoni", ["Dory Tinto", "Contador de Estórias", "Cecchi Chianti"]),
 ("Parmatella", "Parmatella", ["Arinto", "Dona Fátima", "Bolla Prosecco"]),
 ("Fiambre", "Ham", ["Dory Tinto", "Penedo do Lexim", "Cecchi Chianti"]),
 ("Prosciutto e Funghi", "Prosciutto e Funghi", ["Abanico", "Montado Rosé", "Chianti Rufina"]),
 ("Diavola", "Diavola", ["Cecchi Chianti", "Montado Rosé", "Dory Tinto"]),
 ("Tropicale", "Tropicale", ["Mateus Rosé", "Anthilia"]),
 ("Lasagna al Ragù", "Lasagna al Ragù", ["Contador de Estórias", "Cecchi Chianti"]),
 ("Gnocchi ai Quattro Formaggi", "Gnocchi ai Quattro Formaggi", ["Crasto Branco", "Arinto"]),
 ("Gnocchi al Pomodoro", "Gnocchi al Pomodoro", ["Cecchi Chianti", "Montado Rosé"]),
]

MAX_HARM = 5  # quantos pratos mostrar por vinho


def inverter():
    pt, en = {}, {}
    for prato_pt, prato_en, vinhos in PARES:
        for v in vinhos:
            pt.setdefault(v, []).append(prato_pt)
            en.setdefault(v, []).append(prato_en)
    return pt, en


HPT, HEN = inverter()

# ---------------------------------------------------------------- itens
# (seccao, nome, meta, preco, curto|None, desc_pt, desc_en)
# "curto" liga o item a tabela de harmonizacao da carta
B = {}

B["beers"] = ("Cervejas &amp; Sidra", [
 ("Sagres", "30cl · imperial", "1,67 €", None, None, None),
 ("Sagres", "40cl · caneca", "2,37 €", None, None, None),
 ("Sagres Preta", "30cl · imperial", "1,89 €", None, None, None),
 ("Heineken", "25cl · imperial", "2,19 €", None, None, None),
 ("Heineken", "50cl · caneca", "3,90 €", None, None, None),
 ("Heineken", "33cl · garrafa", "3,29 €", None, None, None),
 ("Bandida", "25cl", "2,39 €", None, None, None),
 ("Bandida", "40cl", "3,90 €", None, None, None),
 ("Heineken 0,0%", "25cl", "2,39 €", None, None, None),
])

B["ptred"] = ("Vinhos Portugueses · Tintos", [
 ("Dory Tinto", "13%", "12,90 €", "Dory Tinto",
  "Jovem, vibrante e atlântico, com fruta vermelha fresca, um toque de especiarias e taninos suaves. Da região de Lisboa, pela AdegaMãe. Aragonez, Castelão e Touriga Nacional.",
  "Young, vibrant and Atlantic, with fresh red fruit, a touch of spice and soft tannins. From the Lisbon region, by AdegaMãe. Aragonez, Castelão and Touriga Nacional."),
 ("Esteva", "13,5%", "13,90 €", "Esteva",
  "Intenso e macio, com frutos vermelhos e pretos maduros, notas balsâmicas e taninos redondos. Do Douro, pela Casa Ferreirinha. Touriga Nacional, Tinta Barroca, Touriga Franca e Tinta Roriz.",
  "Intense and smooth, with ripe red and black fruit, balsamic notes and rounded tannins. From the Douro, by Casa Ferreirinha. Touriga Nacional, Tinta Barroca, Touriga Franca and Tinta Roriz."),
 ("Penedo do Lexim", "13%", "14,90 €", "Penedo do Lexim",
  "Touriga Nacional e Aragonez: frutos silvestres, especiarias e mineralidade, com estrutura elegante e taninos macios. De Cheleiros, na região de Lisboa, pela Manz Wine.",
  "Touriga Nacional and Aragonez: wild berries, spice and minerality, with an elegant structure and soft tannins. From Cheleiros, in the Lisbon region, by Manz Wine."),
 ("Contador de Estórias", "13,5%", "18,90 €", "Contador de Estórias",
  "Encorpado e surpreendente, com notas balsâmicas, fruta madura e personalidade marcante. Da Península de Setúbal, terra do Moscatel e de grandes tintos encorpados. Pela Manz Wine.",
  "Full-bodied and surprising, with balsamic notes, ripe fruit and a striking personality. From the Setúbal Peninsula, land of Moscatel and great full-bodied reds. By Manz Wine."),
 ("Abanico Reserva Tinto", "13,5%", "18,90 €", "Abanico",
  "Estruturado e fresco, com fruta vermelha e preta e taninos polidos. Do Dão, pela Casa da Passarella. Touriga Nacional, Alfrocheiro e Jaen, com estágio em barrica.",
  "Structured and fresh, with red and black fruit and polished tannins. From the Dão, by Casa da Passarella. Touriga Nacional, Alfrocheiro and Jaen, aged in barrels."),
 ("Monte da Peceguina Tinto", "14%", "22,90 €", "Peceguina",
  "Encorpado, com fruta madura, acidez fresca e taninos maduros. Do Alentejo, pela Herdade da Malhadinha Nova, em Albernoa.",
  "Full-bodied, with ripe fruit, fresh acidity and ripe tannins. From the Alentejo, by Herdade da Malhadinha Nova, in Albernoa."),
])

B["ptrose"] = ("Vinhos Portugueses · Rosés", [
 ("Mateus Rosé", "11%", "11,90 €", "Mateus Rosé",
  "Leve, frutado e refrescante, com notas de frutos vermelhos e doçura equilibrada. Da Sogrape, desde 1942. No rótulo, o palácio barroco de Mateus, em Vila Real. Vendido em mais de 130 países.",
  "Light, fruity and refreshing, with notes of red berries and balanced sweetness. By Sogrape, since 1942. On the label, the baroque Mateus palace, in Vila Real. Sold in more than 130 countries."),
 ("Montado Rosé", "12,5%", "11,90 €", "Montado Rosé",
  "Fresco e frutado, com notas de frutos silvestres e acidez equilibrada. Do Alentejo, pela José Maria da Fonseca, casa fundada em 1834.",
  "Fresh and fruity, with notes of wild berries and balanced acidity. From the Alentejo, by José Maria da Fonseca, a house founded in 1834."),
])

B["ptwhite"] = ("Vinhos Portugueses · Brancos", [
 ("Dory Branco", "12,5%", "12,90 €", "Dory Branco",
  "Jovem e exuberante, com toranja, lima e maracujá, acidez viva e mineralidade salina atlântica. Da região de Lisboa, pela AdegaMãe. Alvarinho, Arinto, Sauvignon Blanc e Viosinho.",
  "Young and exuberant, with grapefruit, lime and passion fruit, lively acidity and a salty Atlantic minerality. From the Lisbon region, by AdegaMãe. Alvarinho, Arinto, Sauvignon Blanc and Viosinho."),
 ("Muralhas de Monção", "12,5%", "12,90 €", "Muralhas",
  "Leve, cítrico e com efervescência natural, frescura imediata e final limpo. De Monção e Melgaço, no Minho, pela Adega de Monção. Alvarinho e Trajadura.",
  "Light, citrusy and naturally spritzy, with instant freshness and a clean finish. From Monção and Melgaço, in the Minho, by Adega de Monção. Alvarinho and Trajadura."),
 ("Casa Santos Lima Arinto", "13%", "12,90 €", "Arinto",
  "Vibrante e mineral, com acidez viva e notas cítricas e de ananás. Da região de Lisboa, pela Casa Santos Lima, em Alenquer. Arinto 100%.",
  "Vibrant and mineral, with lively acidity and notes of citrus and pineapple. From the Lisbon region, by Casa Santos Lima, in Alenquer. 100% Arinto."),
 ("Crasto Branco", "12,5%", "19,90 €", "Crasto Branco",
  "Fresco e floral, com limão, maçã verde e camomila, sem madeira. Do Douro, pela Quinta do Crasto. Viosinho, Gouveio e Rabigato.",
  "Fresh and floral, with lemon, green apple and chamomile, unoaked. From the Douro, by Quinta do Crasto. Viosinho, Gouveio and Rabigato."),
 ("Dona Fátima", "13%", "29,90 €", "Dona Fátima",
  "Tropical e estruturado, com textura surpreendente: um branco de carácter próprio. De Cheleiros, na região de Lisboa, pela Manz Wine. Jampal, casta rara e quase extinta, recuperada por André Manz.",
  "Tropical and structured, with a surprising texture: a white with a character all its own. From Cheleiros, in the Lisbon region, by Manz Wine. Jampal, a rare and nearly extinct grape, revived by André Manz."),
])

B["itred"] = ("Vinhos Italianos · Tintos", [
 ("Cecchi Chianti DOCG", "13%", "14,90 €", "Cecchi Chianti",
  "Tinto clássico e equilibrado, com frutos vermelhos, especiarias e acidez marcante. Taninos suaves e final fresco. Da Toscana, onde se faz Chianti há mais de 300 anos. DOCG, o nível mais alto das denominações italianas.",
  "A classic, balanced red, with red berries, spice and marked acidity. Soft tannins and a fresh finish. From Tuscany, where Chianti has been made for more than 300 years. DOCG, the highest tier of Italian appellations."),
 ("Chianti Rufina Riserva DOCG", "13%", "26,90 €", "Chianti Rufina",
  "Estruturado e clássico, com frutos maduros, especiarias e madeira bem integrada. Acidez viva, taninos firmes e final longo. Da Toscana, pelos Frescobaldi, família com mais de 700 anos de vinho.",
  "Structured and classic, with ripe fruit, spice and well-integrated oak. Lively acidity, firm tannins and a long finish. From Tuscany, by the Frescobaldi, a family with more than 700 years in wine."),
 ("Passato Barolo DOCG", "14,5%", "44,90 €", "Barolo",
  "Complexo e poderoso, com fruta madura, cereja silvestre, especiarias e leve toque terroso. Taninos sedosos, corpo pleno e final longo. Do Piemonte, de viticultura biológica, pelas mãos de Luca Bosio.",
  "Complex and powerful, with ripe fruit, wild cherry, spice and a light earthy touch. Silky tannins, full body and a long finish. From Piedmont, organically farmed, made by Luca Bosio."),
])

B["itwhite"] = ("Vinhos Italianos · Brancos", [
 ("Donnafugata Anthilia DOC", "12,5%", "20,90 €", "Anthilia",
  "Aromático e fresco, com notas cítricas, tropicais e florais e um final leve. Da Sicília, pela Donnafugata. Anthilia era um dos nomes que os gregos antigos davam à ilha.",
  "Aromatic and fresh, with citrus, tropical and floral notes and a light finish. From Sicily, by Donnafugata. Anthilia was one of the names the ancient Greeks gave the island."),
])

B["itsp"] = ("Vinhos Italianos · Espumantes", [
 ("Bolla Exclusive Prosecco DOC", "11%", "19,90 €", "Bolla Prosecco",
  "Elegante, com maçã verde, pera e um toque floral. Bolha fina e final limpo. Do Véneto, pela Bolla, casa fundada em Soave em 1883. Brut e millesimato: seco e com uvas de uma só colheita.",
  "Elegant, with green apple, pear and a floral touch. Fine bubbles and a clean finish. From the Veneto, by Bolla, a house founded in Soave in 1883. Brut and millesimato: dry and made with grapes from a single harvest."),
])

B["glass"] = ("Vinho da Casa", [
 ("Tinto", "18cl", "3,90 €", None, None, None),
 ("Branco", "18cl", "2,90 €", None, None, None),
 ("Jarro de Branco", "1 L", "11,90 €", None, None, None),
])

B["cocktails"] = ("Cocktails", [
 ("Gin Tónica", None, "9,90 €", None,
  "Gin, tónica, limão e manjericão, com um toque de pimenta rosa. Nasceu na Índia colonial: os soldados britânicos tomavam quinino contra a malária e juntaram-lhe gin para disfarçar o amargo.",
  "Gin, tonic, lemon and basil, with a hint of pink pepper. Born in colonial India: British soldiers took quinine against malaria and added gin to mask the bitterness."),
 ("Aperol Spritz", None, "8,90 €", None,
  "Aperol, Prosecco, um toque de água com gás e rodelas de laranja. O Aperol nasceu em Pádua, no Véneto, e nos anos 1950 o spritz tornou-se o aperitivo de toda a Itália.",
  "Aperol, Prosecco, a splash of sparkling water and orange slices. Aperol was born in Padua, in the Veneto, and in the 1950s the spritz became the aperitivo of all Italy."),
 ("Amalfi Spritz", None, "8,90 €", None,
  "Limoncello, Prosecco e um toque de água com gás. O limoncello, licor feito com a casca dos limões de Amalfi, é o digestivo do sul de Itália. Aqui junta-se às bolhas do Prosecco, que vem do norte.",
  "Limoncello, Prosecco and a splash of sparkling water. Limoncello, a liqueur made from the peel of Amalfi lemons, is the digestif of southern Italy. Here it meets the bubbles of Prosecco, from the north."),
 ("Caipirinha", None, "7,90 €", None,
  "Cachaça 51, lima e açúcar. Nasceu no interior de São Paulo, no início do século XX, como remédio caseiro para a gripe, com alho e mel. O alho e o mel saíram e ficou o cocktail nacional do Brasil.",
  "Cachaça 51, lime and sugar. Born in the São Paulo countryside, in the early 20th century, as a home remedy for flu, with garlic and honey. The garlic and honey went, and Brazil's national cocktail remained."),
 ("Ginovese Spritz", None, "7,90 €", None,
  "Gin, manjericão fresco, açúcar e limão. O manjericão de Génova, o mesmo do pesto, sai da cozinha e entra no copo.",
  "Gin, fresh basil, sugar and lemon. Genoese basil, the same used in pesto, leaves the kitchen and goes into the glass."),
])

B["sangria"] = ("Sangrias", [
 ("Sangria Tinta", "165cl", "19,90 €", None,
  "Feita com vinho tinto, fruta e especiarias suaves. Da Península Ibérica, onde juntar fruta ao vinho era a forma de refrescar os dias quentes. O nome vem de &quot;sangue&quot;, pela cor do vinho.",
  "Made with red wine, fruit and gentle spices. From the Iberian Peninsula, where adding fruit to wine was the way to cool down hot days. The name comes from &quot;sangue&quot;, blood, for the colour of the wine."),
 ("Sangria Branca", "165cl", "19,90 €", None,
  "Feita com vinho branco, fruta, especiarias e um toque cítrico. A mesma tradição ibérica, com vinho branco no lugar do tinto: mais leve, cítrica e perfumada.",
  "Made with white wine, fruit, spices and a hint of citrus. The same Iberian tradition, with white wine instead of red: lighter, citrusy and fragrant."),
 ("Sangria de Frutos Vermelhos", "165cl", "22,90 €", None,
  "Feita com espumante, frutos vermelhos e um toque de hortelã e canela. A nossa versão da sangria, com espumante no lugar do vinho. Os frutos vermelhos dão a cor, a hortelã e a canela dão o aroma.",
  "Made with sparkling wine, red berries and a touch of mint and cinnamon. Our take on sangria, with sparkling wine instead of still. The red berries bring the colour, the mint and cinnamon the aroma."),
 ("Sangria Bandida", "165cl", "20,90 €", None,
  "Feita com sidra Bandida do Pomar, maçã, limão, canela e hortelã. A nossa versão da sangria com sidra portuguesa no lugar do vinho. A maçã reforça o fruto da Bandida, e a canela e a hortelã dão o aroma.",
  "Made with Bandida do Pomar cider, apple, lemon, cinnamon and mint. Our take on sangria, with Portuguese cider instead of wine. The apple brings out the fruit of the Bandida, and the cinnamon and mint bring the aroma."),
])

B["spirits"] = ("Espirituosas", [
 ("Whisky Jameson Black Barrel", None, "5,70 €", None,
  "De Dublin, onde a Jameson destila desde 1780. O Black Barrel passa por barris de bourbon duplamente tostados, que lhe dão notas de caramelo e baunilha.",
  "From Dublin, where Jameson has distilled since 1780. Black Barrel is matured in double-charred bourbon barrels, which give it notes of caramel and vanilla."),
 ("Tanqueray Gin", None, "5,90 €", None,
  "De Londres, criado em 1830 por Charles Tanqueray. Um gin seco e limpo, com zimbro, coentro, angélica e alcaçuz.",
  "From London, created in 1830 by Charles Tanqueray. A dry, clean gin with juniper, coriander, angelica and liquorice."),
 ("Vodka Smirnoff", None, "3,90 €", None,
  "De Moscovo, onde Piotr Smirnov começou a produzir em 1864. Filtrada em carvão vegetal, é hoje a vodka mais vendida do mundo.",
  "From Moscow, where Pyotr Smirnov started distilling in 1864. Charcoal-filtered, it is today the best-selling vodka in the world."),
 ("Aguardente Velha CR&amp;F Reserva", None, "4,90 €", None,
  "Aguardente portuguesa, destilada em alambique de cobre e envelhecida em madeira.",
  "Portuguese brandy, distilled in copper pot stills and aged in wood."),
 ("Cachaça 51 Pirassununga", None, "3,90 €", None,
  "De Pirassununga, no interior de São Paulo. A cachaça mais vendida do Brasil, destilada da cana fresca.",
  "From Pirassununga, in the São Paulo countryside. Brazil's best-selling cachaça, distilled from fresh sugar cane."),
])

B["aperit"] = ("Aperitivos", [
 ("Aperol", None, "3,90 €", None,
  "De Pádua, criado em 1919 pelos irmãos Barbieri. Amargo e alaranjado, com apenas 11% de álcool, feito com laranja, ruibarbo e genciana.",
  "From Padua, created in 1919 by the Barbieri brothers. Bitter and orange, with just 11% alcohol, made with orange, rhubarb and gentian."),
 ("Campari Bitter", None, "4,90 €", None,
  "De Novara, criado por Gaspare Campari em 1860. Vermelho e amargo, com uma receita que nunca foi revelada. O aperitivo de Milão.",
  "From Novara, created by Gaspare Campari in 1860. Red and bitter, with a recipe that has never been revealed. The aperitivo of Milan."),
])

B["digest"] = ("Digestivos", [
 ("Disaronno Amaretto Originale", None, "3,90 €", None,
  "De Saronno, na Lombardia. O aroma lembra amêndoa, mas a base é o caroço de damasco.",
  "From Saronno, in Lombardy. The aroma recalls almond, but it is made from apricot kernels."),
 ("Limoncello del Mediterraneo", None, "3,90 €", None,
  "Da Costa Amalfitana, feito com a casca dos limões da região. Servido bem gelado, como no sul de Itália.",
  "From the Amalfi Coast, made with the peel of the local lemons. Served ice cold, as in southern Italy."),
 ("Amaro Montenegro", None, "4,90 €", None,
  "De Bolonha, criado em 1885 e batizado em honra da princesa Elena do Montenegro. Feito com 40 ervas e botânicos.",
  "From Bologna, created in 1885 and named in honour of Princess Elena of Montenegro. Made with 40 herbs and botanicals."),
 ("Licor Beirão", None, "2,90 €", None,
  "Da Lousã, feito desde 1929 com sementes e plantas aromáticas. O licor mais vendido em Portugal.",
  "From Lousã, made since 1929 with seeds and aromatic plants. The best-selling liqueur in Portugal."),
 ("Baileys Irish Cream", None, "4,90 €", None,
  "De Dublin, criado em 1974. Natas irlandesas e whiskey, num licor que depressa conquistou o mundo.",
  "From Dublin, created in 1974. Irish cream and whiskey, in a liqueur that quickly won over the world."),
 ("Alambre Moscatel de Setúbal", None, "1,90 €", None,
  "Vinho generoso de Setúbal, doce e aromático, com mais de 500 anos de história.",
  "Fortified wine from Setúbal, sweet and aromatic, with more than 500 years of history."),
 ("Ginja", None, "1,90 €", None,
  "De Lisboa e Óbidos, onde a ginja, fruto silvestre da família da cereja, é macerada em aguardente e açúcar. Tradição portuguesa de séculos, servida muitas vezes em copos de chocolate.",
  "From Lisbon and Óbidos, where ginja, a wild sour cherry, is steeped in brandy and sugar. A centuries-old Portuguese tradition, often served in chocolate cups."),
 ("Vinho do Porto", None, "2,90 €", None,
  "Do Douro. A aguardente junta-se a meio da fermentação e guarda a doçura natural da uva. O vinho português mais famoso do mundo.",
  "From the Douro. Brandy is added halfway through fermentation, keeping the grape's natural sweetness. The most famous Portuguese wine in the world."),
 ("Bagaceira", None, "1,70 €", None,
  "Aguardente destilada do bagaço das uvas, o que fica depois de prensado o vinho. Tradição do norte de Portugal, servida no fim da refeição.",
  "A spirit distilled from grape pomace, what is left after the wine is pressed. A tradition from northern Portugal, served at the end of the meal."),
])

B["soda"] = ("Sodas Italianas", [
 ("Fragola", None, "5,90 €", None,
  "Doce e refrescante: xarope de morango, água com gás e gelo, com um toque de lima e hortelã. A soda italiana nasceu nas gelaterias do norte de Itália, onde o xarope de fruta encontrava a água gaseificada para refrescar os verões.",
  "Sweet and refreshing: strawberry syrup, sparkling water and ice, with a touch of lime and mint. The Italian soda was born in the gelaterias of northern Italy, where fruit syrup met sparkling water to cool down the summers."),
 ("Limone", None, "5,90 €", None,
  "Cítrica e vibrante: xarope de lima, água com gás e gelo, com rodela de limão e hortelã. Dos limoeiros em socalcos da Costa Amalfitana, o limão dá a esta soda o seu carácter solar.",
  "Citrusy and vibrant: lime syrup, sparkling water and ice, with a slice of lemon and mint. From the terraced lemon groves of the Amalfi Coast, lemon gives this soda its sunny character."),
 ("Melograno", None, "5,90 €", None,
  "Frutada e elegante: xarope de romã, água com gás e gelo, com um toque de lima e hortelã. Melograno é romã em italiano, símbolo de fartura em todo o Mediterrâneo.",
  "Fruity and elegant: pomegranate syrup, sparkling water and ice, with a touch of lime and mint. Melograno is Italian for pomegranate, a symbol of abundance across the Mediterranean."),
 ("Pesca", None, "5,90 €", None,
  "Suave e aveludada: néctar e xarope de pêssego, água com gás, gelo e hortelã. Inspirada no Bellini, de Veneza, mas sem álcool. Fresca, com bolhas e para qualquer hora do dia.",
  "Smooth and velvety: peach nectar and syrup, sparkling water, ice and mint. Inspired by the Bellini, from Venice, but alcohol-free. Fresh, bubbly and for any time of day."),
])

B["juice"] = ("Sumos Frescos", [
 ("Laranja", "Natural", "3,50 €", None, None, None),
 ("Limonada", "Natural", "2,90 €", None, None, None),
])

B["soft"] = ("Refrigerantes &amp; Águas", [
 ("Coca-Cola", "35cl", "2,90 €", None, None, None),
 ("Coca-Cola Zero", "35cl", "2,90 €", None, None, None),
 ("Guaraná do Brasil", "33cl", "3,20 €", None, None, None),
 ("Fuze Tea Pêssego", "30cl", "2,50 €", None, None, None),
 ("Fuze Tea Limão", "30cl", "2,50 €", None, None, None),
 ("Água Tónica", "20cl", "2,60 €", None, None, None),
 ("Pedras", "25cl", "1,60 €", None, None, None),
 ("Pedras", "75cl", "3,60 €", None, None, None),
 ("Pedras Limão", "25cl", "2,60 €", None, None, None),
 ("Água Purificada", "50cl", "1,30 €", None, None, None),
 ("Água Purificada", "70cl", "1,90 €", None, None, None),
])

B["coffee"] = ("Café", [
 ("Espresso", None, "1,20 €", None, None, None),
 ("Abatanado", None, "1,30 €", None, None, None),
])

ORDEM = ["beers", "ptred", "ptrose", "ptwhite", "itred", "itwhite", "itsp", "glass",
         "cocktails", "sangria", "spirits", "aperit", "digest", "soda", "juice",
         "soft", "coffee"]

# seccoes cujo titulo nao tem chave i18n (igual nas duas linguas)
SEM_I18N = {"cocktails", "sangria"}

TITULOS_EN = {
 "beers": "Beers & Cider",
 "ptred": "Portuguese Wines · Reds", "ptrose": "Portuguese Wines · Rosés",
 "ptwhite": "Portuguese Wines · Whites",
 "itred": "Italian Wines · Reds", "itwhite": "Italian Wines · Whites",
 "itsp": "Italian Wines · Sparkling",
 "glass": "House Wine", "spirits": "Spirits", "aperit": "Aperitifs",
 "digest": "Digestives", "soda": "Italian Sodas", "juice": "Fresh Juices",
 "soft": "Soft Drinks & Waters", "coffee": "Coffee",
}
# nomes de item que mudam em ingles
NOMES_EN = {
 "Tinto": "Red", "Branco": "White", "Jarro de Branco": "Carafe of White",
 "Sangria Tinta": "Red Sangria", "Sangria Branca": "White Sangria",
 "Sangria de Frutos Vermelhos": "Red Berries Sangria", "Sangria Bandida": "Bandida Sangria",
 "Gin Tónica": "Gin &amp; Tonic", "Laranja": "Orange", "Limonada": "Lemonade",
 "Água Tónica": "Tonic Water", "Pedras": "Pedras Sparkling Water",
 "Pedras Limão": "Pedras Sparkling Lemon", "Água Purificada": "Purified Water",
 "Guaraná do Brasil": "Brazilian Guaraná", "Fuze Tea Pêssego": "Fuze Tea Peach",
 "Fuze Tea Limão": "Fuze Tea Lemon", "Vinho do Porto": "Port Wine",
 "Abatanado": "Abatanado (Americano)", "Café": "Coffee",
 "Whisky Jameson Black Barrel": "Jameson Black Barrel Whiskey",
 "Vodka Smirnoff": "Smirnoff Vodka",
 "Aguardente Velha CR&amp;F Reserva": "Aguardente Velha CR&amp;F Reserva",
}
# metas que mudam em ingles
META_EN = {
 "30cl · imperial": "30cl · draught", "40cl · caneca": "40cl · tankard",
 "25cl · imperial": "25cl · draught", "50cl · caneca": "50cl · tankard",
 "33cl · garrafa": "33cl · bottle", "Natural": "Freshly squeezed",
}

# seccoes de vinho: cada item leva a foto da garrafa recortada
COM_GARRAFA = {"ptred", "ptrose", "ptwhite", "itred", "itwhite", "itsp"}
GARRAFAS = Path("/Users/fellipefranchin/dev/sites/vívono/assets/img/vinhos")
# seccoes cujos itens levam foto quadrada, quando ela existe
COM_FOTO = {"cocktails", "sangria", "soda", "juice", "soft"}
FOTOS_BEB = Path("/Users/fellipefranchin/dev/sites/vívono/assets/img/bebidas")


def slug(nome):
    s = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


en_dict = []


def esc(s):
    return s.replace("\\", "\\\\").replace("'", "\\'")


def item_html(sec, i, dados):
    nome, meta, preco, curto, desc, desc_en = dados
    key = f"b.{sec}{i}"
    nome_html = nome
    if nome in NOMES_EN and NOMES_EN[nome] != nome:
        nome_html = f'<span data-i18n="{key}.n">{nome}</span>'
        en_dict.append(f"'{key}.n':'{esc(NOMES_EN[nome])}'")
    meta_html = ""
    if meta:
        if meta in META_EN:
            meta_html = f'<span class="beb-meta" data-i18n="{key}.m">{meta}</span>'
            en_dict.append(f"'{key}.m':'{esc(META_EN[meta])}'")
        else:
            meta_html = f'<span class="beb-meta">{meta}</span>'
    garrafa = ""
    if sec in COM_GARRAFA:
        f = slug(nome)
        if (GARRAFAS / f"{f}.png").exists():
            garrafa = (f'<div class="beb-bottle"><img src="assets/img/vinhos/{f}.png" '
                       f'alt="Garrafa de {nome}" loading="lazy" decoding="async"></div>')
        else:
            raise SystemExit(f"falta a foto da garrafa: {nome} ({f}.png)")
    elif sec in COM_FOTO:
        # o tamanho so entra no nome quando e preciso distinguir (Pedras 25cl / 75cl)
        for cand in ([slug(f"{nome} {meta}")] if meta else []) + [slug(nome)]:
            if (FOTOS_BEB / f"{cand}.jpg").exists():
                garrafa = (f'<div class="beb-thumb"><img src="assets/img/bebidas/{cand}.jpg" '
                           f'alt="{nome}" loading="lazy" decoding="async"></div>')
                break

    corpo = (f'<div class="beb-top"><div class="beb-name">{nome_html}'
             f'{meta_html}</div><div class="beb-dots"></div><div class="beb-price">{preco}</div></div>')
    if desc:
        corpo += f'<div class="beb-desc" data-i18n="{key}.d">{desc}</div>'
        en_dict.append(f"'{key}.d':'{esc(desc_en)}'")
    if curto and curto in HPT:
        pt = " · ".join(HPT[curto][:MAX_HARM])
        en = " · ".join(HEN[curto][:MAX_HARM])
        corpo += f'<div class="beb-harm" data-i18n="{key}.h"><b>Harmoniza</b> · {pt}</div>'
        en_dict.append(f"'{key}.h':'<b>Pairs with</b> · {esc(en)}'")

    if garrafa:
        return f'<div class="beb-item beb-wine">{garrafa}<div class="beb-txt">{corpo}</div></div>'
    return f'<div class="beb-item">{corpo}</div>'


def main():
    partes = []
    for sec in ORDEM:
        titulo, itens = B[sec]
        if sec in SEM_I18N:
            h3 = f"<h3>{titulo}</h3>"
        else:
            h3 = f'<h3 data-i18n="b.h.{sec}">{titulo}</h3>'
            en_dict.append(f"'b.h.{sec}':'{esc(TITULOS_EN[sec])}'")
        corpo = "".join(item_html(sec, i + 1, d) for i, d in enumerate(itens))
        partes.append(f'<div class="beb-block reveal">{h3}<div class="beb-rule"></div>'
                      f'<div class="beb-grid">{corpo}</div></div>')

    linhas = HTML.read_text(encoding="utf-8").split("\n")

    # a linha das bebidas pode comecar pelo bloco da Selecao Especial, que fica como esta
    alvo = [i for i, l in enumerate(linhas) if '<div class="beb-block reveal">' in l]
    assert len(alvo) == 1, f"linha das bebidas: {len(alvo)} candidatas"
    i = alvo[0]
    prefixo = linhas[i][:linhas[i].index('<div class="beb-block reveal">')]
    linhas[i] = prefixo + "".join(partes)

    # bloco EN: tudo entre 'b.eyebrow' e 'b.footnote', preservando as duas pontas
    ini = next(i for i, l in enumerate(linhas) if "'b.eyebrow'" in l)
    fim = next(i for i, l in enumerate(linhas) if "'b.footnote'" in l)
    # guardar as entradas que nao sao deste gerador (titulo, subtitulo, legenda do hero).
    # Tem de ser entrada a entrada e nao linha a linha: uma linha pode misturar as duas coisas.
    geradas = {re.match(r"'([^']+)'", e).group(1) for e in en_dict}
    cabeca = []
    for l in linhas[ini:fim]:
        for entrada in re.findall(r"'[a-zA-Z0-9._]+':'(?:[^'\\]|\\.)*'", l):
            chave = re.match(r"'([^']+)'", entrada).group(1)
            if chave not in geradas:
                cabeca.append("    " + entrada + ",")
    novas = []
    for j in range(0, len(en_dict), 3):
        novas.append("    " + ",".join(en_dict[j:j + 3]) + ",")
    linhas[ini:fim] = cabeca + novas

    HTML.write_text("\n".join(linhas), encoding="utf-8")
    total = sum(len(B[s][1]) for s in ORDEM)
    print(f"bebidas: {len(ORDEM)} blocos · {total} itens · {len(en_dict)} chaves EN")


if __name__ == "__main__":
    main()
