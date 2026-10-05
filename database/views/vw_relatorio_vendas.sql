CREATE OR REPLACE VIEW vw_relatorio_vendas AS
SELECT
    v.id                                   AS venda_id,
    c.nome                                 AS cliente,
    v.data_venda,
    SUM(i.quantidade)                      AS qtd_itens,
    SUM(i.quantidade * i.preco_unitario)   AS subtotal,
    v.desconto_pct
FROM vendas v
JOIN clientes c    ON c.id = v.cliente_id
JOIN itens_venda i ON i.venda_id = v.id
GROUP BY v.id, c.nome, v.data_venda, v.desconto_pct;
