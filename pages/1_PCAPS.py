import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy import ndimage
from skimage import io, color, measure
import pandas as pd
import streamlit as st
import io


def calculadora_propriedades(arquivo_imagem,pixels, mm):
#Inserção da escala, imagem analisada e nome arquivo CSV    
    if pixels > 0:
        um_por_px = (mm / pixels) * 1000
    
    # carregar imagem
        bytes_data = arquivo_imagem.getvalue()
        img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), 0)        
        pixels_to_um = um_por_px #1 pixel = 6,4 um ou 6400 nm

        ret, thresh = cv2.threshold(img,0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        kernel= np.ones((3,3), np.uint8)
        eroded = cv2.erode(thresh, kernel, iterations =1)
        dilated = cv2.dilate(eroded, kernel, iterations =1)

        mask = dilated == 255

        s = [[1,1,1], [1,1,1],[1,1,1]]
        labeled_mask, num_labels = ndimage.label(mask, structure=s)

        img2 = color.label2rgb(labeled_mask, bg_label=0)  

        #medir imagem
        clusters = measure.regionprops(labeled_mask, img)

        #exportar csv
        propList = ['Area', 'equivalent_diameter']        
        output_file = open('teste.csv', 'w')
        output_file.write((','+','.join(propList) + '\n'))

        for cluster_props in clusters:
            output_file.write(str(cluster_props['Label']))
            for i, prop in enumerate(propList):
                if(prop == 'Area'):
                    to_print = cluster_props[prop]*pixels_to_um**2
                else:
                    to_print = cluster_props[prop]*pixels_to_um
                output_file.write(',' + str(to_print))
            output_file.write('\n')
        output_file.close()
    
        df= pd.read_csv('teste.csv')
        df = df.drop('Unnamed: 0', axis=1)
        df = df.rename(columns={'Area':'Área (µm²)', 'equivalent_diameter':'Diâmetro (µm)'})           

    #Boxplot
        
        fig_boxplot, ax = plt.subplots()
        ax.boxplot(df['Diâmetro (µm)'], widths=0.2)
        plt.ylabel('Diâmetro (µm)')

        
    # #Historgrama usadndo Sturge’s rule e exibindo % eixo Y
        fig_hist, ax = plt.subplots() 
        norm_dist = df.shape[0]
        bin_count = int(np.ceil(np.log2(norm_dist)) + 1)

        #array com todos os bins do histograma
        array_diametros = np.array(list(df['Diâmetro (µm)'].sort_values())) #array de diâmetros ordenado em ordem crescente
        array_diametros = np.linspace(array_diametros[-1], array_diametros[0],bin_count+1) #array de diâmetros ajustado para o número de bins

        #Separação dos valores iniciais e finais do eixo X sem arredondamento
        primeiro_valor_his = np.round(array_diametros[-1])
        ultimo_valor_his = np.round(array_diametros[0])
        array_diametros = np.linspace(primeiro_valor_his, ultimo_valor_his,bin_count+1)

        inicio_e_fim = np.append(primeiro_valor_his, ultimo_valor_his)

        #Arredondamento dos valores intermediários do array_diâmetros para valores terminados em zero
        rounded_array = np.fix(array_diametros/10)*10
        rounded_array = rounded_array.astype(float) #conversão array para float
        rounded_array = rounded_array[1:-1]

        #Junção dos valores iniciais, finais e intermediários arredondados do eixo X
        valores_eixo = np.append(rounded_array,inicio_e_fim )

        #plotagem histograma     
        ax.hist(df['Diâmetro (µm)'],
                bins=bin_count,
                weights=np.ones(len(df['Diâmetro (µm)'])) / len(df['Diâmetro (µm)']),
                orientation='vertical',
                color='gray',
                edgecolor='k')
        plt.title('')
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
        plt.xlabel('Diâmetro (µm)')
        plt.xticks(valores_eixo)
        
    
    #planilha com resurmo estatístico
        def formatar(valor):
            return '{:,.2f}'.format(valor)

        descricao = df.describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9])
        descricao['Área (µm²)'] = descricao['Área (µm²)'].apply(formatar)
        descricao['Diâmetro (µm)'] = descricao['Diâmetro (µm)'].apply(formatar)

        pdi = (df['Diâmetro (µm)'].std() / df['Diâmetro (µm)'].mean()) ** 2
        descricao.loc['PDI', 'Diâmetro (µm)'] = '{:.3f}'.format(pdi)

        return img2, df, descricao, fig_boxplot,fig_hist




############################Estrutura do Aplicativo#####################################################

st.set_page_config(page_title='PCAPS',
                    page_icon="🔬",
                    layout="centered",
                    initial_sidebar_state="auto",
                    menu_items=None)

st.subheader('**1.** Anexe o Arquivo de Imagem.', divider='gray')
arquivo_imagem = st.file_uploader("Selecione (ou arraste) um arquivo de imagem")


st.subheader('**2.** Informe os Dados para a Construção da Escala.', divider='gray')
col1, col2 = st.columns(2)
with col1:
    pixels = st.number_input('Insira o valor em Pixels')
with col2:
    mm = st.number_input('Insira o valor em milímetros')

# st.subheader('Arquivo de Imagem e Dados para Construção da Escala:', divider='gray')
# col1, col2, col3 = st.columns(3)
# with col2:
#     pixels = st.number_input('Insira o valor em Pixels')
# with col3:
#     mm = st.number_input('Insira o valor em milímetros')
# with col1:
#     arquivo_imagem = st.file_uploader("Selecione (ou arraste) um arquivo de imagem")

if pixels and mm > 0:
    um_por_px = (mm / pixels) * 1000
    

if arquivo_imagem and pixels and mm:
    st.subheader('**3.** Resultados', divider='rainbow')
    st.write(f'**Valor da Escala:** {um_por_px:.2f} µm/px.')
    img, df, descricao, fig_boxplot, fig_hist = calculadora_propriedades(arquivo_imagem,pixels, mm)
    st.write('**Imagem Segmentada para Conferência:**')
    st.image(img)
    
    st.subheader('3.1. Tabelas', divider='rainbow')
    col1, col2 = st.columns(2)
    with col1:
        st.write('**Resumo Estatístico**')
        descricao
        # Gerar o arquivo Excel para download
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            descricao.to_excel(writer)
            writer.close()
        # Botao de Download
        st.download_button(
            label='Download Resumo Estatístico',
            data =buffer,
            file_name='resumo_estatistico.xlsx',
            mime="application/vnd.ms-excel"
        )        
    with col2:
        st.write('**Dados Individuais de cada Microcápsula**')
        df
        # Gerar o arquivo Excel para download
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer)
            writer.close()
        # Botao de Download
        st.download_button(
            label='Download Dados Individuais',
            data =buffer,
            file_name='dados_individuais.xlsx',
            mime="application/vnd.ms-excel"
        )  
    
    #Gráficos de histograma e boxplot
    st.subheader('3.2. Gráficos', divider='rainbow')
    col1, col2 = st.columns(2)
    with col1: 
        st.write('**Boxlplot de Diâmetro das Microcápsulas**')       
        fig_boxplot       
    with col2:
        st.write('**Histograma de Diâmetro das Microcápsulas**')  
        fig_hist
        st.caption('*Número de classes do histograma calculado conforme Regra de Sturges')

    