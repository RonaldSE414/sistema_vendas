CREATE OR REPLACE PROCEDURE sp_registrar_venda_multipla(
    p_cliente_id   INT,
    p_produtos     INT[],
    p_quantidades  INT[],
    p_desconto_pct NUMERIC,
    INOUT p_venda_id INT DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    i         INT;
    v_nome    TEXT;
    v_preco   NUMERIC(10,2);
    v_estoque INT;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM clientes WHERE id = p_cliente_id) THEN
        RAISE EXCEPTION 'Cliente % não encontrado', p_cliente_id;
    END IF;

    IF COALESCE(array_length(p_produtos, 1), 0) = 0 THEN
        RAISE EXCEPTION 'A venda precisa ter pelo menos um produto';
    END IF;

    IF array_length(p_produtos, 1) IS DISTINCT FROM array_length(p_quantidades, 1) THEN
        RAISE EXCEPTION 'Listas de produtos e quantidades com tamanhos diferentes';
    END IF;

    INSERT INTO vendas (cliente_id, desconto_pct)
    VALUES (p_cliente_id, p_desconto_pct)
    RETURNING id INTO p_venda_id;

    FOR i IN 1..array_length(p_produtos, 1) LOOP
        IF p_quantidades[i] <= 0 THEN
            RAISE EXCEPTION 'Quantidade inválida para o produto %', p_produtos[i];
        END IF;

        SELECT nome, preco, estoque INTO v_nome, v_preco, v_estoque
          FROM produtos WHERE id = p_produtos[i] FOR UPDATE;
        IF NOT FOUND THEN
            RAISE EXCEPTION 'Produto % não encontrado', p_produtos[i];
        END IF;

        IF v_estoque < p_quantidades[i] THEN
            RAISE EXCEPTION 'Estoque insuficiente para "%" (disponível: %)', v_nome, v_estoque;
        END IF;

        INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario)
        VALUES (p_venda_id, p_produtos[i], p_quantidades[i], v_preco);

        UPDATE produtos SET estoque = estoque - p_quantidades[i] WHERE id = p_produtos[i];
    END LOOP;
END;
$$;
