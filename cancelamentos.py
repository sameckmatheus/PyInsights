# scaneando os valores da planilha/tabela

import pandas as pd

tabela = pd.read_csv("nome_do_seu_arquivo.csv")
tabela = tabela.drop("CustomerID", axis=1)

display(tabela)

# identificando e removendo valores vazios

display(tabela.info())
tabela = tabela.dropna()
display(tabela.info())

# quantas pessoas cancelaram e não cancelaram

display(tabela["cancelou"].value_counts())
display(tabela["cancelou"].value_counts(normalize=True).map("{:.1%}".format))

display(tabela["duracao_contrato"].value_counts(normalize=True))
display(tabela["duracao_contrato"].value_counts())

# analisando o contrato mensal

display(tabela.groupby("duracao_contrato").mean(numeric_only=True))

# descobrimos aqui que a média de cancelamentos é 1, ou seja,
# praticamente todos os contratos mensais cancelaram (ou todos)

# então descobrimos que contrato mensal é ruim, vamos tirar ele e continuar analisando

tabela = tabela[tabela["duracao_contrato"] != "Monthly"]

display(tabela)

display(tabela["cancelou"].value_counts())
display(tabela["cancelou"].value_counts(normalize=True).map("{:.1%}".format))

# chegamos agora em menos da metade de pessoas cancelando, 
# mas ainda temos muitas pessoas ai, vamos continuar analisando

display(tabela["assinatura"].value_counts(normalize=True))
display(tabela.groupby("assinatura").mean(numeric_only=True))

# vemos que assinatura é quase 1/3, 1/3, 1/3
# e que os cancelamentos são na média bem parecidos, 
# então fica difícil tirar alguma conclusão da média, vamos precisar ir mais a fundo

# vamos criar gráfico, porque só com números tá difícil de visualizar
import plotly.express as px

for coluna in tabela.columns:
    grafico = px.histogram(tabela, x=coluna, color="cancelou")
    grafico.show()

# com os graficos a gente consegue descobrir muita coisa:
# dias atraso acima de 20 dias, 100% cancela
# ligações call center acima de 5 todo mundo cancela

tabela = tabela[tabela["ligacoes_callcenter"] < 5]
tabela = tabela[tabela["dias_atraso"] <= 20]

display(tabela)

display(tabela["cancelou"].value_counts())
display(tabela["cancelou"].value_counts(normalize=True).map("{:.1%}".format))

# se resolvermos isso, já caímos para 18% de cancelamento
# é claro que 100% é utópico, mas com isso já temos as principais causas (ou talvez 3 das principais):
# - forma de contrato mensal
# - necessidade de ligações no call center
# - atraso no pagamento
