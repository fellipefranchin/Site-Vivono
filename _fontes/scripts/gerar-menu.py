#!/usr/bin/env python3
"""Reescreve a secção do Menu no index.html a partir da ementa de 2026.11.02.

Gera o bloco dos quatro separadores (linha única, como já estava) e o bloco de
chaves EN do menu, preservando as chaves allg.* e menu.tab.* que lá estavam.
"""
import re
from pathlib import Path

HTML = Path("/Users/fellipefranchin/dev/sites/vívono/index.html")

# key, nome PT, nome EN (None = igual), alergénios, preço, destaque ◆, foto
# desc PT, desc EN, história PT, história EN, harmoniza PT (None = sem linha)
D = [
 # ---------------- PASTA ----------------
 ("m.p1", "Lasagna al Ragù", None, "1,3,7,9,12", "14,90 €", True, "lasagna-al-ragu",
  "Sete camadas de massa fresca e seis de ragù de carne cozinhado lentamente, molho de tomate e Grana Padano gratinado no forno.",
  "Seven layers of fresh pasta and six of slow-cooked meat ragù, tomato sauce and Grana Padano gratinated in the oven.",
  "De Bolonha, na Emília-Romanha, onde a lasanha ao forno é o almoço de domingo há gerações. Paciência em camadas: o ragù apura durante horas antes de chegar ao prato.",
  "From Bologna, in Emilia-Romagna, where baked lasagne has been Sunday lunch for generations. Patience in layers: the ragù simmers for hours before it reaches the plate.",
  "Contador de Estórias · Cecchi Chianti"),
 ("m.p2", "Gnocchi al Pomodoro", None, "1,3,7", "12,90 €", False, "gnocchi-al-pomodoro",
  "Gnocchi de batata feitos na casa, molho de tomate e Grana Padano.",
  "House-made potato gnocchi, tomato sauce and Grana Padano.",
  "Em Roma diz-se &quot;giovedì gnocchi&quot;: quinta-feira é dia de gnocchi. A batata chegou tarde à cozinha italiana, mas foi nela que ganhou a sua forma mais delicada.",
  "In Rome they say &quot;giovedì gnocchi&quot;: Thursday is gnocchi day. The potato came late to Italian cooking, but it was there that it took its most delicate form.",
  "Cecchi Chianti · Montado Rosé"),
 ("m.p3", "Gnocchi ai Quattro Formaggi", None, "1,3,7", "13,90 €", False, "gnocchi-ai-quattro-formaggi",
  "Gnocchi de batata feitos na casa, num molho de nata fresca com Gorgonzola, Grana Padano, queijo tipo catupiry e Feta.",
  "House-made potato gnocchi in a fresh cream sauce with Gorgonzola, Grana Padano, catupiry-style cheese and Feta.",
  "Do norte de Itália, onde os queijos de pasta mole e os curados se encontram à mesa. O catupiry é o nosso sotaque brasileiro no molho.",
  "From northern Italy, where soft and cured cheeses meet at the table. The catupiry is our Brazilian accent in the sauce.",
  "Crasto Branco · Arinto"),

 # ---------------- ENTRADAS ----------------
 ("m.e1", "Azeitonas Marinadas", "Marinated Olives", None, "1,90 €", False, "azeitonas-marinadas",
  "Azeitonas verdes marinadas em azeite, vegetais, ervas mediterrânicas e um toque cítrico.",
  "Green olives marinated in olive oil, vegetables, Mediterranean herbs and a hint of citrus.",
  "No Mediterrâneo, a oliveira é sagrada desde a Antiguidade. Na Roma Antiga, já eram as azeitonas a abrir os banquetes.",
  "Around the Mediterranean, the olive tree has been sacred since Antiquity. In Ancient Rome, olives were already opening the banquets.",
  None),
 ("m.e2", "Queijo Curado", "Cured Cheese", "7", "4,90 €", False, "queijo-curado",
  "Fatias de queijo português curado.",
  "Slices of cured Portuguese cheese.",
  "Em Portugal, pôr queijo na mesa é a primeira forma de receber quem chega. Escolhemos um curado português para abrir o apetite.",
  "In Portugal, putting cheese on the table is the first way to welcome a guest. We chose a cured Portuguese cheese to whet the appetite.",
  None),
 ("m.e3", "Pão de Alho", "Garlic Bread", "1,7", "5,90 €", True, "pao-de-alho",
  "Pão artesanal servido com pasta de ricotta, alho confitado e Mozzarella Fior di Latte.",
  "Artisan bread served with ricotta spread, garlic confit and Mozzarella Fior di Latte.",
  "Feito com a mesma massa de longa fermentação das nossas pizzas, acabado de sair do forno a lenha.",
  "Made with the same long-fermented dough as our pizzas, straight from the wood-fired oven.",
  None),
 ("m.e4", "Crostini", None, "1,7,8", "9,40 €", False, "crostini",
  "Crostini com alecrim, servidos com pesto de pistache, pesto rosso e caponata.",
  "Rosemary crostini, served with pistachio pesto, pesto rosso and caponata.",
  "Na Toscana, o pão torrado com o que houvesse em casa era o petisco do campo. Hoje é a forma italiana de abrir a refeição.",
  "In Tuscany, toasted bread topped with whatever was at home was the countryside snack. Today it is the Italian way to open a meal.",
  None),
 ("m.e5", "Di Andria", None, "1,7", "11,90 €", True, "di-andria",
  "Burrata assada com tomate cherry e manjericão, servida com crostini artesanal.",
  "Baked burrata with cherry tomatoes and basil, served with artisan crostini.",
  "Andria, na Puglia, é a terra da burrata. No forno, o interior de stracciatella fica ainda mais cremoso.",
  "Andria, in Puglia, is the home of burrata. In the oven, its stracciatella heart becomes even creamier.",
  None),
 ("m.e6", "Insalata Vívono", None, "7,12", "9,90 €", False, "insalata-vivono",
  "Mix de folhas, grão-de-bico, pimento, beringela e courgette assados, cebola roxa, tomate cherry, azeitonas e lascas de Grana Padano, finalizada com azeite extravirgem e vinagre balsâmico.",
  "Mixed leaves, chickpeas, roasted peppers, aubergine and courgette, red onion, cherry tomatoes, olives and Grana Padano shavings, finished with extra virgin olive oil and balsamic vinegar.",
  "O balsâmico vem de Módena, onde se faz há séculos. É ele que dá à salada o ponto certo entre o doce e o ácido.",
  "The balsamic comes from Modena, where it has been made for centuries. It gives the salad the right balance between sweet and sour.",
  None),

 # ---------------- AS BRASILEIRAS ----------------
 ("m.b1", "Brasiliana", None, "1,7", "14,90 €", True, "brasiliana",
  "Molho San Marzano, Mozzarella Fior di Latte, frango desfiado e queijo tipo catupiry, finalizada com orégano e azeite extravirgem.",
  "San Marzano sauce, Mozzarella Fior di Latte, shredded chicken and catupiry-style cheese, finished with oregano and extra virgin olive oil.",
  "Frango com catupiry é a combinação preferida dos brasileiros. Na Vívono, vai à massa napolitana e ao forno a lenha.",
  "Chicken with catupiry is Brazil's favourite combination. At Vívono, it goes on Neapolitan dough and into the wood-fired oven.",
  None),
 ("m.b2", "Brasiliana Più", None, "1,7", "15,90 €", False, "brasiliana-piu",
  "Molho San Marzano, Mozzarella Fior di Latte, frango desfiado, queijo tipo catupiry e bacon, finalizada com orégano e azeite extravirgem.",
  "San Marzano sauce, Mozzarella Fior di Latte, shredded chicken, catupiry-style cheese and bacon, finished with oregano and extra virgin olive oil.",
  "A nossa Brasiliana com bacon estaladiço por cima, que junta ao frango e ao queijo cremoso um toque fumado.",
  "Our Brasiliana topped with crispy bacon, adding a smoky touch to the chicken and creamy cheese.",
  None),
 ("m.b3", "Calabrese", None, "1,7", "13,90 €", False, "calabrese",
  "Molho San Marzano, Mozzarella Fior di Latte, calabresa brasileira e cebola.",
  "San Marzano sauce, Mozzarella Fior di Latte, Brazilian calabresa sausage and onion.",
  "Não há pizzaria no Brasil sem ela. Calabresa fatiada e cebola, uma tradição com gerações.",
  "There is no pizzeria in Brazil without it. Sliced calabresa and onion, a tradition that goes back generations.",
  None),
 ("m.b4", "Paulistana", None, "1,7", "15,90 €", False, "paulistana",
  "Molho San Marzano, Mozzarella Fior di Latte, calabresa brasileira, cebola e queijo tipo catupiry.",
  "San Marzano sauce, Mozzarella Fior di Latte, Brazilian calabresa sausage, onion and catupiry-style cheese.",
  "Em São Paulo, a capital brasileira da pizza, calabresa com queijo cremoso é pedido certo em qualquer mesa. Aqui, em massa napolitana e no forno a lenha.",
  "In São Paulo, Brazil's pizza capital, calabresa with creamy cheese is ordered at every table. Here, on Neapolitan dough and from the wood-fired oven.",
  None),
 ("m.b5", "Lusitana", None, "1,3,7", "13,70 €", False, "lusitana",
  "Molho San Marzano, Mozzarella Fior di Latte, fiambre, cebola, ovo e azeitonas.",
  "San Marzano sauce, Mozzarella Fior di Latte, ham, onion, egg and olives.",
  "Nasceu em São Paulo, pelas mãos de pizzaiolos italianos, e o nome é uma homenagem aos portugueses. Em Mafra, regressa à terra que lhe deu o nome.",
  "Created in São Paulo by Italian pizzaioli, its name pays tribute to the Portuguese. In Mafra, it returns to the land that gave it its name.",
  None),
 ("m.b6", "Mineira", None, "1,3,7", "13,90 €", False, "mineira",
  "Molho San Marzano, Mozzarella Fior di Latte, bacon, ovo cozido e orégano.",
  "San Marzano sauce, Mozzarella Fior di Latte, bacon, boiled egg and oregano.",
  "Uma homenagem a Minas Gerais, terra da cozinha de fogão a lenha, onde bacon e ovo nunca faltam à mesa.",
  "A tribute to Minas Gerais, land of wood-stove cooking, where bacon and eggs are always on the table.",
  None),

 # ---------------- SELEÇÃO VÍVONO ----------------
 ("m.s1", "Vívono", None, "1,7,8", "14,90 €", True, "vivono",
  "Molho San Marzano, stracciatella, pesto de pistache artesanal, tomate cherry e folhas de manjericão.",
  "San Marzano sauce, stracciatella, artisan pistachio pesto, cherry tomatoes and basil leaves.",
  "A nossa releitura da Margherita de Nápoles: stracciatella no lugar da mozzarella, pesto de pistache e tomate cherry a reforçar o molho. É a pizza que leva o nome da casa.",
  "Our take on the Neapolitan Margherita: stracciatella instead of mozzarella, with pistachio pesto and cherry tomatoes to lift the sauce. The pizza that bears the name of the house.",
  None),
 ("m.s2", "Parma Grana", None, "1,7", "16,90 €", False, "parma-grana",
  "Molho San Marzano, Mozzarella Fior di Latte, Prosciutto di Parma, Grana Padano, geleia de figo e rúcula.",
  "San Marzano sauce, Mozzarella Fior di Latte, Prosciutto di Parma, Grana Padano, fig jam and rocket.",
  "O Prosciutto di Parma, o presunto mais famoso de Itália, ao lado do Grana Padano do vale do Pó: o melhor do norte numa só pizza. A geleia de figo dá o contraponto doce.",
  "Prosciutto di Parma, Italy's most famous ham, alongside Grana Padano from the Po Valley: the best of the north on one pizza. The fig jam adds a sweet counterpoint.",
  None),
 ("m.s3", "Parmatella", None, "1,7,8", "16,90 €", False, "parmatella",
  "Mozzarella Fior di Latte, Prosciutto di Parma, stracciatella, pistache torrado, pesto de pistache artesanal e folhas de manjericão.",
  "Mozzarella Fior di Latte, Prosciutto di Parma, stracciatella, toasted pistachio, artisan pistachio pesto and basil leaves.",
  "Parma e stracciatella num só nome: o presunto curado apenas com sal e tempo encontra a cremosidade da Puglia, e o pistache une os dois.",
  "Parma and stracciatella in a single name: ham cured with nothing but salt and time meets the creaminess of Puglia, and the pistachio brings them together.",
  None),
 ("m.s4", "Prosciutto e Funghi", None, "1,7", "14,70 €", True, "prosciutto-e-funghi",
  "Molho San Marzano, Mozzarella Fior di Latte, prosciutto cotto e cogumelos.",
  "San Marzano sauce, Mozzarella Fior di Latte, prosciutto cotto and mushrooms.",
  "Um clássico das trattorias italianas, de norte a sul. Fiambre italiano e cogumelos, uma combinação que nunca passa de moda.",
  "A classic of Italian trattorias, from north to south. Italian ham and mushrooms, a combination that never goes out of style.",
  None),
 ("m.s5", "Tropicale", None, "1,7", "13,90 €", False, "tropicale",
  "Molho San Marzano, Mozzarella Fior di Latte, fiambre, ananás e cogumelos.",
  "San Marzano sauce, Mozzarella Fior di Latte, ham, pineapple and mushrooms.",
  "O ananás chegou à pizza no Canadá, em 1962, e divide opiniões desde então. Aqui, os cogumelos equilibram o doce.",
  "Pineapple first landed on pizza in Canada, in 1962, and has divided opinion ever since. Here, the mushrooms balance the sweetness.",
  None),
 ("m.s6", "Porcellina", None, "1,7", "12,70 €", False, "porcellina",
  "Molho San Marzano, Mozzarella Fior di Latte, bacon e cebola.",
  "San Marzano sauce, Mozzarella Fior di Latte, bacon and onion.",
  "Porcellina quer dizer porquinha, em italiano. Uma homenagem ao porco, que a Emília-Romanha transformou em arte com os seus enchidos.",
  "Porcellina means little pig in Italian. A tribute to the pig, which Emilia-Romagna turned into an art with its cured meats.",
  None),
 ("m.s7", "Puttanesca", None, "1,4,7", "14,90 €", False, "puttanesca",
  "Molho San Marzano, Grana Padano, alho, anchovas, alcaparras, tomate cherry, pimenta preta, manjericão e orégano.",
  "San Marzano sauce, Grana Padano, garlic, anchovies, capers, cherry tomatoes, black pepper, basil and oregano.",
  "A versão em pizza da pasta alla puttanesca, de Nápoles. Diz-se que o molho nasceu numa noite com pouco tempo e pouca coisa na despensa: alho, anchovas, alcaparras e tomate.",
  "The pizza version of pasta alla puttanesca, from Naples. The sauce is said to have been born one night with little time and little in the pantry: garlic, anchovies, capers and tomato.",
  None),
 ("m.s8", "Piemontese", None, "1,7", "15,90 €", True, "piemontese",
  "Mozzarella Fior di Latte, ricotta com molho de trufas, cebola caramelizada, cogumelos, azeite trufado, Grana Padano e folhas de manjericão.",
  "Mozzarella Fior di Latte, ricotta with truffle sauce, caramelised onion, mushrooms, truffle oil, Grana Padano and basil leaves.",
  "O Piemonte é a terra das trufas, e esta pizza é a nossa homenagem: molho de trufas, azeite trufado, cogumelos e a doçura da cebola caramelizada. A mais sofisticada da casa.",
  "Piedmont is the land of truffles, and this pizza is our tribute: truffle sauce, truffle oil, mushrooms and the sweetness of caramelised onion. The most refined pizza in the house.",
  None),
 ("m.s9", "Giardino", None, "1,7", "10,90 €", False, "giardino",
  "Molho San Marzano, Mozzarella Fior di Latte, tomate cherry, courgette e beringela assadas e rúcula.",
  "San Marzano sauce, Mozzarella Fior di Latte, cherry tomatoes, roasted courgette and aubergine, and rocket.",
  "Do sul de Itália, onde a horta manda na cozinha: tomate cherry, courgette e beringela assadas no forno a lenha e rúcula fresca. Vegetariana de raiz.",
  "From southern Italy, where the vegetable garden rules the kitchen: cherry tomatoes, courgette and aubergine roasted in the wood-fired oven, and fresh rocket. Vegetarian at heart.",
  None),

 # ---------------- CLÁSSICAS ----------------
 ("m.c1", "Margherita", None, "1,7", "10,90 €", False, "margherita",
  "Molho San Marzano, Mozzarella Fior di Latte e folhas de manjericão.",
  "San Marzano sauce, Mozzarella Fior di Latte and basil leaves.",
  "Diz-se que foi criada em Nápoles, em 1889, para a Rainha Margherita de Saboia, com as cores da bandeira italiana. É a prova de fogo de qualquer pizzaiolo.",
  "It is said to have been created in Naples, in 1889, for Queen Margherita of Savoy, in the colours of the Italian flag. The true test of any pizzaiolo.",
  None),
 ("m.c2", "4 Formaggi", None, "1,7", "13,90 €", False, "4-formaggi",
  "Mozzarella Fior di Latte, Grana Padano, Gorgonzola, Feta, mel e folhas de manjericão.",
  "Mozzarella Fior di Latte, Grana Padano, Gorgonzola, Feta, honey and basil leaves.",
  "Não pertence a nenhuma região de Itália e é pedida em todas. Na nossa, um fio de mel equilibra o sal dos queijos.",
  "It belongs to no region of Italy and is ordered in all of them. In our version, a drizzle of honey balances the saltiness of the cheeses.",
  None),
 ("m.c3", "5 Formaggi", None, "1,7", "15,90 €", False, "5-formaggi",
  "Molho San Marzano, Mozzarella Fior di Latte, Grana Padano, Gorgonzola, Feta e queijo tipo catupiry.",
  "San Marzano sauce, Mozzarella Fior di Latte, Grana Padano, Gorgonzola, Feta and catupiry-style cheese.",
  "A 4 Formaggi com sotaque brasileiro: entra o molho de tomate e o catupiry junta-se à mesa como o quinto queijo.",
  "The 4 Formaggi with a Brazilian accent: tomato sauce comes in, and catupiry joins the table as the fifth cheese.",
  None),
 ("m.c4", "Pepperoni", None, "1,7", "12,70 €", False, "pepperoni",
  "Molho San Marzano, Mozzarella Fior di Latte e pepperoni.",
  "San Marzano sauce, Mozzarella Fior di Latte and pepperoni.",
  "Nasceu nos Estados Unidos, pelas mãos dos imigrantes italianos, no início do século XX. Hoje é um clássico em qualquer pizzaria.",
  "Born in the United States, at the hands of Italian immigrants, in the early 20th century. Today it is a classic in every pizzeria.",
  None),
 ("m.c5", "Fiambre", "Ham", "1,7", "12,70 €", False, "fiambre",
  "Molho San Marzano, Mozzarella Fior di Latte e fiambre.",
  "San Marzano sauce, Mozzarella Fior di Latte and ham.",
  "Simples, direto e sem pretensões: a pizza que agrada a todas as gerações.",
  "Simple, honest and unpretentious: the pizza every generation enjoys.",
  None),
 ("m.c6", "Diavola", None, "1,7", "13,70 €", True, "diavola",
  "Molho San Marzano, Mozzarella Fior di Latte, salame picante, &#x27;Nduja e cebola roxa.",
  "San Marzano sauce, Mozzarella Fior di Latte, spicy salami, &#x27;Nduja and red onion.",
  "Diavola quer dizer diabólica. A &#x27;Nduja, enchido picante e cremoso da Calábria, traz o fogo que dá nome à pizza.",
  "Diavola means devilish. &#x27;Nduja, the spicy, spreadable sausage from Calabria, brings the fire that gives the pizza its name.",
  None),

 # ---------------- BAMBINO ----------------
 ("m.ba1", "Margherita", None, "1,7", "8,70 €", False, "bambino-margherita",
  "Molho San Marzano, Mozzarella Fior di Latte e manjericão.",
  "San Marzano sauce, Mozzarella Fior di Latte and basil.",
  "A pizza mais famosa do mundo, no tamanho certo para os maiores apreciadores da mesa.",
  "The most famous pizza in the world, in just the right size for the biggest fans at the table.",
  None),
 ("m.ba2", "Fiambre", "Ham", "1,7", "9,20 €", False, "bambino-fiambre",
  "Molho San Marzano, Mozzarella Fior di Latte e fiambre.",
  "San Marzano sauce, Mozzarella Fior di Latte and ham.",
  "O fiambre que toda a gente adora, numa pizza feita à medida. Pequena no tamanho, grande no sabor.",
  "The ham everyone loves, on a pizza made to measure. Small in size, big on flavour.",
  None),

 # ---------------- DOLCE · pizzas doces ----------------
 ("m.d1", "Nutella", None, "1,6,7,8", "7,80 €", False, "nutella",
  "Nutella, cacau em pó e avelã torrada.",
  "Nutella, cocoa powder and toasted hazelnuts.",
  "De Turim, capital do chocolate italiano, onde no século XIX se juntou avelã ao chocolate e nasceu a gianduia. A Nutella é a sua herdeira direta.",
  "From Turin, Italy's chocolate capital, where in the 19th century hazelnut was added to chocolate and gianduja was born. Nutella is its direct heir.",
  None),
 ("m.d2", "Pistachio", None, "1,7,8", "9,90 €", False, "pistachio",
  "Creme de pistache e pistache torrado.",
  "Pistachio cream and toasted pistachio.",
  "Da Sicília, onde o pistache cresce em solo vulcânico, nas encostas do Etna. O de Bronte, o &quot;ouro verde da Sicília&quot;, tem DOP desde 2009.",
  "From Sicily, where pistachios grow in volcanic soil on the slopes of Etna. Bronte pistachio, the &quot;green gold of Sicily&quot;, has held PDO status since 2009.",
  None),

 # ---------------- DOLCE · sobremesas ----------------
 ("m.d3", "Tiramisù Vívono", None, "1,3,7,8", "5,90 €", True, "tiramisu",
  "Creme de pistache com mascarpone, zabaione e biscoitos Savoiardi embebidos em café, finalizado com cacau em pó e pistache torrado.",
  "Pistachio cream with mascarpone, zabaione and Savoiardi biscuits soaked in coffee, finished with cocoa powder and toasted pistachio.",
  "Nasceu em Treviso, no Véneto, nos anos 1960. Tiramisù quer dizer &quot;levanta-me&quot;. A nossa versão leva pistache, a assinatura da casa.",
  "Born in Treviso, in the Veneto, in the 1960s. Tiramisù means &quot;pick me up&quot;. Our version is made with pistachio, the signature of the house.",
  None),
 ("m.d4", "Brownie", None, "1,3,7", "5,90 €", False, "brownie",
  "Brownie artesanal de chocolate, servido com calda de chocolate e gelato de baunilha.",
  "Artisan chocolate brownie, served with chocolate sauce and vanilla gelato.",
  "Porque nem tudo tem de ser italiano: o brownie nasceu em Chicago, no fim do século XIX. O gelato, esse, é italiano.",
  "Because not everything has to be Italian: the brownie was born in Chicago in the late 19th century. The gelato, however, is Italian.",
  None),
 ("m.d5", "Pudim", None, "3,7", "4,70 €", False, "pudim",
  "Sobremesa cremosa à base de leite condensado, ovos e leite, coberta com calda de caramelo.",
  "Creamy dessert made with condensed milk, eggs and milk, topped with caramel sauce.",
  "De Portugal e do Brasil ao mesmo tempo: o pudim de leite condensado brasileiro nasceu do pudim de ovos português. Duas tradições na mesma colher.",
  "From Portugal and Brazil at once: the Brazilian condensed milk pudim was born from the Portuguese egg pudim. Two traditions in the same spoon.",
  None),
 ("m.d6", "Gelato", None, "7", "3,70 €", False, "gelato",
  "Gelato artesanal italiano. Pergunte pelos sabores disponíveis.",
  "Artisan Italian gelato. Ask about the flavours available.",
  "Da corte florentina dos Médici, onde nasceu no século XVI. Menos ar, mais sabor, como manda a tradição italiana.",
  "Born at the Florentine court of the Medici, in the 16th century. Less air, more flavour, as Italian tradition demands.",
  None),
]

IDX = {d[0]: d for d in D}

# subtítulo de cada separador (PT, EN)
TAGS = {
 "pasta":   ("Feitos na casa, com massa fresca e o tempo que cada receita pede",
             "Made in house, with fresh pasta and the time each recipe calls for"),
 "entradas":("Para começar com leveza e já saber que não vai ficar por aqui",
             "A light start, knowing full well it won't end here"),
 "pizzas":  ("Massa de longa fermentação, assada em forno a lenha",
             "Long-fermented dough, baked in a wood-fired oven"),
 "dolce":   ("Porque algumas coisas na vida são pura paixão, e a sobremesa é uma delas",
             "Because some things in life are pure passion, and dessert is one of them"),
}

# grupos dentro de um separador: (chave i18n do título, título PT, título EN, nota PT, nota EN, [chaves])
GRUPOS_PIZZAS = [
 ("brasileiras", "As Brasileiras", "From Brazil",
  "A alma brasileira no forno napolitano",
  "The Brazilian soul in the Neapolitan oven",
  ["m.b1","m.b2","m.b3","m.b4","m.b5","m.b6"]),
 ("selecao", "Seleção Vívono", "Vívono Selection",
  "As combinações que contam a nossa história, uma fatia de cada vez",
  "The combinations that tell our story, one slice at a time",
  ["m.s1","m.s2","m.s3","m.s4","m.s5","m.s6","m.s7","m.s8","m.s9"]),
 ("classicas", "Clássicas", "Classics",
  "As de sempre, como devem ser, mas com um toque Vívono",
  "The timeless ones, as they should be, with a Vívono touch",
  ["m.c1","m.c2","m.c3","m.c4","m.c5","m.c6"]),
 ("bambino", "Bambino", "Bambino",
  "Para os pequenos da casa. Porque toda a grande história começa pequena",
  "For our youngest guests. Because every great story starts small",
  ["m.ba1","m.ba2"]),
]
GRUPOS_DOLCE = [
 ("doces", "Pizzas Doces", "Sweet Pizzas", None, None, ["m.d1","m.d2"]),
 ("sobremesas", "Sobremesas", "Desserts", None, None, ["m.d3","m.d4","m.d5","m.d6"]),
]

ALT = {  # texto alternativo da foto, em português
 "m.p1":"Lasagna al Ragù", "m.p2":"Gnocchi al Pomodoro", "m.p3":"Gnocchi ai Quattro Formaggi",
}


def alt_de(d):
    key, nome = d[0], d[1]
    if key.startswith("m.b") and not key.startswith("m.ba"): return f"Pizza {nome}"
    if key.startswith("m.s") or key.startswith("m.c"): return f"Pizza {nome}"
    if key.startswith("m.ba"): return f"Pizza Bambino {nome}"
    return nome


def prato(key):
    (_, nome, nome_en, allg, preco, fav, foto, desc, _de, hist, _he, harm) = IDX[key]
    nome_html = (f'<span data-i18n="{key}.n">{nome}</span>' if nome_en else nome)
    fav_html = '<span class="fav" title="Recomendação da casa">◆</span>' if fav else ''
    allg_html = f'<span class="allg">{allg}</span>' if allg else ''
    foto_html = (f'<div class="dish-ph"><img src="assets/img/menu/{foto}.jpg" '
                 f'alt="{alt_de(IDX[key])}" loading="lazy" decoding="async"></div>')
    harm_html = (f'<div class="dish-harm" data-i18n="{key}.h"><b>Harmoniza</b> · {harm}</div>'
                 if harm else '')
    return (f'<div class="dish">{foto_html}<div class="dish-top">'
            f'<div class="dish-name">{nome_html}{fav_html}{allg_html}</div>'
            f'<div class="dish-price">{preco}</div></div>'
            f'<div class="dish-desc" data-i18n="{key}.d">{desc}</div>'
            f'<div class="dish-story" data-i18n="{key}.s">{hist}</div>{harm_html}</div>')


def grelha(keys):
    return '<div class="menu-grid">' + ''.join(prato(k) for k in keys) + '</div>'


def grupo(g):
    chave, pt, _en, nota_pt, _nota_en, _keys = g
    nota = (f'<p class="mg-note" data-i18n="menu.g.{chave}">{nota_pt}</p>' if nota_pt else '')
    return (f'<div class="menu-group reveal"><h3 data-i18n="menu.tab.{chave}">{pt}</h3>'
            f'<div class="mg-rule"></div>{nota}</div>')


def construir_html():
    out = []

    # --- PASTA ---
    tpt, ten = TAGS["pasta"]
    out.append(f'<div class="menu-cat active" id="mc-pasta" data-tag="{tpt}" data-tag-en="{ten}">')
    out.append('<div class="menu-hero reveal"><div class="mh-inner">'
               '<img src="assets/img/menu-pasta.jpg" alt="Gnocchi al Pomodoro e Gnocchi ai '
               'Quattro Formaggi na mesa da Vívono" loading="lazy"></div></div>')
    out.append('<div class="menu-note reveal">'
               '<h4 data-i18n="menu.pasta.h">Pasta fresca ao fim de semana</h4>'
               '<p data-i18n="menu.pasta.p">A nossa Lasagna al Ragù e os gnocchi de batata são '
               'feitos na casa, com massa fresca e o tempo que cada receita pede. Para os servir '
               'sempre no seu melhor, preparamo-los apenas ao fim de semana. Pergunte à nossa '
               'equipa o que preparámos hoje.</p></div>')
    out.append(grelha(["m.p1","m.p2","m.p3"]))
    out.append('</div>')

    # --- ENTRADAS ---
    tpt, ten = TAGS["entradas"]
    out.append(f'<div class="menu-cat" id="mc-entradas" data-tag="{tpt}" data-tag-en="{ten}">')
    out.append(grelha(["m.e1","m.e2","m.e3","m.e4","m.e5","m.e6"]))
    out.append('</div>')

    # --- PIZZAS ---
    tpt, ten = TAGS["pizzas"]
    out.append(f'<div class="menu-cat" id="mc-pizzas" data-tag="{tpt}" data-tag-en="{ten}">')
    for g in GRUPOS_PIZZAS:
        out.append(grupo(g))
        out.append(grelha(g[5]))
    out.append('</div>')

    # --- DOLCE ---
    tpt, ten = TAGS["dolce"]
    out.append(f'<div class="menu-cat" id="mc-dolce" data-tag="{tpt}" data-tag-en="{ten}">')
    for g in GRUPOS_DOLCE:
        out.append(grupo(g))
        out.append(grelha(g[5]))
    out.append('</div>')

    return ''.join(out)


def esc(s):
    return s.replace("\\", "\\\\").replace("'", "\\'")


def construir_en(linhas_antigas):
    """Bloco EN do menu. Reaproveita as chaves allg.* e menu.* que não são de prato."""
    guardar = []
    for ln in linhas_antigas:
        chaves = re.findall(r"'([a-zA-Z0-9._]+)':", ln)
        if chaves and all(k.startswith('allg.') or k in ('menu.eyebrow','menu.title','menu.sub')
                          for k in chaves):
            guardar.append(ln)

    out = list(guardar)
    out.append("    'menu.tab.pasta':'Pasta','menu.new':'New','menu.tab.entradas':'Starters',"
               "'menu.tab.pizzas':'Pizzas','menu.tab.dolce':'Dolce',")
    out.append("    'menu.pasta.h':'Fresh pasta at the weekend',")
    out.append("    'menu.pasta.p':'Our Lasagna al Ragù and potato gnocchi are made in house, "
               "with fresh pasta and the time each recipe calls for. To serve them at their best, "
               "we only make them at the weekend. Ask our team what we have made today.',")
    for g in GRUPOS_PIZZAS + GRUPOS_DOLCE:
        chave, _pt, en, _npt, nen, _k = g
        linha = f"    'menu.tab.{chave}':'{esc(en)}',"
        if nen:
            linha += f"'menu.g.{chave}':'{esc(nen)}',"
        out.append(linha)

    for d in D:
        key, _n, nome_en, _a, _p, _f, _foto, _d, desc_en, _h, hist_en, harm = d
        partes = []
        if nome_en:
            partes.append(f"'{key}.n':'{esc(nome_en)}'")
        partes.append(f"'{key}.d':'{esc(desc_en)}'")
        partes.append(f"'{key}.s':'{esc(hist_en)}'")
        if harm:
            partes.append(f"'{key}.h':'<b>Pairs with</b> · {esc(harm)}'")
        out.append('    ' + ','.join(partes) + ',')
    return out


def main():
    linhas = HTML.read_text(encoding='utf-8').split('\n')

    # 1) substituir a linha dos separadores do menu
    alvo = [i for i, l in enumerate(linhas) if l.startswith('<div class="menu-cat active" id="mc-pasta"')]
    assert len(alvo) == 1, f'linha do menu: {len(alvo)} candidatas'
    linhas[alvo[0]] = construir_html()

    # 2) substituir o bloco de chaves EN do menu
    ini = next(i for i, l in enumerate(linhas) if "'menu.eyebrow'" in l)
    fim = next(i for i, l in enumerate(linhas) if "'b.eyebrow'" in l)
    linhas[ini:fim] = construir_en(linhas[ini:fim])

    HTML.write_text('\n'.join(linhas), encoding='utf-8')
    print(f'menu: {len(D)} pratos · bloco EN reescrito')


if __name__ == '__main__':
    main()
