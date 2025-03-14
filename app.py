
import streamlit as st
import numpy as np
import joblib

# Carregar modelo treinado
modelo_dados = joblib.load('modelo_rede_neural.pkl')
weights = modelo_dados['weights']
scaler = modelo_dados['scaler']

# Função tanh
def tanh(x):
    return np.tanh(x)

# Rede Neural
def neural_network(weights, X):
    W1 = weights[:X.shape[1] * 8].reshape((X.shape[1], 8))
    b1 = weights[X.shape[1] * 8:X.shape[1] * 8 + 8]
    
    W2_start = X.shape[1] * 8 + 8
    W2_end = W2_start + 8 * 6
    W2 = weights[W2_start:W2_end].reshape((8, 6))
    b2 = weights[W2_end:W2_end + 6]
    
    W3_start = W2_end + 6
    W3_end = W3_start + 6 * 1
    W3 = weights[W3_start:W3_end].reshape((6, 1))
    b3 = weights[W3_end]
    
    def tanh(x):
        return np.tanh(x)

    hidden1 = tanh(np.dot(X, W1) + b1)
    hidden2 = tanh(np.dot(hidden1, W2) + b2)
    output = np.dot(hidden2, W3) + b3
    return output.flatten()

# Interface Streamlit
st.title('📐 Previsão de Deformação no Pavimento Aeroportuário (Protótipo)')

st.sidebar.header('Insira os Dados do Pavimento:')

mr_revest = st.sidebar.number_input('MR Revestimento (2507 - 10498)', min_value=2507, max_value=10498, value=3000)
esp_revest = st.sidebar.number_input('Espessura Revestimento (0.08 - 0.40)', min_value=0.08, max_value=0.40, value=0.20, step=0.01)
mr_base = st.sidebar.number_input('MR Base (165 - 450)', min_value=165, max_value=450, value=200)
esp_base = st.sidebar.number_input('Espessura Base (0.15 - 0.60)', min_value=0.15, max_value=0.60, value=0.30, step=0.01)
mr_subbase = st.sidebar.number_input('MR Sub-base (150 - 400)', min_value=150, max_value=400, value=200)
esp_subbase = st.sidebar.number_input('Espessura Sub-base (0.15 - 0.60)', min_value=0.15, max_value=0.60, value=0.30, step=0.01)
mr_subleito = st.sidebar.number_input('MR Subleito (25 - 298)', min_value=25, max_value=298, value=50)

# Botão para realizar previsão
if st.sidebar.button('Calcular Deformação'):
    entrada = np.array([[mr_revest, esp_revest, mr_base, esp_base, mr_subbase, esp_subbase, mr_subleito]])
    entrada_norm = scaler.transform(entrada)
    deformacao = neural_network(weights, entrada_norm)

    st.success(f'📌 **Deformação Prevista:** {deformacao[0]:.6f} m/m')
