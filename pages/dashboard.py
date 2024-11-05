import streamlit as st

# 通过 Streamlit 组件嵌入 HTML、CSS 和 JavaScript，实现增强的计时器
st.title("增强样式的动态计时器")

# 控制计时器的状态
if 'timer_running' not in st.session_state:
    st.session_state['timer_running'] = False

# 启动计时器
if st.button("开始计时"):
    st.session_state['timer_running'] = True

# 停止计时器
if st.button("停止计时"):
    st.session_state['timer_running'] = False

# 使用 JavaScript、CSS 和 HTML 来实现计时器及样式特效
if st.session_state['timer_running']:
    st.components.v1.html("""
        <div id="timer-container" style="display: flex; justify-content: center; align-items: center; height: 100px; background: linear-gradient(90deg, #ff7eb3, #ff758c, #ff6b6b); border-radius: 12px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);">
            <div id="timer" style="font-size: 48px; font-weight: bold; color: white; text-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);">00:00:00</div>
        </div>
        <style>
            #timer-container {
                animation: pulse 1.5s infinite;
            }
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
        </style>
        <script>
            let seconds = 0;
            function updateTimer() {
                seconds += 1;
                let hrs = Math.floor(seconds / 3600);
                let mins = Math.floor((seconds % 3600) / 60);
                let secs = seconds % 60;
                document.getElementById('timer').textContent = 
                    String(hrs).padStart(2, '0') + ":" +
                    String(mins).padStart(2, '0') + ":" +
                    String(secs).padStart(2, '0');
            }
            setInterval(updateTimer, 1000);
        </script>
    """, height=100)
else:
    st.write("计时器已停止")
