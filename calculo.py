import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# Definir a versão do aplicativo
VERSION = "1.5.0"

# Horário de funcionamento da empresa
HORARIO_ABERTURA = datetime.time(7, 55)
HORARIO_FECHAMENTO = datetime.time(17, 45)

# Taxas de horas extras de acordo com as leis trabalhistas do Brasil
TAXA_HORA_EXTRA_50 = 1.5  # 50% de acréscimo
TAXA_HORA_EXTRA_100 = 2.0  # 100% de acréscimo
TAXA_HORA_EXTRA_150 = 2.5  # 150% de acréscimo

# Função para calcular as horas trabalhadas
def calcular_horas():
    # Obter valores dos campos de entrada
    data_inicio = entrada_data_inicio.get()
    data_termino = entrada_data_termino.get()
    valor_hora = float(entrada_valor_hora.get())
    calcular_insalubridade = insalubridade_var.get()

    # Converter datas para formato datetime
    data_inicio = datetime.datetime.strptime(data_inicio, "%Y%m%d")
    data_termino = datetime.datetime.strptime(data_termino, "%Y%m%d")

    # Calcular horas normais e horas extras
    horas_normais, horas_extras = calcular_horas_trabalhadas(data_inicio, data_termino)

    # Calcular o valor total
    valor_total = (horas_normais + horas_extras) * valor_hora

    # Aplicar insalubridade, se necessário
    if calcular_insalubridade:
        valor_total *= 1.2  # Acréscimo de 20% para insalubridade

    # Exibir resultados na tela
    label_horas_normais["text"] = f"Horas Normais: {horas_normais:.2f}"
    label_horas_extras["text"] = f"Horas Extras: {horas_extras:.2f}"
    label_valor_total["text"] = f"Valor Total: R${valor_total:.2f}"

# Função para calcular as horas normais e horas extras com base no horário de funcionamento
def calcular_horas_trabalhadas(data_inicio, data_termino):
    horas_trabalhadas = 0
    horas_extras = 0

    # Calcular horas normais e horas extras
    while data_inicio < data_termino:
        # Calcular o horário de entrada e saída do dia atual
        entrada_dia = datetime.datetime.combine(data_inicio, HORARIO_ABERTURA)
        saida_dia = datetime.datetime.combine(data_inicio, HORARIO_FECHAMENTO)

        # Verificar se o horário de entrada é depois do horário de saída
        if entrada_dia > saida_dia:
            saida_dia += datetime.timedelta(days=1)

        # Calcular as horas trabalhadas no dia atual
        horas_trabalhadas += (saida_dia - entrada_dia).total_seconds() / 3600

        # Verificar se houve horas extras
        if data_inicio.weekday() < 5:  # Verificar se é um dia de semana
            if saida_dia > datetime.datetime.combine(data_inicio, HORARIO_FECHAMENTO):
                horas_extras += (saida_dia - datetime.datetime.combine(data_inicio, HORARIO_FECHAMENTO)).total_seconds() / 3600

        # Avançar para o próximo dia
        data_inicio += datetime.timedelta(days=1)

    # Retornar as horas normais e horas extras
    return horas_trabalhadas, horas_extras

# Criar a interface do usuário
janela = tk.Tk()
janela.title("Cálculo de Horas de Trabalho - Versão " + VERSION)  # Adiciona a versão na barra de título

# Criar campos de entrada
frame_entrada = tk.Frame(janela)
frame_entrada.pack(padx=10, pady=10)

label_data_inicio = tk.Label(frame_entrada, text="Data de Início (Formato: AAAAMMDD):")
label_data_inicio.grid(row=0, column=0, padx=5, pady=5)

entrada_data_inicio = tk.Entry(frame_entrada)
entrada_data_inicio.grid(row=0, column=1, padx=5, pady=5)

label_data_termino = tk.Label(frame_entrada, text="Data de Término (Formato: AAAAMMDD):")
label_data_termino.grid(row=1, column=0, padx=5, pady=5)

entrada_data_termino = tk.Entry(frame_entrada)
entrada_data_termino.grid(row=1, column=1, padx=5, pady=5)

label_valor_hora = tk.Label(frame_entrada, text="Valor da Hora:")
label_valor_hora.grid(row=2, column=0, padx=5, pady=5)

entrada_valor_hora = tk.Entry(frame_entrada)
entrada_valor_hora.grid(row=2, column=1, padx=5, pady=5)

# Adicionar opção para calcular insalubridade
insalubridade_var = tk.BooleanVar()
check_insalubridade = ttk.Checkbutton(frame_entrada, text="Calcular Insalubridade (20%)", variable=insalubridade_var)
check_insalubridade.grid(row=3, columnspan=2, padx=5, pady=5)

# Labels para exibir os resultados
label_horas_normais = tk.Label(janela, text="Horas Normais: 0.00")
label_horas_normais.pack(padx=10, pady=5)

label_horas_extras = tk.Label(janela, text="Horas Extras: 0.00")
label_horas_extras.pack(padx=10, pady=5)

label_valor_total = tk.Label(janela, text="Valor Total: R$0.00")
label_valor_total.pack(padx=10, pady=5)

# Botão para calcular
botao_calcular = ttk.Button(janela, text="Calcular", command=calcular_horas)
botao_calcular.pack(padx=10, pady=5)

# Iniciar loop de eventos
janela.mainloop()
