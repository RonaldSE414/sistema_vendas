CREATE OR REPLACE FUNCTION fn_calcular_total_venda(p_venda_id INT)
RETURNS NUMERIC
LANGUAGE plpgsql
AS $$
DECLARE
    v_subtotal NUMERIC;
    v_desconto NUMERIC;
BEGIN
    SELECT desconto_pct INTO v_desconto FROM vendas WHERE id = p_venda_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Venda % não encontrada', p_venda_id;
    END IF;

    SELECT COALESCE(SUM(quantidade * preco_unitario), 0)
      INTO v_subtotal FROM itens_venda WHERE venda_id = p_venda_id;

    RETURN ROUND(v_subtotal * (1 - v_desconto / 100), 2);
END;
$$;
