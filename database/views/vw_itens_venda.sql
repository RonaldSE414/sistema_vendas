CREATE OR REPLACE VIEW vw_itens_venda AS
SELECT
    i.venda_id,
    p.nome                          AS produto,
    i.quantidade,
    i.preco_unitario,
    i.quantidade * i.preco_unitario AS subtotal
FROM itens_venda i
JOIN produtos p ON p.id = i.produto_id;
