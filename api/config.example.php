<?php
/* =========================================================================
   MODELO de configuração — Vívono Pizzeria
   -------------------------------------------------------------------------
   O ficheiro real `config.php` está no .gitignore (não vai para o GitHub),
   porque ficheiros de config costumam guardar segredos. Este modelo fica
   versionado para o projeto ser auto-documentado e fácil de restaurar.

   PARA USAR NUMA MÁQUINA/SERVIDOR NOVO:
   copie este ficheiro para `config.php` na mesma pasta (api/):
       cp config.example.php config.php
   Os valores abaixo já são os de produção. O Widget ID é público
   (aparece no embed da Featurable), por isso pode ficar aqui.
   ========================================================================= */

// 1) ID do widget criado em app.featurable.com (é público; aparece no embed):
$FEATURABLE_WIDGET_ID = 'd7fd43a8-bf7a-4b46-902b-8fb33a9ef76c';

// 2) Mostrar apenas avaliações com esta nota mínima (1 a 5). 4 = só 4 e 5 estrelas.
$MIN_RATING = 4;

// 3) Nº máximo de avaliações mostradas no site (o layout tem 3 por linha):
$MAX_REVIEWS = 6;

// 4) Horas em cache antes de consultar a Featurable de novo (mantém rápido):
$CACHE_HOURS = 12;
