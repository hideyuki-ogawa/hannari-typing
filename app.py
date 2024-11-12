import streamlit as st
import random
import time
from words_dict import kyo_kotoba_dict


def initialize_session_state():
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'selected_game' not in st.session_state:
        st.session_state.selected_game = kyo_kotoba_dict
    if 'current_word' not in st.session_state:
        st.session_state.current_word = random.choice(list(st.session_state.selected_game.keys()))
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'time_limit' not in st.session_state:
        st.session_state.time_limit = 60  # 60秒のゲーム時間
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0  # text_inputのキーを管理する変数
    if 'countdown_active' not in st.session_state:
        st.session_state.countdown_active = False
    if 'countdown_start' not in st.session_state:
        st.session_state.countdown_start = None


def show_countdown():
    current_time = time.time()
    elapsed = current_time - st.session_state.countdown_start
    remaining = 3 - int(elapsed)
    
    # 問題表示エリア
    st.subheader("📝 もんだい")
    st.text(st.session_state.current_word)
    st.text(f"入力文字: ?")
    st.text(f"ローマ字: ?")

    # 入力エリア（disabled=Trueで無効化）
    st.text_input(
        "⌨️ にゅうりょく",
        key=f"input_{st.session_state.input_key}",
        disabled=True,
        placeholder="カウントダウン中..."
    )
    if remaining > 0:
        st.header(f"⏰ {remaining}")
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.countdown_active = False
        st.session_state.game_active = True
        st.session_state.start_time = time.time()
        st.rerun()



def main():
    st.title(" はんなりデジタルタイピング ")
    initialize_session_state()
    st.image('./image/hannari-han.png', width=200)

    if not st.session_state.game_active and not st.session_state.countdown_active:
        

        # ゲームスタートボタン
        if st.button("🎯 ゲームスタート"):
            st.session_state.game_active = True
            st.session_state.start_time = time.time()
            st.session_state.countdown_active = True
            st.session_state.countdown_start = time.time()
            st.session_state.score = 0
            st.session_state.input_key += 1
            st.rerun()

   # カウントダウン処理
    if st.session_state.countdown_active:
        show_countdown()

    # ゲームアクティブ時の処理
    if st.session_state.game_active:
        # 残り時間の計算
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = max(st.session_state.time_limit - elapsed_time, 0)

        # 時間切れチェック
        if remaining_time <= 0:
            st.session_state.game_active = False
            st.success(f"🎉 ゲームしゅうりょう！ あなたのスコア: {st.session_state.score} てん")
            st.balloons()
            if st.button("🔄 もういちどあそぶ"):
                st.rerun()
            return

        # 残り時間とスコアの表示
        col1, col2 = st.columns(2)
        # Create a placeholder for dynamic time display
        time_placeholder = st.empty()
        progress_text = "⏱️ のこりじかん", f"{int(remaining_time)}びょう"
        
        with col1:
            st.metric("⏱️ のこりじかん", f"{int(remaining_time)}びょう")
        with col2:
            st.metric("🏆 スコア", st.session_state.score)
        

        # 現在の単語とローマ字入力例を表示
        current_word = st.session_state.current_word
        # romaji = words_dict[current_word][1]
        # kotoba_imi = words_dict[current_word][0]
        romaji = st.session_state.selected_game[current_word]

        st.markdown(f"""
        ### 入力する文字: :rainbow[**{current_word}**]
        入力するローマ字例: **{romaji}** 
        """)
        
        # 入力フィールド
        user_input = st.text_input(
            "ここにタイプしてね:",
            key=f"typing_input_{st.session_state.input_key}",
            max_chars=20
        )
        
        # 入力チェック
        if user_input:
            if user_input == st.session_state.current_word:
                len_word = len(st.session_state.current_word)
                st.session_state.score += 10 * len_word
                st.session_state.current_word = random.choice(list(st.session_state.selected_game.keys()))
                st.session_state.input_key += 1
                st.rerun()
            elif len(user_input) >= len(st.session_state.current_word):
                st.error("❌ ざんねん！もういちどチャレンジ！")

    game_desc1, game_desc2 = st.columns(2)

    with game_desc1:
        st.markdown("""
    ### 遊び方
    1. 「ゲームスタート」ボタンを押す    
    2. 画面に出てくる単語をタイプ     
    3. 正解すると10ポイントがもらえるよ！    
    4. 60秒間で何点取れるか勝負だ！    
                    """
                    )
    with game_desc2:
        st.markdown("""
    ### 文字入力の方法
    - 文字が入力出来たら、エンターキーを押してね
    - カタカナ/漢字に変換する場合、スペースキーを押してね
    - 正解したら、[Tab]キーを押して、次の文字を入力しよう！
                    """)

    # ゲーム説明
    st.markdown("""
    ## 画面を見ながら入力できるよう、
    ## 頑張って練習してね！  
    """)

if __name__ == "__main__":
    main()
