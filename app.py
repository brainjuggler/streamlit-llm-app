import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
# これにより、OPENAI_API_KEYが自動的に読み込まれます
load_dotenv()

# --- 中核となる関数 ---
def get_expert_response(user_question, expert_persona):
    """
    ユーザーの質問と専門家のペルソナを受け取り、LLMからの回答を返す関数
    """
    # 選択された専門家に応じてシステムメッセージを定義する
    if expert_persona == "マーケティングの達人":
        system_template = "あなたは世界クラスのマーケティングの達人です。あなたのアドバイスは鋭く、洞察に富み、現代のデジタル戦略に特化しています。"
    elif expert_persona == "テック系インフルエンサー":
        system_template = "あなたは世界クラスのテック系インフルエンサーです。最新のバズワードやスタートアップの専門用語を交えながら、自信たっぷりに複雑な技術トピックを解説します。"
    else:
        system_template = "あなたは親切なアシスタントです。"

    # LangChainのChatモデルを初期化
    llm = ChatOpenAI(model="gpt-4o-mini",temperature=0.7)

    # API呼び出し用のメッセージリストを作成
    messages = [
        SystemMessage(content=system_template), # 専門家のペルソナ
        HumanMessage(content=user_question)     # ユーザーの質問
    ]

    # LLMから回答を取得
    response = llm(messages)
    return response.content

# --- StreamlitのWebアプリ画面 ---

# Webアプリのタイトルを設定
st.title("🤖 AI専門家チャット")

# アプリの概要や操作方法を表示
st.write(
    "このアプリでは、AI専門家とチャットできます。"
    "AIのペルソナ（キャラクター）を選んで、質問を入力すると、専門家レベルの回答が返ってきます！"
)

# formを使ってUI要素と送信ボタンをグループ化する
with st.form(key='expert_chat_form'):
    # ラジオボタンで専門家のペルソナを選択
    expert_choice = st.radio(
        "AI専門家のペルソナを選んでください：",
        ("マーケティングの達人", "テック系インフルエンサー"),
        horizontal=True
    )

    # テキストエリアでユーザーからの質問を入力
    user_input = st.text_area("ここに質問を入力してください：")

    # フォームの送信ボタン
    submit_button = st.form_submit_button(label='専門家の回答を得る')

# --- フォーム送信後の処理 ---
if submit_button:
    if user_input:
        # ユーザーが質問を入力した場合、関数を呼び出して回答を取得する
        response = get_expert_response(user_input, expert_choice)
        # 回答を表示する
        st.write("### 専門家の回答：")
        st.write(response)
    else:
        # テキストボックスが空の場合に警告を表示
        st.warning("送信する前に質問を入力してください。")