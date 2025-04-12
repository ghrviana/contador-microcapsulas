import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy import ndimage
from skimage import io, color, measure
import pandas as pd
import streamlit as st
import io


def properties_calculator(image_file, pixels, mm):
#Inserção da escala, imagem analisada e nome arquivo CSV    
    if pixels > 0:
        um_por_px = (mm / pixels) * 1000
    
    # carregar imagem
        bytes_data = image_file.getvalue()
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
        df = df.rename(columns={'Area':'Area (µm²)', 'equivalent_diameter':'Diameter (µm)'})           

    #Boxplot
        
        fig_boxplot, ax = plt.subplots()
        ax.boxplot(df['Diameter (µm)'], widths=0.2)
        plt.ylabel('Diameter (µm)')

        
    # #Historgrama usadndo Sturge’s rule e exibindo % eixo Y
        fig_hist, ax = plt.subplots() 
        norm_dist = df.shape[0]
        bin_count = int(np.ceil(np.log2(norm_dist)) + 1)

        #array com todos os bins do histograma
        array_diametros = np.array(list(df['Diameter (µm)'].sort_values())) #array de diâmetros ordenado em ordem crescente
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
        ax.hist(df['Diameter (µm)'],
                bins=bin_count,
                weights=np.ones(len(df['Diameter (µm)'])) / len(df['Diameter (µm)']),
                orientation='vertical',
                color='gray',
                edgecolor='k')
        plt.title('')
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
        plt.xlabel('Diameter (µm)')
        plt.xticks(valores_eixo)
        
    
    #planilha com resurmo estatístico
        def formatar(valor):
            return '{:,.2f}'.format(valor)

        descricao = df.describe()
        descricao['Area (µm²)'] = descricao['Area (µm²)'].apply(formatar)
        descricao['Diameter (µm)'] = descricao['Diameter (µm)'].apply(formatar)
        
        return img2, df, descricao, fig_boxplot,fig_hist 




############################Estrutura do Aplicativo#####################################################

st.set_page_config(page_title='ACCP',
                    page_icon="🔬",
                    layout="centered",
                    initial_sidebar_state="auto",
                    menu_items=None)

st.subheader('**1.** Upload the Image File.', divider='gray')
image_file = st.file_uploader("Select (or drag and drop) an image file")


st.subheader('**2.** Enter the Data for Scale Construction.', divider='gray')
col1, col2 = st.columns(2)
with col1:
    pixels = st.number_input('Enter the Value in Pixels')
with col2:
    mm = st.number_input('Enter the Value in Millimeters')

if pixels and mm > 0:
    um_por_px = (mm / pixels) * 1000
    

if image_file and pixels and mm:
    st.subheader('**3.** Results', divider='rainbow')
    st.write(f'**Scale Value:** {um_por_px:.2f} µm/px.')
    img, df, descricao, fig_boxplot, fig_hist = properties_calculator(image_file,pixels, mm)
    st.write('**Segmented Image for Review:**')
    st.image(img)
    
    st.subheader('3.1. Tables', divider='rainbow')
    col1, col2 = st.columns(2)
    with col1:
        st.write('**Statistical Summary**')
        descricao
        # Gerar o arquivo Excel para download
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            descricao.to_excel(writer)
            writer.close()
        # Botao de Download
        st.download_button(
            label='Download Statistical Summary',
            data =buffer,
            file_name='statistical_summary.xlsx',
            mime="application/vnd.ms-excel"
        )        
    with col2:
        st.write('**Individual Data for Each Microsphere**')
        df
        # Gerar o arquivo Excel para download
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer)
            writer.close()
        # Botao de Download
        st.download_button(
            label='Download Individual Data',
            data =buffer,
            file_name='individual_data.xlsx',
            mime="application/vnd.ms-excel"
        )  
    
    #Gráficos de histograma e boxplot
    st.subheader('3.2. Gráficos', divider='rainbow')
    col1, col2 = st.columns(2)
    with col1: 
        st.write('**Boxplot of Microsphere Diameter**')       
        fig_boxplot       
    with col2:
        st.write('**Histogram of Microsphere Diameter**')  
        fig_hist
        st.caption("*Number of Histogram Classes Calculated Using Sturges' Rule*")