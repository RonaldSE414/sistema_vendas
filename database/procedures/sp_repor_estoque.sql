CREATE OR REPLACE PROCEDURE sp_repor_estoque(p_produto_id INT, p_quantidade INT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_quantidade <= 0 THEN
        RAISE EXCEPTION 'A quantidade deve ser maior que zero';
    END IF;

    UPDATE produtos SET estoque = estoque + p_quantidade WHERE id = p_produto_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Produto % não encontrado', p_produto_id;
    END IF;
END;
$$;
