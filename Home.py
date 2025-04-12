import streamlit as st

st.set_page_config(page_title='PCAPS',
                    page_icon="🔬",
                    layout="centered",
                    initial_sidebar_state="auto",
                    menu_items=None)

tab1, tab2 = st.tabs(["Português (🇧🇷)", "English (🇺🇸)"])

with tab1:
    st.title('Apresentação do Projeto')
    st.divider()

    st.write(''' 
    O aplicativo :blue[**P**lataforma **A**utomatizada de **C**ontagem de **M**icrocápsulas (PCAPS)] foi  desenvolvido para automatizar a análise de imagens de microcápsulas obtidas por microscopia.

    Em contraste com o processo mais comumente empregado que envolve a contagem manual das microcápsulas, no processo automatizado o registro de microcápsulas por imagem analisada, medições de diâmetro/área e geração de análises estatísticas é mais rápido e com precisão igual ou superior à contagem manual. 

    Para a realização da análise deve ser fornecida um arquivo de imagem e as informações de sua escala. Uma vez que tenham sido informados, o software utiliza a técnica de segmentação de imagem para realizar a contagem automatizada. Em seguida realiza a medição automática de diâmetros e áreas das microcápsulas identificadas. A partir desses resultados são gerados dados estatísticos descritivos, gráficos de boxplot e histograma da imagem analisada.


    ''')

    st.subheader('Desenvolvedores', divider='blue')
    st.write(''' 
    Esse projeto foi Desenvolvido em Colaboração entre a **UFSJ** e a **UTFPr**
        
    Fernanda de M. Alves¹, Carolina S. Jurkevicz², Ana K.F.C. Pereira¹, Renato M.R. Viana², Gustavo H.R. Viana¹.

    ¹ Universidade Federal de São João del Rei, Campus CCO, Divinópolis-MG, Brasil.  
    ² Universidade Tecnológica Federal do Paraná, Dpto. Acadêmico de Química, Londrina-PR, Brasil.


    ''')
with tab2:
    st.title('Project Presentation')
    st.divider()

    st.write(''' 
    The :blue[**A**utomated **C**apsule **C**ounting **P**latform (ACCP)] application was developed to automate the analysis of microcapsule images obtained through microscopy.

    In contrast to the more commonly used process, which involves manually counting microcapsules, the automated process records microcapsules from analyzed images, performs diameter/area measurements, and generates statistical analyses faster and with equal or greater accuracy than manual counting.

    To perform the analysis, an image file and its scale information must be provided. Once these details are supplied, the software uses image segmentation techniques to perform automated counting. It then automatically measures the diameters and areas of the identified microcapsules. From these results, descriptive statistical data, boxplots, and histograms of the analyzed image are generated.
    ''')

    st.subheader('Developers', divider='blue')
    st.write(''' 
    This project was developed in collaboration between **UFSJ** and **UTFPr**:
        
    Fernanda de M. Alves¹, Carolina S. Jurkevicz², Ana K.F.C. Pereira¹, Renato M.R. Viana², Gustavo H.R. Viana¹.

    ¹ Federal University of São João del Rei, CCO Campus, Divinópolis-MG, Brazil.  
    ² Federal University of Technology - Paraná, Academic Department of Chemistry, Londrina-PR, Brazil.
    ''')

