-- Tabela org
INSERT INTO org (id, login, name, url, image, description) VALUES
(1, 'gondor', 'Reino de Gondor', 'https://gondor.me', 'https://gondor.me/logo.png', 'O orgulho dos homens do sul.'),
(2, 'rohan', 'Reino de Rohan', 'https://rohan.me', 'https://rohan.me/logo.png', 'A terra dos cavaleiros.'),
(3, 'mordor', 'Mordor', 'https://mordor.me', 'https://mordor.me/logo.png', 'Onde a sombra se estende.'),
(4, 'rivendell', 'Valfenda', 'https://rivendell.me', 'https://rivendell.me/logo.png', 'Refúgio dos elfos.'),
(5, 'shire', 'Condado', 'https://shire.me', 'https://shire.me/logo.png', 'Terra dos hobbits.'),
(6, 'moria', 'Moria', 'https://moria.me', 'https://moria.me/logo.png', 'As minas dos anões.'),
(7, 'isengard', 'Isengard', 'https://isengard.me', 'https://isengard.me/logo.png', 'A torre de Orthanc.'),
(8, 'lothlorien', 'Lothlórien', 'https://lothlorien.me', 'https://lothlorien.me/logo.png', 'A floresta dourada.'),
(9, 'arnor', 'Arnor', 'https://arnor.me', 'https://arnor.me/logo.png', 'O reino do norte.'),
(10, 'numenor', 'Númenor', 'https://numenor.me', 'https://numenor.me/logo.png', 'A ilha dos homens elevados.');

-- Produtos
INSERT INTO product (id, org_id, name, description) VALUES
(1, 1, 'Aragorn', 'Herdeiro de Isildur'), (2, 1, 'Boromir', 'Filho de Denethor'), (3, 1, 'Faramir', 'O irmão mais novo'),
(4, 2, 'Éomer', 'Mestre da cavalaria'), (5, 2, 'Théoden', 'Rei de Rohan'), (6, 2, 'Éowyn', 'A dama escudo'),
(7, 3, 'Sauron', 'O Senhor do Escuro'), (8, 3, 'Nazgûl', 'Espectros do Anel'), (9, 3, 'Gothmog', 'Tenente de Morgul'),
(10, 4, 'Elrond', 'Senhor de Valfenda'), (11, 4, 'Arwen', 'A estrela vespertina'), (12, 4, 'Glorfindel', 'Guerreiro lendário'),
(13, 5, 'Frodo', 'Portador do Anel'), (14, 5, 'Samwise', 'Leal jardineiro'), (15, 5, 'Merry e Pippin', 'Hobbits curiosos'),
(16, 6, 'Durin', 'Pai dos anões'), (17, 6, 'Balin', 'Senhor de Moria'), (18, 6, 'Dwalin', 'Irmão de Balin'),
(19, 7, 'Saruman', 'O Branco'), (20, 7, 'Gríma', 'Língua de cobra'), (21, 7, 'Uruk-hai', 'Exército sombrio'),
(22, 8, 'Galadriel', 'Senhora de Lórien'), (23, 8, 'Celeborn', 'Senhor de Lórien'), (24, 8, 'Haldir', 'Guarda da floresta'),
(25, 9, 'Arvedui', 'Último rei de Arnor'), (26, 9, 'Malbeth', 'O vidente'), (27, 9, 'Glóin', 'Pai de Gimli'),
(28, 10, 'Elros', 'Fundador de Númenor'), (29, 10, 'Tar-Míriel', 'Rainha de Númenor'), (30, 10, 'Ar-Pharazôn', 'O último rei');

-- Repositórios (2 por produto, nomes temáticos)
INSERT INTO repository (id, product_id, name, description, url, branch_production) VALUES
(1, 1, 'anduril', 'Espada flamejante de Aragorn', 'https://gondor.me/repos/anduril', 'main'),
(2, 1, 'rangers', 'Dúnedain do norte', 'https://gondor.me/repos/rangers', 'main'),
(3, 2, 'horn-of-gondor', 'O chamado de Boromir', 'https://gondor.me/repos/horn', 'main'),
(4, 2, 'gondorian-guard', 'Guarda da Cidadela', 'https://gondor.me/repos/guard', 'main'),
(5, 3, 'ithilien', 'Terras de Faramir', 'https://gondor.me/repos/ithilien', 'main'),
(6, 3, 'rangers-ithilien', 'Rangers de Ithilien', 'https://gondor.me/repos/rangers-ithilien', 'main');

-- Tags
INSERT INTO tag (id, type, start_date, end_date, year, number) VALUES
('tag1', 'release', '2025-01-01', '2025-01-02', 2025, 1),
('tag2', 'sprint', '2025-02-01', '2025-02-15', 2025, 2),
('tag3', 'hotfix', '2025-03-01', '2025-03-01', 2025, 3);

-- RepositoryTags
INSERT INTO repositorytag (id, type, start_date, end_date, repository_id, sha1) VALUES
('rt1', 'release', '2025-01-01', '2025-01-02', 1, 'sha1abc'),
('rt2', 'sprint', '2025-02-01', '2025-02-15', 2, 'sha1def'),
('rt3', 'hotfix', '2025-03-01', '2025-03-01', 3, 'sha1ghi');

