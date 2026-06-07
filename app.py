import streamlit as str

# Configuração da página
str.set_page_config(page_title="Analizador de Múltiplas 80%+", page_icon="📊", layout="wide")

str.title("📊 Gerador de Múltiplas de Alta Probabilidade (80%+) ")
str.write("Insira os dados dos jogos para calcular a viabilidade matemática da sua múltipla.")

# Inicializar estado para armazenar os jogos adicionados
if 'jogos' not in str.session_state:
    str.session_state.jogos = []

# Formulário para adicionar jogos
str.sidebar.header("🚀 Adicionar Novo Jogo")
with str.sidebar.form(key='form_jogo'):
    time_casa = str.text_input("Time da Casa (ex: Colômbia)", placeholder="Digite o time da casa")
    time_fora = str.text_input("Time de Fora (ex: Jordânia)", placeholder="Digite o time de fora")
    
    str.markdown("---")
    str.write("**Histórico Recente (Últimos 10 jogos):**")
    
    # Critérios de validação (O usuário insere com base no retrospecto do site de análise)
    freg_gol_casa = str.slider("% Jogos do Mandante com Gols (Over 0.5)", 0, 100, 90)
    freg_vitoria_casa = str.slider("% Jogos que o Mandante NÃO perdeu (1X)", 0, 100, 85)
    freg_cantos = str.slider("% Jogos com +7.5 Escanteios combinados", 0, 100, 80)
    
    # Odds oferecidas pela casa de aposta
    odd_gol = str.number_input("Odd para Over 0.5 Gols", min_value=1.01, max_value=2.0, value=1.12, step=0.01)
    odd_dupla = str.number_input("Odd para Dupla Hipótese (1X ou X2)", min_value=1.01, max_value=2.0, value=1.10, step=0.01)
    odd_cantos = str.number_input("Odd para +7.5 Cantos", min_value=1.01, max_value=2.0, value=1.15, step=0.01)
    
    botao_adicionar = str.form_submit_button(label="Analisar e Adicionar Jogo")

# Lógica para adicionar jogo na lista
if botao_adicionar and time_casa and time_fora:
    novo_jogo = {
        "confronto": f"{time_casa} x {time_fora}",
        "mercados": []
    }
    
    # Filtrar apenas mercados com 80% ou mais de chance
    if freg_gol_casa >= 80:
        novo_jogo["mercados"].append({"nome": "Mais de 0.5 Gols", "prob": freg_gol_casa / 100, "odd": odd_gol})
    if freg_vitoria_casa >= 80:
        novo_jogo["mercados"].append({"nome": f"Dupla Hipótese ({time_casa} ou Empate)", "prob": freg_vitoria_casa / 100, "odd": odd_dupla})
    if freg_cantos >= 80:
        novo_jogo["mercados"].append({"nome": "Mais de 7.5 Escanteios", "prob": freg_cantos / 100, "odd": odd_cantos})
        
    str.session_state.jogos.append(novo_jogo)
    str.success(f"Jogo {time_casa} x {time_fora} analisado com sucesso!")

# Botão para limpar os dados
if str.sidebar.button("Limpar Jogos"):
    str.session_state.jogos = []
    str.rerun()

# Exibir os jogos inseridos e calcular as múltiplas
if str.session_state.jogos:
    str.header("📋 Jogos Analisados e Selecionados")
    
    mercados_para_multipla = []
    
    for jogo in str.session_state.jogos:
        with str.expander(f"🟢 {jogo['confronto']}"):
            if not jogo['mercados']:
                str.warning("Nenhum mercado deste jogo atingiu o critério mínimo de 80% de probabilidade.")
            for mercado in jogo['mercados']:
                str.write(f"🎯 **{mercado['nome']}** | Probabilidade: {mercado['prob']*100:.1f}% | Odd: {mercado['odd']:.2e}")
                mercados_para_multipla.append({
                    "confronto": jogo['confronto'],
                    "mercado": mercado['nome'],
                    "prob": mercado['prob'],
                    "odd": mercado['odd']
                })

    # CÁLCULO DA MÚLTIPLA SE houver mercados válidos
    if mercados_para_multipla:
        str.markdown("---")
        str.header("🎲 Sugestão de Bilhete Múltiplo Otimizado")
        
        odd_final = 1.0
        prob_final = 1.0
        
        str.write("O robô combinou os mercados mais seguros para atingir o maior retorno matemático:")
        
        # Tabela demonstrativa
        dados_tabela = []
        for item in mercados_para_multipla:
            odd_final *= item['odd']
            prob_final *= item['prob']
            dados_tabela.append([item['confronto'], item['mercado'], f"{item['odd']:.2f}", f"{item['prob']*100:.1f}%"])
            
        str.table(data={"Jogo": [d[0] for d in dados_tabela], 
                        "Mercado": [d[1] for d in dados_tabela], 
                        "Odd": [d[2] for d in dados_tabela], 
                        "Confiança": [d[3] for d in dados_tabela]})
        
        # Resultados Finais
        col1, col2, col3 = str.columns(3)
        with col1:
            str.metric(label="Odd Final da Múltipla", value=f"{odd_final:.2f}")
        with col2:
            cor_prob = "normal" if prob_final >= 0.80 else "inverse"
            str.metric(label="Chance Real do Bilhete Bater", value=f"{prob_final*100:.1f}%")
        with col3:
            retorno = (odd_final - 1) * 100
            str.metric(label="Lucro Estimado", value=f"+{retorno:.1f}%")
            
        if prob_final >= 0.80:
            str.success("✅ Este bilhete está DENTRO da sua meta de segurança de 80% ou mais!")
        else:
            str.warning("⚠️ Atenção: Ao somar muitos mercados, a chance matemática caiu abaixo de 80%. Considere remover um jogo ou selecionar mercados com porcentagens maiores nas barras laterais.")
else:
    str.info("Insira o primeiro jogo na barra lateral esquerda para começar a montar a sua múltipla.")
