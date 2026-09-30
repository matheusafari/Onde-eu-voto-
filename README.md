# Onde eu voto? — Porto Alegre

Site simples para a pessoa descobrir o endereço do seu local de votação em Porto Alegre digitando a **zona** e a **seção** do título de eleitor.

> Este não é um site oficial. Os dados vêm da lista pública de locais de votação do TRE-RS. Em caso de dúvida, confirme sempre no [site do TSE](https://www.tse.jus.br/servicos-eleitorais/autoatendimento-eleitoral#/atendimento-eleitor/onde-votar).

---

## A ideia

Muita gente, principalmente as pessoas idosas, tem dificuldade para usar os sites oficiais de consulta eleitoral. Eles pedem cadastro, CPF, data de nascimento, nome da mãe, e têm muitos menus e letras pequenas.

A proposta deste projeto é o contrário: **uma página só, com duas perguntas e uma resposta**.

1. A pessoa digita a zona.
2. Digita a seção.
3. Vê o nome da escola e o endereço onde vai votar, com um botão para abrir no mapa.

Quem não sabe a zona e a seção não fica perdido: o site explica onde encontrar esses números (no título de eleitor de papel ou no aplicativo e-Título) e leva direto para a consulta oficial do TSE.

O foco é **Porto Alegre**, com todas as 10 zonas eleitorais da cidade: 1, 2, 111, 112, 113, 114, 158, 159, 160 e 161.

## Pensado para o público idoso

- **Letra grande** em todo o site, usando uma fonte feita para pessoas com baixa visão.
- **Botões A− e A+** para aumentar ou diminuir a letra. O site lembra a escolha na próxima visita.
- **Campos grandes** que abrem o teclado de números no celular.
- **Poucas informações por tela**: só o que a pessoa precisa.
- **Mensagens claras** quando algo dá errado, dizendo o que fazer: faltou preencher, a zona não é de Porto Alegre ou a seção não foi encontrada.
- **Botão "Ver no mapa"**, que abre o endereço no Google Maps para a pessoa ver o caminho.
- **Bom contraste de cores**, no modo claro e no modo escuro do celular.
- **Funciona com leitores de tela**: o resultado é anunciado assim que aparece.

## Como funciona

```
PDF do TRE-RS  ──►  script em Python  ──►  lista de locais  ──►  index.html  ──►  navegador da pessoa
(lista oficial)     (lê e organiza)        (zona, seções,       (site com os
                                            endereço)            dados dentro)
```

1. **Origem dos dados.** O TRE-RS publica a lista de locais de votação de Porto Alegre, com o nome do local, o endereço e as seções de cada um. Essa página foi salva em PDF (`dados/fonte/locais-votacao-tre-rs.pdf`).
2. **Extração.** O script `ferramentas/atualizar_dados.py` lê o PDF e separa cada local em zona, nome, endereço e seções. Ele usa a posição e o tamanho das letras na página para saber o que é nome, o que é endereço e o que é número de seção. Também junta os locais que ficaram divididos entre duas páginas do PDF.
3. **Conferência.** O script avisa se alguma seção aparecer repetida. Na versão atual foram encontrados **346 locais e 3.078 seções**, sem repetição.
4. **Montagem do site.** O script coloca a lista dentro do `index.html`. Assim o site não depende de servidor nem de banco de dados: é um único arquivo que funciona até aberto direto no computador.
5. **Consulta.** Quando a pessoa digita zona e seção, o próprio navegador procura na lista e mostra o local na hora, sem enviar nada pela internet.

### Privacidade

O site não pede nome, CPF nem nenhum dado pessoal, e não envia o que a pessoa digita para lugar nenhum. A busca acontece toda no aparelho de quem está usando.

## Ferramentas usadas

| Ferramenta | Para que foi usada |
|---|---|
| **HTML, CSS e JavaScript** | O site em si. Sem frameworks, para ficar leve e fácil de manter. |
| **Atkinson Hyperlegible** (Google Fonts) | Fonte principal. Foi criada pelo Braille Institute para facilitar a leitura de pessoas com baixa visão. |
| **Literata** (Google Fonts) | Fonte dos títulos. |
| **Python** | Linguagem do script que lê o PDF e atualiza os dados. |
| **pdfplumber** | Biblioteca Python que lê o texto do PDF junto com a posição de cada palavra. |
| **GitHub e GitHub Pages** | Guardar o código e publicar o site de graça na internet. |
| **Lista de locais do TRE-RS** | Fonte oficial dos dados de Porto Alegre. |
| **Consulta do TSE** | Link para quem não sabe a zona e a seção. |
| **Google Maps** | Link para abrir o endereço do local no mapa. |
| **Claude** (inteligência artificial da Anthropic) | Assistente usado no desenvolvimento. Veja abaixo. |

### Como o Claude ajudou

A ideia, o público e as decisões do projeto são do autor. O Claude, assistente de inteligência artificial da Anthropic (modelo Claude Opus 5.5), foi usado como ferramenta de apoio para:

- ler o PDF do TRE-RS e extrair os 346 locais e 3.078 seções, conferindo se havia seções repetidas ou locais cortados entre páginas;
- escrever o código do site (HTML, CSS e JavaScript) e o script de atualização em Python;
- sugerir o visual pensado para idosos: tamanho de letra, contraste, botões grandes e mensagens simples;
- organizar a pasta do projeto e escrever este README.

Todo o conteúdo gerado deve ser revisado por uma pessoa. Os dados vêm de fonte oficial, mas podem mudar: por isso o site sempre indica o TSE como referência final.

## O que tem nesta pasta

| Arquivo | Para que serve |
|---|---|
| `index.html` | O site. É o único arquivo necessário para ele funcionar. |
| `dados/locais-porto-alegre.json` | Todos os locais, com zona, seções e endereço. |
| `dados/locais-porto-alegre.csv` | A mesma lista, uma linha por seção. Abre no Excel. |
| `dados/fonte/locais-votacao-tre-rs.pdf` | O PDF original salvo do site do TRE-RS. |
| `ferramentas/atualizar_dados.py` | Lê um PDF novo e atualiza os dados e o `index.html`. |
| `ferramentas/modelo.html` | O modelo do site (visual e funcionamento), sem os dados. |
| `ferramentas/requirements.txt` | Lista das bibliotecas Python que o script precisa. |
| `.nojekyll` | Arquivo vazio que evita problemas no GitHub Pages. |

## Links

- Consulta oficial do local de votação (TSE): https://www.tse.jus.br/servicos-eleitorais/autoatendimento-eleitoral#/atendimento-eleitor/onde-votar
- Lista de locais do TRE-RS: https://locais-votacao.tre-rs.jus.br/
