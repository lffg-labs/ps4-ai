# Notas

Exemplo do dataset.

| date       | precipitation | temp_max | temp_min | wind | weather |
| ---------- | ------------- | -------- | -------- | ---- | ------- |
| 2012-01-01 | 0.0           | 12.8     | 5.0      | 4.7  | drizzle |
| 2012-01-02 | 10.9          | 10.6     | 2.8      | 4.5  | rain    |
| 2012-01-03 | 0.8           | 11.7     | 7.2      | 2.3  | rain    |
| 2012-01-04 | 20.3          | 12.2     | 5.6      | 4.7  | rain    |
| 2012-01-05 | 1.3           | 8.9      | 2.8      | 6.1  | rain    |

Nosso objetivo com isso é classificar o `weather` (o rótulo de cada instância) a
partir das informações fornecidas.

Etapas do pré-processamento:

1. Transformar a coluna `date` para o mês, que geralmente é o que mais
   influencia no período do tempo.

Vale lembrar que, como todos os outros dados já são numéricos, não foi
necessário fazer nenhum tipo de codificação adicional.

---

- Clara Oliveira
- Eduardo Lemos
- Gabriel Ribeiro
- Luiz Felipe Gonçalves
- Yuri Rousseff
