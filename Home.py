import streamlit as st

st.set_page_config(page_title='PCAPS',
                    page_icon="🔬",
                    layout="centered",
                    initial_sidebar_state="auto",
                    menu_items=None)

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