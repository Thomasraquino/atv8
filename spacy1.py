from collections import Counter
import spacy
import streamlit as st

# Configuração da página no navegador
st.set_page_config(page_title="Análise de Comentários Virais", page_icon="📊")


# Carrega o modelo do spaCy em cache para carregar rápido
@st.cache_resource
def carregar_modelo():
    return spacy.load("pt_core_news_sm")


nlp = carregar_modelo()

# Título e descrição da interface web
st.title("📊 Análise de Palavras em Comentários")
st.markdown(
    "Descubra quais são os termos e assuntos mais frequentes nas postagens das suas redes sociais."
)

# Texto de exemplo padrão
exemplo_comentarios = """Nossa, esse vídeo ficou simplesmente incrível! sensacional a edição! 👏🔥
Caramba, muito bom mesmo. Assistindo em loop!
Sensacional, nunca vi um conteúdo tão bom e incrível nesse perfil.
Achei incrível demais, edições muito boas e conteúdo sensacional.
Muito bom! Parabéns aos envolvidos, ficou surreal de tão bom!
Não gostei muito, achei bem fraco... mas o final foi bom.
Simplesmente incrível! Edição top demais. Parabéns!
Sensacional esse post, me ajudou demais! Muito bom!
Vídeo muito incrível, parabéns pela qualidade sensacional!
Conteúdo incrível, a edição ficou sensacional demais."""

# Área para digitar/colar o texto
texto_input = st.text_area(
    "Cole os comentários aqui:", value=exemplo_comentarios, height=220
)

# Controle deslizante para escolher a quantidade do Top
top_n = st.slider("Selecione a quantidade de palavras no Top:", 5, 20, 10)

# Botão para processar
if st.button("🔍 Analisar Frequência", type="primary"):
    if texto_input.strip():
        doc = nlp(texto_input)

        lemas = [
            token.lemma_.lower().strip()
            for token in doc
            if not (
                token.is_stop
                or token.is_punct
                or token.is_space
                or token.like_num
            )
            and len(token.lemma_) > 1
        ]

        if lemas:
            contagem = Counter(lemas).most_common(top_n)

            st.success("Análise concluída com sucesso!")
            st.subheader(f"🏆 Top {top_n} Palavras / Lemas mais frequentes")

            # Monta os dados para exibir na tabela do site
            dados_tabela = [
                {"Posição": f"#{i}", "Palavra / Lema": p, "Frequência": f}
                for i, (p, f) in enumerate(contagem, start=1)
            ]

            st.dataframe(dados_tabela, use_container_width=True)
        else:
            st.warning(
                "Nenhuma palavra relevante encontrada para analisar após a filtragem."
            )
    else:
        st.error("Por favor, insira algum texto para analisar.")